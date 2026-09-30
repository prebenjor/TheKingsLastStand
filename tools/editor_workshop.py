"""Read-only native editor handoff review. Never imports gameplay automatically.

Object v3 layout follows War3Net Simple/LevelObjectModification binary readers.
Units 13.11 is pinned to our installed editor fixture. Unknown formats remain
explicit unresolved changes, with the complete saved map archived intact.
"""
import argparse
import difflib
import hashlib
import json
import math
import re
import struct
from io import BytesIO
from pathlib import Path

from archive_pack import MPQArchive, member
from authored_map import AUTHORED_MEMBERS, _build_identity

ROOT = Path(__file__).resolve().parents[1]
OBJECT_MEMBERS = {'war3map.' + suffix: suffix in ('w3a', 'w3d', 'w3q')
                  for suffix in ('w3u', 'w3t', 'w3a', 'w3b', 'w3d', 'w3h', 'w3q')}
TRIGGER_MEMBERS = ('war3map.wtg', 'war3map.wct', 'war3map.j', 'war3map.lua')


class MapMembers(dict):
    """Archive contents with explicit diagnostics for unnamed MPQ entries."""
    unlisted = ()


def inventory_gaps(archive, names):
    def key(entry):
        return entry.block_table_index, entry.hash_a, entry.hash_b
    covered = {key(entry) for name in names
               if (entry := archive.get_hash_table_entry(name)) is not None}
    return [{'block_index': entry.block_table_index, 'hash_a': entry.hash_a, 'hash_b': entry.hash_b}
            for entry in archive.hash_table
            if entry.block_table_index < 0xFFFFFFFE and key(entry) not in covered]


def sha(data):
    return hashlib.sha256(data).hexdigest()


class Reader:
    def __init__(self, data):
        self.data, self.pos = data, 0

    def take(self, count):
        if count < 0 or self.pos + count > len(self.data):
            raise ValueError('Truncated or invalid binary record')
        result = self.data[self.pos:self.pos + count]
        self.pos += count
        return result

    def number(self, fmt='i'):
        return struct.unpack('<' + fmt, self.take(struct.calcsize('<' + fmt)))[0]

    def count(self):
        value = self.number()
        if not 0 <= value <= 100000:
            raise ValueError('Invalid record count')
        return value

    def raw(self):
        return self.take(4).decode('ascii')

    def string(self):
        end = self.data.find(b'\0', self.pos)
        if end < 0:
            raise ValueError('Unterminated string')
        return self.take(end - self.pos + 1)[:-1].decode('utf-8')

    def finish(self):
        if self.pos != len(self.data):
            raise ValueError('Unparsed trailing bytes')


def decode_objects(data, extended=False):
    r = Reader(data)
    version = r.number()
    if version not in (2, 3):
        raise ValueError('Unsupported object format ' + str(version))
    result = {}
    for table in ('original', 'custom'):
        for _ in range(r.count()):
            base, custom = r.raw(), r.raw()
            raw = custom if custom != '\0' * 4 else base
            key = table + '/' + raw
            if version == 3:
                extras = [r.number() for _ in range(r.count())]
                if extras not in ([], [0]):
                    result[key + '/editor-metadata'] = extras
            if key + '/base' in result:
                raise ValueError('Duplicate object identity ' + key)
            result[key + '/base'] = base
            for _ in range(r.count()):
                field, kind = r.raw(), r.number()
                rank, pointer = (r.number(), r.number()) if extended else (0, 0)
                if kind == 0:
                    value = r.number()
                elif kind in (1, 2):
                    value = r.number('f')
                    if not math.isfinite(value):
                        raise ValueError('Nonfinite object value')
                elif kind == 3:
                    value = r.string()
                else:
                    raise ValueError('Unknown object value type ' + str(kind))
                end = r.raw()
                if end not in ('\0' * 4, base, custom):
                    raise ValueError('Invalid object end marker')
                field_key = f'{key}/{field}/{rank}/{pointer}'
                if field_key in result:
                    raise ValueError('Duplicate field ' + field_key)
                result[field_key] = {'type': kind, 'value': value}
    r.finish()
    return result


def decode_units(data):
    r = Reader(data)
    if r.take(4) != b'W3do' or (r.number(), r.number()) != (13, 11):
        raise ValueError('Unsupported unit placement format (requires DE 13.11)')
    result = {}
    for _ in range(r.count()):
        u = {'rawcode': r.raw(), 'variation': r.number()}
        u['position'] = [r.number('f') for _ in range(3)]
        u['facing_radians'] = r.number('f')
        u['scale'] = [r.number('f') for _ in range(3)]
        u['skin'] = r.raw()
        for name, fmt in (('skin_flags', 'i'), ('flags', 'B'), ('owner', 'i'),
                          ('unknown', 'H'), ('hp', 'i'), ('mana', 'i'), ('item_table', 'i')):
            u[name] = r.number(fmt)
        u['drops'] = [[{'item': r.raw(), 'chance': r.number()} for _ in range(r.count())]
                      for _ in range(r.count())]
        u['gold'] = r.number()
        u['acquisition'] = r.number('f')
        for name in ('hero_level', 'strength', 'agility', 'intelligence'):
            u[name] = r.number()
        u['inventory'] = [{'slot': r.number(), 'item': r.raw()} for _ in range(r.count())]
        u['abilities'] = [{'ability': r.raw(), 'autocast': r.number(), 'level': r.number()}
                          for _ in range(r.count())]
        mode = r.number()
        if mode == 0:
            random = r.take(4).hex()
        elif mode == 1:
            random = [r.number(), r.number()]
        elif mode == 2:
            random = [{'unit': r.raw(), 'chance': r.number()} for _ in range(r.count())]
        else:
            raise ValueError('Unknown random unit mode')
        u['random'] = {'mode': mode, 'data': random}
        u['color'], u['waygate'], identity = r.number(), r.number(), str(r.number())
        u['reserved'] = [r.number() for _ in range(3)]
        if identity in result:
            raise ValueError('Duplicate creation identity ' + identity)
        result[identity] = u
    r.finish()
    return result


def differences(before, after):
    return [{'key': key, 'before': before.get(key), 'after': after.get(key),
             'status': 'added' if key not in before else 'deleted' if key not in after else 'changed'}
            for key in sorted(before.keys() | after.keys()) if before.get(key) != after.get(key)]


def functions(data):
    script = data.decode('utf-8-sig')
    return {match[1]: match[0] for match in re.finditer(
        r'^function\s+(\w+)\b[^\n]*\n.*?^endfunction\s*$', script, re.M | re.S)}


def compare_members(before, after, labels):
    changed = sorted(name for name in before.keys() | after.keys() if before.get(name) != after.get(name))
    report = {'changed_members': changed, 'art_members_changed': [n for n in changed if n in AUTHORED_MEMBERS],
              'units': [], 'objects': {}, 'trigger_members_changed': [n for n in changed if n in TRIGGER_MEMBERS],
              'script_functions_changed': [], 'unresolved': []}
    report['archive_inventory_warnings'] = {
        label: list(gaps) for label, contents in (('baseline', before), ('edited', after))
        if (gaps := getattr(contents, 'unlisted', ())) }
    for label, gaps in report['archive_inventory_warnings'].items():
        report['unresolved'].append(f'Unenumerated MPQ hash entries in {label}: {len(gaps)}; complete map archived for manual review')
    if 'war3mapUnits.doo' in changed:
        try:
            old, new = (decode_units(x.get('war3mapUnits.doo', b'')) for x in (before, after))
            for diff in differences(old, new):
                a, b = diff['before'], diff['after']
                diff['label'] = labels.get(diff['key'], 'Unmapped placement')
                diff['changes'] = {d['key']: {'before': d['before'], 'after': d['after']}
                                   for d in differences(a or {}, b or {})}
                if a and b and a['rawcode'] != b['rawcode']:
                    diff['status'] = 'replacement-needs-review'
                if diff['status'] != 'changed' or diff['key'] not in labels:
                    report['unresolved'].append('Review placement ' + diff['key'] + ': ' + diff['status'])
                if b and b['rawcode'] != 'sloc' and b['owner'] != 26:
                    report['unresolved'].append('Placement ' + diff['key'] + ' is not Neutral Extra; duplication risk')
                report['units'].append(diff)
        except (ValueError, UnicodeError, struct.error) as error:
            report['unresolved'].append('war3mapUnits.doo: ' + str(error))
    for name, extended in OBJECT_MEMBERS.items():
        if name in changed:
            try:
                decoded = [decode_objects(x[name], extended) if name in x else {} for x in (before, after)]
                report['objects'][name] = differences(*decoded)
            except (ValueError, UnicodeError, struct.error) as error:
                report['unresolved'].append(name + ': ' + str(error))
    if 'war3map.j' in changed:
        try:
            report['script_functions_changed'] = [d['key'] for d in differences(
                functions(before.get('war3map.j', b'')), functions(after.get('war3map.j', b'')))]
        except UnicodeError as error:
            report['unresolved'].append('JASS decoding: ' + str(error))
    if report['trigger_members_changed']:
        report['unresolved'].append('Trigger/custom script changes require source review; generated initialization is not imported')
    known = set(AUTHORED_MEMBERS) | set(OBJECT_MEMBERS) | set(TRIGGER_MEMBERS) | {'war3mapUnits.doo', '(listfile)', '(attributes)'}
    report['other_changed_members'] = [n for n in changed if n not in known]
    report['unresolved'] += ['Review archive member ' + n for n in report['other_changed_members']]
    report['integration_status'] = 'review only; no source imported'
    return report


def read_map(path):
    data = Path(path).read_bytes()
    archive = MPQArchive(BytesIO(data), listfile=False)
    try:
        names = set(member(archive, '(listfile)').decode('utf-8-sig').splitlines())
        names.update(AUTHORED_MEMBERS)
        names.update(OBJECT_MEMBERS)
        names.update(TRIGGER_MEMBERS)
        names.update(('war3map.w3i', 'war3mapUnits.doo', '(listfile)', '(attributes)'))
        contents = MapMembers({name: member(archive, name) for name in sorted(names)
                               if archive.get_hash_table_entry(name) is not None})
        contents.unlisted = inventory_gaps(archive, names)
    finally:
        archive.file.close()
    if Path(path).read_bytes() != data:
        raise ValueError('Map changed while reading; save and close before handoff')
    return data, contents, _build_identity(contents['war3map.w3i'])


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def preserve_baseline(map_path, layout, archive_root, chapter, closed=False):
    if not closed:
        raise ValueError('Human must confirm the map is saved and closed')
    data, contents, build_id = read_map(map_path)
    if build_id != layout['build_id']:
        raise ValueError('Stale build identity; use the current terrain work copy')
    if sha(data) == layout['sha256']:
        raise ValueError('Save once in World Editor before establishing the native baseline')
    for name in ('war3map.w3u', 'war3map.w3a', 'war3map.w3t'):
        if struct.unpack_from('<I', contents[name])[0] != 3:
            raise ValueError('Expected native editor object format 3: ' + name)
    native_units = decode_units(contents['war3mapUnits.doo'])
    labels = {str(i + 4): placement[3] for i, placement in enumerate(layout['placements'])}
    expected = {str(i + 4): placement[0] for i, placement in enumerate(layout['placements'])}
    expected.update({str(i): 'sloc' for i in range(4)})
    if {key: u['rawcode'] for key, u in native_units.items()} != expected:
        raise ValueError('Baseline reference identities differ; review additions/deletions before accepting it')
    for key, unit in native_units.items():
        if unit['rawcode'] != 'sloc' and unit['owner'] != 26:
            raise ValueError('Baseline reference ownership changed: ' + key)
    folder = Path(archive_root) / f'{build_id}-chapter-{chapter}-baseline-{sha(data)[:12]}'
    folder.mkdir(parents=True, exist_ok=False)
    target = folder / Path(map_path).name
    target.write_bytes(data)
    manifest = {'schema': 1, 'build_id': build_id, 'chapter': chapter, 'map': target.name,
                'sha256': sha(data), 'source_path': str(Path(map_path).resolve()), 'closed_confirmed': True,
                'generated_editor_sha256': layout['sha256'], 'labels': labels,
                'members': {name: sha(value) for name, value in contents.items()},
                'archive_inventory_warnings': list(getattr(contents, 'unlisted', ())),
                'status': 'native baseline preserved; chapter edits pending'}
    write_json(folder / 'baseline.json', manifest)
    return folder / 'baseline.json'


def review_map(map_path, baseline_path, archive_root, chapter, closed=False):
    if not closed:
        raise ValueError('Human must confirm the map is saved and closed')
    baseline_path = Path(baseline_path)
    manifest = json.loads(baseline_path.read_text(encoding='utf-8'))
    if manifest['schema'] != 1 or manifest['chapter'] != chapter:
        raise ValueError('Baseline schema/chapter mismatch')
    archive_name = Path(manifest['map'])
    if archive_name.name != str(archive_name):
        raise ValueError('Baseline map must be a sibling filename')
    baseline_data, before, baseline_id = read_map(baseline_path.parent / archive_name)
    if sha(baseline_data) != manifest['sha256'] or baseline_id != manifest['build_id']:
        raise ValueError('Baseline checksum or build identity mismatch')
    data, after, build_id = read_map(map_path)
    if build_id != baseline_id:
        raise ValueError('Edited map and baseline use different builds')
    report = compare_members(before, after, manifest['labels'])
    report.update({'build_id': build_id, 'chapter': chapter, 'baseline_sha256': manifest['sha256'],
                   'edited_sha256': sha(data), 'baseline': str(baseline_path.resolve()),
                   'source_path': str(Path(map_path).resolve())})
    folder = Path(archive_root) / f'{build_id}-chapter-{chapter}-review-{sha(data)[:12]}'
    folder.mkdir(parents=True, exist_ok=False)
    (folder / Path(map_path).name).write_bytes(data)
    write_json(folder / 'review.json', report)
    lines = [f'# Editor workshop chapter {chapter} review — {build_id}', '',
             f"Saved map SHA-256: `{sha(data)}`", '', 'Review only. Source import remains pending.', '',
             '## Terrain/dressing', '', *['- ' + n for n in report['art_members_changed']], '',
             '## Placement changes', '']
    for unit in report['units']:
        lines += [f"- {unit['label']} (creation {unit['key']}): {unit['status']}"]
        for key, value in unit['changes'].items():
            lines += [f"  - {key}: `{value['before']}` → `{value['after']}`"]
    lines += ['', '## Object fields', '']
    for name, fields in report['objects'].items():
        lines += [f'- {name}: {len(fields)} semantic field changes (details in review.json)']
    lines += ['', '## Triggers and custom script', '',
              *['- ' + n for n in report['trigger_members_changed']], '',
              'Changed JASS functions: ' + ', '.join(report['script_functions_changed']), '',
              '## Unresolved / manual review', '', *['- ' + n for n in report['unresolved']], '']
    (folder / 'review.md').write_text('\n'.join(lines), encoding='utf-8')
    if 'war3map.j' in report['changed_members']:
        diff = difflib.unified_diff(before.get('war3map.j', b'').decode('utf-8', errors='backslashreplace').splitlines(True),
                                    after.get('war3map.j', b'').decode('utf-8', errors='backslashreplace').splitlines(True),
                                    fromfile='baseline/war3map.j', tofile='edited/war3map.j')
        (folder / 'script.diff').write_text(''.join(diff), encoding='utf-8')
    return folder / 'review.json'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('baseline', 'review'))
    parser.add_argument('--map', type=Path, required=True)
    parser.add_argument('--chapter', type=int, choices=range(1, 8), required=True,
                        help='Chapter being edited; Chapter 0 establishes the chapter-1 baseline')
    parser.add_argument('--closed', action='store_true', help='Human confirmed save and close')
    parser.add_argument('--layout', type=Path, default=ROOT / 'build/editor-layout.json')
    parser.add_argument('--baseline', type=Path)
    args = parser.parse_args()
    try:
        if args.action == 'baseline':
            result = preserve_baseline(args.map, json.loads(args.layout.read_text(encoding='utf-8')),
                                       ROOT / 'backups/editor-workshop', args.chapter, args.closed)
        else:
            if not args.baseline:
                parser.error('review requires --baseline')
            result = review_map(args.map, args.baseline, ROOT / 'backups/editor-workshop', args.chapter, args.closed)
    except (ValueError, KeyError, OSError, UnicodeError, struct.error) as error:
        parser.exit(1, str(error) + '\n')
    print(result)


if __name__ == '__main__':
    main()

"""Preserving MPQ v0 updates, including complete listfile and CRC attributes."""
from io import BytesIO
from pathlib import Path
import struct
import zlib
from map_archive import MPQArchive, encrypt, read_encrypted


def member(a, name):
    entry = a.get_hash_table_entry(name)
    if entry is None:
        raise ValueError('Missing archive member: ' + name)
    block = a.block_table[entry.block_table_index]
    return read_encrypted(a, name) if block.flags & 0x10000 else (a.read_file(name) or b'')


def lookup(a, name):
    """Use MPQ probing rules, not mpyq's permissive full-table scan."""
    slot = a._hash(name, 'TABLE_OFFSET') % len(a.hash_table)
    for _ in a.hash_table:
        entry = a.hash_table[slot]
        if entry.block_table_index == 0xFFFFFFFF:
            return None
        if entry.hash_a == a._hash(name, 'HASH_A') and entry.hash_b == a._hash(name, 'HASH_B'):
            return entry
        slot = (slot + 1) % len(a.hash_table)
    return None


def pack(source, destination, replacements):
    raw = bytearray(Path(source).read_bytes())
    a = MPQArchive(BytesIO(raw), listfile=False)
    if a.header['offset'] != 0 or a.header['format_version'] != 0:
        raise ValueError('Expected the preserved MPQ v0 baseline without a wrapper')
    files = dict(replacements)
    names = set(member(a, '(listfile)').decode().splitlines()) | set(files) | {'(listfile)', '(attributes)'}
    files['(listfile)'] = ('\r\n'.join(sorted(names, key=str.lower)) + '\r\n').encode()
    original_attrs = member(a, '(attributes)')
    version, flags = struct.unpack_from('<II', original_attrs)
    if (version, flags) != (100, 1):
        raise ValueError('Unsupported MPQ attributes; expected version 100 CRC-only attributes')
    blocks = list(a.block_table)
    hashes = list(a.hash_table)
    crcs = list(struct.unpack('<'+'I'*len(blocks), original_attrs[8:]))
    indices = {}
    for name in list(files) + ['(attributes)']:
        entry = a.get_hash_table_entry(name)
        if entry is None:
            slot = a._hash(name, 'TABLE_OFFSET') % len(hashes)
            for _ in hashes:
                if hashes[slot][4] in (0xFFFFFFFF, 0xFFFFFFFE):
                    break
                slot = (slot + 1) % len(hashes)
            else:
                raise ValueError('Archive hash table is full')
            index = len(blocks)
            hashes[slot] = (a._hash(name, 'HASH_A'), a._hash(name, 'HASH_B'), 0, 0, index)
            blocks.append(None)
            crcs.append(0)
        else:
            index = entry.block_table_index
        indices[name] = index
    for name, data in files.items():
        crcs[indices[name]] = zlib.crc32(data)
    crcs[indices['(attributes)']] = 0
    files['(attributes)'] = struct.pack('<II', 100, 1) + struct.pack('<'+'I'*len(crcs), *crcs)
    for name, data in files.items():
        blocks[indices[name]] = (len(raw), len(data), len(data), 0x81000000)
        raw.extend(data)
    hash_offset = len(raw)
    raw.extend(encrypt(b''.join(struct.pack('<IIHHI', *e) for e in hashes), a._hash('(hash table)', 'TABLE')))
    block_offset = len(raw)
    raw.extend(encrypt(b''.join(struct.pack('<4I', *e) for e in blocks), a._hash('(block table)', 'TABLE')))
    struct.pack_into('<I', raw, 8, len(raw))
    struct.pack_into('<4I', raw, 16, hash_offset, block_offset, len(hashes), len(blocks))
    check = MPQArchive(BytesIO(raw), listfile=False)
    for name in names:
        if lookup(check, name) is None:
            raise ValueError('Engine lookup failed: ' + name)
        if name in files and member(check, name) != files[name]:
            raise ValueError('Archive read-back failed: ' + name)
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    Path(destination).write_bytes(raw)

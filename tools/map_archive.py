"""Preserve editor MPQs while replacing existing files in a build copy."""
from pathlib import Path
from io import BytesIO
import struct
import sys
import zlib

sys.path.insert(0, str(Path(__file__).parent / 'vendor'))
from mpyq import MPQArchive


def encrypt(data, key):
    seed = 0xEEEEEEEE
    out = bytearray()
    for (value,) in struct.iter_unpack('<I', data):
        seed = (seed + MPQArchive.encryption_table[0x400 + (key & 255)]) & 0xFFFFFFFF
        out.extend(struct.pack('<I', (value ^ (key + seed)) & 0xFFFFFFFF))
        key = (((~key << 21) + 0x11111111) | (key >> 11)) & 0xFFFFFFFF
        seed = (value + seed + (seed << 5) + 3) & 0xFFFFFFFF
    return bytes(out)


def read_encrypted(archive, name):
    entry = archive.get_hash_table_entry(name)
    block = archive.block_table[entry.block_table_index]
    archive.file.seek(block.offset + archive.header['offset'])
    data = archive.file.read(block.archived_size)
    key = archive._hash(name.split('\\')[-1], 'TABLE')
    if block.flags & 0x20000:
        key = ((key + block.offset) ^ block.size) & 0xFFFFFFFF
    if block.flags & 0x1000000:
        tail = len(data) % 4
        plain = archive._decrypt(data[:len(data)-tail] if tail else data, key)
        if tail:
            plain += data[-tail:]
        return zlib.decompress(plain[1:]) if len(plain) < block.size and plain[0] == 2 else plain
    count = (block.size + (512 << archive.header['sector_size_shift']) - 1) // (512 << archive.header['sector_size_shift'])
    offsets = struct.unpack('<' + 'I' * (count+1), archive._decrypt(data[:4*(count+1)], (key-1) & 0xFFFFFFFF))
    result = bytearray()
    for i in range(count):
        sector = data[offsets[i]:offsets[i+1]]
        tail = len(sector) % 4
        plain = archive._decrypt(sector[:len(sector)-tail] if tail else sector, (key+i) & 0xFFFFFFFF)
        if tail:
            plain += sector[-tail:]
        expected = min(512 << archive.header['sector_size_shift'], block.size-len(result))
        result.extend(zlib.decompress(plain[1:]) if len(plain) < expected and plain[0] == 2 else plain)
    return bytes(result)


def replace_files(source, destination, replacements):
    raw = bytearray(Path(source).read_bytes())
    archive = MPQArchive(BytesIO(raw), listfile=False)
    blocks = list(archive.block_table)
    for name, contents in replacements.items():
        entry = archive.get_hash_table_entry(name)
        if entry is None:
            raise ValueError('Cannot replace missing archive member: ' + name)
        offset = len(raw) - archive.header['offset']
        raw.extend(contents)
        blocks[entry.block_table_index] = (offset, len(contents), len(contents), 0x81000000)
    table = b''.join(struct.pack('<4I', *block) for block in blocks)
    offset = archive.header['offset'] + archive.header['block_table_offset']
    raw[offset:offset+len(table)] = encrypt(table, archive._hash('(block table)', 'TABLE'))
    struct.pack_into('<I', raw, archive.header['offset']+8, len(raw)-archive.header['offset'])
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    Path(destination).write_bytes(raw)


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    archive = MPQArchive(root / 'TheKingsLastStand.blank-backup.w3m', listfile=False)
    names = read_encrypted(archive, '(listfile)').decode().splitlines()
    for name in names:
        entry = archive.get_hash_table_entry(name)
        if entry is None:
            continue
        block = archive.block_table[entry.block_table_index]
        data = read_encrypted(archive, name) if block.flags & 0x10000 else archive.read_file(name)
        target = root / 'source' / 'template' / name.replace('\\', '/')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data or b'')
        print(name, len(data or b''))

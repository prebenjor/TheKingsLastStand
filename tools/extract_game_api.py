"""Read JASS declarations directly from the installed game's CASC storage."""
import ctypes as C
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r'C:\Program Files (x86)\Warcraft III')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def extract():
    dll_path = ROOT / 'tools/vendor/casclib-build/Release/CascLib.dll'
    lib = C.WinDLL(str(dll_path), use_last_error=True)
    lib.CascOpenStorage.argtypes = [C.c_char_p, C.c_uint32, C.POINTER(C.c_void_p)]
    lib.CascOpenStorage.restype = C.c_bool
    lib.CascOpenFile.argtypes = [C.c_void_p, C.c_char_p, C.c_uint32, C.c_uint32, C.POINTER(C.c_void_p)]
    lib.CascOpenFile.restype = C.c_bool
    lib.CascGetFileSize64.argtypes = [C.c_void_p, C.POINTER(C.c_uint64)]
    lib.CascGetFileSize64.restype = C.c_bool
    lib.CascReadFile.argtypes = [C.c_void_p, C.c_void_p, C.c_uint32, C.POINTER(C.c_uint32)]
    lib.CascReadFile.restype = C.c_bool
    lib.CascCloseFile.argtypes = [C.c_void_p]
    lib.CascCloseStorage.argtypes = [C.c_void_p]
    class FindData(C.Structure):
        _fields_ = [('szFileName', C.c_char * 260), ('CKey', C.c_ubyte * 16),
                    ('EKey', C.c_ubyte * 16), ('TagBitMask', C.c_uint64),
                    ('FileSize', C.c_uint64), ('szPlainName', C.c_char_p),
                    ('dwFileDataId', C.c_uint32), ('dwLocaleFlags', C.c_uint32),
                    ('dwContentFlags', C.c_uint32), ('dwSpanCount', C.c_uint32),
                    ('bFileAvailable', C.c_uint32, 1), ('NameType', C.c_int)]
    lib.CascFindFirstFile.argtypes = [C.c_void_p, C.c_char_p, C.POINTER(FindData), C.c_wchar_p]
    lib.CascFindFirstFile.restype = C.c_void_p
    lib.CascFindNextFile.argtypes = [C.c_void_p, C.POINTER(FindData)]
    lib.CascFindNextFile.restype = C.c_bool
    lib.CascFindClose.argtypes = [C.c_void_p]
    storage = C.c_void_p()
    if not lib.CascOpenStorage(str(GAME).encode(), 2, C.byref(storage)):
        raise RuntimeError('Cannot open installed CASC storage: ' + str(C.get_last_error()))
    output = ROOT / 'tools/reference/installed'
    output.mkdir(parents=True, exist_ok=True)
    result = {'game_root': str(GAME), 'build_info_sha256': sha((GAME / '.build.info').read_bytes()), 'files': {}}
    try:
        sources = {
            'common.j': [f'war3.w3mod:scripts\\common.j', f'war3.w3mod\\scripts\\common.j', f'scripts\\common.j'],
            'blizzard.j': [f'war3.w3mod:scripts\\blizzard.j', f'war3.w3mod\\scripts\\blizzard.j', f'scripts\\blizzard.j'],
            'ItemData.slk': ['war3.w3mod:Units\\ItemData.slk'],
            'UnitData.slk': ['war3.w3mod:Units\\UnitData.slk'],
            'AbilityData.slk': ['war3.w3mod:Units\\AbilityData.slk'],
            'UnitMetaData.slk': ['war3.w3mod:Units\\UnitMetaData.slk'],
            'AbilityMetaData.slk': ['war3.w3mod:Units\\AbilityMetaData.slk'],
            'ItemAbilityFunc.txt': ['war3.w3mod:Units\\ItemAbilityFunc.txt'],
        }
        for name, candidates in sources.items():
            handle = C.c_void_p()
            for path in candidates:
                if lib.CascOpenFile(storage, path.encode(), 2, 0x10, C.byref(handle)):
                    break
            else:
                raise RuntimeError('Cannot locate installed ' + name + ': ' + str(C.get_last_error()))
            try:
                size = C.c_uint64()
                if not lib.CascGetFileSize64(handle, C.byref(size)) or size.value > 8_000_000:
                    raise RuntimeError('Invalid API file size')
                buf = C.create_string_buffer(size.value)
                count = C.c_uint32()
                if not lib.CascReadFile(handle, buf, size.value, C.byref(count)) or count.value != size.value:
                    raise RuntimeError('Incomplete API file read')
                data = buf.raw
                (output / name).write_bytes(data)
                result['files'][name] = {'archive_path': path, 'sha256': sha(data), 'size': len(data)}
            finally:
                lib.CascCloseFile(handle)
        icon_list = C.c_char_p(b'war3.w3mod:ReplaceableTextures\\CommandButtons\\BTN*')
        find_data = FindData()
        find_handle = lib.CascFindFirstFile(
            storage, icon_list, C.byref(find_data),
            str(ROOT / 'tools/vendor/casclib-src/listfile/listfile.txt'))
        if not find_handle:
            raise RuntimeError('Cannot enumerate installed command-button assets: ' + str(C.get_last_error()))
        try:
            icons = []
            while True:
                found = bytes(find_data.szFileName).split(b'\0', 1)[0].decode('utf-8')
                relative = found.split(':', 1)[-1]
                if relative.lower().endswith(('.dds', '.blp')):
                    icons.append(relative)
                if not lib.CascFindNextFile(find_handle, C.byref(find_data)):
                    break
        finally:
            lib.CascFindClose(find_handle)
        icon_data = ('\n'.join(sorted(set(icons), key=str.lower)) + '\n').encode('utf-8')
        (output / 'commandbuttons.txt').write_bytes(icon_data)
        result['files']['commandbuttons.txt'] = {
            'archive_path': 'war3.w3mod:ReplaceableTextures\\CommandButtons\\BTN*',
            'sha256': sha(icon_data), 'size': len(icon_data), 'file_count': len(set(icons))}
    finally:
        lib.CascCloseStorage(storage)
    (output / 'provenance.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    extract()

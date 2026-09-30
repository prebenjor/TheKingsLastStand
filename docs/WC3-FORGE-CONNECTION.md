# wc3-forge MCP connection — 2026-09-30

## Update — 1 October 2026

The historical load blocker below is resolved by the separate patched native build. See [native compatibility implementation and evidence](WC3-FORGE-NATIVE-COMPATIBILITY.md) for the new MCP executable, working copy, preservation checks and remaining limits.

## Historical result

The owner explicitly requested an MCP connection to their installed wc3-forge and map editing. **The connection is configured and responding. Map editing through forge is blocked by its metadata parser.** No map save, format conversion or gameplay/terrain edit occurred.

Codex's global configuration now contains:

```toml
[mcp_servers.wc3-forge]
command = "C:\\Program Files\\wc3-forge\\wc3-forge\\wc3-forge.exe"
args = ["--mcp"]
```

Existing `playwright` and `node_repl` servers were retained. The prior config is backed up locally at `C:/Users/asphy/.codex/config.toml.before-wc3-forge-20260930.bak`; it is not repository content. The documented registration command was:

```powershell
codex mcp add wc3-forge -- 'C:\Program Files\wc3-forge\wc3-forge\wc3-forge.exe' --mcp
codex mcp get wc3-forge
```

The official [Codex MCP documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) describes shared `config.toml` configuration and client restart after adding a server. The wc3-forge [README](https://github.com/StephenSHorton/wc3-forge/blob/main/README.md) documents its built-in `--mcp` stdio proxy. No Node server, external tunnel or third-party hosted service was needed.

## Actual connection evidence

- MCP `initialize` succeeded using protocol `2024-11-05`.
- `tools/list` returned **153 tools**. Advertised server identity is `wc3-forge` / `0.0.1`; this is the MCP server version, not proof of the installed editor's release tag.
- `sessions_list` found one live editor, PID **62292**, with a responding bridge.
- `session_select` pinned calls to that instance. `map_status` reported `loaded: false`, matching the owner's screenshot.
- This turn called the actual stdio MCP endpoint using a temporary local protocol client under ignored `build/forge-session/`. The newly registered server is not yet exposed as a native tool namespace in this already-running conversation. Restart/reload the Codex client to load the configured connection directly. Re-enumerate sessions afterward; the PID is not permanent.

Do not log or copy lockfile authentication tokens. No update/downgrade of World Editor or forge was performed.

## Latest saved map preserved

Input: `C:/Users/asphy/Documents/Warcraft3Maps/kings-last-stand/build/KLS-D-68303d69bf-Development-Terrain.w3m`.

- Saved disk size: **306,165 bytes**.
- SHA-256: **`e8313363d7bcb07a3eb80cb8fd63626f115a07d7184445f89022057c708bfaff`**.
- Last disk modification: **30 September 2026, 23:12:32 Europe/Oslo**.
- Complete immutable copy: `backups/wc3-forge/20260930-e8313363d7bc/KLS-D-68303d69bf-Development-Terrain.w3m`.
- Trial copy: `backups/wc3-forge/20260930-e8313363d7bc/KLS-D-68303d69bf-Development-Forge.w3m`.
- Preservation manifest: `backups/wc3-forge/20260930-e8313363d7bc/preservation.json`.

No World Editor process was found during this inspection. This establishes preservation of the latest saved disk bytes, not a new human confirmation that every intended edit was saved. Preserve the complete archive and request clarification if the owner supplies a newer file.

Read-only archive inspection found **26 members**, no unlisted active MPQ entries, and **102 placed-unit records**, including the current native 13.11 unit format. Preserve all members, including skins, regions, cameras, groups, lighting and other editor data outside the six-art-layer capture allowlist. No semantic import or clean Chapter 0 baseline is claimed.

## Exact map-load failure

After selecting PID 62292, `map_open` was called with the trial map path. It returned:

```text
Bridge error -32000: Handler threw: parse war3map.w3i:
w3i: tech count 12800 exceeds 289 bytes remaining (min 8 bytes/element)
at offset 301: unexpected EOF
```

The call reported `isError: true`. There were no subsequent save or edit calls. SHA-256 comparisons confirmed the original, preserved archive and trial copy remained equal to the input hash. The map has **not** successfully loaded in forge.

### Format evidence and diagnosis

| Member | Actual saved format |
|---|---|
| `war3map.w3i` | Version **39**, 590 bytes |
| `war3map.w3e` | Version 12 |
| `war3mapUnits.doo` | Version **13**, subversion **11** |
| `war3map.doo` | Version 13 |
| `war3map.w3u`, `.w3t`, `.w3a` | Object version 3 |
| `war3map.wtg`, `.wct` | Native `0x80000004` wrappers |

The published [forge W3I parser](https://github.com/StephenSHorton/wc3-forge/blob/main/internal/formats/w3i/w3i.go) declares known layouts through version 33. It attempts that older shape for higher versions without handling the newer layout extensions, producing incorrect downstream counts on this version-39 file. This is a reproducible forge compatibility blocker; the error alone does **not** establish map corruption or an outdated World Editor.

The upstream latest release queried during this investigation was **v1.0.7**, published 5 September 2026, before Blizzard's 12 September Forsaken Kingdom build 24268. No compatible newer release was established. Do not infer the installed forge release number from its generic MCP `0.0.1` identity.

## Next work before safe authoring

1. Add/obtain explicit native W3I-39 reading and lossless writing support in forge. Compare its reader/writer with current installed-editor fixtures rather than guessing offsets or lowering a version integer.
2. Establish preservation of native doodad/unit 13.11 fields, object-v3 data, trigger wrappers and skin/import/lighting data. The first metadata failure prevents any claim about subsequent parser compatibility.
3. Open only the archived trial copy, confirm counts/positions and map state, then perform the documented no-change round-trip comparison once compatibility permits it.
4. Compare every member before adopting forge saves. Preserve unknown data and refuse unexplained omissions. A terrain-only preview is not proof that units/objects/triggers survive.
5. Continue the owner's layout integration and workshop through the shared catalogs after acceptable round-trip evidence. Keep Redtusk removed, cliffs and troll camp intact, and make moved references actual runtime placements.

Do not downgrade World Editor, remove native sections, relabel an incompatible map as an older format, or silently replace metadata with another map to make `map_open` succeed. A supported compatibility fix must preserve the user's complete work.

Current gameplay package remains **KLS-D-68303d69bf**. Installed/gameplay files are unchanged. No engine gameplay checks or automated regression suite were requested/run for this connection setup; the protocol handshake, tool discovery, attempted load and hash inspection are the recorded evidence.

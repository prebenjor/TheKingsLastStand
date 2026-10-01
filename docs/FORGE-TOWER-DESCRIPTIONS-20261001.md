# Forge support-tower description pass — 2026-10-01

Updated h003, kT12, kT22 and kT32 through the live Forge object API. Descriptions identify living allied heroes/troops, 15 HP every 3 seconds, 650 range, building exclusion and boss suppression. Each has racial flavour; source catalog matches.

The user's Sanctuary healing failure is still open. Existing saved JASS contains the healing loop; no gameplay fix or Warcraft verification is claimed.

Save As initially failed while replacing the open archive with Access Denied. Exported pending edits to `build/forge-session/20261001-support-towers`, opened that folder, then packaged a fresh `build/KLS-D-68303d69bf-Development-Forge-20261001-Towers.w3m`. Original Forge and Terrain maps remain unchanged.

Export SHA-256: `b93e3270be1eb923c3dd7d797730ceed0640554041ea3881cc66f31f50f62d42`.

Direct comparison of its MPQ payload against the original found only `war3mapSkin.w3u` changed; every other original map member is identical. The exported Warcraft HM3W wrapper puts MPQ at offset 512; the current Python review reader requires the MPQ slice for this export. Forge reopened it successfully. No test suite or Warcraft acceptance check was run. This is an editing artifact, not a new installed gameplay build.

Next live check: place an injured allied hero beside a completed Sanctuary Tower during ordinary play and observe HP over three seconds. Building-only failure would agree with the existing target exclusion.

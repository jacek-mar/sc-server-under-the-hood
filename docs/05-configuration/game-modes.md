# Game modes, gameplay ids and maps

> Status: **Stage 1.** Mode ids come from the comment block above
> `cvars.mm_defaultGameplay` in `default_platform_config.lua` ("not all work").
> Localised names come from the official page.

## 1. Gameplay (mode) ids

| Id | Name | Id | Name |
|---:|------|---:|------|
| 0 | none | 16 | last man standing |
| 1 | space battle | 17 | transport escort |
| 2 | capture the flag | 18 | open space |
| 3 | capture the base | 19 | mission script |
| 4 | **control** | 20 | PvP mission |
| 5 | practice | 21 | **football** |
| 6 | tutorial | 22 | battle royale |
| 7 | PvE mission | 23 | capture the base 2 |
| 8 | free space | 24 | hunger games |
| 9 | **sentinel** | 25 | one against all |
| 10 | king of the hill | 26 | ATDM |
| 11 | **bomb the base** | 27 | zombie |
| 12 | TDM | 28 | close distance |
| 13 | GTDM | 29 | autogen DM |
| 14 | clanship | 30 | three teams DM |
| 15 | capture the frag | 31 | april control |

Default `mm_defaultGameplay = 3`. Ids in **bold** are the arcade PvP set used by
the shipped queues (`{4,9,11}` = control, sentinel, bomb the base; `3` is also
used on higher-MMV queues).

## 2. Queue "mode keys" → in-game names

| Key | Localised name | | Key | Localised name |
|-----|---------------|-|-----|---------------|
| `april_control`, `atdm` | Paper conflict | | `PVE_MISSION`, `QUESTS` | Pick scenario |
| `ARENA` | Portals | | `PVE_MISSIONS` | Missions |
| `BRAWL` | Brawls | | `PVE_RANDOM` | Random mission |
| `capture_the_base` | Beacon capture | | `PVP` | PvP Arena |
| `capture_the_base_2` | Four lives | | `RAID` | Special operation |
| `CloseDistance`, `CLOSE_DISTANCE` | Close contact | | `RANDOM_BFS` | Conquest |
| `COOP_VS_AI` | Skirmish | | `sentinel` | Combat recon |
| `CUSTOM_GAME` | Custom battle | | `three_teams_dm` | Orion's belt |
| `football` | Spaceball | | `TOURNAMENT` | Tournament |
| `gtdm` | Survival | | `zombie` | Curse of the Leviathan |
| `hunger_games` | Last man standing | | `OPEN_WORLD_MAP` | Map |
| `one_against_all` | Beetle in the anthill | | `OPEN_WORLD_START` | Undock |

## 3. Maps referenced by the shipped queues

PvP arcade/coop: `s1338_devilsjaw`, `s1338_pandora_anomaly`,
`s1338_pandora_dreadnwreck`, `s1340_thar_aliendebris13`,
`s1340_aliendestsatation`, `s1340_thar_gasgiant`, `s1347_livestation`,
`s1420_ceres3_asteroidcity`, `s1420_ceres3_northmsite`,
`s8256_thar_barrierdebris`, `s8256_thar_lavastone`, `s8256_thar_threshold`.

Brawl: `football` (21), `da_prototype` (13 GTDM), `paper_airplanes` (26 ATDM).

PvE rotation (`MatchMaker_SetPveSchedule`): `pve_frozen_station`,
`s1550_pve_asteroid_building`, `s1550_pve_bigship_building(_2)`,
`s1550_pve_capture_repairbase`, `pve_desttown`, `pve_stealth`; permanent:
`pve_transit_emp_rock_frontier`. 2-hour rotation, up to 12 rotating levels.

Tournament maps (`tournament_levels`): devilsjaw, pandora_dreadnwreck,
thar_aliendebris13, ceres3_asteroidcity, ceres3_northmsite,
thar_barrierdebris, thar_lavastone, thar_threshold, desttown.

### Level ↔ mode (Stage 2 result)

* Every map named by a shipped queue exists under `data/levels/<group>/<name>/`
  (`area1`–`area4`, `federation`, `event`, `football`, `dreadnoughtbattle/…`)
  together with `<name>.map` (a one-line `zone "mapskit\maps\…"` pointer) and a
  folder with `scene.xml`, `pathfinding.nav`, `layers.xml`, `editorhelpers.xml`.
* `data/levels/active_maps.list` (193 entries) is the list of **active** maps:
  4 in `area1`, 23 `area2`, 15 `area3`, 8 `area4`, 9 `federation`,
  15 `dreadnoughtbattle`, 88 `global_world` (open-world campaign zones, `_ow`)
  and 29 `open_world`, plus `football`, `test_ai`, `tutorial_leviathan`.
* Spawn spots carry a `GameplaysMask`, but almost all bits are set, so it does
  **not** discriminate modes. Mode support is visible instead through
  mode-specific entities in `scene.xml`: `VitalPoint_Team#_Beacon[A-C]`
  (control beacons), `VitalPoint_Beacon#_RC` / `_RC_King` (capture / king of
  the hill), `BtB_BombSite_*` (bomb the base), `VitalPoint_PVE_*`,
  `ClanShip_*`, `OpenWorld_*`.
* Per-level table (generated): [level-catalogue.md](level-catalogue.md)
 . The entity-family → gameplay-id mapping there is
  *inferred* and should be confirmed by running each mode.
* Queue levels that are special: `football` has no team spawn spots (separate
  football logic), `s1338_pandora_anomaly` / `da_deathstar` / `allidium_yard`
  use other spawn-spot naming and show 0/0.

## 4. Brawl schedule

`BrawlManager_SetupSchedule` takes a **28-day cycle** (day 1 = first Monday of
2018) of `{ days, time_intervals (hours), gameplay }`. Shipped schedule: every
day of the cycle, hours 1–2, 9–10, 15–16, 17–18, 19–20, 21–22 →
`three_teams_dm`. Available gameplays: football, gtdm, hunger_games,
one_against_all, sentinel, capture_the_base, atdm, zombie, close_distance,
autogen_dm, three_teams_dm, april_control.

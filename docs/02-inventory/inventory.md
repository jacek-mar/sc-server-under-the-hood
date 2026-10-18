# Resource inventory

> Status: **Stage 1 — complete at directory level**, partial at file level.
> Counts taken 2026-10-10 from the private working copy.

## 1. Private inputs (not part of the public repo)

| Folder | Content | Files | Size |
|--------|---------|------:|-----:|
| `sc-server-files/star conflict/` | Steam depot: client + server | 6 987 | 11.9 GB |
| `sc-server-files/Targem/` | `%LOCALAPPDATA%\Targem` of the analyst: runtime logs, MongoDB data, profile | 174 | 1.2 GB |
| `random-materials/` | Community material (Discord export, community wiki, saved official page) | 343 | 28 MB |

`Targem/` contains personal data (Windows user name, local paths) — treat as
private; do not commit.

## 2. `star conflict/` — depot layout

| Path | Files | MB | What it is |
|------|------:|---:|------------|
| `win64/` | 11 | 23 | Client: `game.exe`, FMOD, OpenSSL/curl, `local_server.xml`, `launch_server_and_db.bat` |
| `cloud/` | 108 | 305 | **Server**: service executables, `data/` (config + generated XML), bundled `mongodb/` |
| `data/` | 6 813 | 11 522 | Game content shared by client and DedicatedServer |
| `sys_data/` | 41 | 1 | Minimal system data (UI, materials, env settings) |
| `docs/` | 1 | 0.04 | `matchmaking.md` (official, Russian) |
| `EmptySteamDepot/` | 0 | 0 | Placeholder (what Linux Steam installs natively) |
| root | ~13 | | `CrashReporter.*`, `launch_mongodb.bat`, `launch_server.bat`, `files.list`, `launcher-settings.zip`, OpenSSL/curl DLLs, shortcuts |

`files.list` (≈400 KB) is the depot manifest of relative paths — useful as a
checksum-free index of the original distribution.

### 2.1 `cloud/` executables (**32-bit x86 PE**, ~1.0–2.7 MB each except where noted; corrected 2026-10-11 with `pefile` - only `win64/game.exe` and `cloud/mongodb/*.exe` are x64)

`AchievementServer`, `AdventureServer`, `Authenticator`, `ChatServer`,
`ClanServer`, `ConfigServer`, `CrashReporter`, `DedicatedServer` (**11 MB**,
contains the whole game simulation), `EarlyMatchMaker`, `GameRewardDispencer`,
`Hub`, `LeaderboardServer`, `LoadBalancer`, `LobbyServer`, `MatchMaker`,
`QuestServer`, `ScriptsServer`, `Shard` (2.7 MB), `StatServer`, `Tournament`,
`Universe`, `ZoneCoordinator`. Plus `libcrypto-1_1_tg.dll`, `libssl-1_1_tg.dll`
(custom-named OpenSSL 1.1), `libcurl.dll`.

### 2.2 `cloud/data/` configuration and generated data

| File(s) | Size | Purpose |
|---------|-----:|---------|
| `default_platform_config.lua` | 138 KB | **Master server policy**: 271 cvars + queues, schedules, loot rules |
| `cloud.xml` | 1.7 KB | Node/service topology |
| `*.cfg` (16) | tiny | Per-service cvars (`common`, `hub`, `shard`, `loadbalancer`, `chat_server`, `dediserver`, …) |
| `store.xml` | 15 MB | Generated store catalogue |
| `vessel_custom_elements*.xml`, `vessel_presets.xml` | 0.3–1.4 MB | Ship customisation/presets |
| `quests.xml`, `ship_quests.xml`, `clan_quests.xml` | 286 / 7 / 0 KB | Quests |
| `defmod_rules*.xml`, `store_rules.xml`, `autogen.xml` | 0.1–0.2 MB | Def-modification/store rules, auto-generated defs |
| `achievements.xml`, `medals.xml`, `titles.xml`, `stickers.xml`, `account_auras.xml` | | Meta-progression |
| `zones.xml` | 44 KB | Open-world zones |
| `universe.xml`, `war.xml`, `karma.xml`, `faction_rep.xml`, `regions.xml`, `tournaments.xml` … | <10 KB | Small rule files (see [data-files](../05-configuration/data-files.md)) |
| `geo.gbin` | 379 KB | GeoIP binary (country → region mapping, *inferred*) |
| `sstring.flog` | 4 KB | String table log (*unknown*) |
| `chat/stop-list.txt`, `white-list.txt` | | Chat filter lists |

### 2.3 `cloud/mongodb/`

Unmodified MongoDB **2.6.12** Windows binaries (`mongod`, `mongo` shell, dump/
restore/import/export tools; AGPL-3.0 notice included), `config.cfg`
(`bind_ip=127.0.0.1`), `launch.bat`, `admin.bat` (`mongo.exe 127.0.0.1/cosmosim`)
and a 21 MB `mongo-r2.6.12.zip` source/binary archive.

### 2.4 `data/` (client + dedicated server content)

| Path | Files | MB | Notes |
|------|------:|---:|-------|
| `gamedata/def` | 169 | 35 | Core definitions (ships, modules, AI, effects…) |
| `gamedata/shared` | 80 | 4.5 | Shared tables: `def_ids.lua`, `loot_tables.lua`, `quests*.lua`, `battle_pass.lua`, `clan_*.lua`, `login_rewards.lua`… |
| `gamedata/spell` | 6 | 1 | Spell/ability tables |
| `levels/` | 2 414 | 1 324 | ~25 level groups (`area1..4`, `global_world` 489 MB, `envsettings`, `open_world`, `federation`, dreadnought, football, tutorial…) |
| `ui/` | 3 489 | 536 | Client UI: `graphics`(2 452 `.sanim`), `textures`, `locale` (243), `scripts` (262 Lua) |

File types across the depot: `.sanim` 2452, `.dds` 1456, `.lua` 922, `.xml` 740,
**`.pak` 588**, `.map` 249, `.nav` 226, `.dat` 130, `.txt` 112, `.cfg` 38,
`.exe` 37, `.dll` 13, `.bat` 6.

## 3. `Targem/` runtime profile (private)

| Folder | Content |
|--------|---------|
| `StarConflict/cloud/Hub/logs/` | Per-service logs `<serviceId>_<name>_<date>.log` + Hub log; **best source for startup behaviour** |
| `StarConflict/cloud/mongodb/data/` | MongoDB 2.6 data files: DBs `cosmosim_*`, `stats_cosmosim_*`, `achievements_*`, `delivered_*`, `games_*`, `logs_*`, `local` |
| `StarConflict/logs/<timestamp>/` | Client `game.log`, `game.net.log`, `chat.log`, `combat.log` |
| `StarConflict/profiles/0001.prfl`, `user_config.xml`, `user_bindings.xml`, `store_cache.dat` | Client profile/settings |
| `StarConflict-old/` | Earlier session (2026-10-09) |
| `StarWrath/` | Logs from a different Targem title (2026-09-19) — unrelated |

## 4. `random-materials/`

| Item | Content | Value |
|------|---------|-------|
| `STAR CONFLICT COMMUNITY EDITION.md` | Community-maintained how-to (DB editing, config tweaks, bots, Linux) | **High** |
| `STAR CONFLICT — MMO SPACE ACTION - (…).html` | Saved copy of the official "Local Game Launch" page + end-of-service notice | **High (authoritative)** |
| `Star_Conflict_Preservation_Project_001.1/…json` (6 pages) | Discord `#general-eng` export: 5 717 messages 2026-04-17 → 2026-10-10 | Medium (noisy; contains personal data) |
| `…-html/…html` (6 pages) | Same export, HTML | duplicate |
| `avatars/`, `emojis/`, `discrub_media/` | Media from the export | none |

Detailed digests: [sources/source-register.md](../sources/source-register.md).

## 4a. Stage 2 additions

* **`.pak`**: 588 archives directly in `data/` — `models_*` 239, `mapskit_*`
  (map/background kits) 215, `textures_*` 90, `sound_*` 37, `fonts*` 2, plus
  `strings`, `shaders`, `particles`, `video`, `misc`. All start with the magic
  `TPAK` + version 7.
* **Locales (12):** chinese, czech, english, french, german, hungarian, polish,
  portuguese, russian, spanish, turkish, ukrainian — `ui/locale/<lang>/` holds
  only localised textures (`textures.txt`, 219 `.dds`) and `uiresources.txt`;
  text strings live in `data/strings.pak`. Language metadata (font pack, links)
  is in `gamedata/locale.lua`.
* **Lua gamedata:** 298 plain-text `.lua` files (≈ 44 MB), no bytecode — see
  [gamedata-catalogue](../05-configuration/gamedata-catalogue.md).
* **Static readability of the Lua data** *(observed: full static parse by the
  maintainers' tooling, no Lua executed; spot-checked by hand against S3)*.
  The 298 gamedata files plus `cloud/data/default_platform_config.lua` hold
  **559,236 assignments** that a static reader can recover without running
  Lua, and 7,836 function calls. Almost all data files are plain table
  literals. The largest are `def/ex/active.lua` (84,144 assignments),
  `def/ex/prices_modules.lua` (43,118), `def/ex/craft.lua` (34,070) and
  `def/ex/ship.lua` (26,960). 4,209 constructs stay opaque to static
  reading: 2,264 standalone calls (for example in `def/designersdefs.lua`),
  1,330 function bodies kept as expressions, 568 unsupported statements and
  47 multi-value returns. Their effect is known only at run time. Tools that
  edit or check this data can treat it as data, except for those constructs
  and the `Configure*` functions of the platform config (20 definitions, see
  [config-system](../05-configuration/config-system.md)).
* **Levels:** 193 active maps — see [level-catalogue](../05-configuration/level-catalogue.md).

## 5. Not yet inventoried (Stage 2+)

* Per-file catalogue of `data/gamedata/**` (id tables, defs) and `cloud/data/*.xml` schemas.
* Contents of the 588 `.pak` archives (container format unknown).
* `levels/` map list with game-mode compatibility (`levelsDesc` names ↔ folders).
* `ui/locale` string tables (languages available).
* Embedded strings/imports of every executable (only Hub, Shard, MatchMaker,
  DedicatedServer, Authenticator, LoadBalancer, ScriptsServer, game.exe were
  string-dumped).

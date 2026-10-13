# Scripts and configs inside `misc.pak`

> Status: **Stage 2 finding (observed).** `data/misc.pak` (15.9 MB, 2023 files)
> was opened with a reader for the [TPAK format](tpak-format.md). It holds the
> client/server **Lua scripts as LuaJIT 2.x bytecode** (magic `1B 4C 4A`),
> plus a few plain-text configs. Only names and structure are recorded here;
> the extracted files stay in the git-ignored `work/` folder.

## 1. Plain-text files in `misc.pak` root

| File | Purpose |
|------|---------|
| `config.cfg` | Default client config (Quake-style): `exec address.cfg`, `set cl_versionType "live"`, commented `net_masterServer{NewsFeed,Status,Version,Addresses}Url`, `cl_autoDisconnectTime 4`, key binds, camera/replay binds, defaults (`cl_combatLog 3`, `g_shadowDistance 1000`, sound volumes…). `exec platform_config.cfg` |
| `platform_config.cfg` | Platform overrides (empty: only a commented `bind alt+f4`) |
| `autotest.cfg`, `autotests.cfg`, `autotests*.txt`, `test_maps.list` | **Headless test harness** — shows how to start a dedicated battle from the executable (see §3) |
| `chat-aliases.txt` | Alias table for chat commands (`who ↔ кто`, `quit`, `whisper`, `friends`, `ignore` …); `/chat_listDanglingAliases` validates it |
| `models_stats.txt`, `textures_stats.txt` | Resource statistics |

Note `address.cfg` is `exec`-ed by `config.cfg` but is **not** in `misc.pak`;
it is probably the (absent) per-build master-server address file — see
[open questions](open-questions.md).

## 2. Script groups (88 Lua files, bytecode)

| Group | Files (examples) | Role |
|-------|------------------|------|
| `scripts/masterserver.lua` | 1 (23 KB) | **Master-server RPC vocabulary**: result/enum tables for every cloud operation (see [masterserver-enums.md](masterserver-enums.md): 78 enums with numeric values + 1 name-only group, ~1000 members — battle pass, mail, clan actions, leaderboards, privileges, travel results, league teams, profile stats…) |
| `scripts/scripts_server/main.lua` | 18 KB | **ScriptsServer** main: global event engine (`ZoneInstanceEvents`, `ConfigureGlobalEvents`, ownership/expansion events per faction, `SetTimerScale`, `forceEvents`) |
| `scripts/general/events*.lua` | `events.lua`, `events_global.lua`, `events_boss.lua`, `events_piratsboss*.lua`, `events_pirate_invasion.lua`, `events_cyber_invasion.lua`, `events_greenwave.lua`, `events_mining.lua`, `event_manager.lua` | Open-world event definitions (Green/alien, Pirate, Jericho, Federation, Empire ownership/expansion; boss events; patrols) |
| `scripts/general/missions*.lua`, `quests.lua`, `point_manager.lua`, `module_base*.lua`, `special_ow_features.lua`, `mining*.lua`, `ow_fast_fly.lua` | | PvE missions, quest logic, open-world features |
| `scripts/ai/*` | `constants.lua`, `cosmos_constants.lua`, `questconstants.lua`, `achievementconstants.lua`, `spellconstants.lua`, `globalfunctions.lua`, `lua_data_formats{,_client,_server}.lua`, `main.lua`, `main_scripts_server.lua`, `adventure_*.lua` | Shared constants/enums and bootstrap per process type |
| `scripts/dump_*_wiki.lua`, `specs_dump.lua`, `wikigeneralfunctions.lua` | | Developer tooling that dumps ship/weapon/ammo/zone/achievement data for the wiki |
| `scripts/automatization/*` | `def_data.lua`, `def_presets.lua`, `def_screenshots.lua`, `lua_export.lua` | Content automation helpers |
| `scripts/system/*`, `m3d*.lua`, `debug.lua`, `profile.lua` | | Engine/Lua utility layer (`oop`, `linq`, `argcheck`, `pcall`, `math`, `prnd`) |
| `scripts/hangar.lua`, `dummymenu*.lua`, `gamepad.lua`, `bindings.lua`, `posteffects*.lua`, `gamestore.lua`, `fb.lua`, `skillmanager.lua`, `leaderboards.lua` | | Client-side UI/hangar/game-store glue |

Bootstrap order seen in constant pools: `main_scripts_server.lua` →
`ai/lua_data_formats_server.lua`, `gamedata/shared/zones.lua`,
`scripts/gamestore.lua`, `scripts/masterserver.lua`, `ai/cosmos_constants.lua`
(`execscript`). `scripts_server/main.lua` executes `scripts/general/global_functions.lua`,
`gamedata/shared/zones.lua`, `scripts/general/events_global.lua`,
`gamedata/designers_constants.lua`, `scripts/general/constants.lua`.

### Event ids visible in ScriptsServer (names)

`GREEN_OWNERSHIP`, `GREEN_EXPANSION`, `GREEN_PRE_EXPANSION`,
`ATTACK_GREEN_CHINABOSS`, `PRE_ATTACK_GREEN_CHINABOSS`, `PIRATE_*`,
`JERICHO_*`, `FEDERATION_*`, `EMPIRE_*` (each `OWNERSHIP`, `EXPANSION`,
`PRE_EXPANSION`), plus `DIRECTOR_BOSS_EVENTS`. These are the symbolic names behind the
numeric `eventDefName` values used in `default_platform_config.lua`
(see [open-world-and-services](../05-configuration/open-world-and-services.md#5-scriptsserver-global-events)).
ScriptsServer hooks: `OnZoneHasConflictChanged`, `OnZoneIsCivilianChanged`,
`OnZoneRaceChanged`, `OnZoneOwnerChanged`, `StarMapPrepare`, `OnUpdate`,
`OnNewData`, `OnStart`; config: `config_testTimeModifier`, `RNDSeed`,
`enableOriginalQuests`, `disableQuests`.

### How the ScriptsServer event loop works *(disassembly, 2026-10-13)*

The 40 functions in `scripts_server/main.lua` are the global event engine
(no event *content* — that is in `scripts/general/events*.lua` and
`default_platform_config.lua`). Mechanics recovered from the bytecode:

* **State lives per zone.** `ScriptsServer.zones[<id>].activeEvents[<name>]`
  holds each running event's live state. On start the engine walks every
  zone and every active event; if the matching `Events[<name>]` definition is
  gone it calls `ScriptsServer.RemoveEvent`, and it copies the definition's
  `disableOriginalQuests` / `enableOriginalQuests` flag into the zone's
  `disableQuests`. Then it seeds the RNG (`RNDSeed`, once, from
  `GetU64Time`).
* **Event processors.** `EVENTS_PROCESSORS` maps an event kind to a pair of
  handlers. Two kinds are built in:
  * **timer events** (`CommonTimerEventStart` / `CommonTimerEventUpdate`):
    run for a fixed duration from `startTime`;
  * **parameter events** (`CommonParamEventStart` / `CommonParamEventUpdate`):
    carry a numeric `actualParam` that grows by `growParamPerMinute` each
    minute, clamped between `minActualParam`/`maxActualParam` and shaped by
    `softMinimum`/`softMaximum` and a `power` curve; `initEventParam` /
    `nextEventInitParam` set the starting and follow-up values. These are the
    "escalation" meters behind faction ownership/expansion events.
* **Per-tick update.** `OnUpdate` advances every active event by the elapsed
  real time (`GetU64Time`, scaled by the debug `testTimeModifier` /
  `SetTimerScale`), calls the processor's update, and raises
  `NotifyEventStateChanged` when a phase boundary is crossed. `OnNewData`
  re-reads definitions; `HasActiveEventInZone` is the query used by other
  scripts.
* **Faction ownership events** (`OwnershipStart` / `OwnershipUpdate`) are a
  specialisation driven by zone owner/race/conflict changes, which is why the
  hooks above feed it.

Operator relevance: event cadence is wall-clock based and resumes from stored
per-zone state, so stopping and restarting the ScriptsServer continues events
rather than restarting them; the only global speed lever is the debug time
modifier. Forcing or disabling events is done through `forceEvents` /
`ConfigureGlobalEvents` in the platform config
([zone-events](../05-configuration/zone-events.md)), not by editing this
bytecode.

## 3. Starting a battle server directly from the executable (autotest harness)

`autotests.cfg` / `autotest.cfg` document a minimal **headless dedicated
battle** run with the game executable (no cloud):

```
set sv_dedicated 1
set net_allowCheats 1
set sv_timeoutBeforeFinishWithoutClients 3000
set sv_numBots 24
set net_autoGamePort 1
game test_ai          # load a level (needed first, "otherwise crashes in UI")
wait 10
sv_start
set cheat_fastRespawn 1
wait 10
test_gameplays test_maps.list   # "<level> <Gameplay>" per line, e.g. "s1338_devilsjaw Control"
```

Cvar/command meanings (from names, ⚠ to verify): `sv_dedicated` run as
dedicated server; `sv_start` start the listen server; `net_autoGamePort`
choose a free port automatically; `sv_numBots` bot count;
`sv_timeoutBeforeFinishWithoutClients` idle shutdown (ms); `test_gameplays`
cycles levels/gameplays for `test_gameplaysTime` seconds each.
`test_maps.list` uses gameplay *names* (`Control`) and the same level ids as
the matchmaker queues.

> This is the most direct lead for a **cloud-less community battle server**
> (Stage 5, Q14/E): run a DedicatedServer-style process standalone and have
> clients `connect` to it (community: `sv_start`/`connect` use unencrypted
> RakNet; `SCMD_CONNECT_DEDICATED_SERVER` is the encrypted cloud path).
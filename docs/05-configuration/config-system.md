# Configuration system

> Status: **Stage 1 draft.** Verified against shipped files and Hub/service logs.

## 1. Layers (highest effect first)

| # | Layer | File | Format | Edited by |
|---|-------|------|--------|-----------|
| 1 | Topology | `cloud/data/cloud.xml` | XML | admin |
| 2 | Service command-line | spawned by Hub, e.g. `-cloudAddr <id> -hostInstanceId 1 -hub 127.0.0.1:3850 -outputDir …` | args | Hub only |
| 3 | Per-service cvars | `cloud/data/<service>.cfg`, then `<service>_local.cfg` | console script | admin |
| 4 | Shared cvars | `cloud/data/common.cfg`, then `common_local.cfg` | console script | admin |
| 5 | Policy | `cloud/data/default_platform_config.lua` | Lua | admin / designer |
| 6 | Game definitions | `data/gamedata/**.lua` → generated `cloud/data/*.xml` | Lua → XML | designer |
| 7 | State | MongoDB | BSON | server (admin via GUI) |

### `.cfg` files (console scripts)

Plain Quake-style console scripts: `set <cvar> <value>`, `bind`, `exec <file>`,
`//` comments. Each ends with `exec <name>_local.cfg`; the `_local` files are
**optional overrides that are not shipped** (the log prints
`failed to read file 'common_local.cfg'` — harmless). **Put your own changes in
`*_local.cfg`** so that updates of the stock files never clobber them.

Shipped values (complete):

| File | Content |
|------|---------|
| `common.cfg` | `cl_maxFps 60`; `alt+f4` → quit; commented `db_redisHost "127.0.0.1:6379\|connpool=5"`, `cl_versionType "live"` |
| `hub.cfg` | `hub_listenTo 3850`; `hub_detachChildProcesses 1`; (commented `coordinator_timeout 3000`) |
| `loadbalancer.cfg` | `lb_listenTo 3801` |
| `shard.cfg` | `shard_listenTo 3802`; `steam_useMicroTxnSandbox 1`; `sm_overloadCounterLimit 20` |
| `chat_server.cfg` | `chat_server_port 3815` |
| `statserver.cfg` | `ss_averagingPeriod 60.0` |
| `dediserver.cfg` | `cl_maxFps 32` (server tick 30 fps = 2 × `sv_updateRate` 15), `script_gcWorkBudget 0`, `s_masterVolume 0`, `tm_enable 0`, `ssh_port 2222`, `ai_logSquads 5`, `ai_convoyDefendRadius 300`, `sv_lootCrateScanTime 3`, `ai_kiteDistance 5000` |
| `achievement_server.cfg`, `authenticator.cfg`, `game_reward_dispencer.cfg`, `lobby_server.cfg`, `matchmaker.cfg`, `quest_server.cfg`, `zone_coordinator.cfg` | only `exec <name>_local.cfg` |

Datasource search path (`cloud/datasources*.txt`): `./data`, `../data`,
`../sys_data`, `../local_data` — i.e. cloud data directory first, then the
shared game data, then system data, then an optional `local_data` override
directory *(inferred: later/earlier priority to be tested)*.
`datasources_defs_build.txt` omits `local_data` and is used by
`prepare_shared.bat`.

### Database cvars (found in binaries, not set in shipped cfg)

`db_mongoHosts`, `db_name`, `db_stats_name`, `db_adm_name`, `db_atlas_name`,
`db_redisHost`, `db_redisLoggerHost`, `db_awaitMajoritySync`,
`db_backgroundIndexes`, `db_dedicatedDbCollectionSuffix`, `db_logMessages`,
`db_logTimesMoreThan`, `db_artificialQueryDelay`. Community: "single shard DB
and region-specific managers" are configurable through these in
`common_local.cfg` (undocumented). When a *local build* is detected the Shard
rewrites default `db_name`/`db_stats_name` (`cosmosim`, `stats_cosmosim`) to
`cosmosim_<WindowsUser>` / `stats_cosmosim_<WindowsUser>`.

### Hub cvars (from strings)

`hub_listenTo`, `hub_detachChildProcesses`, `hub_destoryChildrenAfter`,
`hub_cloudXmlURL`, `hub_cloudXmlUpdateInterval`, `hub_reloadCloudXml`,
`hub_maintainanceStateURL`, `hub_overrideStatus`, `hub_statusReportFile`,
`hub_statusReportInterval`, `hub_routes`, `coordinator_tickInterval`,
`coordinator_timeout`, `coordinator_dsLoadingPriority`,
`coordinator_procdumpTimeout`, `coordinator_dontSpawnIfHubDisconnected`,
`ssh_port`, `ssh_passwd`, `ssh_MOTD`, `ssh_privateKeyFile`,
`ssh_publicKeyFile`, `ssh_sendLastConLines`, `net_useP2PSockets`.
Semantics for most of these are **unverified** (name-derived).

## 2. `cloud.xml`

```xml
<Cloud debug="0">
  <CommonCVars><CVar name="dbg_disableLuaDataFormatChecking" value="1"/></CommonCVars>
  <Node address="127.0.0.1:3850" dediServerHost="1" id="1" region="1">
    <Service type="1"/> <Service type="2"/> …  <Service type="22" priority="0"/> <Service type="23"/>
  </Node>
</Cloud>
```

| Attribute | Meaning (from the file's header comment) |
|-----------|------------------------------------------|
| `Node@address` | Host address to spawn services on **and the address handed to clients** |
| `Node@dediServerHost` | Node may host DedicatedServer processes |
| `Node@id`, `region` | Node id; region id (1 = default; `regions.xml` maps country codes to RU/EU/US/AS) |
| `Service@type` | Service type enum (see [architecture](../03-architecture/architecture.md#2-services)) |
| `Service@path` | Absolute path of executable **on the remote host** (not used in the default file) |
| `Service@priority` | Launch order: 0 low, 1 medium (default), 2 high |
| `CommonCVars` | cvars applied to every service |

**Everything the Hub parser reads** *(static, `Hub::ApplyConfigurationXml`, 2026-10-14)* - more than the shipped file uses:

| Element / attribute | Notes |
|---|---|
| `Cloud/CommonCVars/CVar@name,value` | cvars for every service of every node (shipped) |
| `Cloud/ServiceCVars/CVar@serviceType,name,value` | cvars for every service **of one type** (not in the shipped file) |
| `Node@address`, `@id`, `@region`, `@dediServerHost` | as above; a node without `id` is ignored ("has no id assigned, IGNORING THAT NODE") |
| `Node@publicIF` | an extra address stored in the node descriptor; name suggests the **public interface** of the node. Not read by any service by name; its effect is untested (Q62) |
| `Node@noGameSession`, `Node@noZoneInstance` | flags (booleans); by name: the node does not host battle sessions / open-world instances *(inferred)* |
| `Node@disabled` | the node is skipped |
| `Node/CommonCVars/CVar@name,value` | cvars for the services **of this node** |
| `Service@type`, `@priority` | as above |
| `Service@additionalParams` | extra parameters for that service process *(inferred: command line)* |
| `Service/CVar@name,value` | cvars for **this service instance** - e.g. a second Shard on the same node with its own `shard_listenTo` ⚠ untested |

`Service@path` is named only in the file's header comment; the parser
strings do not show it. Which wins between a `cloud.xml` cvar and the same
cvar in a service's `.cfg` / the platform Lua is untested.

Multi-node layouts are *possible in principle* (several `<Node>`s, `path`
attribute, LoadBalancer "balance between separate nodes") but have never been
tested by this project.

## 3. `default_platform_config.lua`

One file configures **every** service. At the bottom a dispatcher selects a
function on the global `service_type` string (set by the engine before the
config runs). The shipped file has Russian comments; a community English
translation of them exists on a fan site (source S17, link only, spot-checked
faithful; see the [source register](../sources/source-register.md)):

| `service_type` | Function | Notable content |
|----------------|----------|-----------------|
| `ST_SHARD` | `ConfigureShard()` | Accounts, store prices, premium, squad/wing limits, MMV formula cvars, offers, brawl schedule, battle pass, league bans, adaptive bot presets |
| `ST_MATCHMAKER` | `ConfigureMatchmaker()` | **All queues** (`queuesConfig`, `queuesConfigLo`), low-online thresholds, default gameplay, reward-rate schedule, PvE rotation |
| `ST_DEDICATED_SERVER` | `ConfigureDediServer()` + `ConfigureDediServerFlags(queueFlags)` | Per-battle rules: loot rules by rank, leaver penalties, rewards, events, bot presets |
| `ST_ZONE_INSTANCE` | `ConfigureZoneInstance()` | Open-world rules (47 cvars) — "restart cloud after changing these" |
| `ST_SCRIPTS_SERVER` | `ConfigureScriptsServer()` | Global events (`ConfigureGlobalEvents`, commented examples), timer scale |
| `ST_GAME_REWARD_DISPENCER` | `ConfigureGRD()` | Bonus gold, gold events, cron scheduler enable |
| `ST_LOAD_BALANCER` | `ConfigureLoadBalancer()` | `lb_limitPlayersOnShardTo = 800`, greeting-message cvars pushed to clients |
| `ST_CHAT_SERVER` | `ConfigureChatServer()` | Anti-spam "awareness" model |
| `ST_UNIVERSE` | `ConfigureUniverse()` | Universe id, faction kill factors, zone reward shares |
| `ST_QUEST_SERVER`, `ST_ACHIEVEMENT_SERVER`, `ST_LOBBY_SERVER`, `ST_LEADERBOARD_SERVER`, `ST_ZONE_COORDINATOR`, `ST_TOURNAMENT`, `ST_CLAN_SERVER`, `ST_ADVENTURE_SERVER`, `ST_HUB` | `Configure<Name>()` | See [cvar reference](cvar-reference.md) |

Helper API exposed to this Lua by the engine (names found in the file):
`MatchMaker_ReconfigureQueues(queues[, isLowOnline])`,
`MatchMaker_SetRewardRates`, `MatchMaker_SetPveSchedule`,
`BrawlManager_SetupSchedule`, `Shard_SetupBattlePassActivation`,
`QuestServer_SetupBattlePassActivation`, `Shard_SetupLeagueForbiddenEquipment`,
`Lobby_SetupLeagueForbiddenEquipment`,
`DedicatedServerServices_SetupBotPresetForbidden`,
`DedicatedServcerServices_SetLootRules` *(sic — original misspelling)*,
`DedicatedServerServices_SetIterativeLoot`,
`LoadBalancer_SetGreetingMessageCVars`, `Leaderboards_Configure`,
`Leaderboards_Routes`, `ScriptsServer:ConfigureGlobalEvents`,
`ScriptsServer:SetTimerScale`, plus `sys.new`, `sys.mergeTable`, `sys.log`.

### Gotchas found while reading the file

* `ConfigureAdventureServer()` is defined **twice** (line ≈998 with
  `cvars.adventure_saveGiverOffers = 0`, and an empty one at ≈2149). Lua uses
  the last definition, so the first one never runs *(inferred)*.
* The shipped file still contains 2023–2025 event dates (`creditsEventStart`,
  `battlePassStart`, `reward_eventGoldTimePeriod`…). Events are **time-window
  based on the server clock**; to run an event now, change the dates.
* Many comments say "restart cloud after changing these cvars" — there is no
  hot reload for the Lua policy (ConfigServer may push some values — unverified).
* The Hub logs `No 'RegionWeightProportion' table!` although `ConfigureHub()`
  defines one — the Hub probably evaluates it before executing the platform
  config, or the Hub does not run this file at all. *Open question.*
* `local x3fw = 3` ("x3 first win") multiplies daily first-win XP for
  PvP/PvE/Coop/Brawl; also pushed to clients through the LoadBalancer greeting.

## 4. Applying changes

| Changed | Do |
|---------|----|
| `*.cfg` / `default_platform_config.lua` | Restart the cloud (Hub + services) |
| Lua game definitions under `data/gamedata` that servers consume as XML | Run `cloud/prepare_shared.bat` (MongoDB must be running), then restart |
| `cloud.xml` | Restart Hub (`hub_reloadCloudXml` / `hub_cloudXmlURL` suggest a runtime reload path — untested) |
| MongoDB documents | Stop server **and** client first; restart afterwards |

See also: [matchmaking guide](matchmaking-guide.md),
[game modes](game-modes.md), [data files](data-files.md),
[cvar reference](cvar-reference.md), [cvar notes](cvar-notes.md).

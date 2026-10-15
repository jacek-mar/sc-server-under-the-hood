# Server architecture

> Status: **Stage 1 draft.** Facts marked *(observed)* come from the shipped
> logs/configs; *(official)* from Gaijin's "Local Game Launch" page;
> *(inferred)* are analyst conclusions to be verified.

## 1. Concept

A **node** is a bundle of server applications plus databases *(official)*.
The **Hub** is the first process started. It reads `cloud/data/cloud.xml`,
spawns every service listed there as a child process, and routes messages
between them *(official, observed)*. All services connect back to the Hub
(`-hub 127.0.0.1:3850`) and register themselves under a service id.

```
                      +---------------------------------------------+
  game.exe  -----3801->  LoadBalancer  (picks shard / node)          |
  (client)  -----3802->  Shard  (auth, store, mail, ship equipment)  |
                      |                                             |
                      |  Hub :3850  (spawns + routes everything)    |
                      |   |-- MatchMaker -- DedicatedServer(s)       |
                      |   |-- ZoneCoordinator -- ZoneInstance(s)     |
                      |   |-- Universe, QuestServer, ClanServer ...  |
                      |                                             |
                      |   MongoDB :27017          Redis :6379 (opt.) |
                      +---------------------------------------------+
```

## 2. Services

Type ids are the numeric `type` attribute used in `cloud/data/cloud.xml`
(enum documented in a comment in that file). "In default node" = listed in the
shipped `cloud.xml`.

| Type | Executable | Role (official description unless noted) | In default node |
|-----:|------------|-------------------------------------------|:---:|
| – | `Hub.exe` | Starts/stops other services, routes messages (ST_HUB=5, not in cloud.xml) | entry point |
| 1 | `LoadBalancer.exe` | Balance between separate nodes; first thing a client talks to *(inferred: login greeting)* | ✔ |
| 2 | `Shard.exe` | Authorisation, purchases, mail, ship equipment, and other; owns the persistence layer | ✔ |
| 3 | `MatchMaker.exe` | Matchmaking players/teams, creates game sessions, adds players | ✔ |
| 4 | `DedicatedServer.exe` | Battle ("game room") server; one process per battle. Spawned on demand, *not* in cloud.xml | on demand |
| 7 | `GameRewardDispencer.exe` | Issues rewards after battles/sessions | ✔ |
| 8 | `Authenticator.exe` | User authorisation / online-state service | ✔ |
| 9 | `ChatServer.exe` | Player chat | ✔ |
| 11 | `ConfigServer.exe` | Pushes configuration updates to services | ✔ |
| 12 | `Universe.exe` | Global state of the "universe" / zone maps and clan conflicts | ✔ |
| 13 | `QuestServer.exe` | Quest state, progress, completion, rewards | ✔ |
| 14 | `ZoneCoordinator.exe` | Tracks active zones and directs players to them | ✔ |
| 15 | *(ZoneInstance)* | Like DedicatedServer but for the open world; launched by ZoneCoordinator. Uses `DedicatedServer.exe` *(inferred: no separate exe)* | on demand |
| 16 | `LobbyServer.exe` | Pre-game lobby: rooms, lineups, readiness | ✔ |
| 17 | `AchievementServer.exe` | Achievement progress and rewards | ✔ |
| 18 | `LeaderboardServer.exe` | Leaderboards (needs Redis; data in Redis, descriptions in MongoDB - [static summary](../08-reverse-engineering/service-summaries-static.md#4-leaderboardserverexe-type-18-in-cloudxml-needs-redis)) | ✔ |
| 19 | `ClanServer.exe` | Clan data, membership and requests | ✔ |
| 20 | `Tournament.exe` | Schedules tournaments, builds teams, tracks rounds (from `tournaments.xml`, [static summary](../08-reverse-engineering/service-summaries-static.md#3-tournamentexe-type-20-in-cloudxml)) | ✔ |
| 21 | `EarlyMatchMaker.exe` | Pre-queue 1v1 ready-check matchmaker, off by default (`emm_enableEMM` 0); **not** started by default ([static summary](../08-reverse-engineering/service-summaries-static.md#1-earlymatchmakerexe-type-21-not-in-cloudxml)) | ✘ |
| 22 | `ScriptsServer.exe` | Runs server-side scripts (global events); priority 0 (started last) | ✔ |
| 23 | `AdventureServer.exe` | Adventure scenarios/events | ✔ |
| – | `StatServer.exe` | Metric aggregation; configured by `stat_server_cfg.xml` (ports 4000–4008); not started by default *(inferred)*; older 2013 build, see [static summary](../08-reverse-engineering/service-summaries-static.md#2-statserverexe-no-type-id-not-in-cloudxml) | ✘ |
| – | `CrashReporter.exe` | Targem crash reporter shim | – |

Other types in the enum: 6 `ST_ADMIN_CONSOLE`, 10 deprecated — "should not occur".

### Service ids (observed)

Services register with ids of the form `<type*8 in hex><…><sequence>`:
`810000000000001` (LoadBalancer), `1010000000000002` (Shard),
`1810000000000003` (MatchMaker), `3810000000000004` (GameRewardDispencer) …
`B010000000000011` (ScriptsServer). The Hub itself is `2800000000000001`.
Useful for correlating `Hub/logs/<id>_<name>_<date>.log`.

## 3. Start-up sequence *(observed in hub log)*

1. Hub executes `common.cfg` → `common_local.cfg` (optional) → `hub.cfg` →
   `hub_local.cfg` (optional).
2. Hub parses `cloud.xml`, applies `<CommonCVars>`, computes the digest.
3. Coordinator spawns the 17 services in priority/type order. `Universe` and
   `AdventureServer` are slow to come up (~15 s each); `ScriptsServer` last.
4. Each service starts, executes `common.cfg` + its own `.cfg` (+ `_local.cfg`),
   then calls its `Configure<Name>()` function from
   `cloud/data/default_platform_config.lua` (see
   [config system](../05-configuration/config-system.md)).
5. Shard initialises persistence (MongoDB) and creates/consistency-checks
   collections (`Persistence::_CreateTables`).
6. Services connect to the Hub and register. Whole cluster takes roughly
   **40–90 seconds** on a desktop PC (first run is slower).

## 4. Ports

| Port | Component | Source |
|-----:|-----------|--------|
| 3850 | Hub (`hub_listenTo`) | `hub.cfg`, `cloud.xml` |
| 3801 | LoadBalancer (`lb_listenTo`) | `loadbalancer.cfg` |
| 3802 | Shard (`shard_listenTo`) — client "masterServer" connection | `shard.cfg`, client log |
| 3815 | ChatServer (`chat_server_port`) | `chat_server.cfg` |
| 2222 | SSH debug console (`ssh_port`, dedicated server cfg). **Disabled** while `ssh_passwd` is empty | `dediserver.cfg`, logs |
| 9001 | Hub HTTP status endpoint (`GET /status?key=…`, JSON) — **observed**, see [verification log](../04-installation/verification-log.md) | runtime |
| 27017 | MongoDB (bound to 127.0.0.1) | `mongodb/config.cfg` |
| 6379 | Redis (optional, leaderboards) | `common.cfg` (commented) |
| 4000–4008 | StatServer providers (alias lb, shard, mm, main_hub, auth, chat, quest, achiev, zone) | `stat_server_cfg.xml` |
| 35000/udp | DedicatedServer battle (first battle; range/allocation to confirm) | observed, [protocol-observed](../08-reverse-engineering/protocol-observed.md) |
| ephemeral | ZoneInstance ports | *to be analysed* |

> **Observed:** Hub, LoadBalancer, Shard and ChatServer listen on `0.0.0.0` (all interfaces); only MongoDB is loopback-only.
>
> Official warning: the Hub **accepts connections from any address**; the
> `address` in `cloud.xml` only controls which address is *handed to clients*.
> See [security](../07-administration/administration.md#5-security).

## 5. Data & configuration layers

| Layer | Location | Consumed by |
|-------|----------|-------------|
| Game definitions (Lua) | `data/gamedata/**.lua` | client **and** DedicatedServer (read directly) |
| Generated server data (XML) | `cloud/data/*.xml` | most cloud services |
| Generator | `cloud/prepare_shared.bat` → `DedicatedServer.exe -prepareSharedData` | produces the XML from the Lua |
| Service policy | `cloud/data/default_platform_config.lua` | each service's `Configure*()` |
| Per-service cvars | `cloud/data/*.cfg` (+ optional `*_local.cfg`) | each service |
| Topology | `cloud/data/cloud.xml` | Hub |
| Persistent state | MongoDB (`%LOCALAPPDATA%\Targem\StarConflict\cloud\mongodb\data`) | Shard and most others |

## 6. Client ↔ server

* The client (`win64/game.exe`) has a login drop-down: `localhost` (default) or
  `server` + address/port. Login with a new name auto-creates an account.
* `win64/local_server.xml` makes the client start MongoDB and Hub itself and shut
  them down on exit (Steam launch). A "Launch server" button runs
  `win64/launch_server_and_db.bat`.
* Client communicates with the cloud via LoadBalancer → Shard ("masterServer"),
  then battles run on a DedicatedServer process.

## 7. Open architectural questions

See [open-questions](../08-reverse-engineering/open-questions.md): wire
protocol, multi-node/region topology (`RegionWeightProportion` warning, 
`regions.xml`), DedicatedServer port allocation, EarlyMatchMaker role.

Per-service MongoDB collection presence and source modules: [service-data-map](../08-reverse-engineering/service-data-map.md) (generated).

# Four lesser-documented services, read statically

> Analysis of 2026-10-11/12. Static strings/cvar analysis of
> `EarlyMatchMaker.exe`, `StatServer.exe`, `Tournament.exe` and
> `LeaderboardServer.exe` (the four executables [architecture.md](../03-architecture/architecture.md)
> §2 lists with the least detail). Nothing was executed. Cross-checked
> against [cvar-defaults.md](../05-configuration/cvar-defaults.md) and the
> module/collection map [service-data-map.md](service-data-map.md). Tournament
> and LeaderboardServer *are* in the shipped `cloud.xml`
> (architecture.md marks them "✔ in default node"); EarlyMatchMaker and
> StatServer are not.

## 1. `EarlyMatchMaker.exe` (type 21, not in `cloud.xml`)

A **separate, pre-queue "ready check" matchmaker** for 1-on-1 pairing, distinct
from the main `MatchMaker.exe`. Evidence: log strings `EnterMMQueue: uid = %s,
uidOpponent = %s`, `EMM: %s record: uid = %s, region = %u, mmRank = %u,
mmValue = %u`, `EMM: Change record: uid = %s, isReady = %s`. The Shard side
(`SessionManager`/`Task_EMM*`) creates and updates these records
(`Task_EMMUpdateRecord` reads the account's vessel locks, battle slots,
autogen inventory, squad and tournament records before writing the match
record; `Task_EMMChangeReady` flips the `isReady` flag after loading battle
slots), so a client locks in its ship/loadout before the actual pairing
happens - the "early" in the name.

Cvars *(file)*: `emm_enableEMM` (default **0** - the feature is off even when
the process runs), `emm_minAccountRank` (default **7**: accounts below this
rank never enter EMM), `emm_checkRegion` (0), `emm_mmValueDiff` (200: maximum
MMV gap for a pair). Service id `ST_EARLY_MATCHMAKER`. It needs
`emm_enableEMM = 1` (Shard) *and* a `cloud.xml` entry for type 21 to do
anything; neither is shipped, so it looks like a mode that was not active in
the final build *(inferred)*. Not required for a stock community node.

## 2. `StatServer.exe` (no type id, not in `cloud.xml`)

A **metric-aggregation and clan-event logging service**, separate from the
telemetry sinks covered in
[external-services-and-login-modes](external-services-and-login-modes.md).
Logs clan-economy events by name (`CLAN_ASSIGN_EMBLEM`, `CLAN_BANK_TRANSFER`,
`CLAN_NAME_CHANGE`, `CLAN_RACE_CHANGE`, `CLAN_REGISTRATION`,
`CLAN_TAG_CHANGE`, `CLAN_UPGRADE`) and leaderboard decay
(`clanLeaderboardsDecay_interval` 60 min, `clanLeaderboardsDecay_percents` 1%,
cvar table). `ReportCloudStatistics: Failed to Insert` writes periodic cloud
status into the DB; `office.targem.ru:996`
([external-services-and-login-modes](external-services-and-login-modes.md))
is a vendor reporting endpoint, dead on a community node. It carries its own
**legacy SSH console build** with weaker compiled-in defaults (port 22,
non-empty password) - security finding S-22. It is the only executable built
from a materially older codebase: PE timestamp **2013-11-08** (all others are
2026-10-07/09, [pe-imports.md](pe-imports.md)) and it also embeds its own
copies of `AES.cpp`/`Bignum.cpp` instead of calling `libcrypto`
([service-data-map.md](service-data-map.md) §2) - a much older build of the
shared engine kept around just for this one service. **Recommendation**: do
not start it on a network-exposed node; if you need its metrics, run it
behind the same firewall rules as the rest of the cloud and override
`ssh_port`/`ssh_passwd` in `statserver_local.cfg` first.

## 3. `Tournament.exe` (type 20, in `cloud.xml`)

Runs scheduled tournaments from **`cloud/data/tournaments.xml`** (shipped,
1 KB; schema in [xml-schemas](../05-configuration/xml-schemas.md), summary in
[data-files](../05-configuration/data-files.md)). The shipped file has
`enable="1"`, 3 rounds, 10 min registration, 1 min preparation, 10 min rounds,
round-reward multipliers 0 / 0.5 / 1 / 2 by wins, and **two weekly
tournaments** (`d="0" h="17"` and `d="6" h="16"`, ranks 7-9, bots
`BotsT3E`) paying 0 / 150 / 250 / 400 gold by wins. `Failed to read
'tournaments.xml'` / `Failed to load tournament!` are the log symptoms of a
missing or broken file. Lifecycle logged
in plain English: `Load tournament: registration continues` ->
`preparing first round` -> `preparing round %d` -> `round %d is active` ->
`full tournament time expired`; team forming logs `Creating game for teams %d
and %d`, `Teams %d and %d created`, `Team %d win the game in this round`,
`RoundRewards`; failure modes `Insufficient players for team making`, `No
players for team making`, `No team or standalone record for uid %s`. It also
references the **league-team** event names `LEAGUE_TEAM_ACCEPT_INVITE`,
`LEAGUE_TEAM_KICK`, `LEAGUE_TEAM_LEAVE`, `LEAGUE_TEAM_NAME_CHG` (event/log
identifiers; the league-team *admin* tasks such as `banLeagueTeam` live in the
Shard, [shard-admin-tasks.md](shard-admin-tasks.md)). Persists through
the `tournament`/`tournamentRecords`/`leagueTeams` collections
([service-data-map.md](service-data-map.md) §1). To change tournaments on a
community node, edit `cloud/data/tournaments.xml` (day `d` is presumably the
weekday, `h`/`m` the start time - timezone and weekday base untested).

## 4. `LeaderboardServer.exe` (type 18, in `cloud.xml`, needs Redis)

Confirms the "needs Redis" note in architecture.md with code: `Failed to
persistence::InitRedis()`, `CloudService::Init(): can't initialize redis
logger` - leaderboard data lives in **Redis**, not MongoDB (MongoDB only
stores the leaderboard *descriptions*, via `persistence::LoadLeaderboardDescs`
and the `leaderboards`/`leagueTeams` collections). Each leaderboard
description (`LeaderboardDesc`) carries a reward type restricted to one of
`LET_PLAYER` / `LET_CLAN_MEMBER` / `LET_LEAGUE_TEAM` / `LET_MAJOR_LEAGUE_TEAM`,
and a position range (`posMin`/`posMax`); update **routes** map in-game events
to leaderboard updates (`LeaderboardServer: no event name for route`, `no
target for route`, `unknown update type for route` - i.e. a route is
`{event, target, updateType}`). Leaderboards **decay** on a schedule
(`LbrdOp_Decay`, `DecayLeaderboard: multi-decay, %s times more powerful!` for
a missed tick) and **expire** (`ExpireLeaderboard: next expiration: %s`,
`looks like we missed %s ticks` - both tolerant of the service having been
down). Clan/league-team removal cleans up their leaderboard entries
(`LbrdOp_DeleteClan`, `LbrdOp_DeleteClanMember`, `LbrdOp_DeleteLeagueTeam`).
**Practical point for hosting**: a node without Redis can still run - the
cloud.xml comment calls Redis "optional" - but `LeaderboardServer` will log
init failures and leaderboards stay empty/stale; this matches the
`db_redisHost` line being commented out in `cloud/data/common.cfg`
(config-system.md).

## 5. Cross-reference

All four are already listed in [architecture.md](../03-architecture/architecture.md)
§2 with a one-line role and their `cloud.xml` type id; this document only adds
the static detail the strings give. None of this touches authentication or
credential handling.

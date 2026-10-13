# Client ↔ cloud protocol — observed vocabulary and sequences

> Status: **observed** (client `game.net.log` + DedicatedServer log of a real
> local session, 2026-10-10/11, build 1.99.0.167293). Message *names* and call
> order only — the binary wire format is **not** documented yet (Q14). Names
> match the enums in [masterserver-enums.md](masterserver-enums.md) and the
> `cl_netLog*` / `game.net.log` facility of the client.

## 1. Transport summary

| Leg | Transport | Port | Evidence |
|-----|-----------|-----:|----------|
| Client → LoadBalancer | TCP | 3801 | client log `connecting to load balancer at 127.0.0.1:3801` |
| Client → Shard ("masterServer") | TCP | 3802 | `Closed connection with masterServer addr …:3802`; `SCMD_ASSIGNED_SHARD` |
| Client → ChatServer | TCP | 3815 | listens on 0.0.0.0; sends bytes at connect |
| Client → DedicatedServer (battle) | **UDP** (game networking) | 35000 in the first battle (`server: started at port 35000`) | monitor: `udp+ DedicatedServer 35000`; DS log |
| Services → Hub | TCP | 3850 | Hub log |
| Everything → MongoDB | TCP | 27017 | |

Battle port selection: the DedicatedServer logged
`Dedicated server launched on address 127.0.0.1|35000` — 35000 is likely the
base of a configured range (`net_autoGamePort` / `net_gamePort`, ⚠ to confirm
with a second concurrent battle). The address is advertised from `cloud.xml`.

## 2. Login handshake (order as seen in `game.net.log`)

```
client                                   server
 -> (TCP connect LB:3801)
 <- SCMD_LB_CVARS            load-balancer cvars (greeting message cvars, e.g. x3 first-win)
 <- SCMD_ASSIGNED_SHARD      which shard to use
 -> SCMD_KEEP_ALIVE (req 1)
 <- SCMD_AUTH_REQ            server asks for credentials
 -> CCMD_AUTH_REQUEST (req 2)
 <- SCMD_AUTH_ACK            accepted
 -> CSCMD_ASYNC_REQ AC_SERVER_INFO, AC_WELCOME_MSG, AC_MOTD
 -> CCMD_STORE (store sync) + AC_LOAD_INITIAL_PLAYER_DATA, AC_CLAN_REQUEST_DESC,
    AC_LOBBY_INFO, AC_FRIENDS_SEND_REQUEST, AC_MAIL_GET, AC_LEADERBOARD_GET_DESCS,
    AC_TEACHING_LIST, AC_SQUAD_INFO, AC_LEAGUE_TEAM_INFO, AC_QUESTS, AC_ADVENTURES
 <- SCMD_STORE / CSCMD_ASYNC_REQ responses (resp: <req id>)
```

Request pattern: all "RPC" calls travel as `CSCMD_ASYNC_REQ` carrying an
`AC_*` action id, answered by `CSCMD_ASYNC_REQ resp: <req>`; the store/inventory
sync uses `CCMD_STORE` ↔ `SCMD_STORE`. Round-trip on loopback ≈ 30 ms
(`new RTT: 33ms`).

## 3. Message names seen

| Class | Names |
|-------|-------|
| Control | `SCMD_LB_CVARS`, `SCMD_ASSIGNED_SHARD`, `SCMD_AUTH_REQ`, `CCMD_AUTH_REQUEST`, `SCMD_AUTH_ACK`, `SCMD_KEEP_ALIVE` |
| Transport of RPC | `CSCMD_ASYNC_REQ` (both directions), `CCMD_STORE`, `SCMD_STORE` |
| Notifications | `SCMD_NOTIFICATION`, `SCMD_QUEST_NOTIFICATION`, `SCMD_VESSEL_NOTIFICATION`, `SCMD_USER_PROFILE_NOTIFICATION` |
| Battle hand-over | `SCMD_CONNECT_DEDICATED_SERVER`, `SCMD_GAME_ENDED` |
| `AC_*` actions | `AC_SERVER_INFO`, `AC_WELCOME_MSG`, `AC_MOTD`, `AC_LOAD_INITIAL_PLAYER_DATA`, `AC_SET_USERDATA`, `AC_SEND_EARLY_PLAYER_LOG`, `AC_UNIVERSE_GET`, `AC_ZONES_LUA_ACTIVE_EVENTS_UPDATE` (polled ~1/min), `AC_MM_INFO`, `AC_ENTER_MM_QUEUE`, `AC_BATTLE_SLOT_CHANGE_VESSEL`, `AC_USER_PROFILE_GET`, `AC_CLAN_REQUEST_DESC`, `AC_LOBBY_INFO`, `AC_FRIENDS_SEND_REQUEST`, `AC_MAIL_GET`, `AC_LEADERBOARD_GET_DESCS`, `AC_TEACHING_LIST`, `AC_SQUAD_INFO`, `AC_LEAGUE_TEAM_INFO`, `AC_QUESTS`, `AC_ADVENTURES`, `AC_SURVEY_GET_NEW`, `AC_SURVEY_RESULTS` |

Community (unverified) note: the packet-type name array in the executable
starts with `AC_LOAD_INITIAL_PLAYER_DATA` — consistent with the first RPC
after authentication above.

## 4. Matchmaking → battle sequence (one Coop-vs-AI "newbie" queue, 1 player)

| Time | Event |
|------|-------|
| t | client `AC_ENTER_MM_QUEUE` |
| t+~0 | MatchMaker decides; Hub log: `Request to launch game … launching game server 3 on node 1` (region priority list, `AR_RU 0.5559`) |
| t+1 s | Hub spawns `DedicatedServer.exe` with params `-cloudAddr 2010000000000003 -hostInstanceId 1 -hub 127.0.0.1:3850 -outputDir <Hub dir> -gsid 3 -regionId 1` (service id prefix `20…` = type 4 × 8 as 0x20) |
| t+5 s | DS connects to Hub as `2000000000000003`, reads **GameSessionParameters** from MongoDB (`_id`, `queueFlags`, `coop_vs_ai`, `queueSpec`, `maxPlayers`, `botsCount`, `rate_exp`, reward fields, players/vessels) |
| t+6 s | `Starting dedicated game server. gameMode 9 (sentinel), gameDuration 900, levelName 's1338_pandora_dreadnwreck', maxPlayers 8, botCount 1`; `server: started at port 35000` |
| t+7 s | client `SCMD_CONNECT_DEDICATED_SERVER` → UDP connect from client port; `server: incoming connection … authorize…`; client sends its **list of running process names** (`Client 0, uid 2. process list: …`) |
| t+13 s | `Client 0 (<name>, 2) joined the game. team 1`; first snapshot (4.7 KB) |
| end | DS writes per-player result (`isLeaver`, `leaveFineCoef`, `vesselsRewards` …) to the DB; `SCMD_GAME_ENDED`; Hub `DeleteDediServer`; process exits |

Notes:
* `gameMode 9` came from the queue's `levelsDesc` entry for this map
  (`{4,9,11}` list → Sentinel chosen), not from the player.
* Game duration 900 s and reward/bonus calculations (`PlayerRewardBonuses
  rank …, mastery …`) are computed in the DedicatedServer, using
  `ConfigureDediServer()` cvars.
* DS warns `SetCvarValue: could not find cvar 'event_custom'` — a config entry
  with no engine cvar in this build (harmless).

## 5. Privacy finding — process list upload

On connecting to a DedicatedServer the client reports the **names of all
running processes** (anti-cheat telemetry) in the server log. A community
server operator receives this data; treat it as personal data
([administration → privacy](../07-administration/administration.md#privacy)).
Clients should know a server can see it.
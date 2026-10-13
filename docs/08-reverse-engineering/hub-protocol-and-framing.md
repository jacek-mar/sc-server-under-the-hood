# Hub, cloud messages and TGP framing (static analysis)

> Analysis of 2026-10-11. Static analysis of `Hub.exe` strings and code (build
> 1.99.0.167293) (strings and machine code),
> cross-checked by string presence in `Shard.exe`, `LoadBalancer.exe`,
> `ChatServer.exe`, `DedicatedServer.exe` and the client `game.exe`. **Nothing
> was executed or captured**: header layouts below are read from machine code
> and are *(disasm)*; semantics marked *(inferred)* need a capture to confirm
> (WP-1/WP-2, needs maintainer approval). Part of the answer to Q14 (framing).
> Companion docs: [protocol-observed](protocol-observed.md),
> [masterserver-enums](masterserver-enums.md),
> [architecture](../03-architecture/architecture.md).

## 1. Layers found in the binaries

| Layer (source file) | Where | Role *(inferred from strings/code)* |
|---------------------|-------|-------------------------------------|
| `NetSocket` / `NetChannel` / `NetEndpoint` | all services, client | TCP sockets with `select`, keep-alive (`SendKeepAlive`), send buffer cap, disconnect reasons, cvar `net_dumpCloudMsg` |
| **`CloudChannel` / `CloudMessage` / `CloudService`** | all cloud services (Hub, Shard, LB, ...) | **inter-service messages** with a 27-byte routing header (section 2); services register themselves with the Hub |
| **`TGPChannel` / `TGPEndpoint` / `TGPMessage`** | all services **and the client `game.exe`** | **opcode/request framed messages** with a 12-byte header and a checksum (section 4) - the client-facing master channel |
| `ProtoServer` / `ProtoMessage` | all services | peer handshake with inbound/outbound channel maps, `ClaimPeerID`, `EnforcePeerID`, duplicate interconnection prevention; purpose (stat system / peer mesh) not pinned down |
| `JSONPServer` | Hub | the HTTP status endpoint (`jsonp_listenPort` 9001) |
| `SSHServer` (`SSH.cpp`) | all | legacy SSH Lua console (V-7) |
| `StatSystemEndpoint`, `StatsdClient`, `GonalyticsClient`, `RedisLogger`/`TRedisEndpoint` | all | optional telemetry (UDP statsd 8125, gonalytics 37331, Redis logs) - all disabled by default |
| `HubSvc`/`WinService`, `ASelfUpdater` | Hub | Windows-service install (`-install/-uninstall/-start/-stop`), self-updater |

## 2. Cloud message header and routing rules *(disasm)*

`CloudChannel::ConstructMessage` needs at least **27 (0x1b) bytes**; the first
field is read with `ntohl` and is the payload length (limit **0x3FFFE5**, i.e.
frame <= 4 MiB; error `message size is too big`); the header is then copied
as-is. The in-memory message object (after an 8-byte object prefix) mirrors the
wire header; the dump format `Cloud message dump: %u, %u, %u, %s, %s, %u, %u`
prints it in this order:

| Offset | Size | Field | Notes |
|--------|------|-------|-------|
| 0 | u32 | payload length | network byte order (`ntohl`) |
| 4 | u16 | field A | request/correlation id *(inferred; used by `FindRequestDesc`)* |
| 6 | u16 | field B | *(inferred)* second id/flag |
| 8 | u64 | source address | printed as hex service id (`%I64X`) |
| 16 | u64 | destination address | |
| 24 | u8 | **routing rule** | `routing.hrr.*`, table below |
| 25 | u16 | **command** | the "command" printed by `OnMessageToHub: Unknown command %d` |

Service addresses are 64-bit ids; the *service type* is derived from the
address (`ExtractServiceType`, `ExtractServiceType(addr) == ST_HUB`), the
convention "type x 8 in hex" from the first sessions (Hub `2010000000000003`
for service 3 etc., see [protocol-observed](protocol-observed.md)).

**Routing rules** (jump table in `Hub::OnMessage`, value = table index):

| Value | Name (`hrr.`) | Meaning *(inferred from name + handler)* |
|------:|---------------|-------------------------------------------|
| 0 | `TO_HUB` | message for the hub itself (`OnMessageToHub`, commands incl. launch requests, config) |
| 1 | `HUB_BROADCAST` | broadcast between hubs (`OnHubBroadcast`) |
| 2 | `TO_ADDR` | deliver to an explicit destination address |
| 3, 4 | `TO_SHARD_H_U` | to the Shard chosen by **hash of the user id** (two values share one handler) |
| 5 | `TO_EVERY_O_T` | to **every** service **of a type** |
| 6 | `TO_ANY_O_T` | to **any one** service of a type |
| 7 | `TO_QS_H_U` | QuestServer by user-id hash |
| 8 | `TO_AS_H_U` | AchievementServer by user-id hash |
| 9 | `TO_AU_H_U` | Authenticator by user-id hash |
| 10 | `TO_AD_H_U` | AdventureServer by user-id hash |

Values above 10 take the error path `unknown routeRule %d`. The Hub keeps
per-uid routing (`SendMessageToShardByUid() failed ... due to !sAddr`, quest/
achievement/authenticator/adventure variants): a message for a given user is
sent to the one service instance selected by the user id, so a replacement
service has to register under the same routing keys.

## 3. Hub behaviour worth knowing *(strings + cvars)*

* **Registration:** a connecting service sends a register message; failures log
  `Connectee at %s failed to register itself`; success logs `registered itself
  as <addr>`. A new hub ("node") must present the same **involved-nodes digest**
  and cloud address; a different **build string** (`1.99.0.167293` is compared)
  makes the hub hibernate (`outdated version`). A hub that is in maintenance
  mode makes newly connected hubs follow.
* **Cloud configuration:** `cloud.xml` is loaded from file or downloaded from
  `hub_cloudXmlURL` every `hub_cloudXmlUpdateInterval` (120 s) (default URL
  empty = file only); a digest of the document is logged; `ApplyConfigurationXml`
  needs a `Cloud` node and a node entry for itself; duplicate cloud addresses
  abort the reconfiguration; `hub_reloadCloudXml` re-reads it on demand.
* **Coordinator** (`coordinator_tickInterval` 10 s): each tick computes
  services to launch/destroy; `coordinator_timeout` (600 s) removes silent
  services and dedicated servers, `coordinator_procdumpTimeout` (600 s) makes a
  crash dump of a hung one; `coordinator_dontSpawnIfHubDisconnected` (1) blocks
  spawning on a not fully connected cloud (the observed "services die when the
  Hub stalls" failure, V-5). Spawn command line (format string):
  `"%s" -cloudAddr %s -hostInstanceId %u -hub %s ...` + `-instId %s -regionId %d`
  (services) or `-gsid %s -regionId %d` (dedicated servers); `ZoneInstance`
  launches are routed to a hub chosen by region (`ChooseHubByRegion`, overload
  modes "full scale"/"regional"; `coordinator_zoneInstanceUsToEu`).
* **Maintenance:** `enterMaintenanceMode` / `leaveMaintenanceMode` console
  commands, cvar `cloud_maintenanceMode`, URL `hub_maintainanceStateURL`;
  status is also written by `hub_statusReportFile` every
  `hub_statusReportInterval` (60 s) and via the JSONP endpoint.
* **Debug aids for a lab node:** `net_dumpCloudMsg 1` logs **every cloud
  message** sent/received (decoded header + hex), `hub_logToAuthenticatorMessages
  1` logs everything routed to Authenticators, `dbg_logAdminTask`,
  `cl_netLogEnabled`. These give a protocol trace **without any packet-capture
  tooling** on the loopback/LAN node (candidate for WP-1; remove after use,
  messages may contain personal data and password hashes).

## 4. TGP frame (client-facing channel) *(disasm, `TGPChannel::ConstructMessage`)*

```
 0               4       6       8       10      12
 +---------------+-------+-------+-------+-------+----------- ... ---------+
 | payload length| fld a | fld b | fld c |checksum|        payload         |
 | u32 big-end.  | u16BE | u16BE | u16BE | u16 BE |  `length` bytes        |
 +---------------+-------+-------+-------+-------+----------- ... ---------+
```

* Frame = 12-byte header + `length` bytes; `length` <= **0x3FFFF4**
  (`message size is too big`), otherwise the channel is closed; a frame is
  read only when the whole `12 + length` bytes are buffered.
* The three u16 fields *(disasm, 2026-10-13)*: `TGPChannel::ConstructMessage`
  (`Shard.exe` VA 0x514b40) byte-swaps wire offsets 4, 6, 8, 10 into message
  object offsets 0x0c, 0x0e, 0x10, 0x12, and `TGPEndpoint::OnMessage` logs
  `opcode %d, req %d/%d` with object 0x10 as the opcode and 0x0c/0x0e as the
  pair. So: **offset 4 = request id, offset 6 = second id of the pair
  (response/"in reply to", inferred by analogy with the engine's MongoDB
  client that logs `reqId`/`respId`), offset 8 = opcode**, offset 10 =
  checksum. The Shard's `SessionManager::OnMessage` branches on that opcode
  field (e.g. values 4 and 0x18 right after the log line).
* The payload is handed to a **bit stream** (`BitStream.cpp`,
  `TargemBitStream.cpp`): the code passes `length * 8` bits, so fields inside
  the payload are bit-packed, not byte-aligned; the type layer is
  `Reflect\TypeDatabase.cpp` (`cl_dumpTypeDb`).
* **Checksum** (offset 10, 16 bit): recomputed with the checksum field zeroed;
  mismatch -> `checksumOfData != checksumInMsg ( %x != %x )` and disconnect.
  Algorithm *(disasm)*: a **progressive MurmurHash2A-style hash** (multiplier
  `0x5BD1E995`, shift 24; final avalanche `h ^= h >> 13; h *= m; h ^= h >> 15`)
  with **seed `0x1337533D`**, fed first with the 12 header bytes (little-endian
  in-memory form of length/a/b/c and a zero checksum), then with the payload
  bytes; the **low 16 bits** of the 32-bit result are sent. It is an
  integrity/accident check, **not authentication**. (Variant detail: the
  state is initialised on the first update as `seed ^ <first chunk length>` =
  `seed ^ 12`, and each update call finishes its own tail bytes.)
* The same checksum string is present in the client `game.exe`, so the client
  very probably uses this framing on its TCP connections (LB, Shard, Chat)
  *(inferred; needs one capture)*; the UDP battle
  channel is a different (RakNet-derived) stack.

## 5. Observations for operators and implementers

* **No transport authentication on the cloud channel** other than the
  registration message: any process that can reach the Hub's TCP port (3850)
  and speaks the 27-byte framing can register as a service (S-04/S-05 context).
  Keep 3850 and all service ports on loopback/LAN.
* **SSH console logs failed passwords in clear** (`SSHServer: failed auth
  attempt ( passwd: '%s', addr: %s )`): log files must be treated as secret;
  anybody mistyping a password leaves it in the log (new finding S-24, Low).
* The routing table shows which services are **per-user sharded**: Shard,
  QuestServer, AchievementServer, Authenticator, AdventureServer. A
  re-implementation of one of them must honour the same routing key (hash of
  the uid) or run as a singleton.
* The tight coupling between the build string, the cloud digest and the
  version check means mixed-build nodes cannot join one cloud (relevant for
  multi-node community clouds and for a replacement service that reports a
  different build).

## 6. Client authentication entry at the Shard *(strings + disasm, `SessionManager`)*

* A client connection is `NetChannel` + TGP; until it has sent
  `CCMD_AUTH_REQUEST` anything else is rejected (`Client at %s is not yet
  authorized, but have sent something aside from CCMD_AUTH_REQUEST`). The reply
  is `SCMD_AUTH_ACK` (`AcceptClientOnChannel ... logged in as %s`); a second
  login of the same uid is `Multiple login at shard`.
* The request carries a **password hash that is AES-encrypted** and is decoded
  with an integer key (`Decoding password hash using '%d' as a key`, field
  limit 255 bytes); afterwards `Task_AuthUser` is pushed. This is the code
  behind S-19: the *hash* is the credential.
* Two compatibility gates apply before login: `client has unacceptable game
  version %s` and `client has unacceptable data hash %x`. The data-hash list
  is read from `sm_dataHashUpdateUrl` every `sm_dataHashUpdateInterval` (60 s);
  its shipped default is **empty**; log lines `read datahash %d '%s', using %d
  as supposed data hash from clients`, `skipping datahash ... due to
  incompatible version`. `net_checkVersion` (default 1) is the engine-side
  client/server version verifier. With an empty list the check is skipped: `SessionManager` sets a flag when
  the list count is 0 and accepts the client without comparing (2026-10-12,
  Q3).
* Keep-alive: `didn't send keep-alive for too long, disconnecting`.

## 6a. All version and data checks between client, Shard and battle server *(disasm, 2026-10-13)*

Build 1.99.0.167293 (the build string is embedded in `game.exe`,
`DedicatedServer.exe`, `Shard.exe`, `Hub.exe` and `LoadBalancer.exe`).
There are **five** checks in total; three of them can reject a client.

| # | Where | What is compared | On mismatch | Switch |
|---|---|---|---|---|
| C1 | Client login window (Lua, `data/ui/scripts/windows/loginwnd.lua` `RequestServerStatus`/`UpdateWarningText`) | `GetAppVersion()` against a version string fetched over HTTP from `net_masterServerVersionUrl` | **Warning text only**; the Log in button stays enabled (`GetLoginStatus` only checks the input fields). For a Steam account with `cl_versionType` `live`/`test`/`pubtest` it also calls `Steam_MarkContentCorrupt()` (Steam then re-validates the files, *inferred* from the Steamworks API name) and shows a message box; the `QuitGame()` after it is commented out | Skipped when the URL is empty - the shipped client `config.cfg` (misc.pak) has the URL line commented out, so **inactive on a stock client** |
| C2 | Shard, first login message (`SessionManager`, around VA 0x40af5c) | client build string vs. own build | Reply `0x23`, connection refused; log line `has unacceptable game version` only if a log-level cvar is >= 1 | none; accepted if **either side's build string is `local`** |
| C3 | Shard, same message | client data hash vs. the list from `sm_dataHashUpdateUrl` (entry must also match the version) | refused, `has unacceptable data hash` | **empty list = accept everything** (shipped default, 2026-10-12) |
| C4 | Battle server handshake, command `0x90` in state `SS_SRV_VERSION_CHECK` (`NetworkSystem.cpp`, `DedicatedServer.exe` VA 0x445d1b) | (a) a protocol number that must be **14**, and a 7-bit mode value that must equal the server's mode; (b) the build string | (a) `Invalid protocol version for client` -> disconnect `DR_BAD_PROTO_VERSION` (2); (b) `Invalid game build number for client '%s', expected '%s', got '%s'` -> `DR_BAD_GAME_VERSION` (3) | (b) only when `net_checkVersion` = 1 (default) and an internal server flag is set; accepted if either side is `local`; (a) always |
| C5 | Battle server, same message | **Entity-defs hash**: a pair (number of entity defs, 32-bit hash) | `Invalid EntityDefs for client` -> `DR_BAD_GAMEDATA_VERSION` (4) | none - **always enforced** |

**Build compatibility rule (C2, C4b; `IsCompatibleClientVersion`, also
exposed to Lua):** both strings non-empty, split at `.`, same number of parts,
and every part **except the last** equal. So `1.99.0.<any>` is compatible with
`1.99.0.167293`; a different last part is accepted (the DS logs `Client '%s'
has compatible version (%s), but it's different from mine`). A one-part string
must match exactly.

**What the entity-defs hash covers (C5):** the routine that logs `Entity Defs
hash %08X. calculated in %0.2f ms` (`DedicatedServer.exe` VA 0x43d720; the
same string exists in `game.exe`) stores the number of entity defs and feeds
a hash with the **names** (string + length) of every entity def, every spell
def and every account-aura def, in registry (load) order. Def *values* are
not hashed. Consequences *(inferred from the code, not yet tested)*:

* adding, removing, renaming or re-ordering a def (ship, module, weapon,
  projectile, spell, aura) on one side only -> every battle join fails with
  `DR_BAD_GAMEDATA_VERSION`, while Shard login still works (C2/C3 do not look
  at defs);
* changing numbers inside an existing def (hull, damage, prices, flags) does
  **not** trip C5 - consistent with test V-10 (hull edit on the server only,
  client joined and the DS was authoritative);
* the community reports from batch 006 (I4) split along this line: an extra
  weapon slot or new item = new defs -> lockout; balance edits -> desync
  only. Proposed test: add one def on a server copy, expect reason 4 in the
  client log).

**Answer to the community claim (b008 K4) "two client checks and one server
check; the server one can be bypassed by hard-coding the client's values":**
partly right. The client has one active-by-design check (C1, warning only,
off by default); the client *sends* the values for C2-C5; its receive side of the handshake
was not disassembled (`game.exe` contains the same `NetworkSystem` code,
including the server role used by practice games). The server side has two places (Shard
C2/C3, battle server C4/C5). Patching is not needed for the build check:
`net_checkVersion 0` on the battle server disables C4b, `local` as build
string passes C2/C4b, and the build-number part may differ anyway. **C4a and
C5 cannot be switched off by configuration** - a host who changes the set of
defs must ship the same def files to every client.

## 7. Open points

* Not to be confused: `TMEndpoint::OnMessage: FindRequestDesc failed, reqId = %d, respId = %d` (in every service) belongs to the engine's own **MongoDB wire-protocol client** (`TargeMongo\TMEndpoint.cpp`, checks `OP_REPLY`, i.e. MongoDB `requestID`/`responseTo`), not to the TGP or cloud channel.

* ~~Which u16 is opcode / request id / response id~~ **TGP pinned (2026-10-13, §4)**; for the cloud header the roles of fields A/B (offsets 4/6) are
  still inferred - needs a capture or `net_dumpCloudMsg` output.
* Handshake/authentication on the TGP channel (key exchange, `SCMD_*` ordering)
  - `CRYPTO` use found in S-21; needs capture (WP-2).
* The `ProtoServer` peer protocol: who uses it (statsystem vs. nodes).
* Exact numeric `command` values: the per-service command enums are the
  `SCMD_*`/`CSCMD_*`/hub command tables of
  [masterserver-enums](masterserver-enums.md) *(the hub-internal enum was not
  separated there)*.

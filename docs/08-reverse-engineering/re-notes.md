# Reverse-engineering notes

> Status: **Stage 1 — first observations only.** Everything here is derived
> from static strings, file layout and logs. No decompilation has been done.
> Respect the licence terms ([legal](../09-community-edition/legal-and-licensing.md)):
> analysis for interoperability/community-server purposes only; do not publish
> proprietary binaries, assets or large verbatim extracts.

## 1. Binary facts

| Binary | Size | Observations |
|--------|-----:|--------------|
| `cloud/*.exe` services | 1.0–2.7 MB | Same engine framework, Hub-style console, own `NetEndpoint`/`NetChannel` layer, `ConCmdSystem`, `CloudConsoleCommands.cpp`, `HubConsoleCommands.cpp`, `ScriptServer_Commands.cpp` (source file names leak via assertion strings) |
| `cloud/DedicatedServer.exe` | 11.2 MB | Full game simulation + `-prepareSharedData` generator |
| `win64/game.exe` | 15.8 MB | Client; `D3DX9_43`, FMOD Ex, XInput 1.3 |
| Crypto/network | | Custom-named OpenSSL 1.1 (`libssl-1_1_tg*.dll`), libcurl 7.62.0 / OpenSSL 1.1.0h (HTTP client) |
| Scripting | | **LuaJIT 2.1.0-alpha** (`luaJIT_BC_%s` bytecode names, Lua 5.1 API) |
| Build | | Hub `1.99.0.167293`, 2026-10-09 14:07:47 |

Strings dumps were produced with a trivial ASCII extractor (≥ 6 chars);
counts: Hub 3.9k, MatchMaker 4.6k, Shard 12.1k, DedicatedServer 38.7k,
game.exe 38.0k lines.

## 2. Process model

* All services share one binary template: parse args
  (`-cloudAddr <id> -hostInstanceId <n> -hub <host:port> -outputDir <dir>`),
  execute `common.cfg` + `<svc>.cfg`, run `default_platform_config.lua` with the
  global `service_type`, connect to the Hub, register with the id.
* Hub → children via `ProcessDesc` (`CreateProcess`), detached unless
  `hub_detachChildProcesses = 0`.
* Message routing: `hub_routes`, `OnMessageToHub`, `OnHubBroadcast`
  (unknown-command guards). Message ids are numeric, protocol undocumented.
* Persistence layer (`Persistence`, `TMEndpoint`, `TaskManager`): Mongo access
  with seeds list, `_CreateTables`, optional Redis logger.
* `sys.new`, `sys.mergeTable`, `sys.log` are the Lua *sys* module used in config.

## 3. Data formats seen

| Ext | Count | Hypothesis | Status |
|-----|------:|------------|--------|
| `.pak` | 588 | TPAK v7 archive — **format fully documented**: [tpak-format.md](tpak-format.md); all 588 paks readable; inventory in [pak-contents.md](../02-inventory/pak-contents.md) | solved |
| `.map` / `.nav` | 249 / 226 | Level geometry/object map / navmesh | unknown |
| `.sanim` | 2452 | UI animation | unknown |
| `.dds` | 1456 | DirectDraw textures | standard |
| `.xbt`, `.pvrt`, `.gtf` | 1 each | Texture containers (Xbox/PowerVR/PS3) | rare leftovers |
| `.dat` | 130 | Binary data (decals, atlas …) | unknown |
| `.gbin` | 1 | `geo.gbin` GeoIP | unknown |
| `.mel` | 1 | `material_list.mel` | unknown |
| `.lua` | 922 | Plain Lua source (possibly some bytecode — to check) | readable |
| `.flog` | 1 | `sstring.flog` | unknown |

## 4. Interesting leads

1. **Server-side Lua is plain text.** Most gameplay rules (defs, quests, loot,
   queues) can be changed without touching binaries.
2. **Protocol:** the client talks to LoadBalancer (3801) then Shard (3802).
   `client_lua_rpc_allowlist.lua` in `gamedata/def` documents which Lua RPCs
   the client may call — a good map of the client→server surface.
3. **Config-visible features** unused by shipped config: `hub_cloudXmlURL`
   (remote topology), `db_mongoHosts` (replica sets), `RegionWeightProportion`
   (multi-region), `net_useP2PSockets`.
4. **SSH debug console** in each engine process (`ssh_*`).
5. **Community:** modders already know "near all standard Lua 5.1 API
   functions", `outputDebugString` from the in-game `luaServer`, and how to
   modify `.pak` Lua scripts (statement in Discord; no details recorded).

## 4a. Community-reported RE knowledge (secondary source, unverified)

From the Discord preservation channel (Apr–Oct 2026), anonymised. **Treat as unverified leads** — chat statements are not authoritative:

| Topic | Claim | Tools / pointers mentioned |
|-------|-------|----------------------------|
| `.pak` | "tpak v7" container; same family as older Crossout-era paks; uses DEFLATE, "nothing like zip"; documented for ~10 years | quickBMS + `clutch.bms`; GitHub a community `tpak` extractor (GitHub); an "SC pak extractor" on a game-hacking forum |
| Scripts | Top-level scripts are **LuaJIT bytecode** in the client paks; the server-side Lua in this depot is plain text | – |
| Transport | **RakNet** is used for client↔server; `sv_start` / `connect` console paths use *unencrypted* RakNet; the `SCMD_CONNECT_DEDICATED_SERVER` message triggers an *encrypted* connection (not compatible with `sv_start`) | Wireshark is noisy; capture only SC traffic |
| Message types | Packet type names are stored in an array in the executable; the first id is `AC_LOAD_INITIAL_PLAYER_DATA`; callbacks hand packets to Lua | – |
| Auth / tokens | "most things aren't encrypted; the encrypted parts are figured out" (statement, no details) | – |
| Lua API | Near-complete Lua 5.1 API known; `outputDebugString` available through the in-game `luaServer`; `.pak` Lua can be modified | – |

*(analyst note)* A single TCP-heavy observation in the same channel matches
the Hub's TCP-looking `NetEndpoint` logging; RakNet is UDP-based, so both
may coexist (RakNet for battles, TCP for cloud services) — **to be verified**
by capture.

## 4b. Further community RE leads (Russian channel, batch 003, S15; ⚠ unverified)

Pre-release work (May–Sep 2026) by individuals who captured traffic of the
official service; much of it is superseded by the server files published on
2026-10-09, but some statements are useful hypotheses for protocol work (Q14):

| Topic | Claim (paraphrased) | How we can verify |
|-------|---------------------|-------------------|
| Channels | Client↔master server (login, hangar, shop) runs over **TCP** (the LoadBalancer/Shard ports); **RakNet/UDP is used only inside battles** | Observed ports (V-5): TCP 3801/3802/3815 and UDP 35000 — consistent |
| Serialisation | Booleans are sent as single bits without byte padding (byte-wise readers break) | Needs capture/decode (WP-1) |
| Crypto | Only the **password** is AES-protected on the master channel; no XOR layer; hash/version verification is done by the server | Q24; compare with the `Authenticator` log. Batch 004 adds a contrary/complementary claim: the client sends a locally stored password *hash* (clear salt) as the credential (security.md S-19, SV-10) |
| RakNet security | The battle channel has a RakNet *security layer* (`InitializeSecurity`, `PublicKey`, `AllowIncomingConnections`); local battle instances run with it disabled; a real remote instance needs keys handed over by the master side | DedicatedServer imports; Docker project's patches ([docker.md](../04-installation/docker.md) §3.2) |
| Local instance | The battle process a client starts locally is the same program the node starts; capture on loopback UDP 35000 | V-5 observed `DedicatedServer.exe` on UDP 35000 |
| Client patching | A distributable client patcher (SHA-256-verified, separate copy of `game.exe`) is needed only for *non-stock* servers; groups: `security` (client) vs. `maxconn/vesselhash/launchconfig/dock_actor` (server side) | n/a for the stock node |
| Open world | One zone instance per location; instances spin up when a player enters; warp-gate repair needs several instances | `ZoneCoordinator`/`ZoneInstance` logs |
| Lua | Large parts of server logic are in plain Lua in the depot; client Lua in paks is LuaJIT bytecode; the client exposes coordinates/view matrix to Lua (cheat risk) | luajit-bytecode.md, lua-api-surface.md |
| Integrity | Pak file hashes are stored in the executable; "removing the integrity check is a 4-byte edit" (client) | Not needed for server work; legal caution in [legal-and-licensing.md](../09-community-edition/legal-and-licensing.md) |

Third-party reimplementations mentioned (⚠ not reviewed, **not** copied into
this repository): a Go master-server that reaches the hangar and a capture
proxy, both published by community members on GitHub.

## 5. Proposed methodology (status 2026-10-11: steps 1 and 3 largely done)

1. Passive: strings, imports, PE metadata for every executable; catalogue
   console commands/cvars per service (`tools/` scripts).
2. Dynamic: run the node with verbose logging (`cl_netLogEnabled`,
   `cl_dumpTypeDb`, `net_dumpCloudMsg`, `db_logMessages 2`) and capture
   loopback traffic (Wireshark/`rawcap`) while logging in, queuing, buying.
3. Data: dump all Mongo collections after scripted actions (diffing) to derive
   the schema; compare `prepare_shared` input/output.
4. `.pak` format: sample headers, compare against file table in `files.list`.
5. Only then consider decompilation (Ghidra) of Shard/MatchMaker for protocol
   structure; keep notes of *behaviour*, not code.

## 6. Handy cvars for tracing (from strings; semantics to verify)

`cl_netLogEnabled`, `cl_netLogCompress`, `cl_netLogSendPeriod`,
`cl_logServerAddress`, `cl_dumpTypeDb`, `net_dumpCloudMsg`,
`db_logMessages` (1 brief, 2 full — per config comment), `db_logTimesMoreThan`,
`hub_logToAuthenticatorMessages`, `cl_combatLog` (0–4).

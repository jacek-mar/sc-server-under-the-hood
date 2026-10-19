# Verification log (hands-on runs)

> Evidence level: **observed**. Each entry states date, method, result. This
> is the project's own testing record; unverified claims elsewhere should be
> promoted here when tested. Build: `Hub 1.99.0.167293 (Oct 9 2026)`.
> Host: Windows 10 Pro 22H2, x64, desktop CPU, no GPU needed for the server.

## V-1 — cold start of a full node from the depot copy (2026-10-10)

**Method.** From the private depot copy: start `cloud\mongodb\mongod.exe`
(config `./config.cfg`, `--dbpath %LOCALAPPDATA%\Targem\StarConflict\cloud\mongodb\data`),
then `cloud\Hub.exe` (working directory `cloud\`), both hidden windows,
no client.

| Result | Value |
|--------|-------|
| MongoDB ready | ~1 s (`waiting for connections on port 27017`), v2.6.12, journal recovery not needed |
| Hub alive after | 90 s, stayed up |
| Processes | **19** (Hub + 17 services + mongod) |
| Memory (working set) | Hub 37 MB; Shard 114 MB; Achievement/Adventure/Clan/GRD/Lobby ≈ 111 MB; Quest 118 MB; others ≈ 31 MB; mongod 122 MB → **≈ 1.2 GB total** |
| Log noise this session | no ERROR except 11× `Unknown message 5 from '0'` and 1× `Unknown message 16` in the Shard log (handshake-time, benign) |
| Warnings | `No 'RegionWeightProportion' table!`, `RedisLogger: incorrect service id`, `GetLastSystemFrameTime() is too large` on frame 1–2 (start-up stall) |
| DB rename | Shard logs *Detected local build* and rewrites `db_name`, `db_stats_name` **and `db_dedicatedDbCollectionSuffix`** (→ `_<WindowsUser>`) |

### Listening sockets (TCP, all `0.0.0.0` except Mongo)

| Port | Process | Notes |
|-----:|---------|-------|
| 3850 | Hub | service bus (services connect here) |
| 9001 | Hub | **HTTP JSONP/JSON status endpoint** (see §V-3) |
| 3801 | LoadBalancer | client entry |
| 3802 | Shard | client "masterServer" connection |
| 3815 | ChatServer | chat (binary protocol; sends data right after connect) |
| 27017 | mongod | `127.0.0.1` only |

No UDP listeners while idle. DedicatedServer / ZoneInstance sockets only
appear when a battle/zone starts (Q1 still open). **Everything except Mongo is
bound on all interfaces** — consistent with the official warning; use a
firewall.

## V-2 — shutdown behaviour

* Hub started hidden has no console; `Stop-Process` on Hub made the services
  exit by themselves within 10 s (they quit when the Hub link drops); one
  (`LobbyServer`) lingered and had to be stopped. After a forced Hub kill,
  check for leftover service processes before the next start.
* A graceful stop needs the Hub console (`/enterMaintenanceMode`, `/quit`) —
  run the Hub with a visible window (`start "" /D cloud Hub.exe`) for that.
* MongoDB was stopped with a normal terminate; its journal protects the data.

## V-3 — Hub status endpoint (port 9001)

```
GET /status?key=<built-in key>     ->  200 text/json
GET anything else / wrong key       ->  403
```

The **key is a constant compiled into `Hub.exe`** (visible in its strings), so
every stock node uses the same one — treat the endpoint as unauthenticated.
It returns JSON (no cache headers):

```json
{ "ver": "1.99.0.167293 (Oct  9 2026)", "cpu": 0.7, "noDS": 0, "gs": 0, "zi": 0,
  "maintenance": 0, "hub_state": 0, "hub_updating_stage": 0,
  "svcs": [ { "type": "ST_SHARD", "sysload": 0.0, "listens": 3802, "ssh": 2222, "tql": 1, "mode": 3 }, … ] }
```

| Field | Meaning (inferred) |
|-------|--------------------|
| `gs` | running game servers (battles) |
| `zi` | running zone instances |
| `noDS` | missing/needed dedicated servers (0 = ok) |
| `maintenance`, `hub_state`, `hub_updating_stage` | mirrors of the cvars `cloud_maintenanceMode`, `hub_state`, `hub_updating_stage` |
| `svcs[].type` | service type name (`ST_*`) |
| `svcs[].listens` | TCP port the service listens on (0 = none) |
| `svcs[].ssh` | SSH debug port (2222; SSH server itself disabled without password) |
| `svcs[].tql` | task-queue length (Shard only) |
| `svcs[].mode` | service mode code (0–3; semantics unknown) |

Use it for health checks (`gs`, `zi` and service list); keep it off the
internet.

## V-4 — MongoDB launched through `cmd /c launch.bat` with a hidden window

First attempt: `cmd /c launch.bat` (hidden) produced no listening mongod — the
process disappeared with the console. Starting `mongod.exe` directly with the
same arguments worked. For unattended starts use `mongod.exe -f ./config.cfg
--dbpath <dir>` directly (or a service wrapper), not the batch file under a
hidden window.

## V-5 — real client session via Steam (2026-10-10/11)

**Setup.** Steam client launch (`-launchLocalServer`, `win64/local_server.xml`),
login to `localhost` as an existing local user, hangar, queue a Training/Coop
battle, leave. Monitoring: periodic process/port snapshots, the Hub status
endpoint, service and client logs.

| Observation | Value |
|-------------|-------|
| Client ? servers started | client log: `LocalServerAndDb: started MongoDB process …, Redis process 0 and Hub process …` ~37 s after client start |
| Full node ready (17 services) | **7–8 min** on a 2-core i3-4330 *while the client and other apps were loading*; 17 services in < 90 s when nothing else ran (V-1) |
| Login | immediate once ready: LB ? `SCMD_AUTH_*` ? store sync, ~0.7 s |
| Battle | MatchMaker ? Hub spawn ? `DedicatedServer.exe` up in ~6 s; level loaded, client joined ~13 s after queue; **UDP 35000** |
| Hub status during battle | `gs: 1`; back to `0` when DS removed |
| Cleanup after battle | `Coordinator::DeleteDediServer`, DS process exits ~1.5 min after the player left |

### Failure modes seen (important for operators)

| Symptom | Cause | Remedy |
|---------|-------|--------|
| Only 4 of 17 services stayed alive; others "started" then vanished | Machine at 100 % CPU (client loading + other apps). Hub main loop stalled **65 s** (`frame 2 … too large`) and services timed out registering | Start the server first, wait until all services are up (`/status` ? `svcs: 17`), then start the client; keep CPU free. Prefer = 4 fast cores |
| Hub log `Caught application terminal signal 21`, then `Failed to TerminateProcess(...) error 5` for every service | A console window of the Hub/services was closed (signal 21 = Ctrl-Break/close) — services are in a different security context and could not be killed by the Hub | Never close the service console windows; use the Hub console `/quit` or close the Hub window once |
| Client "No more loadbalancers available" (error 10061) | Server not (fully) up yet | Wait for ports 3801/3802 |
| Server, Mongo and services keep running after the **client exits** (even when the client started them) | Observed (user reports "old issue"): the client does not shut the local server down when started this way | Stop them yourself (see below) |

### Clean shutdown (verified)

1. `Hub.CloseMainWindow()` (WM_CLOSE to the Hub console window) ? **Hub and all
   17 services exited in 8 s**.
2. MongoDB: `mongo.exe 127.0.0.1/admin --eval "db.shutdownServer()"` ?
   mongod exits cleanly (client gets "server should be down").
No leftovers (earlier `Stop-Process` on Hub left one service).

## Not yet verified

* ~~Multi-player / remote client over LAN~~ - done, V-9. WAN still open.
* ~~Second concurrent battle (port allocation)~~ - done, V-9 (L-7). PvP
  arena queue: locked below account rank 3, not reached in V-9.
* ~~Account creation for a new name~~ - done, V-9 (auto-created on first
  login). Redis leaderboards; Linux/Proton still open.

## V-6 — attempt to read engine cvar defaults from a service console (2026-10-11)

* A service executable started by hand (`MatchMaker.exe`, no arguments) uses
  defaults `-cloudAddr 1800000000000000 -hub 127.0.0.1:3850`, loads its cfg
  chain, connects to the Hub and to MongoDB (`Persistence … initialized`), then
  **exits ~8 s later**: the Hub's coordinator logs *"destroying <id>…"* for any
  service that is not listed in `cloud.xml` (`ServiceDesc cant be found,
  creating a new one` → destroyed on the next tick). With no Hub reachable it
  exits at once (`Hub has (been) disconnected, shutting down`).
* The in-process console (`StdConImp input reading thread`) is not usable
  through redirected pipes (no console output captured).
* Conclusion: reading `mm_squad*MMVPenalty`, `mm_skilled*` etc. needs either
  the SSH debug console (`ssh_passwd` set; per-service `ssh_port`) or a
  Hub-launched service with a visible console window. Not done yet (V-8).

## V-7 — built-in SSH console works; engine cvar defaults read (2026-10-11)

**Result:** every service has an SSH debug console that can be enabled from
config; through it all effective cvar values were dumped for 17 services
(**Q6 solved**). Reproducible recipe (test copy of `cloud\`, loopback only):

1. Create a host key pair: `ssh-keygen -t rsa -b 2048 -m PEM -f ssh_host_rsa`
   (private key **must be PEM RSA**; public key in OpenSSH `.pub` format) in the
   service's executable directory.
2. In `cloud/data/<service>_local.cfg` (or `<service>.cfg` for services
   without a `_local` hook: `config_server`, `universe`, `lbrd_server`,
   `clan_server`, `tournament`, `scripts_server`, `adventure_server`) put:
   ```
   set ssh_passwd "<secret>"
   set ssh_port 23NN            # unique per service
   set ssh_privateKeyFile "ssh_host_rsa"
   set ssh_publicKeyFile "ssh_host_rsa.pub"
   ```
   Without the key files the log says `SSH server is disabled: RSA host key
   file paths are empty`; with an empty password `… ssh_passwd is empty`.
3. Connect with a client that still speaks the legacy algorithms: the server
   offers **only** `diffie-hellman-group1-sha1`, host key `ssh-rsa`, cipher
   `aes128-cbc`, MAC `hmac-sha1`, and **no `exec` channel** (shell only).
   Windows OpenSSH 9.5 works with
   `-oKexAlgorithms=+diffie-hellman-group1-sha1 -oHostKeyAlgorithms=+ssh-rsa
   -oCiphers=+aes128-cbc -oMACs=+hmac-sha1 -tt`; user name is ignored
   (`admin` used); `paramiko` ≥ 3 refuses the key exchange.
4. The prompt is a **Lua** prompt (`Script error: [string "console_string"]` for
   anything else). Useful forms:
   * `= cvars.mm_botsCount` — evaluate and print the value (shown as
     `CONSOLE | value` in the service log);
   * `sys.log('text')` — write to the service log;
   * `/cvarList <substring>` — console command: list cvars with effective
     values (`name ^5= "value"`); `/cmdList` lists commands (same `/` syntax as
     the Hub console).
   Output of a command appears in the **service log file**, not in the SSH
   session.

**Findings:**

| Cvar | Effective value (engine default unless set by shipped Lua) |
|------|------------------------------------------------------------|
| `mm_squad2MMVPenalty`, `mm_squad3MMVPenalty`, `mm_squad4MMVPenalty` | `0` (no squad MMV penalty) |
| `mm_skilledPlayer`, `mm_skilledSquad` | `35` |
| `mm_losStreakMMVDecrease` | `""` (no loss-streak decrease) |
| `mm_enableCoopVsAi`, `mm_enableLeague` | `1`, `1` |
| `mm_arcadeMaxSquadSize` | `2` |
| `mm_universeArenaMaxSquadSize` / `…WingMinSquadSize` | `8` / `3` |
| `mm_useLowestRankIfLessBattles` | `0` |
| `emm_enableEMM`, `emm_minAccountRank` | `0`, `7` (EarlyMatchMaker disabled) |
| `crash_dumpType` | `65` |

The complete list (436 cvars, effective values) is
[engine-cvars.md](../05-configuration/engine-cvars.md). DedicatedServer /
ZoneInstance cvars (`sv_*`, `ai_*`, `ship_*`) are not in it — those processes
were not running during the dump.

## V-8 — Windows Firewall prompts (maintainer report, 2026-10-11)

When executables are started from a **new path** (a different copy of the
depot, the Steam folder vs. `sc-server-files`, `work\probe`), Windows
Defender Firewall asks to allow each one that opens a listening socket (Hub,
Shard, LoadBalancer, ChatServer, mongod, DedicatedServer, game.exe …). Until
the prompts are answered the program's start-up may stall. We observed
the firewall "waiting and blocking access to the last started apps". This very
likely contributed to the earlier failures where the Hub stalled for ~60 s and
services timed out (V-5). **Operators:** start once and answer all prompts
(Private network is enough for a local server; Public only if you host
publicly), or pre-create firewall rules for the depot's `cloud\*.exe` and
`mongod.exe`. After the prompts were answered, all 17 services (with SSH
consoles) came up in 20 s.

## V-9 — LAN test: node on one PC, clients on two PCs (2026-10-12)

Setup *(observed)*: host = Windows 10 Pro, 2 cores / 4 threads, wired;
second PC = Windows 10 Pro, 4 cores, wired; same /24 LAN; both on Steam build
id `25826043` (1.99.0.167293, hash prefixes identical). The node ran from a
**copy** of the Steam folder (separate Mongo data
directory); both game clients ran from their **Steam** copies with the
client's built-in local node disabled in `win64\local_server.xml`. Host
firewall: program rules for the node's `cloud\*.exe`, limited to the two lab
machines, plus block rules for 27017/9001/SSH from the client PC and an
outbound block for `CrashReporter.exe` (S-25).
Addresses below are placeholders: `<HOST_IP>` (LAN), `<CLIENT_IP>`,
`<VBOX_IP>` / `<HYPERV_IP>` (virtual adapters on the host, left enabled).

| Test | Result |
|---|---|
| L-0 baseline (`cloud.xml` = 127.0.0.1, client on the host, entry `localhost`) | Node READY 26 s after Hub start, 17 services, no firewall prompt (rules pre-created). Login 0.5 s (LB 3801 -> shard 3802 + chat 3815). **"Training" = local practice game** (`Starting practice game. gameMode 6, levelName 'tutorial_leviathan'`), no DedicatedServer. Matchmaker battle: queue 10.6 s, DS on `127.0.0.1|35000`, level loaded 9.6 s after the match |
| L-1 `cloud.xml` Node address = `<HOST_IP>:3850`, client on the host (`localhost`) | READY 28 s, no "no my node" loop. Client still reaches the LB on 127.0.0.1:3801 but is sent to the **shard at `<HOST_IP>:3802`** (address from `cloud.xml`). DS: `Dedicated server launched on address <HOST_IP>|35000` - **not** a virtual adapter. Battle to the end, no crash, no `dediserver_exceptions` -> **the stock Windows build accepts a genuine LAN address (Q30)** |
| L-2/L-3 remote login (second PC, entry `server`, address `<HOST_IP>`) | The port box is pre-filled with **3801**; plain address works. LB -> shard `Authorized uid … from <CLIENT_IP>` in ~0.25 s; chat authenticated, channels joined. **A new name creates an account on first login** (uid 2, account rank 1). Store and chat work |
| L-4 remote battle | Queue 10.3 s; client connects to `<HOST_IP>|35000` over UDP (MTU 1492); the per-program rule is enough for UDP |
| L-5 squad (both PCs) | Squad invite works; squad matched together (`Creating game for uids: 1, 2`), same team (`sqid 1`) vs 2 bots, `gameMode 11` run as a COOP game. Matchmaker decision log shows the map choice: the most-played map/mode of the group is filtered out. `botPresetName` empty -> DS applies `AiPreset.Default`; MatchMaker reports **LOW online mode**. PvP arena is locked for account rank < 3 (client UI) |
| L-6 minimal firewall (port rules instead of program rules) | Works with TCP 3801, 3802, 3815, 3850 + UDP 35000-35099. Without **3850**: login, chat, battles fine -> **the Hub port is node-internal**. Without **3815**: login and battles fine, **chat fails silently** (client: `PEC_PINGPONG_TIMEOUT on <HOST_IP>:3815`, reconnect every 25 s, no on-screen error; chat server receives nothing). 27017 and 9001 time out from the client PC in all rounds |
| L-7 concurrent battles | Two solo players queuing at the same moment are **merged into one game**; queuing after the first battle has started gives a second DS: ports **35000 and 35001** (sequential). A running COOP game accepts no joiners (`Skilled player can join: no`). Two DS + client on the 2-core host: Hub CPU ≤ 0.59 |
| L-8 wrong address in `cloud.xml` (not a local interface) | `Hub::ApplyConfigurationXml: there is no my node in xml` -> `Failed to m_hub.Init()` -> Hub waits 10 s for children and **exits** (no restart loop, no services; MongoDB stays up) |
| L-9 credential observations (values never printed) | `accounts.password` = **64 lowercase hex characters** for every account; two accounts with the same password have **identical** values; no salt field -> **no per-user salt**. The client has **no password-change function**. "Remember password" keeps **one** login (user + password); it is not in `user_config.xml`, the registry or Windows Credential Manager - candidate: the fixed-size binary profile `profiles\0001.prfl` (rewritten on every exit) |
| L-10 capture (partial; passive raw-socket tool on the host, 15 min) | UDP 35000: **RakNet** (offline-message magic `00ffff00fefefefefdfdfdfd12345678`; client `0x05` open-connection request, server `0x06` reply). TCP 3801/3802/3815: **no TLS** record header, low-entropy length-prefixed framing (S-21 consistent). Limitation: only host->client TCP was visible to the raw socket; client->host TCP needs a capture on the client side |

Other observations *(observed)*:

* Log layout: service logs flat in `%LOCALAPPDATA%\Targem\StarConflict\cloud\Hub\logs\<serviceId>_<service>_<yyyy_mm_dd>.log`; battle servers in `…\logs\<yyyy_mm_dd>\dediserver<N>.log`. Clients buffer `game.log` until exit.
* Privacy: the DS logs the client's **full process list** (S-09 confirmed); the chat server logs **message text** and the start of the client's chat **session token**; all accounts from one PC report the same `clientId` (`win_<guid>`, per installation).
* The ChatServer names its own address in the handshake log as the **Hyper-V switch** address (`<HYPERV_IP>:3815`) although the client is on the LAN - harmless here, but it derives "own address" from the adapter list.
* Start-up noise on the shard (`Unknown message 5/16`) right after start; the tutorial mission logs repeated Lua errors (`gen_phases.lua:1264 … nWoWMsgTimer (a nil value)`) without visible effect.
* Load: node + one client + VS Code on the 2-core host stayed responsive; no service died.
* Firewall: no "allow access" prompt appeared in any round. Note for repeats *(inferred, standard Windows behaviour, not exercised here)*: answering such a prompt with **Cancel** creates a *block* rule for that program, which overrides port allow rules - do not press it during port-rule tests.

### V-9 addendum - PW-1: password-storage claim checked (2026-10-12)

A community source (b007 J1) described `accounts.password` as a single SHA-256
pass over a fixed, account-independent prefix plus the password. Checked
**value-free**: the password of a test account was typed into a script
(hidden input), the script computed the claimed value in memory and
MongoDB compared it with the stored one; only MATCH / NO MATCH was printed.
The prefix constant is deliberately not reproduced in this repository.

| Account | As typed | Lower-cased |
|---|---|---|
| test account 1 | MATCH | no match |
| test account 3 (checked twice) | MATCH | no match |

Result *(observed)*: `accounts.password` = lowercase hex of **SHA-256(fixed
global prefix + password as typed)** - one pass, no per-user salt, no case
folding (test account 4 shares account 3's password and stored value).
Whether the client trims leading/trailing spaces before sending is not yet
tested. Consequences: [security S-07](../07-administration/security.md).

## V-10 - LAN 2026-10-11: two-sided capture, live consoles, admin tasks, client data (2026-10-12)

Same setup as V-9 (node copy on the host `<HOST_IP>`, second PC `<CLIENT_IP>`
with a set of helper scripts, throw-away test accounts A-D = uid 1-4). Only
the second PC's client was used; all values from the test database stayed
private; checks on credentials were value-free (only the test accounts'
authentication data was analysed).

| Test | Result *(observed)* |
|---|---|
| L-10b two-sided capture (own passive tool on both PCs, 10 min each) | Each raw-socket capture sees only the TCP its **own** host sends (plus UDP both ways) - combining both captures gives the full picture. **No TLS on any port.** Client -> LB 3801: TCP connection with **no client payload**; the LB sends ~460 bytes unprompted. First client -> Shard frame (~710 bytes, big-endian u32 length prefix): client version string and nickname **in clear**, ~384 bytes with random-like entropy (7.46 bits/byte; three 128-byte parts, consistent with RSA-1024-sized blocks *(inferred)*), the per-installation `clientId` (`win_<guid>`), a 64-character lowercase hex value (not any stored account hash, not in any node log; meaning unknown), then plain structured fields. The stored `accounts.password` value of the account **does not occur** in either capture (hex, raw, reversed, partial) -> the database value is not sent as a plain credential (S-19 not observed in clear) |
| CON live console dumps (battle running) | Battle-server `/cvarList` complete (**971 cvars**), battle-server `/cmdList` 228 names, Shard and Hub `/cmdList`, MatchMaker `/cvarList mm_` (51 cvars, live values). The battle server's console output arrives in the **SSH session**, not in the service log. Shard/Hub consoles sometimes drop a new connection ~0.2 s after accept - retry works. On connect the console replays recent log lines ("Some previous output") |
| AT-1 admin task queue | A task document without `pickedBy` is **never picked up** (no error). With `ctm_debugTaskPickup 1` the Shard prints its selector: **`{ serviceType: 2, pickedBy: 0 }`** - a task needs `pickedBy: 0`. Then: `playerInfo` picked within seconds, Shard writes `pickedBy` (its service id), `pickedAt`, `finishedAt` (ms epoch), `success`, `errMsg`, `result` (`admRole`, `username`, `nickName`, `uid`, `bannedTill`). `mute` (1 h, category 1) -> `chatMutedTill` = now + 1 h, `muteCategory` stored as **5**; effective **immediately** (client chat notice "muted for 60 min", red warning with remaining time on each attempt; chat server still logs the blocked message text). Requester with `admRole player` -> `Not enough privilege`. `cancelMute` without `reason` -> `Specify the reason please`; with reason -> `chatMutedTill` 0, chat works at once |
| AT-3 password reset by copying `accounts.password` | Copying another account's stored value works as a reset at once (log-in with the other password succeeds, the old one gets `Accounts: invalid password for user ...`); restoring the value restores the old password. Client disconnect reason **36** follows a rejected login (41 = normal logout) |
| AT-4 `give` task | `{cmd: "give", uid, reason, value: "credits" or "goldCredits", amount}` **adds** the amount (8/8 success); the client shows the new balance at the next login |
| L-9b "remember password" | The remembered nickname and password are not in `user_config.xml` (only `cl_savePassword`, which stays **0** while "remember" is active), the registry, Credential Manager or the logs. `profiles\0001.prfl` (fixed 301 525 bytes): magic `RHPP`, version 7, a profile-name field and **~500 bytes of encrypted-looking data**, the rest padding; only this header changes per exit; the nickname is not readable in it. A value-free scan of the whole client profile found the account's stored server hash in **no** form -> the remembered login is kept encrypted/obfuscated in the profile header *(inferred)*; plain password vs hash inside it and portability to another PC not tested |
| L-11 / L-11b ship stat edited on the server only (`def/ex/ship.lua`) | Starter ship hull 5190 -> 51 900 and later -> 10. Hangar always shows the client's value (5943 = 5190 + 14.5 % module bonus). With hull 10 the in-battle HUD showed **11** and the ship died to one shot after the shield was down -> **the battle server is authoritative for ship stats and uses the server's Lua; the hangar shows the client's local copy** (visible mismatch, no error). Module hull bonus is multiplicative |
| L-13 loot-rule fix (Q45) | Stock rules make the DS pick the **undefined** table `CommonRanks_1_3` silently (no error line). After renaming the six `CommonRanks_<band>` references to the existing `_v3` tables the DS picks `CommonRanks_1_3_v3`; post-battle loot = credits in every container |
| L-14 `address.cfg` (Q46) | `set net_masterServerAddress "<HOST_IP>"` in `address.cfg` in the game root or in `win64\`: no effect on the login screen (address field empty, port 3801 pre-filled), nothing in the client log |
| L-12a/b store-id tests | Postponed (needs a store item visible to new accounts and a `prepare_shared` run) |

Other observations *(observed)*: a test id `CON` cannot be used for folders
(reserved Windows device name); the general store works for new accounts,
the player-to-player marketplace is locked by progression (on the official
service also by a number of battles per ship, as players remember it). All edited node files
were restored byte-identical; the test accounts keep the AT-4 credits/gold.

## V-11 - server-only tests: prepare_shared, settings reload, admin tasks (2026-10-13)

Server-side tests on the host's node copy (V-9 state), no game client.
Test accounts as in V-10 (uid 1-4); requester uid 1 had `admRole
root` only during the admin-task block. Every edited node
file was backed up and restored (hash-checked); afterwards
`tools/data_drift_check.py` reported the node copy identical to its V-9
state.

| Test | Result *(observed)* |
|---|---|
| S11-R0 start-up | Hub start -> READY in 28 s (MongoDB already up); Hub-only restarts 27-32 s; clean Hub close 10 s |
| S11-R1 `prepare_shared` (`DedicatedServer.exe -logFileName prepare_shared.log -nullCon -prepareSharedData -ds datasources_defs_build.txt`, Hub stopped, MongoDB running) | 9 s, exit 0. Rewrote **29** `cloud/data` XML files - every one **byte-identical** to the shipped file (only timestamps changed): `account_auras`, `achievements`, `atlas_special_values`, `autogen`, `autogen_special_values`, `aux_limits`, `battle_pass`, `bot_preset_exclusion_lists`, `clan_emblems`, `clan_quests`, `clan_ship`, `faction_rep`, `karma`, `league_equipment_lists`, `medals`, `offers`, `quests`, `ship_quests`, `skills`, `starter_pack`, `store`, `titles`, `tournaments`, `universe`, `vessel_custom_elements`, `vessel_custom_elements_rules`, `vessel_presets`, `war`, `zones`. **Not** written: `special_values.xml`, `regions.xml` and all hand-maintained files (`loot_tables`, `store_rules`, `slot_machines`, `stickers`, `defmod_rules*`, cfg files). Database use: reads and writes the **atlas id table** (`atlas_<db>.ids`: one document, 1 205 module -> atlas id entries, ids 1-1205, `counter` 1206 = the 1 205 `atlasId` attributes in `store.xml`) and the autogen id table. Log line `Entity Defs hash 71367FCA` = the stock build's entity-defs hash (reference for lab GD-1). Side effect: the run also opens the battle-server SSH console if `dediserver_local.cfg` enables it |
| S11-R2 settings reload | Console Lua assignment (`cvars.x = v`) changes a cvar **immediately** in that process; `ctm_debugTaskPickup 0 -> 1` changed behaviour at once. `*_local.cfg` + restart: wins for cvars the platform Lua does not assign (`sm_overloadCounterLimit`, `ctm_debugTaskPickup`), **loses** for cvars it assigns (`store_maxUniqueModules`, `sv_tokenCreditsDailyLimit`, `mm_botsCount`, `mm_lowOnlineLo`). Console output of the cloud services goes to the service log; `/cvarList` prints values, Lua `print()` printed nothing. Details: [settings-reload-map.md](../05-configuration/settings-reload-map.md) |
| S11-R3 admin tasks (DB-verified) | `unlockAllVesselNodes {uid, vid}` -> that vessel gets `unlockedMask: NumberLong(-1)` (all nodes), level/exp unchanged. `give {uid, vid, value: "level", amount: 3}` -> vessel level 1 -> 4 (**additive**), audit log `ACCOUNT_EXP_GOT {type: VESSEL, levelOld, levelNew, expAdd}`. `give {value: "exp"}` -> `Incorrect value name` (vessel values accepted: `level`, `munition` + `index`, `hullCondition`; there is no per-ship exp). `give {value: "vesselExpPool", amount: 5000}` -> account free synergy +5000. `assignRole {uid, role}` -> `accounts.admRole`. `ban {uid, category: 1, durationInHours: 1, rules, reason}` -> `bannedTill` = now + 1 h (ms), `banCategory` 1 (stays after `cancelBan`); `cancelBan {uid, reason}` -> `bannedTill` 0. Ban and role changes leave **no** entry in the `logs` audit collection. `changeNickName {uid, nickname}` -> `accounts.nickName` and `stats_<db>.accountsStats.nickName`, audit `NICK_CHG {oldNickName, nickName}`; the task **refused the original auto-created test name** (`Invalid nickname`) - nickname validation is stricter than account auto-creation (name restored directly in the DB) |
| Q48 value-free check | The audit collection `logs_<db>.logs` stores every connection as `CON {premium, method, ip, fp}`; `fp` is a 64-hex value. Two distinct `fp` values exist: one used only by the account played on the host PC, one shared by all four accounts played from the second PC -> **per machine, not per account**. The second PC's `fp` occurs verbatim in that PC's V-10 client-side captures (MATCH, value not printed) -> the unidentified 64-hex login value of V-10 is this machine fingerprint, stored server-side with the client IP |

Gotchas: a helper script named `con.py` hangs Python (Windows device name
`CON` - same trap as the V-10 test id); Shard/MatchMaker consoles drop
2-3 of 4 new connections before authentication - retry.

## V-12 - allied bots in Special Operations (PvE raids) (2026-10-13)

Question: can a stock node add **allied** bots to a Special Operations
battle? "Special Operations" (game wiki S14, page `SPECIAL_OPERATIONS`:
10-12-ship operations Alien Destroyer, Defiler, Return to Eden) are the
**PvE raids** of the server config, not the 4-player PvE missions. Node copy
of V-9, one client on the host PC, one test account (uid 1). The database
was backed up first (cold copy + `mongodump`); the account was prepared by
direct DB edit with the node stopped (`accountRank` 1 -> 7, credits added);
two ships were bought in the client with `store_allowAllItemsForBying = 1`.
Each variant was applied to the platform Lua from the pristine file, with
`mm_decisionLog = 33`; the node was restarted for every variant. Verdict
from the battle-server log: game-session document and "MM teams
composition" (bots listed in the player's team).

**Gates (static, then observed):**

| Gate | Where | Value |
|---|---|---|
| Client menu lock | `data/ui/scripts/work/uigamedefs.lua`, `UI.rankLocks` (account rank) | raid **7**, PvE missions 4, custom game 5, PvP 3 |
| Raid by ship rank | `cloud/data/aux_limits.xml` `/PVEMissions/Mission raid="1"` | `pve_raid_waterharvest_t3/t4/t5` ship rank 7-9 / 10-12 / 13-17 (Alien Destroyer); `pve_raid` 10-17 (Defiler); `pve_planetoidraid` 13-17 (Return to Eden) - names matched to the wiki by rank band and day *(inferred)* |
| Raid schedule | `aux_limits.xml` `RaidSchedule` (generated from `RaidSchedule` in `data/gamedata/shared/pve_missions/base.lua`, a file the client also has) | `Period start/finish` = **hour of the week** 0-167, hour 0 = Monday 00:00 **GMT** (designer comment above `RaidSchedule` in `base.lua`, our translation: "0 = Monday, minimum period one hour, everything in GMT; works from hour i to j + 1"; observed: a queue at 18:58 GMT on a Tuesday gave the Alien Destroyer); one raid level per **even** hour; Mon/Thu Return to Eden, Tue/Sat Alien Destroyer, Wed/Fri Defiler, Sunday rotates - matches the wiki's "one hour, with one-hour breaks" |
| Ship rank vs account rank | `aux_limits.xml` `LockRank` | ship ranks 1-10 need account rank 1, 11-15 need 5, 16-18 need 10 |
| Solo entry | `mm_raidSquadFilter` (shipped 0 = anyone); the per-queue `squadFilter = 4` (wings only) is commented out | on the live service operations were for groups of 10-12 ships (wiki; `mm_raidMinWingSize` ships as 10); a stock node lets one player start a raid |

**Results** *(observed)*, all `pve_raid_waterharvest_t3`, one player, rank-9 ship:

| Test | Change | Game-session document / DS start line | Allied bots |
|---|---|---|---|
| SO-0 | stock raid queue (`special = { pve_raid = 1, gameMode = 7 }`) | `gameMode 7`, `pve_raid 1`, `maxPlayers 12`, **`botsCount 0`**, `queueSpec 5`; `botCount 0`, `gameDuration 1200` | 0 |
| SO-1 | raid queue `botsCount = 3` | `botsCount 0` - the queue value is **replaced** (the V-9 coop battle got 2 bots from a queue without `botsCount`, so the MatchMaker computes bot counts itself; whether a queue `botsCount` is honoured in any mode is untested) | 0 |
| SO-2 | raid queue `botsCount = 3, botsInTeam1 = 3` | `botsCount 0`, `botsInTeam1 3` (passed through) | 0 |
| SO-4 | DS cvars `sv_numBots 3`, `sv_botsInTeam1 3`, `sv_forceBotTeam 1` in `ConfigureDediServer()` | `botsCount 0`, `botCount 0` (the DS log does not show cvar assignments) | 0 |
| SO-3 | `lobby_reqPlayersPvEMin = 1` | the PvE custom-game list offers **missions only, no raids**; the bot selector (8/12/16/20/24) appears for **PvP** custom games only; a PvE lobby shows capacity 1/4 | - |

Conclusion: on a stock node **no configuration route adds bots to a
Special Operations battle** - the MatchMaker sets the raid game's
`botsCount` to 0 regardless of the queue, and the client offers neither
raids nor bots in PvE custom games. Whether the battle server would spawn
allies in `gameMode 7` with a non-zero count is open (Q50).

Gotchas: setting the host clock **back** while the node runs stalls the
login queue (the LoadBalancer accepts clients, never hands them on; the
client reports heavy load) until the node is restarted; battle-log file
times then run backwards, so pick battle logs by number, not by time.

## V-13 - server-only tests: admin-task queue, roles, layer order, database port (2026-10-16)

Node copy with its own database folder (a copy of a seeded test database: four
test accounts), no game client. Every config edit was backed up and restored
byte-identical; the game folder matched its manifest afterwards. *(observed)*
unless marked otherwise.

| Topic | Result |
|---|---|
| Queue throughput | The Shard picks up **one task per poll, every ~5 s**: five tasks inserted together finished at 1.6, 6.6, 11.6, 16.6 and 21.6 s (about 12 tasks per minute). Plan bulk actions accordingly |
| Duplicate content | Two documents with the same content and different `_id`s are **both executed** (a `give` of 1 credit applied twice). Re-inserting the same `_id` fails on the unique `_id` index, so a client-generated `_id` makes submission idempotent |
| Interrupted task | A document left "picked" (`pickedBy` = the Shard's service id, `pickedAt` set, no `finishedAt`) is **not re-picked or recovered** after a node restart; its effect is not applied. Other tasks are not blocked by it. `pickedBy` is the Shard's service id (`0x1010000000000002`) |
| Unknown fields | Extra top-level fields in a task document are ignored (`playerInfo` succeeded) |
| `ctm_taskDebugDelay` | set to 20000 in `shard_local.cfg`, no visible delay (task finished within 1.5 s); meaning unclear |
| Tasks newly verified | `give` `premiumTill` (amount = hours; +24 h = +86 400 000 ms), `give` `tokenCredits`, **`set`** (`value: "credits"`: sets the exact value), `giveTitle` (`title` = id from `titles.xml`), `giveVesselCustomElement` (`item` = custom element name; stored in `freeVesselCustomElements`), `mutePermanent` / `banPermanent` (store the int64 maximum **2^63 - 1** in `chatMutedTill` / `bannedTill`; `cancelMute` / `cancelBan` reset to 0), `enterMMode` / `leaveMMode`, `createAccount`, `assignRolePrivileges` |
| Maintenance mode via admin task | `enterMMode` with `minutesLeft: 5` → Hub log counts down once per minute (`Entering maintenance mode in N minute(s)`), at zero `Hub state: HS_ONLINE -> HS_MAINTENANCE`, and the Shard logs **`Disconnecting all clients due to maintenance mode`**. Admin tasks keep working in maintenance; `leaveMMode` returns to `HS_ONLINE`. What the client shows is not yet observed |
| `createAccount` | creates the account with a uid from `counters` and an `accountsStats` document (26 fields; the starter kit is added at first login). **`password` is stored verbatim**, not hashed: a value the client can log in with must already be in the stored format ([security S-07](../07-administration/security.md)). `allowLogin: 1` is stored; `0` was not stored |
| Custom roles | Roles in `web_adm.admRoles` (layout as in [admin-tasks-howto §4a](../07-administration/admin-tasks-howto.md)) are read **only at Shard start-up**: neither a role written directly nor one created with `assignRolePrivileges` granted anything until the node was restarted; afterwards a role with `gmView` could run `playerInfo` and was refused `give` (`Not enough privilege`). `assignRolePrivileges` merges the role into the existing document |
| Layer order of cvars (Shard, `ctm_debugTaskPickup`, visible as `Pick up adming task...` every 5 s) | `cloud.xml` `<ServiceCVars>` (value 1) **beats** `shard_local.cfg` (0); the platform Lua (0) **beats** `cloud.xml` (1). Effective order: cfg chain → `cloud.xml` service cvars ("Applying service options") → platform Lua |
| Wrapping `Configure*` functions | A block inserted before the dispatcher at the end of the platform Lua that replaces the global `ConfigureShard` with a wrapper (call the original, then assign cvars) takes effect: the dispatcher calls the globals by name |
| Database on a non-default port | `set db_mongoHosts "127.0.0.1:27118"` in `common_local.cfg` + `mongod --port 27118`: the Shard logs `mongo://127.0.0.1:27118`, all service connections go there, tasks work (answers the port part of Q9; another host is untested) |
| Connections of a running node | `currentOp` with `$all: true` lists **15 client connections** from the services while the node runs and none when only MongoDB runs (a tool's own sockets, including a driver's monitoring connection, must be excluded) |
| Ship document | `vessels[]`: `vid` (int64), `defName`, `equipped` (35 int64 slots: 0 or the `iid` of an `items[]` entry), `munition` (2 × `{def, amount, res}`), `skillRating`, `exp`, `level`, `hullCondition` (double), `conserved`, `customElements` (14 × `{defName, till}`); `unlockedMask` (int64) only after unlocking research nodes |
| Client libraries | PyMongo 3.13 (last line with MongoDB 2.6 support) works against 2.6.12 from Python 3.12 and 3.13 (int64, `findAndModify`, collection and index listing, `currentOp`); the bundled `mongodump` works with `--host/--port` |

## V-14 - server-only tests: where granted items are stored on the account (2026-10-19)

Node copy with its own database folder (a copy of a seeded test database),
no game client. A `root` account granted items to a test account through the
admin-task queue; the account document was read back afterwards.
*(observed)*

| Grant | Result on `accounts` |
|---|---|
| `giveTitle` `title: 3`, then `4` | `acquiredTitles: [{id: 3}, {id: 4}]` (numeric ids from `titles.xml`); `title` (active title id) stays `0` |
| `giveVesselCustomElement` `item: "<element name>"` | `freeVesselCustomElements: {"<element name>": NumberLong(1)}` - an object of name -> count |
| `giveAutogenModule` `classId: 0`, `rank: 10` | one `autogenItems[]` entry `{iid, upgradeLevel: 0, rollData: [19 numbers], exp: 0}`; `iid` taken from the `iid` counter |
| `give` `item: <store id>`, `amount` (no `value`) | the `item` parameter is the **numeric store id** (`<Item id>` in `store.xml`); a `defName` or `value: "item"` gives `Incorrect value name` |
| - a munition | `items[]` entry `{iid, defName, amount, ench, timeEnd}`; a second grant **adds to the same entry** (same `iid`) |
| - craft resources, parts and blueprints (`CraftResource_Base`, `craft`) | `craftResources.<defName>` = amount (no `iid`) |
| - an avatar / a motto (taunt) | `acquiredAvatars` / `acquiredMottos`: objects keyed by `defName` with value `1`; the active `avatar` / `motto` (a `defName` string) is set to the **last granted** one |
| - junk (`Junk_Base`) | refused: `Unsupported item type` |

Still open: delivery of `adminMail` item attachments (needs a client login)
and where junk items are stored.

## V-15 - server-only tests: HTTP store and quest patches (Q72) (2026-10-19)

Node copy with its own database folder (a copy of a seeded test database),
no game client. Two new files `shard_local.cfg` and `quest_server_local.cfg`
pointed the patch cvars at a loopback HTTP server (interval 15 s); both
files were removed afterwards. *(observed)*

| Test | Result |
|---|---|
| Store items patch, one item, arriving during start-up | Shard logs `new patch content arrived` + XML, then dies (Hub `OnDisconnect … reason 5`); the node keeps running without a Shard |
| Same patch arriving after the Shard is ready (file served 404 first) | 404 handled: `ReceiveItemsPatch() failed, err: 404`; once the file is served, the Shard dies 0.15 s after `new patch content arrived` |
| Patch with the complete original `<Item>` line, only `price` changed | same crash |
| Crash dumps (3) | exception **0xC00000FD stack overflow** in `_chkstk`; static: `ApplyItemsPatchReal` needs a 0x130174-byte frame, `Shard.exe` reserves 1 MiB of stack -> **every items patch crashes the stock Shard** |
| Special values patch | fetched, logged, ignored; no crash |
| Quest patch (unchanged copy of `quests.xml`) | polled every 15 s; applied once per start (`Quest groups patched`, `UpdateQuestsNewPatch`), unchanged content ignored; no errors |

Details: [http-store-quest-patch §2a](../05-configuration/http-store-quest-patch.md).


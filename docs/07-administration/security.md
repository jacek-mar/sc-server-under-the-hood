# Security analysis and hardening guide

> Status: **first full version (2026-10-11).** Scope: the released server
> software (`cloud/` node, MongoDB, DedicatedServer) as an operator would run
> it, plus requirements for any future community edition. Replaces the short
> table in [administration.md §5](administration.md#5-security), which stays as
> a summary.
>
> Method: static review of the depot configuration, our own observed runs
> ([verification-log](../04-installation/verification-log.md)), the schema
> ([schema.md](../06-database/schema.md)), the protocol notes
> ([protocol-observed.md](../08-reverse-engineering/protocol-observed.md)) and
> the audit script `tools/security_audit.py`. Evidence tags as elsewhere:
> *(official)*, *(observed)*, *(file)* = read from shipped files, *(community)*,
> *(inferred)*, ⚠ unverified. **No exploit was developed or tested against
> third-party systems**; items marked ⚠ are hypotheses to verify on your own
> lab node.

## 1. Executive summary

The node is engineered for **trusted localhost / friends use**. Almost every
internal trust boundary is "same machine, same user". The vendor notice says so
too *(official)*. Running it on the public internet therefore needs
compensating controls from the operator. The five most important facts:

1. **MongoDB 2.6.12 without authentication** holds *everything* (accounts,
   currencies, bans, admin roles). Anyone who reaches it owns the game. It is
   loopback-only by default *(file, observed)* — keep it that way.
2. **Admin = a string in the DB** (`accounts.admRole`, e.g. `gm`, `support`),
   and `auth_infinitePremiumForRoles = "gm;support"` *(file)*. There is no
   separate admin credential system found so far ⚠.
3. **Hub, LoadBalancer, Shard, ChatServer listen on all interfaces**
   *(observed)* and the Hub status page (9001) uses a key that is identical in
   every build *(observed)*. Internal services trust whoever connects ⚠.
4. **Account auto-creation is on** (`auth_allowInternalAutoCreate = 1`
   *(file)*): any username/password string creates an account.
5. **Bundled third-party code is old**: OpenSSL 1.1.0h (2018), libcurl 7.62.0
   (2018), MongoDB 2.6.12 (2016), LuaJIT 2.1 alpha, RakNet-style UDP transport
   *(file / community)*. They cannot be patched by an operator.

**Bottom line:** run a *private* node (loopback, LAN, or VPN overlay) with the
baseline in §6; for a public server add the §7 profile (network segmentation,
DB isolation, gated registration, monitoring) and accept the residual risk
documented in §8.

## 2. Assets and threat actors

| Asset | Where | Why it matters |
|-------|-------|----------------|
| Player credentials (`accounts.username/password`, `puid`, `steamID`) | MongoDB `accounts` | Reuse of passwords across sites; login impersonation |
| Currencies / inventory / progress | MongoDB `accounts`, `*stats*` | Integrity of the game economy |
| Personal data in logs and DB (`lastIP`, `netStat.ip`, nick, chat) | DB, `Hub/logs`, chat logs | Operator is a data controller (see §7.6) |
| Admin capability | `admRole`, SSH console, Hub host access | Full control of the game |
| The host | Windows machine running the node | Services run as the operator's user; the client can be attacked by a hostile server and vice versa |

| Actor | Capability | Typical goal |
|-------|-----------|--------------|
| Anonymous remote player | Can reach 3801/3815/3850/3802/35000.. with a stock or patched client | Create accounts, flood, cheat, crash services |
| Cheater / modded client | Controls the client binary and its messages | Gain items/currency, bypass checks, lag-switch |
| Malicious operator | Controls the server and the downloaded client data | Attack players' PCs, harvest data |
| Local user on the host / other LAN host | Reaches loopback/LAN ports | DB edit, SSH console |
| Scanner/botnet | Internet-wide | Hits exposed Mongo, SSH, RDP, DoS |

## 3. Attack surface (observed ports)

Ports from [architecture.md](../03-architecture/architecture.md) and the
verification runs; bind address *(observed)* unless noted.

| Port | Service | Bind | Exposure advice |
|------|---------|------|-----------------|
| 3850/tcp | Hub (cloud control, service registration) | 0.0.0.0 | **Internal only.** Clients on a stock node connect through the LB, not the Hub ⚠ — verify before closing, because the client login address points here in the local setup |
| 9001/tcp | Hub HTTP status (`/status?key=…`) | 0.0.0.0 | **Never public** (static key) |
| 3801/tcp | LoadBalancer (client entry) | 0.0.0.0 | Public if serving remote players |
| 3802/tcp | Shard (accounts, game state) | 0.0.0.0 | Reached by clients after LB redirect ⚠; restrict to players' sources if possible |
| 3815/tcp | ChatServer | 0.0.0.0 | Public if serving remote players |
| 35000/udp (+ range ⚠) | DedicatedServer (battle) | 0.0.0.0 | Public; allocation range still open (Q1) |
| 27017/tcp | MongoDB | 127.0.0.1 *(file)* | **Never public** |
| 2222/tcp (per service in `ssh_port`) | SSH console | all; disabled unless `ssh_passwd` set *(file)* | Disabled or private only |
| 6379/tcp | Redis (optional) | ? | Loopback only |

`tools/security_audit.py --listening` prints this table for a running node.

## 4. Findings

Severity is for a node exposed to the internet. IDs are stable for
referencing from issues.

| ID | Sev | Finding | Evidence | Recommendation |
|----|-----|---------|----------|----------------|
| S-01 | High | MongoDB has no authentication and holds credentials, currencies, bans, roles | *(file)* `mongodb/config.cfg` has only `bind_ip`; services connect without credentials *(official, community)* | Loopback only; OS firewall deny; never publish 27017; restrict NTFS ACL on `mongodb/data` |
| S-02 | High | Admin identity is a DB field (`admRole`); `gm;support` get infinite premium | *(file)* `auth_infinitePremiumForRoles`; schema field `admRole` | Treat DB write access = root. Review who can open a Mongo GUI on the host; audit `admRole` values after any import |
| S-03 | High | SSH debug console = full Lua prompt in the service process; algorithms are legacy only (group1-sha1, ssh-rsa, aes128-cbc, hmac-sha1) | *(observed)* V-7 | Leave `ssh_passwd` empty in production. If needed: >=16 random chars, firewall, or bind via an SSH tunnel on a private net **2026-10-13:** the console's Lua state can `require("ffi")` (lua-runtime-surface) -> console access = native code execution in the service process. |
| S-04 | Med | Hub status key identical in every build; endpoint binds all interfaces | *(observed)* | Firewall 9001; if monitoring is needed, scrape from loopback and publish through an authenticated reverse proxy |
| S-05 | Med | Internal services listen on 0.0.0.0 and (for the Hub) register any connecting service by id | *(observed)* ports; registration by `Registering on a hub … as <id>` in logs | Host firewall: allow 3801/3815/(35000 range) to the world; allow 3850/3802 only from required sources; keep everything else loopback. **LAN V-9 (observed):** clients need TCP 3801 + 3802 (+3815 for chat) and UDP 35000+; **3850 is node-internal** |
| S-06 | Med | Account auto-creation enabled | *(file)* `auth_allowInternalAutoCreate = 1`; *(observed V-9)* a new name typed on the `server` login screen creates the account on first login | Public: set 0 and create accounts through a controlled script/DB tool; or accept and rate-limit at the network edge |
| S-07 | Med | `password` stored in `accounts.password` (string): **64 lowercase hex characters, no per-user salt** - two accounts with the same password store identical values *(observed V-9, values not printed)*; **scheme confirmed by a value-free check (2026-10-12):** one SHA-256 pass over a fixed global prefix + the password as typed (community lead b007 J1; prefix not reproduced here) - a leaked DB is open to fast dictionary attacks, identical passwords are visible, and anyone who knows the prefix can compute the stored value of any password (admin reset, but also offline cracking). **Design note for future servers:** do not keep this scheme for new passwords; accept the legacy value only to migrate (re-hash with a slow salted function on the next successful login) | *(file)* schema; *(observed)* format/equality; algorithm ⚠ | Verify with a throw-away account (compare field length/format). If it is a fast unsalted hash, treat DB dumps as credential leaks and warn users about password reuse **b008 K10:** new players report typing their **official** credentials into private servers; with a fast, unsalted hash over a global prefix any host (or anyone with a DB copy) can test guesses offline -> advise unique passwords per server. |
| S-08 | Med | Outdated bundled libraries (OpenSSL 1.1.0h, libcurl 7.62.0, MongoDB 2.6.12) | *(file)* `tools/security_audit.py` | Block outbound connections of the node except what you need; do not expose any service that parses third-party TLS/HTTP |
| S-09 | Med | Client uploads its running process list to the DedicatedServer on connect; the DS writes it into its log (`Client 0, uid N. process list: …`) | *(observed, again on LAN V-9)* [protocol-observed §5](../08-reverse-engineering/protocol-observed.md#5-privacy-finding--process-list-upload) | Disclose to players if you host; do not persist the data; consider it for anti-cheat only |
| S-10 | Med | `connect`/`sv_start` unencrypted on the wire; `SCMD_CONNECT_DEDICATED_SERVER` encrypted. *(observed V-9 capture)* TCP 3801/3802/3815 carry no TLS records (length-prefixed custom framing); UDP battles are RakNet | *(community)*; TLS absence *(observed)* ⚠ | Assume plaintext on LAN/WAN for everything but that message; do not reuse a real password |
| S-11 | Low | `dbg_disableLuaDataFormatChecking = 1` set by the vendor in `cloud.xml` | *(file)* | Keep; do not feed untrusted data files; validate custom Lua/XML before deploy |
| S-12 | Low | MongoDB server-side JS enabled (`noscripting` commented out) | *(file)* | Try `noscripting = true` on a lab node; keep if services break |
| S-13 | Low | `auth_logIncomingMessages = 1`, `auth_apiDbgLog = 1` on authenticator/shard | *(file)* engine-cvars | In our runs logs held IP:port and connection events, no password strings *(observed, 2 logs)*; still re-check after changes, rotate/clean logs |
| S-14 | Low | No log rotation/cleanup | *(observed)* | Scheduled cleanup (§6) |
| S-15 | Low | Windows Firewall prompts per new exe path can stall startup and invite "allow all" clicks | *(observed)* V-8 | Pre-create explicit rules for the exact exe paths (§6.2) |
| S-16 | Info | Rewards/loot tuning from the DB or Lua is possible by anyone with file access | *(community)* | Treat depot dir as code; file ACL, integrity hashes |
| S-17 | Info | Client trusts the server (official warning: a malicious server may compromise the client) | *(official)* | Players: sandbox/VM for unknown servers; operators: publish only signed/known data |
| S-18 | Med | Third-party container images/scripts patch the server executables in place and publish wide port ranges (incl. the Hub status port 9001) with default console passwords | *(observed)* patterns match the shipped build; port list from the project README | Review before use; see [docker.md](../04-installation/docker.md) section 4.2; patch into a separate copy, record hashes, publish only the needed ports |

| S-19 | Med ⚠ | **Hash used as the credential** (community claim, single source, batch 004 G13): the client stores a password hash locally (remember-me) with a salt embedded in clear in the client and sends that hash as the password; the server compares it with `accounts.password`. If true, a leaked DB or client profile = account takeover without cracking, and server-side hashing adds nothing | *(community)* ⚠ unverified; design plausible | Treat DB dumps and client profiles as credentials; unique throw-away passwords; SV-10 to confirm; clean-room design: send password inside an encrypted channel, hash server-side with a slow salted hash, issue session tokens ([§9](#9-requirements-for-a-clean-room-community-edition-profile-d)). A server-side patch that re-hashes would break stock clients' stored values **V-10 (observed):** the stored `accounts.password` value occurs in neither capture side nor anywhere in the client profile; the login frame carries a ~384-byte encrypted-looking block and the remembered login sits encrypted/obfuscated in the `0001.prfl` header -> pass-the-hash *in clear* not observed; whether the encrypted block wraps the stored hash stays open (not reverse-engineered by decision). |
| S-20 | Low | Shipped executables (all services, client and battle server) lack ASLR/DEP/CFG linker flags (VC++ 2010 toolchain); `mongod.exe` has ASLR+DEP | *(file)* [pe-imports.md](../08-reverse-engineering/pe-imports.md) | Keep the node off untrusted networks (profile A/B); optionally enable Windows Exploit Protection per executable (untested) |
| S-21 | Info | No executable imports `libssl`; services speak a custom RakNet-style channel built from `libcrypto` RSA/AES/SHA primitives (no `SSL_*`/TLS strings in Shard, LoadBalancer, DedicatedServer, client) | *(file)* static; capture needed to confirm (SV-9) | Do not assume transport confidentiality; keep the LAN/overlay private; S-19 applies without a TLS layer |
| S-22 | Low | `StatServer.exe` (not started by the shipped `cloud.xml`, not in the 17-service node) carries an older SSH console build whose **compiled-in defaults are `ssh_port 22` and a non-empty `ssh_passwd`** (a weak placeholder word); all 21 other executables default to port 2222 and an empty password (console disabled). Started by hand without a `statserver_local.cfg` override it would expose a Lua console with a known default password | *(file)* static, [cvar-defaults.md](../05-configuration/cvar-defaults.md) section 3; not exercised | Do not run `StatServer.exe` on an untrusted network; if you do, set `ssh_passwd` empty/strong and `ssh_port` in `statserver_local.cfg` |
| S-23 | Medium | Admin tasks are **Mongo documents** (`adminTasks`): the Shard executes whatever a producer inserts; authorisation uses fields *inside the document* (`requestedByUid` -> `accounts.admRole`, role `root` always allowed, or `requestedByService = gaijin_gdpr` which skips the user check). The producer is not authenticated, and the stock MongoDB has no authentication | *(disasm)* [shard-admin-tasks.md](../08-reverse-engineering/shard-admin-tasks.md); not exercised | Same rule as S-02: DB write access = full admin. Keep MongoDB on 127.0.0.1, never expose 27017; a replacement admin plane must authenticate producers **V-10 (observed):** confirmed at runtime - a `root` account plus a document with `serviceType: 2`, `pickedBy: 0` runs `mute`/`give`/`playerInfo`; anyone with database write access can therefore mute, grant currency or read account data; a `player` requester is refused (`Not enough privilege`). Copying `accounts.password` between accounts also resets passwords instantly (V-10). |
| S-24 | Low | The SSH console implementation logs **failed login attempts with the typed password in clear** (`SSHServer: failed auth attempt ( passwd: '%s', addr: %s )`) and successful logins with user name and address; the cloud channel has no authentication beyond service registration and the TGP checksum is a non-cryptographic MurmurHash2A variant (seed `0x1337533D`) | *(disasm)* [hub-protocol-and-framing.md](../08-reverse-engineering/hub-protocol-and-framing.md); not exercised | Treat service logs as secrets when the console is enabled; do not rely on the checksum for integrity against an attacker; `net_dumpCloudMsg` dumps all cloud messages - lab only |
| S-25 | Medium | `CrashReporter.exe` defaults to upload crash dumps and script errors over **plain HTTP to a vendor host** (`crash_url` = `http://crashdumps.targem.ru:55080/submit`); the dump type `0x41` includes data segments and referenced heap memory (keys, passwords, tokens, player data) | *(file/cvar)* [external-services-and-login-modes.md](../08-reverse-engineering/external-services-and-login-modes.md); launch on a community node not tested | Set `crash_url` empty or to an own collector in `*_local.cfg`; block outbound traffic of `CrashReporter.exe`; keep dump directories private |
| S-26 | Medium | **Community client-side tooling runs code and distributes data.** The community mod manager (S18) executes every `mods/*.py` on each start (also disabled ones, and a file chosen in "Import" before confirmation) and recommends disabling the antivirus as a troubleshooting step; host launchers that download modified clients from per-server file servers are being built (b006 I5). No malicious code was found in the reviewed tool | *(file)* static review [community-mod-manager.md](community-mod-manager.md) §5; launchers not reviewed | Players/operators: read mods before use, never disable AV for them; prefer data-only patches with published hashes (§7.5); a launcher must verify signatures/hashes from a trusted source and should never fetch executables silently |
| S-27 | Low | **Chat server log holds message text and a session-token prefix**: `<nick>:<uid> --> #channel: <text>` for every chat line and `Authenticating uid=…/token=<prefix>...` at chat login | *(observed V-9)* | Treat chat-server logs as personal data (retention, access); do not publish logs; clean-room: log metadata only **V-10:** confirmed again - the chat server logs the text of messages it blocks for a muted player. |
| S-28 | Low | Every login logs a per-installation `clientId` (`win_<guid>`), identical for all accounts used on one PC; shard logs also hold the client IP:port | *(observed V-9)* | Privacy notice for public servers; useful for abuse handling (multi-accounting), but personal data **2026-10-13 (static + value-free check):** `clientId` = `win_` + the Windows **`MachineGuid`** (registry `HKLM\SOFTWARE\Microsoft\Cryptography`), read by `game.exe`; a lab login from the host matched exactly -> a persistent OS machine id, identical on every community server a player joins (cross-server tracking possible); the same client function also reads disk information (`%s%08X`) - candidate input of the unidentified 64-hex value in the login frame (Q48). **2026-10-13 (V-11, value-free):** the server **stores** a 64-hex machine fingerprint `fp` and the client IP for every connection in the audit collection `logs_<db>.logs` (`CON` events), per machine, not per account; this is the login frame's 64-hex value. A community server therefore keeps a durable machine id + IP history of every player - cover it in the privacy notice and a retention policy. |
| S-29 | Medium | **Game Lua is not sandboxed** (community claim, b008 K3; partly supported statically): the LuaJIT FFI library (`cdef`, `metatype`), `package.loadlib` and `loadstring`/`dofile` are compiled into `game.exe` and `DedicatedServer.exe`; `game.exe` imports `ShellExecuteA`. Any Lua or data a player loads from a launcher or file server - and any community Lua a host runs on the battle server - must be treated as **executable code** | *(strings, 2026-10-12)*; reachability of `ffi` from scripts not proven (Q47) | Players: only load client files from sources they trust, prefer unmodified Steam files; distribution channels: signed/hashed manifests over TLS, no service running as root/Administrator; hosts: review third-party Lua like code; downstream designs: strip FFI/shell/file functions from the script runtime or isolate the process (AppContainer/restricted token) **2026-10-13 static confirmation ([lua-runtime-surface](../08-reverse-engineering/lua-runtime-surface.md)):** `ffi` preloaded and `package`/`debug` opened in the client and 21/22 services; `io`/`os` removed but no sandbox; nothing removes `require`/`loadlib`/`ffi`. |
| S-30 | Low | **Client-started local node on player PCs listens on all interfaces**: a Steam start runs MongoDB + Hub via `win64/local_server.xml`; the services bind `0.0.0.0` even with the stock node address `127.0.0.1` (V-1), so the LB, Hub port and the Hub status endpoint 9001 (built-in key, S-04) are reachable from the network if the firewall allows it; normal remote play still fails because the LB hands out the shard address `127.0.0.1` | *(observed V-1 binds; file `local_server.xml`; community report b008 K11)* | Players: answer firewall prompts for the local server with *private network only* or block them; start `win64\game.exe` directly when not using the local server |

### 4.1 Authentication and session handling ⚠ to research

Not yet known: how the client proves identity after the first
login (session token vs. password each connect), token lifetime, reuse by the
DedicatedServer (`auth_dsHeartbeatTimeout = 5000` *(file)*), and whether the
DedicatedServer trusts the client's reported stats or the Shard only.
Candidates: Authenticator and Shard logs with `auth_logIncomingMessages`,
message vocabulary in [masterserver-enums.md](../08-reverse-engineering/masterserver-enums.md).
These belong in Q14 (protocol).

### 4.2 Abuse and game integrity

* **Account flooding / nickname squatting** — S-06. Index `{username:1}` is
  unique, so collisions are rejected, but creation is unthrottled ⚠.
* **Stress-bot flag**: `auth_allowStressBots = 0` *(file)* — keep 0.
* **Antibot counter** `shard_minAntibotCounterForMailSending = 50`,
  `shard_is2StepAuthForMailSendingNeeded = 1` *(file)* — mail sending is
  gated; see [cvar-notes](../05-configuration/cvar-notes.md) before changing.
* **Currency caps**: `sv_tokenCreditsDailyLimit = 1000` *(file)* limits
  iridium per day; `aux_limits.xml` holds hard caps. They protect the live
  economy, not a DB written directly.
* **Cheating in battle**: the DedicatedServer is authoritative for
  simulation *(inferred from architecture)*; no anti-cheat module was found
  in the node. Cheating risk is mostly client-side modification — see
  [administration](administration.md#5-security) "Modified clients".
* **Chat**: `ChatServer` on 3815; moderation relies on `bannedTill`/chat ban
  fields in the DB *(file, schema)*; no automated filter shipped (community).

## 5. Deployment profiles

| Profile | Who | Network | Controls required |
|---------|-----|---------|-------------------|
| **A. Solo/offline** | One player | Loopback only | Default stock setup; do not forward ports |
| **B. LAN/friends** | Trusted group | LAN or private overlay (WireGuard/Tailscale/ZeroTier) | §6 baseline + firewall scope to the overlay subnet |
| **C. Public community server** | Strangers | Internet | §6 + §7, dedicated host/VM, no other services on it, written privacy notice |
| **D. Clean-room community edition (future)** | Project | Internet | §9 requirements |

Profile B is the recommended default for early community use: the weaknesses
in §4 are mostly *network trust* problems, which an overlay VPN removes.

## 6. Baseline hardening (profiles A–C)

### 6.1 Host

* Run on a **dedicated machine/VM**, a **non-administrator user** with no
  personal data (a service account), no RDP exposed, OS patched.
* Place the depot where only that user and administrators can write
  (prevents tampering of Lua/XML/EXE).
* Do **not** run a game client and a public server under the same user.
* Keep a clean copy of the original depot and checksums to detect tampering
  (`Get-FileHash` over `cloud\*.exe`, `cloud\data\*`).

### 6.2 Windows Firewall (example; the port list was tested on a LAN, V-9)

Default inbound = block, then allow by program path (avoids the per-exe prompt
problem, V-8):

```powershell
# Run elevated. Adjust $root to the depot path.
$root = "<game>\star conflict\cloud"
# Public-facing services only:
foreach ($e in "LoadBalancer.exe","ChatServer.exe","DedicatedServer.exe","Shard.exe","Hub.exe") {
  New-NetFirewallRule -DisplayName "SC node $e" -Direction Inbound -Action Allow `
    -Program "$root\$e" -Protocol Any -Profile Any
}
# Never allow MongoDB or mongo shell from outside:
New-NetFirewallRule -DisplayName "SC block 27017" -Direction Inbound -Action Block `
  -Protocol TCP -LocalPort 27017
New-NetFirewallRule -DisplayName "SC block hub status/ssh" -Direction Inbound -Action Block `
  -Protocol TCP -LocalPort 9001,2222,2300-2330
```

For profile B replace `-Profile Any` by `-RemoteAddress <overlay subnet>`.
**Tested on a LAN (V-9, Q25):** remote clients need only **TCP 3801, 3802**
(+ **3815** for chat; without it chat fails silently) and **UDP 35000+**
(one port per concurrent battle, allocated upwards from 35000). **TCP 3850
(Hub) is not used by clients** - keep it closed to the outside. Port rules
(`-Protocol TCP -LocalPort 3801,3802,3815` and `-Protocol UDP -LocalPort
35000-35099`) work as well as program rules. If Windows shows an "allow
access" prompt, do not press Cancel during such tests: it creates a block
rule for that program.

### 6.3 Configuration

| Setting | Where | Recommended |
|---------|-------|-------------|
| `bind_ip` | `cloud/mongodb/config.cfg` | `127.0.0.1` (stock) |
| `ssh_passwd` | `*_local.cfg` | empty (disabled); never in a stock `.cfg` |
| `auth_allowInternalAutoCreate` | `default_platform_config.lua` | `0` on public nodes |
| `auth_allowStressBots`, `auth_closedPTRMode` | same | `0` |
| `store_allowAllItemsForBying` | same | `0` on public nodes (it is a gift of every item) |
| `lb_disallowAccess` | `loadbalancer_local.cfg` | `1` during maintenance only |
| Overrides | `*_local.cfg`, not stock files | keeps diffs reviewable ([config-system](../05-configuration/config-system.md)) |

### 6.4 Data and backups

* Backup the DB with `mongodump` while the node is stopped or quiesced; store
  encrypted, off-host; test restore. (T-1 in the work plan.)
* Keep `mongodb/data` out of cloud-sync folders (it contains hashes and IPs).
* Never commit `*_local.cfg`, key files (`ssh_privateKeyFile`) or Hub status
  keys; see CLAUDE.md rules.

### 6.5 Logs and monitoring

* Hub logs are per service and grow unbounded: schedule cleanup (e.g. keep 14
  days) and compress older.
* Watch for: repeated `TMEndpoint::OnDisconnect … reason 3` bursts from one
  IP (flood or flapping client), services missing from `/status`
  (`svcs < 17`), CPU saturation (the observed failure mode on 2 cores).
* Alert on: new `admRole` values in `accounts`, abnormal currency jumps
  (`tokenCredits` etc.), new accounts per minute.
* Query from loopback: `GET http://127.0.0.1:9001/status?key=<key>`.

### 6.6 Operating practice

* Staged updates: change on a copy node first (the "probe node" method used in
  this project: private copy with its own DB name).
* Principle of least privilege for helpers: Mongo GUI used only while the
  node is stopped *(community advice)*; remove the GUI's saved connection
  afterwards.
* Document who has host and DB access; rotate if that changes.

## 7. Additional measures for a public server (profile C)

### 7.1 Network edge

* Put the host behind a provider firewall/security group that only exposes
  the client-facing ports; rate-limit new connections per source IP
  (`iptables hashlimit` / provider DDoS tools). Game UDP (battle) is
  amplification-prone if reflected ⚠ — drop unsolicited UDP not from known
  client flows where possible.
* Prefer a distinct IP for the game node; no shared hosting with web apps.
* If you need monitoring from outside, use an authenticated reverse proxy
  (mTLS or token) to `127.0.0.1:9001`, not a port forward.

### 7.2 Database isolation

* Keep MongoDB on the same host, loopback only (stock). If it must be remote
  (multi-host, Q9): private VLAN + firewall allow-list + OS-level access
  controls; MongoDB 2.6 offers auth but the services' connection string has
  no credential slot we found ⚠ (the community mentions an "undocumented db
  config in `common_local.cfg`").
* Run `mongod` under its own low-privilege account if you can.

### 7.3 Registration and abuse control

* Gate account creation: set `auth_allowInternalAutoCreate = 0` and add
  accounts via a small admin tool (T-2 in the plan) with input validation
  (type-safe numbers; see the "free synergy went negative" community report).
* Temp-ban at the edge on bursts; use `bannedTill` for in-game bans.
* Keep a throw-away-credentials warning on the login page/README (S-07).

### 7.4 Admin access

* Admin actions through the DB tool on the host only, with an audit log
  (who, when, what). No shared Mongo GUI sessions.
* Keep the list of `admRole` accounts minimal and re-checked on each deploy.

### 7.5 Client-side safety (players and operators)

* Only connect to servers you trust *(official warning)*; the operator also
  must never distribute modified executables — distribute data only, with
  hashes.
* Operators: publish exact files/hashes for any client data patch; avoid
  executables.
* Players: virtual machine or sandbox user for unknown servers; do not run
  other sensitive apps (the process list is uploaded, S-09).

### 7.6 Privacy / legal (see [legal](../09-community-edition/legal-and-licensing.md))

* Data stored: username, password (hash ⚠), e-mail if used, `lastIP`,
  `netStat.ip`, nick, chat, hardware fingerprint for `isSingleUidOnPC`
  *(file/schema)*. Publish a short notice; define retention (e.g. IPs 30 days).
* Provide a deletion path (remove account documents and related
  `*stats*`, mail and battle records by `uid`).
* Terms of the official notice apply: no monetisation, label "Unofficial
  Server".

### 7.7 Incident response

1. Isolate: block inbound at the firewall; stop Hub (clean stop recipe in
   verification-log).
2. Preserve: copy `Hub/logs`, `mongodb/data` (stopped), firewall logs.
3. Assess: new `admRole`s, mass currency changes, unknown accounts,
   changed files vs. the clean depot hashes.
4. Rotate: SSH passwords/keys, any shared credentials; force password change
   (document that passwords are server-local).
5. Restore from the last known-good backup; document the root cause in the
   issue tracker (no personal data).

## 8. Residual risks (accepted in profiles B–C)

* Unknown memory-safety bugs in closed-source C++ services parsing
  attacker-controlled network data (RakNet-like UDP, custom TCP).
* Vendored libs with published vulnerabilities (S-08) reachable only if the
  node makes outbound TLS/HTTP calls ⚠ (not verified which services do).
* Client-side cheating: no integrity layer observed.
* Lack of transport encryption for most game traffic (S-10).

## 9. Requirements for a clean-room community edition (profile D)

If a new server is ever written (separate repository), minimum security
properties, derived from the weaknesses above:

1. **Authentication**: salted slow password hash (Argon2id/scrypt), per-session
   tokens with expiry, optional external identity provider hook (community
   asked for it); rate limits and lockout.
2. **Authorization**: roles separate from player data; admin API with its own
   credentials and audit log; never a DB flag alone.
3. **Transport**: TLS for control channels; authenticated, encrypted battle
   traffic or at least signed session tokens bound to the battle instance.
4. **Service trust**: mutual authentication between internal services
   (shared secret/mTLS), bind to loopback/private by default.
5. **Datastore**: authentication on, least-privilege roles per service,
   schema validation, typed numeric fields with bounds (the community
   corrupted `accountExpPool` by hand-editing).
6. **Input validation and fuzzing** of every packet type from the vocabulary
   in [masterserver-enums.md](../08-reverse-engineering/masterserver-enums.md);
   strict length checks; no `eval` of client data.
7. **Observability**: structured logs with PII minimisation; metrics endpoint
   with auth; anomaly alerts (§6.5).
8. **Updates**: pinned, maintained dependencies; reproducible builds; SBOM.
9. **Privacy by design**: no process-list upload; documented retention;
   deletion API.
10. **Compatibility mode**: keep the legacy client protocol behind a separate
    listener so its weaknesses do not shape the rest.

## 10. Implemented in this repository

| Item | Status |
|------|--------|
| `tools/security_audit.py` — read-only audit of config, Mongo bind/auth, SSH, account auto-create, bundled libs, optional listening ports. Run: `.venv\Scripts\python.exe -X utf8 -I tools\security_audit.py "sc-server-files\star conflict" --listening` | ✅ (run on the stock depot 2026-10-11: 0 High, 6 Med, 2 Low) |
| This chapter and updated [administration.md](administration.md) pointer | ✅ |
| Firewall script in §6.2 | ⚠ drafted, untested |
| Hardening tests (S-07 hash type, S-04..S-05 reachability from LAN, `noscripting`) | ☐ lab work, see §11 |

## 11. Verification backlog (lab experiments)

| # | Experiment | Closes |
|---|-----------|--------|
| SV-1 | Create a throw-away account; inspect `accounts.password` (length, charset, per-user variation with identical input) - **done V-9:** 64 hex, identical for identical passwords | S-07 |
| SV-2 | From a second host: scan the node ports; try Hub 3850 and Shard 3802 from outside; test with the §6.2 rules - **done V-9** (LAN; WAN open) | S-05, Q2/Q3 |
| SV-3 | Start `mongod` with `noscripting = true`; run login + battle | S-12 |
| SV-4 | Enable `ssh_passwd` on one service: confirm bind interface and that the port is closed by firewall rules | S-03 |
| SV-5 | Grep logs after login/purchase/chat for credential-like strings with `auth_logIncomingMessages` on | S-13 |
| SV-6 | Observe outbound connections of every service (`netstat`/Resource Monitor) while idle and in battle | S-08 |
| SV-7 | Verify account auto-create off: login with unknown name returns a clean error | S-06 |
| SV-8 | Count how many new accounts per minute can be created from one client | §4.2 |
| SV-9 | Packet capture: which messages are plaintext, token reuse - **partly done V-9** (host-side capture: no TLS, RakNet UDP; client->host TCP still missing) | S-10, §4.1 **V-10: done** - two-sided capture (each host's raw socket sees only its own outgoing TCP; both together = full view): no TLS anywhere, login frame layout recorded, stored hash not sent in clear. |
| SV-10 | With a throw-away account: compare the value the client stores locally (profile files, no real credentials), the value in `accounts.password` and the Shard/Authenticator log; test whether a second client can log in using only the stored value; check whether the client transport is TLS (version, certificate use) - **partly done V-9:** no salt, no TLS on TCP; client storage location of the remembered login not yet found | S-19, S-07, Q24 **V-10: largely done** - stored value not on the client in clear (profile header encrypted/obfuscated), copy-reset works (V-10); open: decryption of the header/login block and portability of a copied profile. |

## 12. References inside the repository

[administration.md](administration.md) · [architecture.md](../03-architecture/architecture.md) ·
[mongodb.md](../06-database/mongodb.md) · [schema.md](../06-database/schema.md) ·
[engine-cvars.md](../05-configuration/engine-cvars.md) ·
[protocol-observed.md](../08-reverse-engineering/protocol-observed.md) ·
[open-questions.md](../08-reverse-engineering/open-questions.md) ·
[community-faq.md](community-faq.md)

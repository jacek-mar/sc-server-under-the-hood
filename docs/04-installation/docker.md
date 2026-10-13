# Docker and container deployments

> Status: **analysis of a third-party project + our design recommendation
> (2026-10-11).** We have **not run** the container image ourselves (no Docker
> host in the lab yet, see backlog DK-1..DK-8). What *was* checked locally:
> every byte pattern the project's patchers look for, against the shipped
> executables (section 3). Behavioural claims of the project's author are
> tagged *(community)* and stay ⚠ until reproduced.

## 1. Verdict

| Question | Answer |
|----------|--------|
| Is the project useful? | **Yes — the most useful community artefact so far for hosting.** It is the first documented path to run the stock node on a Linux server, and it records several non-obvious facts (Wine allocator assertion, MongoDB version coupling, node-address resolution, battle-port range) that we would otherwise have had to discover. |
| Is it ready to be recommended as-is? | **Not yet as the default.** It works by **patching 20 of the 22 shipped executables in place** (every service incl. Hub and DedicatedServer, 1 byte each; plus 13 code-cave patches in `DedicatedServer.exe`), publishes a wide port range, ships a default console password and has no graceful shutdown. Treat it as a **reference implementation and experiment base**; adopt the architecture, harden the details (section 6). |
| Best architecture for this class of setup | **Split deployment:** native `mongod` 2.6 + Redis in their own containers, the 32-bit Windows service executables under Wine in one "node" container, depot mounted from the operator's own copy (never baked into an image), config as a separate overlay. This matches option **L0** of [linux-native-and-portable-server.md](../09-community-edition/linux-native-and-portable-server.md). |

## 2. What the project is

* Repository: <https://github.com/AlexIndustrial/starconflict-community-edition-docker>
  ("Star Conflict — Unofficial Server in Docker"); local reference copy in
  `random-materials/` (private). MIT licence for scripts/configs; no game files.
* Announced on 2026-10-09 in the community channel (source S15) and updated on
  2026-10-10 ("works behind a reverse proxy"). Author states the README was
  written with an AI assistant and is still in flux.
* Size: ~1 250 lines — `Dockerfile`, `entrypoint.sh`, two Compose files,
  `.env.example`, six helper scripts.

### 2.1 Topology

```
                 docker compose
 +----------------------+   +------------+   +-------------+
 | sc-server            |   | mongo:2.6  |   | redis:7     |
 |  debian-bookworm     |-->| 27017      |   | 6379        |
 |  wine + wine32       |   +------------+   +-------------+
 |  Hub.exe -> 16 svcs  |------------------------^
 |  DedicatedServer.exe |
 +----------------------+
   ^ ./game  (bind mount: cloud/ data/ sys_data/ copied from the Steam depot)
   ^ sc-logs volume (Hub logs, generated SSH host key + password)
```

| Piece | What it does |
|-------|--------------|
| `Dockerfile` | `debian:bookworm-slim` (linux/amd64) + `wine wine32 wine64`, `WINEARCH=win64`; **no game files** → image builds in seconds and is redistributable |
| `scripts/sync-game.sh` | `rsync` of `cloud/` (minus its Mongo data and `win64/`), `data/`, `sys_data/` from a Steam copy into `./game/` (~11 GB) |
| `entrypoint.sh` | (1) optionally adds `SERVER_HOST` as a secondary `/32` address inside the container netns and makes the hostname resolve to it first in `/etc/hosts`; (2) runs the two binary patchers; (3) rewrites `Node address=` in `cloud.xml`; (4) writes `common_local.cfg` (`db_mongoHosts`, `db_redisHost`) and `hub_local.cfg` (SSH console); (5) waits for Mongo and Redis; (6) `wine Hub.exe` |
| `docker-compose.yml` | `mongo:2.6` (`--smallfiles`, published to loopback only), `redis:7-alpine` (appendonly), `sc-server` with `NET_ADMIN` and published ranges |
| `docker-compose.prod.yml` | Override: `network_mode: host` for hosts that own the public IP |
| `scripts/patch-addr-assert.py` | 1-byte patch of every `*.exe` (section 3.1) |
| `scripts/patch-security-check.py` | 13 code-cave patches in `DedicatedServer.exe`, enabled by `PATCH_SECURITY=1` (section 3.2) |
| `scripts/player-forward.py` | Player-side TCP/UDP forwarder `127.0.0.1:<port>` → VPS, fallback when the server is behind NAT without DNAT |
| `scripts/hub-console.sh` | SSH into the Hub console on `127.0.0.1:2222` (author: password login still failing) |
| `scripts/prepare-shared.sh` | `DedicatedServer.exe -prepareSharedData` inside the container (our `prepare_shared.bat` equivalent) |

## 3. Technical claims and what we could verify

### 3.1 Wine allocator assertion — `patch-addr-assert.py`

*Claim (community):* the engine's memory kernel reserves a `VirtualAlloc` pool
at an unaligned address and executes `int 3` if it does not get exactly that
address; Windows returns it unchanged, Wine rounds to 64 KiB, so every
executable dies under Wine. The patch turns the `int 3` (`CC`) into `nop`
(`90`) at one place.

*Our check (read-only byte-pattern search, build Hub 1.99.0.167293):*
the 9-byte pattern occurs **exactly once in 20 of the 22** executables of
`cloud/` and in none of the other two (`CrashReporter.exe`, `StatServer.exe`);
the patched form occurs nowhere in the unmodified depot. The patch is therefore
well-formed for this build. Whether it is *sufficient* under Wine is the
author's observation (winedbg) — **not reproduced** (DK-2).

### 3.2 Null-call guard in `DedicatedServer.exe` — `patch-security-check.py`

*Claim (community):* when the node address is not the machine's real local
address (a dummy interface, `/etc/hosts` trick, DNAT), the global crypto object
used by `RakNet::InitializeSecurity` stays zero and the first indirect call
through it crashes the battle process; the guard substitutes the worker of the
branch a real (loopback) battle uses and cleans the stdcall stack.

*Our check:* all **13 patterns match exactly once** in the unmodified
`DedicatedServer.exe` (SHA-256 `061175da…2378`, 11 150 096 bytes) and none is
already patched. Three of the shorter patterns (code-cave paddings) also occur
in other executables, which is harmless because the script only ever touches
`DedicatedServer.exe` and demands a single match. The patch set carries
migration code for three earlier iterations (v2.1–v2.3) — i.e. it was found by
trial; treat it as **empirical, not understood**.

*Related community RE statements (S15, ⚠):* the same three patched functions are
named `InitializeSecurity`, `PublicKey` and `RakPeer::AllowIncomingConnections`;
a client-side counterpart (disabling the RakNet security handshake) is needed
only if one runs **non-stock** (own) servers; the stock client↔stock
DedicatedServer pair already works (our V-5). This is consistent with Q14
(*SCMD_CONNECT_DEDICATED_SERVER encrypted*) and suggests that **the RakNet
security layer is configured by data the Hub hands to the instance** (keys/node
address), which fails when the address is "spoofed". Not verified.

### 3.3 MongoDB version coupling

*Claim:* the 2015-era driver issues `aggregate` without the `cursor` option and
creates indexes by inserting into `system.indexes`; on MongoDB ≥ 3.6 / ≥ 4.2
this yields `FailedToParse: 'cursor' option is required` and
`InvalidNamespace: system.indexes` (dead queue/clans/factions). Hence
`mongo:2.6`. **Consistent** with the bundled `mongod` 2.6.12 and our own schema
dump ([mongodb.md](../06-database/mongodb.md)); a community comment suggests
trying DocumentDB-style compatibility layers — not evaluated.
*(community, plausible)* `mongod.exe` 2.6 itself crashes under Wine
(`file_allocator.cpp:92`), which is why the project uses a native Linux image.

### 3.4 Node address and hostname

*Claim:* the Hub finds "its" `<Node>` by matching `cloud.xml` `address` against
local interface addresses (otherwise `there is no my node in xml` and restart
loop; interfaces flagged `NOARP`, e.g. `dummy`, are not seen under Linux), and
DedicatedServer processes resolve the hostname for their `-hub` argument.
Consistent with the Hub command line we observed (`-hub 127.0.0.1:3850`,
[protocol-observed.md](../08-reverse-engineering/protocol-observed.md)) and
with `Node address="127.0.0.1:3850"` in the shipped `cloud.xml`; the exact
matching rules are open (Q2, DK-3).

### 3.5 Ports

The project publishes (TCP **and** UDP): `3800–3830`, the Hub port `3850`,
`35000–35099` (battles; `net_gamePort=35000`, further battles via
`net_autoGamePort`), `9000–9010`, plus loopback-only `2222`, `27017`, `6379`.

| Range | Our evidence | Comment |
|-------|--------------|---------|
| 3850 | Hub (observed) | needed |
| 3801 / 3802 / 3815 | LoadBalancer / Shard / Chat (observed) | needed by clients |
| 3800–3830 (rest) | not observed in use | likely too wide — Q25 |
| 35000–35099 | DS on UDP 35000 (observed, Q1) | battle range; the project says missing forwarding = "network error" at battle entry |
| **9000–9010** | **9001 = Hub HTTP status endpoint with a static key (S-04)** | the project calls this range "spare"; **do not publish it** |
| 2222 | Hub SSH console | keep on loopback (as the project does) |

## 4. Assessment

### 4.1 Strengths

* Correct core decision: Wine only where unavoidable, **native Mongo 2.6 and
  Redis**, depot mounted not copied into the image (cleaner for the licence
  terms of the official notice, and the image is shareable).
* Idempotent, single-match, fail-safe patchers with explicit status output;
  `PATCH_SECURITY` is opt-in.
* Documents real failure signatures with causes (`there is no my node`,
  `Aggregate: !ok`, dedicated-server dump in `Hub/dediserver_exceptions/`).
* Verified (author, 2026-10-10): full battle through a LAN address and through
  a white IP behind DNAT; performance in Docker reported as fine *(community)*.

### 4.2 Risks and gaps

| # | Finding | Impact | Mitigation |
|---|---------|--------|------------|
| D-1 | **In-place binary patching** of the operator's copy (20 exes) at each start | Build-specific; silently wrong on any other build; modifies "game files" the user may want pristine | Patch once into a *separate* copy (`game-patched/`) and record before/after SHA-256; refuse unknown hashes |
| D-2 | `.env.example` says the guard is **mandatory whenever `SERVER_HOST` ≠ 127.0.0.1**, the README says a *genuine* local address works unpatched, and option A (real public IP, host network) still sets `PATCH_SECURITY=1` | Contradiction ⇒ the real trigger is not understood | Test matrix DK-3 (loopback / own LAN IP / spoofed IP × patch on/off) |
| D-3 | Published `9000–9010` (includes Hub status key endpoint) and 30 consecutive ports `3800–3830` | Larger attack surface, S-04/S-05 | Publish only what Q25 proves needed |
| D-4 | Default `SSH_PASSWD=hub1234` in compose; password echoed to the log and stored in the volume | Weak secret on a console that runs Lua | Random per install (the script already can), never echo, loopback only |
| D-5 | Shutdown = `wineserver -k` on SIGTERM (hard kill) | Services killed without their normal shutdown; our clean stop is `Hub` window close then DB shutdown | Send the Hub console `quit` first (see D-6), `stop_grace_period: 60s` |
| D-6 | Hub console "password auth fails" | Maintenance mode and graceful quit unavailable | Our recipe (V-7) is known to work: PEM RSA host key and a client that still offers `diffie-hellman-group1-sha1` / `ssh-rsa` / `aes128-cbc` / `hmac-sha1`; user name ignored. `hub-console.sh` uses a stock modern `ssh` command line, which very likely cannot negotiate those algorithms ⚠ (untested) |
| D-7 | Runs as root; `NET_ADMIN` for interface games; no `HEALTHCHECK` | Larger blast radius | Drop `NET_ADMIN` when host networking is used; add health check against the Hub status endpoint (`svcs=17`, from inside the container) |
| D-8 | `mongo:2.6` is an unmaintained upstream tag with no authentication | Tag may disappear; no auth | Pin by digest and mirror to your own registry (`docker save`); keep it on a private network |
| D-9 | `hub-console.sh` hard-codes the volume name `starconflict_sc-logs` | Breaks if the Compose project name differs | Use `docker compose exec` |
| D-10 | Game version coupling: "same build as the clients" | Any client with a different build fails | Document the build id (`1.99.0.167293`, 2026-10-09) and the hashes in section 3 |
| D-11 | 11 GB `./game` copy on a bind mount of any file system | Wine on case-insensitive paths / ownership problems on non-ext4 hosts ⚠ | Prefer ext4/xfs; see LX-5 case-sensitivity scan |

### 4.3 Things the project does that we do **not** recommend copying

* The **player-side loopback forwarder** (`player-forward.py`, or an OUTPUT
  `DNAT` rule for `127.0.0.1`) as a distribution method: it puts a script or
  root firewall rule on every player's PC. It is a debugging fallback only.
* Spoofing an address on a `dummy` interface to impersonate a public IP: it is
  what forces the binary patch. Use the real address (host networking, or
  macvlan/ipvlan) whenever possible.

## 5. Network designs

| Design | When | Needs |
|--------|------|-------|
| **A. Host network** (prod override) | Linux host owns the public/LAN IP | `SERVER_HOST=<own IP>`; `FAKE_IF_MODE=none`; publish nothing, firewall instead |
| **B. DNAT from a VPS** | Home server behind NAT, public IP lives on a cheap VPS | DNAT + MASQUERADE of the TCP+UDP port set; secondary `/32` inside the container; **requires** the `DedicatedServer.exe` guard (if D-2 holds) — author verified a full battle this way |
| **C. Overlay (WireGuard/Tailscale)** | Friends-only | Same as A with the overlay address as `SERVER_HOST`; smallest attack surface |
| **D. Player-side forwarder** | Debugging only | see 4.3 |

For all designs the client connects through the login screen's **server**
entry using the node's address and Hub port (`3850`) — the community advice is
to give the plain IP; the Hub port is the default, so a port may be left out
(*community, ⚠ test*).

## 6. Recommended approach (our blueprint)

*Design sketch — not tested; the numbers in brackets refer to the findings above.*

1. **Three containers, one purpose each:** `mongo` (2.6, pinned digest, volume,
   no published port) [D-8], `redis` (loopback), `node` (Wine + Hub). No
   interface fiddling inside `node`; use host or macvlan networking [4.3].
2. **Depot handling:** the depot is mounted **read-only** at `/opt/sc/depot`;
   an init step builds `/opt/sc/run` from it with: generated `*_local.cfg`,
   `cloud.xml` node address, and — if enabled — the patched exes. The step
   prints `sha256(before) → sha256(after)` per file and aborts on unknown
   hashes [D-1, D-10]. Config and Lua edits live in a **separate overlay
   directory** (git-trackable, one `apply`/`revert`), cf. T-3 in the work plan.
3. **Wine:** `WINEARCH=win64` with 32-bit support (as the project), fixed
   `WINEPREFIX` on a volume, `WINEDEBUG=-all` in production and one named
   switch to turn it on for debugging. One `node` container per Hub (Q9 is open
   for multi-node).
4. **Secrets:** per-install random console password in a Docker secret/file
   [D-4]; no defaults in the repo.
5. **Lifecycle:** health check = Hub status `svcs=17` read from loopback inside
   the container [D-7]; stop = Hub console `quit` (or window-close equivalent),
   wait, then `wineserver -k`; `stop_grace_period` ≥ 60 s [D-5]; start order
   Mongo → Redis → node (the entrypoint's `nc` loop is fine).
6. **Ports:** publish only the Q25-validated set; keep 9001, 2222, 27017, 6379
   on loopback or an internal network [D-3]. Use the host firewall template in
   [security.md](../07-administration/security.md) §6.
7. **Backups:** nightly `mongodump` (2.6 tools in a sidecar), config overlay
   in git, `docker save` of the pinned images [D-8].
8. **Resources:** idle node ≈ 1.2 GB RAM and 19 processes on Windows
   (observed); add per battle process. Community estimates for a busy open
   world are much higher (≈ 1.5–2 GB per zone instance, one instance per
   open-world location ⚠) — measure before promising capacity.
9. **Legal:** no game files or patched executables in images or on registries;
   label the server "Unofficial Server"; no monetisation (official terms,
   [legal-and-licensing.md](../09-community-edition/legal-and-licensing.md)).

Minimal Compose skeleton (illustrative):

```yaml
services:
  mongo:
    image: mongo:2.6@sha256:<pin-your-digest>
    command: ["mongod", "--smallfiles", "--bind_ip", "0.0.0.0"]
    volumes: [mongo-data:/data/db]
    networks: [internal]            # no published ports
  redis:
    image: redis:7-alpine
    command: ["redis-server", "--appendonly", "yes"]
    networks: [internal]
  node:
    build: ./node                   # debian + wine only, no game files
    network_mode: host              # design A; real address, no NET_ADMIN
    volumes:
      - ${SC_DEPOT}:/opt/sc/depot:ro
      - ./overlay:/opt/sc/overlay:ro
      - sc-run:/opt/sc/run
      - sc-logs:/logs
    environment: { SERVER_HOST: "${SERVER_HOST}", SC_PATCH: "addr,security" }
    stop_grace_period: 60s
    healthcheck: { test: ["CMD", "/opt/entry/health.sh"], interval: 30s }
networks: { internal: { internal: true } }
volumes: { mongo-data: {}, sc-run: {}, sc-logs: {} }
```
(With host networking the node reaches `mongo`/`redis` through published
loopback ports; a pure-bridge variant needs design B.)

## 7. Docker vs. other hosting options

| Option | Strength | Weakness | Our take |
|--------|----------|----------|----------|
| Windows host, stock files | Zero patches, officially supported path | Windows licence/cost, per-exe firewall prompts (V-8) | Best for a PC at home |
| **Docker + Wine (this project)** | Cheap Linux VPS, reproducible, easy to snapshot | Binary patches, Wine quirks | **Best for 24/7 servers today** |
| Proton/Wine without containers | No Docker | Manual, fragile ([linux-proton.md](linux-proton.md)) | Fine for experimenting |
| Native Linux services | Ideal long-term | Requires re-implementation ([implementation-options.md](../09-community-edition/implementation-options.md)) | Future |

## 8. Lab backlog

| ID | Test | Closes |
|----|------|--------|
| DK-1 | Build and run the project unmodified on a Linux x86_64 host; record start-up time, RAM, `svcs=17` | verification of the "Status" table in the README |
| DK-2 | Run the Hub **without** `patch-addr-assert` under the same image: which exes die and how? | 3.1 |
| DK-3 | Matrix: node address loopback / host LAN IP / spoofed IP × `PATCH_SECURITY` 0/1 → does a battle start? | D-2, Q2, Q3 |
| DK-4 | Same matrix on **stock Windows** with `cloud.xml` set to the LAN IP (is the dedicated-server crash reproducible without Wine?) | D-2; may explain community "LAN client cannot join" reports |
| DK-5 | Port minimisation: publish only 3850, 3801, 3802, 3815, 35000+ and observe what a remote client still needs | Q25, D-3 |
| DK-6 | Hub console login with the V-7 recipe against the container | D-6 |
| DK-7 | Graceful stop sequence and Mongo consistency after `kill` | D-5 |
| DK-8 | Measure RAM/CPU for one idle node, one coop battle, one open-world instance | capacity planning |

## 9. Reuse policy

The project is MIT-licensed; we **link to it and describe it, we do not copy
its scripts** into this CC0 repository. A hardened Compose bundle would have to
be written independently (see
[linux-native-and-portable-server.md](../09-community-edition/linux-native-and-portable-server.md) §8)
and would not contain patched executables.

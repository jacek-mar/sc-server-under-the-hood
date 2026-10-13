# Beyond Windows — Linux-native and portable server options (theoretical)

> **Design analysis - not verified, not a plan.** This page compares options for a
> possible future server built by a *separate* project. Nothing here was built
> or tested, and nothing here is a recommendation of this repository.
>
> Written 2026-10-11. Nothing here was built or tested on Linux. Facts marked *(file)* come from the depot (inspected with
> `pefile`), *(community)* from chat reports, ⚠ means assumption. Companion
> pages: [implementation-options](implementation-options.md) (architectures and
> languages), [linux-proton](../04-installation/linux-proton.md) (what people
> run today), [security](../07-administration/security.md).

## 1. Starting point — what the Windows dependency really is

| Component | Finding | Source |
|-----------|---------|--------|
| 22 service executables in `cloud/` (Hub, Shard, LB, DedicatedServer …) | **32-bit x86 PE** (`Machine 0x14c`), console subsystem | *(file)* |
| `DedicatedServer.exe` | 32-bit PE, ~10.9 MB, imports only `kernel32/advapi32/user32/shell32/ws2_32/winmm/iphlpapi/imm32/comdlg32` + bundled OpenSSL/curl — **no Direct3D** | *(file)* |
| Hub | additionally imports `pdh.dll` (Windows performance counters) | *(file)* |
| MongoDB | **x64** Windows build 2.6.12; the same version exists for Linux (protocol-compatible) | *(file)* + ⚠ |
| Game client | `win64/game.exe` x64 + D3DX9 + FMOD; the old native Linux client is gone | *(file, community)* |
| Config regeneration | `prepare_shared.bat` = `DedicatedServer.exe -prepareSharedData …` — the *engine itself* turns Lua data into XML | *(file)* |
| Launch glue | `.bat` files, `%LOCALAPPDATA%\Targem\StarConflict` profile | *(file)* |

Corrections/implications:

* [linux-proton.md](../04-installation/linux-proton.md) says "Windows x64
  binaries only" — true for the client, **not** for the server: the node is
  **32-bit**. On Linux this means a 32-bit-capable Wine (the newer
  "WoW64" mode of Wine avoids installing 32-bit system libraries ⚠), and on ARM
  hosts an x86 emulation layer *plus* 32-bit support ⚠.
* The server's Win32 surface is **small and boring** (sockets, files, time,
  threads, console). That is a good sign for Wine compatibility, and the few
  special cases (performance counters, adapter info) are testable.
* The battle simulation is the only part that is *not* replaceable by data or
  config; every "Linux-native" idea below has to say what it does with
  `DedicatedServer.exe`.

## 2. The Minecraft analogy — what "community server" means there

The Minecraft ecosystem is a useful template because the stock server was
closed in distribution form but heavily extended and re-implemented. Mapping
(⚠ from general knowledge of that ecosystem):

| Minecraft practice | Equivalent for Star Conflict | Feasibility |
|--------------------|------------------------------|-------------|
| **Vanilla server jar** run as-is on any OS | Stock node under Wine/Proton | Works today (community) |
| **Patched vanilla** (Spigot/Paper-style: source patches for performance + plugin API) | No source → only *binary* patching/hooking of the PE files, or data/Lua overlays. Brittle and legally grey; Lua gameplay scripting and config overlays are the legitimate "plugin" layer | Overlays: yes. Binary patches: avoid |
| **Plugin/mod APIs** (Bukkit, Sponge, Forge/Fabric) | Server-side Lua scripts (`ScriptsServer`, zone events, queue config) + data packs | Yes — already exists; needs documented API (lua-api-surface) |
| **Proxy networks** (BungeeCord/Velocity) in front of many backends | Gateway/LB layer in front of several nodes/regions; session routing; auth | Option B in implementation-options |
| **Protocol translators** (Geyser-style) | Gateway that lets a *different* client talk to the stock protocol — or stock client talk to a new backend | Long term |
| **From-scratch re-implementations** (Minestom, Cuberite, Glowstone) | Clean-room control plane (D) and eventually own simulation (E) | High effort; most "universal" |
| **Container images + one-command install** (`docker-minecraft-server`) | Compose stack: Wine+node, Mongo, admin UI | Medium; the single biggest adoption lever |
| **Control panels / "eggs"** (Pterodactyl-style templates) | Start/stop/log/backup/config UI; server templates | Medium (Stage 4 tooling) |
| **Server lists, version handshakes, community protocol wiki** | Public registry with "Unofficial Server" label; capability handshake; this repo's docs as the spec | Low-Med |
| **Backup/rollback tools, world managers** | Mongo dump + config snapshot, account import/export | Low |

The *lesson* of that ecosystem: adoption came from (1) an easy way to run the
thing, (2) an extension API, (3) a documented protocol, **then** (4)
re-implementations. Our order should be the same — see §6.

## 3. Option ladder (from "least change" to "most universal")

### L0 — Stock node in Wine/Proton, containerised

* Wine (prefix) in a headless container; services are console programs.
* Replace Windows `mongod.exe` with a **native Linux MongoDB 2.6** (loopback,
  inside the same container/pod) — Hub and services speak the Mongo wire
  protocol and cannot tell ⚠.
* Pros: no new code; works for x86-64 hosts now; tracks stock behaviour.
* Cons: Wine layer overhead and bugs; 32-bit support; ARM needs emulation;
  Hub's `pdh`-based stats may degrade ⚠; `TerminateProcess`-style management
  quirks already seen on Windows (verification-log); still EOL Mongo.
* Effort: low. **This is track A of the roadmap in container form.**

### L1 — Linux-native control plane + Wine only for the battle server

* New native services (Rust/Go) replace Hub, LB, Shard, Chat, MM, Rewards …
  (options C/D). Only `DedicatedServer.exe` (and `prepare_shared` mode if
  still needed) remains under Wine, *one process per battle*.
* Wine is then confined to a **small, isolated worker image**; the public
  attack surface and the 32-bit/ARM question shrink to "battle workers".
* The per-battle process model maps directly to **game-server orchestration**
  patterns (allocate a worker, hand over a session, reap on exit) — what the
  Hub does today. Orchestrators such as Kubernetes-based game-server
  allocators or Nomad are the generic equivalent ⚠ (design option, not a
  requirement; a plain process pool is enough for community scale).
* Effort: high (needs WP-1…WP-3 of implementation-options). Biggest gain per
  effort *after* L0.

### L2 — Native re-hosting of the PE (no source)

Theoretical routes to run `DedicatedServer.exe` without Wine:

| Route | Idea | Verdict |
|-------|------|---------|
| Static binary translation | Lift x86 PE to LLVM IR / native ELF with a Win32 shim layer | Research-grade, large and fragile; **not recommended** |
| User-mode PE loader + thin Win32 shim (own) | Re-implement the ~100 imported Win32/WinSock APIs on Linux and load the PE | Equivalent to writing a mini-Wine; possible *because* imports are few ⚠, but unclear gain over using Wine itself |
| x86 emulation (e.g. on ARM) | Run the unchanged 32-bit binary via an x86 emulator + Wine | Useful for cheap ARM hosts; performance unknown |

Legal note: the notice permits *use and modification of server files*
*(official)*; static translation still falls under that but yields no
redistributable asset, so it is a private technique at best.

### L3 — Native battle server (re-implemented simulation)

* A new authoritative simulation (flight model, weapons, AI, zones), written
  Linux-first (any language), speaking the stock client's UDP protocol.
* Needs the full battle protocol + client-side expectations (physics, hit
  validation, replication). This is *the game engine*, i.e. option E.
* Only worth it if the community wants a new/modified client or to escape the
  32-bit/closed DS entirely. Would make the server natively
  multi-platform, multi-arch, and moddable like Minetest/Luanti-class engines.

### L4 — "Universal" packaging of whatever exists

Independent of L0–L3:

| Technique | Benefit |
|-----------|---------|
| Static single-binary builds (Rust/Go) for linux-x86_64, linux-aarch64, windows, macOS | One download per platform; trivial ops |
| OCI multi-arch images + Compose/Helm | Same recipe for home server, VPS, cluster |
| XDG-compliant paths and env-var config (replace `%LOCALAPPDATA%`, `.bat`) | Native feel; read-only root filesystems |
| systemd units / Windows service wrapper from one config | Reliable restarts, logging to journal |
| WebAssembly/WASI for pure-logic parts (matchmaker, rules, loot rolls) | Run the same logic in server, tests, browser tools ⚠ optional |

## 4. Porting hazards to plan for (any native-Linux direction)

| Hazard | Why | Mitigation |
|--------|-----|-----------|
| **Case sensitivity** | Data authored on Windows may reference `Foo.lua` as `foo.lua` | Normalise at load; test on case-sensitive FS; case-insensitive overlay as fallback ⚠ unverified count |
| **Path/encoding** | Backslashes, mixed encodings (Cyrillic comments, BOMs; project already hit ANSI issues) | UTF-8 everywhere in new code; treat input as bytes |
| **Line endings in cfg/Lua/XML** | CRLF parsers | Tolerant parser |
| **Data generation step** | XML is produced by `DedicatedServer.exe -prepareSharedData` from Lua | Either run it once under Wine at build time, or re-implement the export (inputs are Lua tables → deterministic; test by diffing against stock output — task B-5) |
| **Bytecode scripts** | LuaJIT 2.1.0-alpha bytecode in `misc.pak` is version-specific | Use source scripts; re-implement from lifted docs; do not redistribute bytecode |
| **Clock/timezones** | Events are dated; cron-like cvars | Run in UTC; explicit event calendar tool |
| **Process management** | Hub spawns/kills services; Windows signals | Explicit supervisor semantics (graceful stop, orphan reaping) |
| **UDP ports per battle** | One DS per battle, port range open question (Q1) | Host networking or explicit port map per worker |
| **32-bit limits** | DS address space ~2–4 GB | Observe memory under load before sizing workers |
| **Time-of-check issues on shared FS** | Mongo data dir, logs on network FS | Local SSD; no NFS for Mongo |

## 5. Comparison

| Criterion | L0 Wine container | L1 native CP + Wine workers | L2 PE re-hosting | L3 native sim | L4 packaging only |
|-----------|:----:|:----:|:----:|:----:|:----:|
| New code needed | none | large | large | very large | small |
| Linux-native feel | low | high (CP) / low (workers) | medium | full | n/a |
| ARM friendliness | poor | good CP, poor workers | emulated | good | good |
| Security surface | old stock services | small CP, isolated workers | as L1 | smallest | unchanged |
| Time to value | days | months | uncertain | years | days |
| Reversible | yes | yes | yes | n/a | yes |
| Risk | Wine bugs | protocol unknowns | engineering sink | scope | none |

## 6. Suggested order (all theoretical)

1. **L0 + L4 first**: a Compose recipe (Wine node + native Mongo 2.6) and a
   Linux ops guide — answers Q19 and Q20 and produces the "download and run"
   experience the community asks for.
2. **Measure** under Wine: memory, CPU per battle, startup time, `pdh`
   behaviour, 32-bit constraints (lab tasks LX-1…LX-6 below).
3. In parallel start **protocol work** (WP-1…3), because every native
   direction depends on it.
4. Build **L1 incrementally** (strangler path), starting with gateway and chat;
   keep the Wine battle worker until a real alternative exists.
5. Treat **L2/L3** as research tracks; revisit only if the community wants a
   modified client or Wine proves unreliable.

## 7. Lab backlog (Linux, when a host is available)

| # | Task | Output |
|---|------|--------|
| LX-1 | Wine WoW64 + `mongod` 2.6.12 native: start Hub, count services (17?) | Verified compose recipe, V-4 |
| LX-2 | Same in a rootless container, headless (no X11) | Image size, required packages |
| LX-3 | Run one battle (coop vs AI): DS memory/CPU, port used | Sizing numbers, Q1 |
| LX-4 | Check Hub stats/health without `pdh` (status JSON) | Compatibility note |
| LX-5 | Case-sensitivity scan: references vs actual file names in `data/gamedata` and `cloud/data` | List of mismatches |
| LX-6 | `prepare_shared` under Wine vs on Windows: byte-compare generated XML | Confirms portable build step |
| LX-7 | ARM host + x86 emulation + Wine (optional) | Feasibility note |
| LX-8 | Remote client from Windows to the Linux node (LAN) | Closes Q2/Q3 on Linux |

## 8. Decision points (for the downstream project; not taken here)

1. Is the goal "run the stock server well on Linux" (L0/L4 — near term) or
   "own the server" (L1+, long term)? They are compatible; L0 should come first.
2. Willingness to depend on Wine for battle workers for the foreseeable future.
3. Target hosts: x86-64 only, or also ARM (home servers/cheap VPS)?
4. Whether to ship a Compose bundle in this repository's `/docker` folder (the
   planned layout in the roadmap) — it contains no Gaijin files, only recipes.

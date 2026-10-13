# Community edition — implementation options (languages, architectures, practices)

> **Design analysis - not verified, not a plan.** This page compares options for a
> possible future server built by a *separate* project. Nothing here was built
> or tested, and nothing here is a recommendation of this repository.
>
> Written 2026-10-11. Solution type, languages and frameworks are decided by
> a separate downstream project. This page turns what the reverse-engineering
> work has established into concrete options and trade-offs. Wherever the text
> below says "recommended", read it as *the analyst's assessment at the time*,
> offered as one input, not as a project decision. Evidence tags as elsewhere; statements about *other*
> projects are general knowledge, not researched here ⚠ (verify before citing).
> Companion pages: [roadmap](roadmap.md) (tracks/milestones),
> [legal-and-licensing](legal-and-licensing.md),
> [security §9](../07-administration/security.md#9-requirements-for-a-clean-room-community-edition-profile-d).
> Scope reminder: any code lives in a **separate repository**; this one stays
> analysis-only (CLAUDE.md §1).

## 1. What we know that constrains the design

| # | Fact | Source | Consequence |
|---|------|--------|-------------|
| K1 | A node = ~17 service executables started by a Hub from `cloud.xml`; a battle = one `DedicatedServer.exe` process per match | architecture.md, verification-log | The system is already *service-oriented*; boundaries for replacement exist |
| K2 | `cloud.xml` has a per-service `path` attribute ("absolute path to executable") and the Hub spawns what is listed | cloud.xml header *(file)* | A custom executable *could* be slotted in for one service type ⚠ (needs the Hub registration protocol) |
| K3 | Client ↔ LB/Shard/Chat is **TCP**, message-based: `SCMD_*`/`CCMD_*`, async RPC `CSCMD_ASYNC_REQ` with `AC_*` action ids (master-server enums: 1 011 members in 79 groups), request/response ids, store sync pair | protocol-observed *(observed)*, masterserver-enums | Names and sequences known; **byte framing and serialisation unknown** (Q14) |
| K4 | Battle traffic is **UDP** to the DedicatedServer; `SCMD_CONNECT_DEDICATED_SERVER` is reported encrypted, `connect`/`sv_start` plaintext | observed + community ⚠ | Needs capture work; key/derivation unknown |
| K5 | The DedicatedServer takes `-cloudAddr -hub -gsid -regionId` and reads *GameSessionParameters* (queue, players, vessels, rewards) from **MongoDB**, then writes results back | protocol-observed §4 *(observed)* | A replacement control plane must (a) speak to DS as the Hub does and (b) provide that document, *or* keep stock Hub+Mongo |
| K6 | Game logic and content are **data-driven Lua/XML**: ~23 000 `Def.*` definitions, queue/event configuration in `default_platform_config.lua`, server scripts (`ScriptsServer`, zone events) as Lua | gamedata-catalogue, zone-events | Content can be reused unmodified if the new server embeds Lua (LuaJIT 2.1.0-alpha dialect) |
| K7 | The simulation (flight, weapons, AI, physics) lives inside closed-source `DedicatedServer.exe` / `ZoneInstance` | binaries | Re-implementing it is a game-engine project, not a server project |
| K8 | Client executes only 34 allow-listed server→client Lua calls | lua-rpc-allowlist *(observed)* | Defines the maximum "script surface" of a custom battle server |
| K9 | DB document schema is known (collections, indexes, fields) | schema.md *(observed)* | Account import/export and save editors are feasible regardless of server language |
| K11 | `prepare_shared` is a **build step**: Lua in `data/gamedata/shared` -> generated XML (`aux_limits.xml`, `store.xml`, `quests.xml`, ...) read by Shard and DS at start; the client keeps its own copy of the shared Lua | config-pipeline-and-limiters *(disasm + file)* | A replacement data pipeline must reproduce the generated files (or the services that read them) and keep client/server copies consistent |
| K12 | The MatchMaker hands the DS a single `botPresetName` (+ counts) in the game-session document; the Shard rate-limits requests per channel (cvars `sm_req*`) | config-pipeline-and-limiters *(disasm)* | Small, well-defined contracts for matchmaking output and gateway protection |
| K10 | Official permission covers use/modification of server files, no monetisation, label "Unofficial Server" | legal notes *(official)* | Reusing the stock DS and Lua content is explicitly allowed; clean-room is for *our code*, not a legal necessity for these parts |

## 2. Architectural options

| Option | Idea | Reuses stock | New code | RE needed | Effort | Main risk |
|--------|------|--------------|----------|-----------|--------|-----------|
| **A. Operations wrapper** | Don't replace anything: supervisor, config overlay, web admin/status, backup, Docker/Wine images, save editor | Everything | Tooling only | None beyond what exists | Low | Not "a new server"; inherits every limitation of K1-K5 |
| **B. Protocol gateway / proxy** | A man-in-the-middle in front of stock services: per-IP rate limits, allow-lists, TLS tunnel, logging, packet validation, optional login gate | All services | One network daemon + dissector | Framing only (Q14) | Low-Med | Cannot add features beyond filtering; encrypted parts opaque |
| **C. Strangler replacement** | Keep stock Hub, DS, Mongo; replace services *one at a time* with new executables registered in `cloud.xml` (first: Chat, Authenticator/LB gate, MatchMaker, Leaderboard, Rewards) | Hub, DS, remaining services | New services + protocol library | Client↔service framing **and** Hub↔service protocol | Med-High | Hub protocol (`TMEndpoint`) unknown; incremental value but each service needs deep fidelity |
| **D. Clean-room control plane + stock DS** | New single binary replaces Hub, LB, Shard, Chat, MM, Rewards, Lobby, Quests, Universe…; spawns stock `DedicatedServer.exe`, provides its session document | DS (+ data files) | Whole control plane | Full client protocol, DS↔Hub protocol, DS Mongo reads | High | Large surface; every client RPC (1 011 enum members, not all RPCs) must be answered correctly |
| **E. Full clean-room incl. battle simulation** | New game server and, necessarily, new/modified client | Assets only | Everything | Total | Very high | Different project: client expects stock sim/protocol; contradicts the community consensus "make SC1 work" |

**Reading of the evidence:** D is the natural *end state* and C is the safest
*path* to it; A and B are valuable immediately and are not wasted work (B's
dissector doubles as the RE tool for C/D). E should only be considered if the
community later wants a *new* game.

### 2.1 One possible staged path ("strangler fig"; assessment, not a decision)

1. **Stage 0 — knowledge**: wire capture, framing, type-db, Hub protocol
   (open: Q14, Q23, security SV-9). Output = a *language-neutral* spec.
2. **Stage 1 — A+B**: wrapper/admin + gateway/dissector (useful to every
   operator and to security: rate limit, allow-list).
3. **Stage 2 — C**: first replaced services with the smallest blast radius:
   ChatServer, then Authenticator/LB gate (external auth, registration
   policy), then Leaderboards, then MatchMaker (better bot/MMV logic).
4. **Stage 3 — D**: when the RPCs used by a normal play session are covered and stock
   Hub/Shard can be dropped; replace Hub last (spawn DS directly).
5. **Gate** before each stage: a conformance suite (§5) passes against
   *recorded real traffic* from the stock node.

Hybrid note: a new control plane can be written as a **modular monolith**
(one process, internal modules mirroring service types behind interfaces) so
that it can start small and still be split into separately registered services
for the strangler phase.

## 3. Language options

Criteria derived from the project: untrusted binary input from the internet
(security §4), Windows **and** Linux hosting (Wine today), single-binary
deployment for non-expert operators, embedding Lua, contributor pool,
protocol prototyping speed.

| Language | Strengths | Weaknesses | Fit |
|----------|-----------|------------|-----|
| **Rust** | Memory safety for packet parsing; no GC pauses; single static binary; `tokio`/`mio`, `nom`/`binrw` parsers; `mlua` can embed **LuaJIT**; strong fuzzing (`cargo-fuzz`) | Steeper learning curve; smaller hobbyist pool | **Best technical fit**, recommended for protocol core and services |
| **Go** | Fast to write; goroutines map to per-connection handlers; single binary; huge ops/tooling ecosystem; easy contributor onboarding; `gopher-lua` (Lua 5.1, *not* LuaJIT semantics) or cgo LuaJIT | GC (fine at this scale); less compile-time safety for parsers; Lua bytecode/semantics differences | **Best pragmatic fit**; recommended alternative if contributor velocity matters most |
| **C# / .NET 8** | Excellent Windows story (original is Windows-only); good async, `System.IO.Pipelines`, `Span<T>`; NLua/MoonSharp or P/Invoke LuaJIT; precedent in game-server emulators | Runtime dependency or larger self-contained binary; Linux ops less familiar for some | Strong candidate for a Windows-heavy community |
| **C++** | Same ecosystem as the original; direct reuse of `RakNet`-class libraries if the transport is RakNet; LuaJIT native | Memory-safety burden on untrusted input; build complexity; smaller modern contributor appetite | Only for narrow components (e.g. transport shim) |
| **TypeScript / Node.js** | Fastest prototyping; many hobby game servers; JSON/Mongo native | Single-thread CPU limits; binary protocols clumsy; Lua embedding weak | Good for *admin web UI* and prototype dissectors |
| **Python** | Best for RE tooling (already used here), Kaitai/scapy, fast experiments | Not for the production server (perf, deployment) | Tools, test harness, conformance runner |
| **Java/Kotlin** | Mature server ecosystem, Netty | JVM footprint; Lua embedding via LuaJ (5.2) | Possible, no special advantage |
| **Elixir/Erlang** | Excellent for many concurrent sessions, supervision trees (mirrors Hub) | Niche; binary protocols fine but contributor pool small | Interesting, not recommended for volunteers |
| **Lua (LuaJIT)** | The game's own content language | Not a systems language | **Keep as the content/gameplay scripting layer** (K6) |

**Assessment (input only, not a recommendation of this project):** *Rust for the protocol library and long-running services;
Lua (LuaJIT via `mlua`) for gameplay scripts and event logic so the shipped
`Def.*`/queue/event data runs unmodified; Python for tooling and conformance
tests; TypeScript only for an optional web admin UI.* If the community values
onboarding speed over compile-time guarantees, substitute **Go** — the spec
(§4) is language-neutral, so the decision is reversible.

Caveat on Lua: the stock engine uses **LuaJIT 2.1.0-alpha** and ships some
scripts as **bytecode** (`misc.pak`). Bytecode is version-specific and must not
be redistributed by us; a new server should load *source* scripts (the
gamedata files are plain text) and re-implement any bytecode-only server
scripts from our lifted documentation ([luajit-bytecode](../08-reverse-engineering/luajit-bytecode.md),
[zone-events](../05-configuration/zone-events.md)).

## 4. Formats and specification artefacts

"What format?" has three layers:

| Layer | Recommended format | Why |
|-------|--------------------|-----|
| **Legacy wire protocol spec** | Declarative **Kaitai Struct** (`.ksy`) per message + prose in Markdown + **Wireshark Lua dissector** generated/hand-written | One source of truth generates parsers for Rust/Go/C#/Python; the same format fits TPAK and DB documents; testable against captures |
| **Test vectors** | Captured sessions as `pcap` + extracted **JSON/NDJSON** event streams, annotated, with secrets scrubbed | Golden files for conformance and fuzz seeds |
| **Internal service API (new code)** | **Protobuf** or **FlatBuffers** (or plain Rust traits in a monolith) | Only needed once the monolith is split; avoid inventing a new wire format for old clients |
| **Persistent state** | Stock-compatible document schema ([schema.md](../06-database/schema.md)) in MongoDB-compatible form *or* SQL (PostgreSQL JSONB / SQLite) behind a repository interface | Keeps save editors and account import working; SQLite makes tiny nodes single-file |
| **Server configuration** | **TOML** (or YAML) for the new server; the stock `*.cfg`/Lua overlays remain for stock components | Human-editable, comment-friendly, schema-validatable |
| **Content** | Original Lua/XML **as is**, overlaid by community patches (diff-friendly, no Gaijin files in the repo) | Compatibility and clear licence boundary |

**MongoDB note** ⚠: the stock services use a 2.6-era driver; newer MongoDB
majors are reported to have dropped the legacy opcodes it relies on. Options:
(a) keep the bundled 2.6.12 on loopback (stock behaviour, EOL), or
(b) write a minimal **wire-protocol shim** that answers only the handful of
queries `DedicatedServer.exe` issues (K5), so the real database can be modern
and never network-exposed. (b) is a contained, testable component and would
also remove the largest item from the security findings (S-01, S-08).

## 5. Established practices to adopt

From long-lived game-emulator and reimplementation projects (WoW/Ragnarok
emulators such as MaNGOS/TrinityCore-style and rAthena/Hercules-style
login/char/map server splits, OpenTTD/OpenRA-style reimplementations, and
community-documented protocols like the Minecraft protocol wiki — ⚠
general knowledge):

1. **Protocol docs before code**, kept as a living, versioned spec with
   evidence tags; implementers consume the spec, not each other's code.
2. **Clean-room discipline**: record provenance of every spec statement
   (capture id, file, experiment); implementers work from the spec; never
   paste decompiled code. Our evidence-tag system already supports this.
3. **Conformance test-suite from recorded traffic**: replay captured client
   sessions against the new server and diff responses; run the same suite
   against stock services to validate the suite itself.
4. **Fuzzing from day one** for every parser (cargo-fuzz/AFL++) seeded by the
   captures; fail closed; strict length limits (security §9).
5. **Data-driven content separate from engine code**; overlay mechanism for
   community balance changes; versioned content packs with hashes.
6. **Scripting/plugin boundary** with explicit capability limits (mirrors the
   client RPC allow-list, K8).
7. **Layered configuration** (defaults → file → env → CLI), `*_local` style
   overrides, no secrets in repo.
8. **Observability**: structured logs with PII minimisation, metrics,
   health endpoint with auth, a "replay/record" debug mode.
9. **Packaging**: Docker/Compose + native zip, reproducible builds, SBOM,
   signed releases; a one-file "run a node" path for non-experts.
10. **Community governance**: public server registry/list with
    "Unofficial Server" labelling, RFC-style process for protocol/DB
    changes, code of conduct, bus-factor ≥ 3 maintainers, CC0/permissive
    licence for specs and a licence for code chosen deliberately (CC0 is for
    documents; code typically MIT/Apache-2.0 or GPLv3 — decision needed).
11. **Compatibility handshake**: advertise server capabilities/version so
    patched clients and launchers can adapt; keep legacy mode isolated.

## 6. Proposed work packages (what unblocks what)

| WP | Deliverable | Unblocks | Needs |
|----|-------------|----------|-------|
| WP-1 | Capture + framing spec for LB/Shard/Chat TCP (Kaitai) | B, C, D | Wire capture (maintainer approval for tooling), Q14 |
| WP-2 | Hub↔service (`TMEndpoint`) protocol notes | C, D | Capture on loopback, Hub/service strings |
| WP-3 | DS session contract: exact Mongo documents read/written by DS | D, shim | Mongo profiler/log on a battle |
| WP-4 | UDP battle handshake and `SCMD_CONNECT_DEDICATED_SERVER` key derivation | direct client↔custom DS only; not needed if stock DS reused | RE, high effort |
| WP-5 | Wireshark dissector + record/replay tool (Python first) | everything | WP-1 |
| WP-6 | Prototype: "hello server" — LB greeting, auth ack, empty store, MOTD; see stock client reach main menu | go/no-go for C/D | WP-1 |
| WP-7 | Chat service replacement as first strangler component | validates Hub protocol | WP-2, WP-6 |
| WP-8 | Mongo shim for DS reads | removes DB exposure | WP-3 |

**Go/no-go gates**: after WP-6 (can a stock client log into code that is not
Gaijin's?) and after WP-7 (can a replaced service live inside a stock Hub?).
If WP-6 fails (e.g. a hard encrypted handshake with unknown keys), fall back
to A+B and keep operating the stock node — which is already a complete
solution.

## 7. Decisions that belong to the downstream project (not taken here)

1. Target end state: C (hybrid, stock DS + Hub) or D (own control plane)?
2. Primary language: Rust vs Go vs C# (assessed in section 3; criteria, not a verdict).
3. Licence of the future code repository (MIT/Apache-2.0 vs GPL; CC0 stays for
   docs).
4. Permission to install capture tooling (Wireshark/Npcap or `pktmon`) —
   required for WP-1/2/3 (also security SV-9).
5. Where the new repository lives and who may contribute (clean-room
   contributor statement).

# Changelog

All notable changes to this documentation. Format:
[Keep a Changelog](https://keepachangelog.com/). Versions stay `0.x` while
verification on Windows, Linux and LAN setups continues.

## [Unreleased] - 0.3.0

### Fixed
- Quick start no longer says that closing the client stops the server (the
  verified §4 says it does not), and the FAQ's connect answer gives login port
  3801 instead of Hub port 3850 (V-9). Both contradictions were found while
  translating (playground 011).

### Added
- **Queue reference cross-check** (playground task 006, reviewed): 55 queue
  instances and 395 map/mode combinations; every named queue and brawl pair
  confirmed; `leagueQueue` row completed
  ([queue reference](docs/05-configuration/queue-reference.md)).
- **Quest layer comparison** (playground task 003, reviewed): `quests.lua` and
  `quests.xml` disagree on event days in 18 quests and carry many one-sided
  fields ([tuning-recipes](docs/05-configuration/tuning-recipes.md)); new
  open question Q70.
- **Russian translations** (playground task 011, reviewed) of the quick
  start, troubleshooting and the operator FAQ, plus the translators' term list,
  in [docs/ru/](docs/00-index.md). They are brought up to date with today's
  English text, including the 002 additions.
- **Glossary** ([01-overview/glossary.md](docs/01-overview/glossary.md)), a new
  document from playground task 008 (reviewed): 74 game and server terms with
  the English and Russian words players use, each checked against its doc or
  game-file source, plus the core matchmaking terms.
- **Quest-vs-queue lint** (playground task 002, reviewed): the seven quests
  blocked when Detonation (11) is removed from every queue, and four quests
  whose mode (8 or 10) no shipped queue offers
  ([community FAQ](docs/07-administration/community-faq.md), Q61 amended).
- **Static parse of the Lua data** (playground task 001, reviewed):
  559,236 statically readable assignments in 299 files, with the 4,209
  constructs that need run time listed by kind
  ([inventory §4a](docs/02-inventory/inventory.md)). How
  `ConfigureMatchmaker()` builds and registers the two queue sets
  ([queue reference §1](docs/05-configuration/queue-reference.md)).
- **Community digest batch 013** and a third Steam forum re-crawl
  ([source register](docs/sources/source-register.md), T1-T13, SF36-SF45):
  forced faction ownership of open-world sectors, edits without effect when
  the node is not restarted, storage limits, the Steam branch check (only
  build 25826043 exists); new open questions Q68 (seed-chip scope) and Q69
  (PvP-only ship bans), Q61 amended (campaign mission needs Detonation).
- **Server-only tests V-13** ([verification-log](docs/04-installation/verification-log.md)):
  admin-task queue throughput (one task per ~5 s), duplicate and interrupted
  tasks, nine more verified tasks incl. maintenance mode, permanent
  mute/ban and account creation ([admin-tasks-howto §3a](docs/07-administration/admin-tasks-howto.md)),
  custom roles read only at start-up, full cvar layer order including
  `cloud.xml` ([settings-reload-map §2a](docs/05-configuration/settings-reload-map.md)),
  database on a non-default port, ship document structure.
- **Verification on real hardware** ([verification-log](docs/04-installation/verification-log.md)):
  a node hosted on one Windows PC with clients on two PCs in a LAN - remote
  login, matchmaker battles, squads, concurrent battles, the minimal set of
  client-facing ports, failure signatures; live service consoles; admin
  tasks; a full `prepare_shared` run (29 generated XML files, byte-identical
  to the shipped ones).
- **Settings reload map** ([settings-reload-map](docs/05-configuration/settings-reload-map.md)):
  which changes apply live (service console), at restart (`*_local.cfg`,
  where the platform Lua does not override it) or only after
  `prepare_shared`.
- **Admin operations** ([admin-tasks-howto](docs/07-administration/admin-tasks-howto.md)):
  the Shard's admin-task queue with verified examples (player info, mute,
  ban, role, currency and premium grants, ship level and research unlock,
  nickname change), custom admin roles (`web_adm.admRoles`) and the
  broadcast-mail format (`adminMail`, attachment types).
- **Client compatibility** ([hub-protocol-and-framing](docs/08-reverse-engineering/hub-protocol-and-framing.md) §6a):
  all version and data checks between client, Shard and battle server; the
  battle server's entity-definition check explains why adding or renaming
  definitions on a server locks out unmodified clients.
- **Who reads which game-data file** ([gamedata-readers](docs/05-configuration/gamedata-readers.md)):
  only the client and the battle server load `data/gamedata` directly; the
  other services use the generated `cloud/data` XML.
- **Security**: findings S-19 to S-30 in the [security chapter](docs/07-administration/security.md)
  (password storage, transport without TLS, machine identifiers and logs,
  Lua runtime surface, client-started local nodes); tested firewall port
  list for LAN hosting.
- Reference documents: cvar defaults for all executables, cvar catalogue,
  module and ship definition models, quest semantics, store/zone/rule
  semantics, bot presets, event ships/mail/clan ship, DLC crediting notes,
  matchmaker decision log, console commands, Shard admin tasks and
  privileges, service data map, static summaries of rarely used services,
  external endpoints and login modes, Lua runtime surface, master-server
  enums with numeric values.
- Operator tools: [`tools/data_drift_check.py`](tools/data_drift_check.py)
  (compare a server's data files with the original install, stale or
  hand-edited generated XML, shifted store ids), alongside `queue_lint.py`,
  `defname_check.py` and `security_audit.py`
  ([config-validation-tools](docs/07-administration/config-validation-tools.md),
  [tools/README](tools/README.md)).
- Reviews of community projects: [Docker packaging](docs/04-installation/docker.md)
  and the [community mod manager](docs/07-administration/community-mod-manager.md)
  (including a shipped loot-rule defect it works around).
- Operator FAQ and tuning recipes extended from anonymised community reports,
  each cross-checked against the shipped files; latest additions: which
  edits need the same files on every client (definition names), the
  "Experimental destroyer" is an AI boss, Galactic Standards = `goldCredits`;
  new open question Q49 (AI/boss hulls as player ships), since extended with
  a static comparison; craft recipe files, module slots bound to model bones,
  the PvE custom-game player minimum, and what admin roles change.
- Further static findings: how definitions get display names (most have none;
  set `uiName` and add a client string) in
  [data-files](docs/05-configuration/data-files.md); what a client may send to
  the battle server (an allowlisted Lua-RPC channel with no ship/stat values)
  in the [security chapter](docs/07-administration/security.md); the
  LeaderboardServer's Redis layout and the ScriptsServer event loop in the
  reverse-engineering notes; the client will not run in a Remote Desktop
  session; and the cloud message header's request/response id fields.
- Operator tool [`tools/ref_lint.py`](tools/ref_lint.py): finds references to
  definitions that do not exist; with `--reference` it shows only what an
  edit introduced ([config-validation-tools](docs/07-administration/config-validation-tools.md) §2b).
- [Data invariants](docs/05-configuration/data-invariants.md): eleven rules
  that edits must not break, and the 184 references in the shipped data that
  point at undefined names (including the eight loot tables of the stock
  loot rules).
- [Titles, achievements, offers, auras, presets, seed chips](docs/05-configuration/progression-xml-semantics.md):
  meaning of the remaining generated XML files, with translated rules from
  the source comments.
- `ZoneCoordinator.exe` summary (open-world instance dispatcher) in
  [service-summaries-static](docs/08-reverse-engineering/service-summaries-static.md);
  data search roots (`datasources*.txt`, `sys_data`) in
  [data-files](docs/05-configuration/data-files.md); case-sensitivity scan
  for Linux hosting (LX-5); static findings for DLC crediting (Q44) and the
  `address.cfg` location (Q46).
- **Special Operations (PvE raids)** ([V-12](docs/04-installation/verification-log.md)):
  access gates (client rank locks, ship-rank bands, weekly raid schedule,
  solo entry) and a lab test showing that no configuration route adds
  allied bots to a raid; new open question Q50.
- **Pirate destroyers** ([pirate-destroyers](docs/05-configuration/pirate-destroyers.md)):
  definition ids, English display names, parent hulls, spawning events and
  module loadouts of the open-world pirate destroyer bosses, plus the
  static facts that bear on flying one (Q49).
- **Fan-site Knowledge Base review** (S17 in the
  [source register](docs/sources/source-register.md)): all 17 articles and
  the setup guide checked against our docs; five community claims turned
  into test proposals Q51-Q55 (PvE level limits and `nan`, currency
  overflow, Experimental destroyer grant, editing resources, alien weapons
  on player ships), linked from the FAQ, tuning recipes and pirate
  destroyers.
- **Community guide update** (S11, online version of 2026-10-14): delta
  digest O1-O14 in the [source register](docs/sources/source-register.md);
  new open questions Q56 (loose files vs `.pak`), Q57 (vessel-id
  allocation), Q58 (`storeItemId` semantics), Q59 (battle-pass reward
  errors); new recipes (resource holding limits, mole crates, battle-pass
  comments translated), a "new ship" chain in
  [data-files](docs/05-configuration/data-files.md), Linux DB editing, FAQ
  entries.
- **Static answers (2026-10-14):** id counters (`counters`, next free
  id, `vid` unique per database) in [mongodb.md](docs/06-database/mongodb.md)
  §3a (Q57, Q54); `storeItemId` duplicate rule (Q58); no server-side DLC
  check on battle-pass rewards and the Shard command
  `dbg_testBattlePassUnlockPremium` (Q59); signed 32-bit currency limit
  (Q52); `default_modules` fallback at ship spawn (Q55); raid games always
  get `botsCount = 0` from the MatchMaker (Q50).
- **Community reports, 13-14 October** (digest P1-P15 in the
  [source register](docs/sources/source-register.md)): FAQ answers on safe
  database editing, Steam starts colliding with a running MongoDB (client
  local-server autostart), the request limiter, the new-account starter kit
  (`starter_pack.lua`, `synergy_on_start`), mode lists for co-op, karma,
  cosmetic grants (custom elements, stickers) and seed-chip slots on alien
  hulls; new tuning recipes; open questions Q60 (account refused after
  edits) and Q61 (bots in the bomb mode); Q49 amended.
- **Steam community discussions** (new source S19, 9-14 October; digest
  SF1-SF24 in the [source register](docs/sources/source-register.md)):
  the official setup guide's new "before you start" warnings; FAQ answers on
  MongoDB start failures, "Server under heavy load" (a login-queue text),
  the duplicate-package fatal error, rank 16-17 matchmaking and loot, co-op
  PvE queues, a second client, hosting behind NAT, Steam achievements and
  premium overflow; tuning recipes for bots, gold, iridium, infinite premium
  and the clan ship; open questions Q62 (NAT hosting) and Q63 (premium time
  limit); Q35, Q45, Q59 and security finding S-28 amended.
- **Community reports, 14-15 October, and a second Steam forum crawl**
  (digest R1-R19 and SF25-SF35 in the
  [source register](docs/sources/source-register.md)): security finding
  S-31 (an undisclosed client route to server console commands, with
  interim hardening advice); a host-reported Wine start-up tip for Linux and
  macOS; repeatable quests (answers SF23), clan values for solo play and the
  clan creation cost; FAQ and tuning-recipe additions; open questions Q64
  (login-name case), Q65 (client route to the console), Q66 (respawn times
  and start countdown - partly solved: `countdown_duration` and the
  per-death respawn penalty per mode in `gameplaysettings.lua`) and Q67
  (asteroid visibility); Q44, Q49 and Q61 amended.
- **`tools/queue_lint.py`: loot-rules checks** - L1 warns when a ship rank
  1-17 has no row in `DedicatedServcerServices_SetLootRules` (the shipped
  config has none for ranks 16-17, so those ships get no loot search), L2
  reports row syntax errors (missing tier, `lt` or numeric `iter`, rank out
  of range, duplicate rank, missing comma; exit status 1), L3 prints which
  ranks share which tables. Documented in
  [config-validation-tools](docs/07-administration/config-validation-tools.md).
  Two further information checks: I2 (queues whose squad rank range differs
  from the rank range) and I3 (vs-AI templates that include the bomb mode).
- **Static answers (2026-10-14, second block):** hosting behind NAT - three
  "override external host" settings found, host only, the LoadBalancer pair
  apparently only with two or more Shard/chat servers (Q62, partly solved);
  "cannot enter the battle" - the 53 matchmaker refusal codes with their
  client messages and likely causes after hand edits, no karma-based check
  ([troubleshooting](docs/04-installation/troubleshooting.md), Q60); premium
  time - the client display keeps 32 bits of the seconds left, so 68 years or
  more shows as zero while the client's expiry check still counts it as
  active (Q63); mail and trading from a new PC - the 2-step setting
  `shard_is2StepAuthForMailSendingNeeded` (FAQ); cosmetic grants with the
  admin task `giveVesselCustomElement`; the client's file index - duplicate
  paths between packages are fatal and a packed file most likely wins over a
  loose one with the same path (Q56, static lead); the bomb mode's rules in
  `gameplaysettings.lua` and no bot-side bomb behaviour found (Q61); S-28
  corrected (the single-account-per-PC flag feeds login and matchmaking, not
  trading).
- **Static answers (2026-10-14, third block):** the full `cloud.xml`
  schema read by the Hub (`ServiceCVars`, per-node and per-service cvars,
  `publicIF`, `noGameSession`, `noZoneInstance`, `disabled`,
  `additionalParams`) in [config-system](docs/05-configuration/config-system.md);
  file precedence settled - a packed file always wins over a loose file with
  the same path ([data-files](docs/05-configuration/data-files.md), Q56); the
  battle server copies the session's `botsCount` into `sv_numBots` (Q50
  solved); squads are checked against `mmSquadRank` only after
  `maxSquadTimeInQueue` (Q35); no seed-chip slots anywhere on the alien and
  boss hull chains (Q49); starter-pack XML schema and selling cosmetic items;
  troubleshooting tables for MongoDB start failures, the memory-leak dialog
  and two more messages.
- **`tools/data_drift_check.py`**: two new checks - inventory-extension step
  rows (invariant I-12, new in
  [data-invariants](docs/05-configuration/data-invariants.md)) and a light
  Lua syntax check of changed files (brackets, strings, blocks, missing
  commas; zero findings on the 327 shipped Lua files).

### Changed
- FAQ: the "Experimental destroyer" answer no longer says it cannot be
  flown; it has no store entry, and flying it is open (Q49).
- Premium time: `accounts.premiumTill` is the expiry as a Unix timestamp in
  milliseconds; the `give` admin task takes hours.
- `LICENSE` carries the full CC0 1.0 legal code; scope, trademarks and the
  terms for servers built from this material are in `NOTICE.md`.
- Only the read-only operator tools are published (see `tools/README.md`).
- Several earlier statements corrected (32-bit service executables,
  `tournaments.xml` is shipped, `loot_tables.xml` content, community advice
  on per-ship stats).

## [0.2.0] - 2026-10-11

### Added
- English translations of all cvar comments of the shipped platform config
  and a generated [cvar reference](docs/05-configuration/cvar-reference.md).
- Queue reference, open world and services, game modes, generated level
  catalogue, XML schemas, game-data catalogue, locale catalogue, zone events.
- TPAK archive format, LuaJIT bytecode notes, Lua API surface, pak contents,
  observed protocol vocabulary, binary capability sheets, PE imports.
- Live database schema and MongoDB notes.
- First live runs: node start-up, real client login and battle, clean
  shutdown, built-in SSH console.
- Security chapter, operator FAQ, tuning recipes, implementation-option and
  Linux-native analyses (design comparisons, not plans).
- Licence: CC0 1.0.

## [0.1.0] - 2026-10-10

### Added
- Repository structure and documentation skeleton (overview to community
  edition, sources).
- Inventory of the released server and client, architecture (service
  layout, ids, ports, start-up sequence), configuration system, matchmaking
  guide (adapted from the official Russian document), data-file catalogue,
  installation quick start, troubleshooting, legal notes, source register.

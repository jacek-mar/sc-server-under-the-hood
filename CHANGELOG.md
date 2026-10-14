# Changelog

All notable changes to this documentation. Format:
[Keep a Changelog](https://keepachangelog.com/). Versions stay `0.x` while
verification on Windows, Linux and LAN setups continues.

## [Unreleased] - 0.3.0

### Added
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

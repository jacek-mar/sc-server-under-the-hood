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
  new open question Q49 (AI/boss hulls as player ships).

### Changed
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

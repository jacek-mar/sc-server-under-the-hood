# Star Conflict Server — Under the Hood

Unofficial, community documentation of the **Star Conflict dedicated server
software** that Gaijin Entertainment released when official support ended
(9 October 2026): how it is built, what it can do, how to install, configure and
operate it — and an information base that separate projects (for example a
community-edition server) can build on. This repository analyses and documents;
it does not choose or build the solution.

> **Unofficial.** This project is not affiliated with or endorsed by Gaijin
> Entertainment, Targem Games or StarGem Inc. It contains **no game files**.
> Obtain the game and server from Steam. Servers built from this material must
> not be monetised and must be labelled **"Unofficial Server"** (see
> [legal notes](docs/09-community-edition/legal-and-licensing.md)).

## Start here

| I want to… | Read |
|------------|------|
| Understand what was released | [Overview](docs/01-overview/overview.md) |
| Run a local server in 5 minutes | [Quick start](docs/04-installation/quick-start.md) |
| Host for friends / the internet | [Quick start §5](docs/04-installation/quick-start.md#5-playing-with-friends--hosting-for-others), [Security chapter](docs/07-administration/security.md), [Operator FAQ](docs/07-administration/community-faq.md) |
| Change matchmaking, bots, rewards | [Matchmaking guide](docs/05-configuration/matchmaking-guide.md), [CVar notes](docs/05-configuration/cvar-notes.md) |
| Edit my save / accounts | [MongoDB](docs/06-database/mongodb.md) |
| Know how the server is built | [Architecture](docs/03-architecture/architecture.md), [verification log](docs/04-installation/verification-log.md) |
| Query/edit the database | [MongoDB](docs/06-database/mongodb.md), [schema](docs/06-database/schema.md) |
| Look up events, queues, cvars, levels | [zone events](docs/05-configuration/zone-events.md), [queues](docs/05-configuration/queue-reference.md), [cvars](docs/05-configuration/cvar-reference.md), [levels](docs/05-configuration/level-catalogue.md) |
| Understand protocol / file formats | [observed protocol](docs/08-reverse-engineering/protocol-observed.md), [Hub, cloud and TGP framing](docs/08-reverse-engineering/hub-protocol-and-framing.md), [TPAK format](docs/08-reverse-engineering/tpak-format.md), [LuaJIT bytecode](docs/08-reverse-engineering/luajit-bytecode.md) |
| Help reverse-engineer / contribute | [RE notes](docs/08-reverse-engineering/re-notes.md), [Open questions](docs/08-reverse-engineering/open-questions.md), [CONTRIBUTING](CONTRIBUTING.md) |
| Tweak economy / loot / bots | [Tuning recipes](docs/05-configuration/tuning-recipes.md), [bot presets](docs/05-configuration/bot-presets.md), [caps pipeline](docs/08-reverse-engineering/config-pipeline-and-limiters.md), [event ships, mail, clan ship](docs/05-configuration/event-ships-mail-and-clan-ship.md) |
| Check my config edits before restarting | [Operator tools](tools/README.md), [config validation](docs/07-administration/config-validation-tools.md), [when settings take effect](docs/05-configuration/settings-reload-map.md), [MatchMaker decision log](docs/05-configuration/matchmaker-decision-log.md) |
| GM / admin actions, accounts, mail | [Admin tasks how-to](docs/07-administration/admin-tasks-howto.md), [Shard admin tasks](docs/08-reverse-engineering/shard-admin-tasks.md), [privilege per task](docs/08-reverse-engineering/shard-task-privileges.md), [external services and login modes](docs/08-reverse-engineering/external-services-and-login-modes.md) |
| See what is still unknown | [Open questions](docs/08-reverse-engineering/open-questions.md), [Roadmap (analysis)](docs/09-community-edition/roadmap.md) |
| Think about a new/Linux-native server | [Implementation options](docs/09-community-edition/implementation-options.md), [Linux-native & portable](docs/09-community-edition/linux-native-and-portable-server.md) |

Full table of contents: [docs/00-index.md](docs/00-index.md).

## Status

**Documentation v0.3 (in progress).** Inventory, architecture, configuration
(cvars with English text, queues, events, data files), database schema,
archive and script formats, security analysis and operator procedures are in
place. Verified on Windows: a local node, a LAN setup with clients on two
PCs, admin operations and the data-generation step. Not yet verified: Linux
(Wine/Proton, Docker) and internet-facing hosting. Every statement carries an
evidence tag - *(official)*, *(observed)*, *(community)*, *(inferred)* or
⚠ unverified - see the [source register](docs/sources/source-register.md).
What is still unknown is listed in the
[open questions](docs/08-reverse-engineering/open-questions.md).

## Repository layout

```
docs/      Documentation (numbered by theme; see docs/00-index.md)
tools/     Read-only checks for server operators (see tools/README.md)
CLAUDE.md  Rules for contributors and AI agents
LICENSE    CC0 1.0 - public domain dedication (legal code)
NOTICE.md  Scope of the dedication, trademarks, terms for servers
```

## Regenerating the cvar reference

```powershell
.venv\Scripts\python.exe -X utf8 tools\extract_cvars.py "<game>/star conflict/cloud/data/default_platform_config.lua" docs/05-configuration/cvar-reference.md
```

## License

Everything authored here is dedicated to the public domain under **CC0 1.0**
(see [LICENSE](LICENSE)). This repository holds analysis only - no Gaijin code
or assets. Game content and trademarks belong to their owners; scope and
exclusions are listed in [NOTICE.md](NOTICE.md).

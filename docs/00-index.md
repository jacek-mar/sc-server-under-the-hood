# Documentation index

Status legend: ✅ substantive draft · 🟡 partial · ⬜ planned (no file yet).

## 01 Overview
| Doc | Status |
|-----|:------:|
| [overview.md](01-overview/overview.md) — what was released, goals, key facts, legal summary | ✅ |
| glossary.md — terms (MMV, shard, node, wing…) | ⬜ |

## 02 Inventory
| Doc | Status |
|-----|:------:|
| [inventory.md](02-inventory/inventory.md) — depot layout, counts, runtime profile, source materials | ✅ (dir level) |
| file-catalogue.md — per-file catalogue | ⬜ |

## 03 Architecture
| Doc | Status |
|-----|:------:|
| [architecture.md](03-architecture/architecture.md) — services, ids, startup, ports, layers | ✅ |
| protocol.md — wire protocol | ⬜ (Stage 5) |

## 04 Installation
| Doc | Status |
|-----|:------:|
| [quick-start.md](04-installation/quick-start.md) | ✅ ⚠ partly unverified |
| [linux-proton.md](04-installation/linux-proton.md) | 🟡 community-reported |
| [troubleshooting.md](04-installation/troubleshooting.md) | 🟡 |
| [verification-log.md](04-installation/verification-log.md) — hands-on test record (V-1..V-8 local node; **V-9 LAN test** with two PCs, **V-10 LAN 2026-10-11** (two-sided capture, live consoles, admin tasks, remember-login location, server-authoritative ship stats, loot fix): remote login, battles, squad, minimal ports, concurrent battles, credential observations; **V-11 node-only lab**: `prepare_shared` output, settings reload, more admin tasks, machine fingerprint) | ✅ |
| [docker.md](04-installation/docker.md) — community Docker project: analysis, patch check, risks, hardened blueprint, lab backlog DK-1..8 | ✅ ⚠ not run by us |

## 05 Configuration
| Doc | Status |
|-----|:------:|
| [config-system.md](05-configuration/config-system.md) — layers, cfg, cloud.xml, Lua dispatcher | ✅ |
| [matchmaking-guide.md](05-configuration/matchmaking-guide.md) | ✅ |
| [game-modes.md](05-configuration/game-modes.md) — gameplay ids, maps, brawl schedule | ✅ |
| [data-files.md](05-configuration/data-files.md) — `cloud/data` catalogue | 🟡 |
| [settings-reload-map.md](05-configuration/settings-reload-map.md) — when a setting takes effect: live console, `_local.cfg` vs platform Lua, `prepare_shared` (lab V-11) | ✅ |
| [gamedata-readers.md](05-configuration/gamedata-readers.md) — **generated**, which program reads each `data/gamedata` file (client / battle server / both / via XML) | ✅ |
| [cvar-notes.md](05-configuration/cvar-notes.md) — curated English notes | 🟡 |
| [cvar-reference.md](05-configuration/cvar-reference.md) — **generated**, 271 cvars, English + original RU comments | ✅ |
| [gamedata-catalogue.md](05-configuration/gamedata-catalogue.md) — **generated**, Lua game-data files, def-name families, ship matrix | ✅ |
| [level-catalogue.md](05-configuration/level-catalogue.md) — **generated**, 194 active levels with mode entities | ✅ |
| [xml-schemas.md](05-configuration/xml-schemas.md) — **generated**, structure of `cloud/data/*.xml` | ✅ |
| [engine-cvars.md](05-configuration/engine-cvars.md) — **generated**, 436 engine cvars with effective values | ✅ |
| [open-world-quests.md](05-configuration/open-world-quests.md) — **generated**, 11 personal open-world quests | ✅ |
| [zone-events.md](05-configuration/zone-events.md) — **generated**, open-world event ids and parameters (from bytecode) | ✅ |
| [locale-catalogue.md](05-configuration/locale-catalogue.md) — **generated**, 13 string tables: key counts, families, def coverage (no text) | ✅ |
| [tuning-recipes.md](05-configuration/tuning-recipes.md) — where to change economy/loot/bots/events (community leads cross-checked with files) | 🟡 |
| [quests-semantics.md](05-configuration/quests-semantics.md) — **generated**, quest system: enums, Lua→XML mapping, cross-check | ✅ |
| [module-defs.md](05-configuration/module-defs.md) — **generated**, weapon/module definition model, marks, price override merge, store.xml cross-check | ✅ |
| [cvar-binary-catalogue.md](05-configuration/cvar-binary-catalogue.md) — **generated**, cvar names in binaries vs shipped config, battle-server cvar descriptions | ✅ |
| [cvar-defaults.md](05-configuration/cvar-defaults.md) — **generated**, 1 420 cvar registrations from the 22 service executables and the x64 client: type, compiled-in default, description (services only); live value vs default | ✅ |
| [matchmaker-decision-log.md](05-configuration/matchmaker-decision-log.md) — how to read the MatchMaker decision log (PvP hands/destroyer rules, PvE by buffs/mission level), static catalogue | ✅ |
| [event-ships-mail-and-clan-ship.md](05-configuration/event-ships-mail-and-clan-ship.md) — where event-ship parts come from, mail rules, clan-ship (dreadnought) requirement (static answers Q34/Q42/Q43) | ✅ |
| [bot-presets.md](05-configuration/bot-presets.md) — bot behaviour presets, lineups and tier/rank rules (answers Q28 statically) | ✅ |
| [ship-defs.md](05-configuration/ship-defs.md) — **generated**, ship definition data model: files, inheritance, stat fields and ranges, link to store/DB | ✅ |
| [store-zones-rules-semantics.md](05-configuration/store-zones-rules-semantics.md) — meaning of store/zone/rule XML attributes, generator vs hand-maintained files | ✅ |
| [queue-reference.md](05-configuration/queue-reference.md) — every queue incl. brawl/sector/league/raid | ✅ |
| [open-world-and-services.md](05-configuration/open-world-and-services.md) — ZoneInstance, Universe, quests, leaderboards, global events | ✅ |
| economy-and-rewards.md | ⬜ |

## 06 Database
| Doc | Status |
|-----|:------:|
| [mongodb.md](06-database/mongodb.md) | ✅ |
| [schema.md](06-database/schema.md) — **generated**, DB/collection/index/field schema from a live node | ✅ |

## 07 Administration
| Doc | Status |
|-----|:------:|
| [security.md](07-administration/security.md) — security analysis: threat model, 28 findings (S-01..S-28), hardening profiles, firewall recipe (port list LAN-tested, V-9), requirements for a clean-room edition, lab backlog | ✅ |
| [config-validation-tools.md](07-administration/config-validation-tools.md) — `defname_check.py` / `queue_lint.py`: def-name and queue-block checks, results on the shipped config | ✅ |
| [console-commands.md](07-administration/console-commands.md) — **generated**, console commands with usage strings and the Shard admin-task list | ✅ ⚠ static |
| [community-mod-manager.md](07-administration/community-mod-manager.md) — review of the community tool SCPatcher / "Star Conflict Mod Manager" v0.1 (by Furebel): how it patches Lua/XML, bundled mods checked against the depot, security review, shipped loot-rule defect (Q45) | ✅ ⚠ static |
| [admin-tasks-howto.md](07-administration/admin-tasks-howto.md) — operator how-to for Shard admin tasks: required document fields (`pickedBy: 0`), verified `playerInfo`/`mute`/`cancelMute`/`give`, static parameters of `ban`, `assignRole`, `unlockAllVesselNodes`, safety notes | ✅ |
| [community-faq.md](07-administration/community-faq.md) — operator FAQ from community questions, cross-checked with files | 🟡 |
| [administration.md](07-administration/administration.md) — console, logs, backups, security | ✅ ⚠ |

## 08 Reverse engineering
| Doc | Status |
|-----|:------:|
| [re-notes.md](08-reverse-engineering/re-notes.md) | 🟡 |
| [tpak-format.md](08-reverse-engineering/tpak-format.md) — TPAK v7 archive format (verified, reader in tools/) | ✅ |
| [luajit-bytecode.md](08-reverse-engineering/luajit-bytecode.md) — LuaJIT bytecode reader/disassembler (87/87 scripts) | ✅ |
| [lua-api-surface.md](08-reverse-engineering/lua-api-surface.md) — **generated**, Lua globals used by scripts | ✅ |
| [ow-mission-script.md](08-reverse-engineering/ow-mission-script.md) — open-world `Mission` script hooks | ✅ |
| [ow-events-catalog.md](08-reverse-engineering/ow-events-catalog.md) — **generated**, 126 open-world mob/boss event definitions | ✅ |
| [pe-imports.md](08-reverse-engineering/pe-imports.md) — **generated**, PE metadata, imports, mitigations, crypto primitives | ✅ |
| [config-pipeline-and-limiters.md](08-reverse-engineering/config-pipeline-and-limiters.md) — `prepare_shared` → `aux_limits.xml` pipeline, Shard request limiter, MatchMaker bot-preset selection (static) | ✅ |
| [shard-admin-tasks.md](08-reverse-engineering/shard-admin-tasks.md) / [shard-admin-tasks-table.md](08-reverse-engineering/shard-admin-tasks-table.md) — admin-task queue (`adminTasks`), authorisation (`admRole`, `web_adm.admRoles`), 58 task handlers with parameters (generated table) | ✅ |
| [shard-task-privileges.md](08-reverse-engineering/shard-task-privileges.md) — **generated**: all 58 Shard admin tasks mapped to their required privilege (17-entry table recovered from `AccessPrivileges.cpp`) | ✅ |
| [service-data-map.md](08-reverse-engineering/service-data-map.md) — **generated**: per-executable MongoDB collection presence (7 databases) and exclusive/shared source modules | ✅ |
| [service-summaries-static.md](08-reverse-engineering/service-summaries-static.md) — static read-up of `EarlyMatchMaker.exe`, `StatServer.exe`, `Tournament.exe`, `LeaderboardServer.exe` | ✅ |
| [hub-protocol-and-framing.md](08-reverse-engineering/hub-protocol-and-framing.md) — Hub and service layers, 27-byte cloud header and routing rules, TGP 12-byte frame with MurmurHash checksum, Hub behaviour and cvars (static) | ✅ |
| [lua-runtime-surface.md](08-reverse-engineering/lua-runtime-surface.md) — which LuaJIT libraries game scripts can reach: `ffi` preloaded, `package`/`debug` opened, `io`/`os` removed, in the client and 21/22 services (static; Q47, S-29) | ✅ |
| [external-services-and-login-modes.md](08-reverse-engineering/external-services-and-login-modes.md) — outbound endpoints (Steam/VK/FB/crash upload), login-mode cvars, crash-dump privacy, command-line switches (static) | ✅ |
| [binary-endpoints-and-options.md](08-reverse-engineering/binary-endpoints-and-options.md) — **generated**: URLs/host names and command-line switch candidates per executable | ✅ |
| [lua-rpc-allowlist.md](08-reverse-engineering/lua-rpc-allowlist.md) — 34 server→client RPC names | ✅ |
| [protocol-observed.md](08-reverse-engineering/protocol-observed.md) — observed client/cloud message names and sequences | ✅ |
| [pak-scripts.md](08-reverse-engineering/pak-scripts.md) — scripts/configs inside misc.pak, headless battle start | ✅ |
| [masterserver-enums.md](08-reverse-engineering/masterserver-enums.md) — **generated**, master-server RPC enums (names + numeric values since 2026-10-13) | ✅ |
| [pak-contents.md](02-inventory/pak-contents.md) — **generated**, contents of all 588 paks | ✅ |
| [binary-capability-sheets.md](08-reverse-engineering/binary-capability-sheets.md) — **generated**, per-executable names | ✅ |
| [open-questions.md](08-reverse-engineering/open-questions.md) | ✅ living |

## 09 Community edition
| Doc | Status |
|-----|:------:|
| [roadmap.md](09-community-edition/roadmap.md) | 🟡 |
| [legal-and-licensing.md](09-community-edition/legal-and-licensing.md) | 🟡 |
| [linux-native-and-portable-server.md](09-community-edition/linux-native-and-portable-server.md) — Linux-native/portable options L0-L4, Minecraft-ecosystem analogy, porting hazards, lab backlog LX-1..8 | ✅ |
| [implementation-options.md](09-community-edition/implementation-options.md) — architectures A-E, language comparison, formats, practices, work packages WP-1..8 | ✅ |

## Sources
| Doc | Status |
|-----|:------:|
| [sources/source-register.md](sources/source-register.md) — S1–S18, Discord digests batches 001–006 (b006 I1-I20), SCPatcher (S18) | ✅ |

## Conventions

* One theme per file; new topics get a new numbered folder only if they don't
  fit an existing one.
* Evidence tags: *(official)*, *(observed)*, *(community)*, *(inferred)*, ⚠.
* Paths relative to the depot root `star conflict/` unless stated; user data in
  `%LOCALAPPDATA%\Targem\StarConflict\`.
* Never paste proprietary files or personal data; summarise.
* Language: English only; adaptations/translations of sources are welcome.
* Python tooling runs only inside the project `.venv` (see `CLAUDE.md`).

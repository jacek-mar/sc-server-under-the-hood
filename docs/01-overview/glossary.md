# Glossary - game and server terms (EN/RU)

> Status: first version, 2026-10-18, 74 entries. Maps the words players use
> (English and Russian) to the terms these docs and the game files use.
> The "Docs / file term" column was checked against the cited source. The
> player words are *(community)* usage, collected from chat wording and
> not verified. Use them to search, not as definitions.

Russian words are given as players write them; they are not translations
of the docs.

## Matchmaking terms used throughout these docs

| Term | Meaning | Source |
|---|---|---|
| MMV (`mmValue`) | Matchmaking value: one number per player, computed from ship rank, efficiency and other modifiers. Queues accept bands of it, for example `19-24`, upper bound exclusive | [matchmaking-guide](../05-configuration/matchmaking-guide.md) §4-5 |
| Rank (`mmRank`) / squad rank (`mmSquadRank`) | Ship-rank limits that a queue checks for a solo player or for a squad | [matchmaking-guide](../05-configuration/matchmaking-guide.md) §8 |
| Squad | Players who queue together; checked by squad rank and the `squad_*` cvars | [matchmaking-guide](../05-configuration/matchmaking-guide.md) §8, Q35 |
| Wing | The group that enters sector (sector conquest) queues; size limits come from `mm_sectorMinWingSize` / `mm_sectorMaxWingSize` (5 / 8) | [engine-cvars](../05-configuration/engine-cvars.md) |
| Low-online set | `queuesConfigLo`, the queue set used below 250 players online; on small servers it is the one in use | [queue-reference](../05-configuration/queue-reference.md) §1 |

## Server and services

| Concept | Docs / file term | Players say (EN) | Players say (RU) | Source |
|---|---|---|---|---|
| Bot presets | `bot presets` | bot preset, bot setup | настройки ботов | [community-faq](../07-administration/community-faq.md) |
| Cvar | `cvar` | cvars, console variable | квар, консольная переменная | [community-faq](../07-administration/community-faq.md) |
| Hub | `Hub` | hub server | хаб, сервер хаба | [community-faq](../07-administration/community-faq.md) |
| Matchmaker | `MatchMaker` | matchmaking, match maker | матчмейкер, подбор боя | [community-faq](../07-administration/community-faq.md) |
| Platform config | `default_platform_config.lua` | platform config, queue config | конфиг платформы, настройки очередей | [community-faq](../07-administration/community-faq.md) |
| Prepare shared | `prepare_shared` | prepare shared, regenerate shared data | генерация общих данных | [community-faq](../07-administration/community-faq.md) |
| Queue | `queues` | queue, match queue | очередь, очереди | [community-faq](../07-administration/community-faq.md) |
| Reload settings | `reload map` | reload settings, reload config | перезагрузить настройки | [settings-reload-map](../05-configuration/settings-reload-map.md) |
| Server node | `node` | server node | серверный узел | [community-faq](../07-administration/community-faq.md) |
| Shard | `Shard` | shard server | шард, сервер шарда | [community-faq](../07-administration/community-faq.md) |
| Starter pack | `starter_pack.xml`, `StarterPackBase` | starter pack, starting ships, starter kit | стартовый набор, стартовые корабли | [tuning-recipes](../05-configuration/tuning-recipes.md) |

## Game modes

| Concept | Docs / file term | Players say (EN) | Players say (RU) | Source |
|---|---|---|---|---|
| Battle royale | `battle royale` | battle royale mode | королевская битва | [game-modes](../05-configuration/game-modes.md) |
| Beacon capture | `capture_the_base`, `Beacon capture` | capture beacons, beacon capture | захват маяков | [game-modes](../05-configuration/game-modes.md) |
| Beacon control | `control` | beacon control | контроль маяков | [game-modes](../05-configuration/game-modes.md) |
| Brawls | `BRAWL` | brawl, brawls | потасовка, потасовки | [game-modes](../05-configuration/game-modes.md) |
| Combat recon | `sentinel` | combat recon | разведка боем | [game-modes](../05-configuration/game-modes.md) |
| Coop ai | `coopQueueTemplate` | co-op vs AI, coop, co op | кооператив, против ИИ | [matchmaking-guide](../05-configuration/matchmaking-guide.md) |
| Detonation | `Bomb the base` | detonation, bomb mode | детонация, детонацию, подрыв | [community-faq](../07-administration/community-faq.md) |
| Football | `football` | space football | космобол | [game-modes](../05-configuration/game-modes.md) |
| Free space | `free space` | free flight | свободный космос | [game-modes](../05-configuration/game-modes.md) |
| Last man standing | `last man standing` | last survivor | последний выживший | [game-modes](../05-configuration/game-modes.md) |
| Open space | `open space` | open world, os | открытый космос, открытом космосе, ОК | [community-faq](../07-administration/community-faq.md) |
| Pve missions | `PvE mission` | pve, missions | ПвЕ, миссии | [game-modes](../05-configuration/game-modes.md) |
| Pvp arena | `PVP` | pvp, arena | ПвП, арена | [game-modes](../05-configuration/game-modes.md) |
| Team battle | `TDM` | team battle, team deathmatch | командный бой | [game-modes](../05-configuration/game-modes.md) |
| Transport escort | `transport escort` | escort mission | сопровождение транспорта | [game-modes](../05-configuration/game-modes.md) |

## Ships

| Concept | Docs / file term | Players say (EN) | Players say (RU) | Source |
|---|---|---|---|---|
| Alien hull | `alien hulls` | alien ship, alien ships | инопланетный корабль, инопланетные корабли | [community-faq](../07-administration/community-faq.md) |
| Battle slots | `BattleSlotPrice` | battle slot cost, extra ship slot | цена боевого слота | [xml-schemas](../05-configuration/xml-schemas.md) |
| Biomorph | `biomorph` | biomorphs | биоморф, биоморфы | [community-faq](../07-administration/community-faq.md) |
| Command fighter role modules | `command2017.lua` | command fighter | командный штурмовик | [module-defs](../05-configuration/module-defs.md) |
| Destroyer | `destroyer` | destroyers, dessie | эсминец, эсминцы | [community-faq](../07-administration/community-faq.md) |
| Ecm role modules | `ecm2017.lua` | ecm, ecm interceptor | РЭБ | [module-defs](../05-configuration/module-defs.md) |
| Fighter | `fighter` | fighters | штурмовик, штурмовики | [xml-schemas](../05-configuration/xml-schemas.md) |
| Frigate | `frigate` | frigates | фрегат, фрегаты | [pirate-destroyers](../05-configuration/pirate-destroyers.md) |
| Guard frigate role modules | `guard2017.lua` | guard frigate | фрегат прикрытия | [module-defs](../05-configuration/module-defs.md) |
| Interceptor | `interceptor` | interceptors, intie | перехватчик, перехватчики | [ship-defs](../05-configuration/ship-defs.md) |
| Recon role modules | `recon2017.lua` | recon, recon interceptor | разведчик | [module-defs](../05-configuration/module-defs.md) |
| Ship energy | `energy` | capacitor, ship energy | энергия, конденсатор | [community-faq](../07-administration/community-faq.md) |
| Ship hull | `hull` | hull strength, ship health | корпус, прочность корпуса | [community-faq](../07-administration/community-faq.md) |
| Ship rank | `rank` | ship rank, ship ranks | ранг корабля, ранги кораблей | [ship-defs](../05-configuration/ship-defs.md) |
| Ship shield | `shield` | shields, shield strength | щит, щиты | [community-faq](../07-administration/community-faq.md) |
| Ship slots | `slot_bones` | module slots, weapon slots | слоты модулей | [community-faq](../07-administration/community-faq.md) |
| Ship speed | `speed` | ship speed, max speed | скорость корабля | [community-faq](../07-administration/community-faq.md) |
| Ship tier | `ship_tier` | tier, tiers | тир, тиры | [ship-defs](../05-configuration/ship-defs.md) |
| Tackler role modules | `tackler2017.lua` | tackler | заградитель | [module-defs](../05-configuration/module-defs.md) |

## Items and equipment

| Concept | Docs / file term | Players say (EN) | Players say (RU) | Source |
|---|---|---|---|---|
| Ammunition | `munition` | ammo, ammunition | боеприпасы, патроны | [ship-defs](../05-configuration/ship-defs.md) |
| Blueprints | `blueprints` | blueprint, bp | чертёж, чертежи | [community-faq](../07-administration/community-faq.md) |
| Crafting | `craft_ingredients` | craft, crafting recipe | крафт, рецепт крафта | [community-faq](../07-administration/community-faq.md) |
| Implants | `implants` | implant, pilot implant | имплант, импланты | [source-register](../sources/source-register.md) |
| Inventory expansion | `InventoryExtensions` | inventory expansion, warehouse space | расширение склада | [xml-schemas](../05-configuration/xml-schemas.md) |
| Loot crates | `LootCrate` | loot crate, loot crates, loot box | контейнер, контейнеры | [config-system](../05-configuration/config-system.md) |
| Module grade | `mark` | mk, module mark | мк, уровень модуля | [module-defs](../05-configuration/module-defs.md) |
| Modules | `modules` | module, ship module | модуль, модули | [community-faq](../07-administration/community-faq.md) |
| Resources | `resources` | resource, materials | ресурсы, материалы | [community-faq](../07-administration/community-faq.md) |
| Seed chips | `autogen modules` | seed chip, seed chips | сид-чип, сид-чипы, сид чипы | [community-faq](../07-administration/community-faq.md) |
| Weapons | `weapon` | weapons, ship gun | оружие, пушка | [community-faq](../07-administration/community-faq.md) |

## Currencies

| Concept | Docs / file term | Players say (EN) | Players say (RU) | Source |
|---|---|---|---|---|
| Credits | `credits` | credit, silver credits | кредиты, кредитов | [community-faq](../07-administration/community-faq.md) |
| Free synergy | `accountExpPool` | free synergy, account synergy | свободная синергия | [community-faq](../07-administration/community-faq.md) |
| Galactic standards | `goldCredits` | GS, galactic standards, gold credits | ГС, галактические стандарты | [community-faq](../07-administration/community-faq.md), [schema](../06-database/schema.md) |
| Iridium | `tokenCredits` | iridium, tokens | иридиум, иридиума | [community-faq](../07-administration/community-faq.md), [schema](../06-database/schema.md) |
| Iridium daily cap | `sv_tokenCreditsDailyLimit` | daily iridium cap, iridium limit | лимит иридиума | [community-faq](../07-administration/community-faq.md) |
| Karma reset | `KarmaResetCost` | reset karma, karma price | сброс кармы | [community-faq](../07-administration/community-faq.md) |
| Premium | `premiumTill` | premium time, premium account | премиум, премиум аккаунт | [community-faq](../07-administration/community-faq.md) |
| Premium prices | `PremiumTimePrices` | premium price, premium cost | цена премиума | [xml-schemas](../05-configuration/xml-schemas.md) |
| Repair cost | `repair_cost` | repair bill, repair price | стоимость ремонта | [community-faq](../07-administration/community-faq.md) |
| Ship price | `premiumPrice` | premium ship price | цена премиум корабля | [ship-defs](../05-configuration/ship-defs.md) |
| Ship synergy | `synergy` | ship xp, ship experience | синергия, опыт корабля | [community-faq](../07-administration/community-faq.md) |

## Organisation (corporations, squads)

| Concept | Docs / file term | Players say (EN) | Players say (RU) | Source |
|---|---|---|---|---|
| Clan | `clan` | corp, corporation | корпа, корпорация, корпорации | [community-faq](../07-administration/community-faq.md) |
| Clan creation cost | `ClanRegistrationCost` | corp price, corp cost, create corp, make a corporation | цена корпы, создать корпорацию, стоимость корпорации | [community-faq](../07-administration/community-faq.md), `cloud/data/special_values.xml` |
| Clan rank | `ClanHighRank` | corp rank, clan rank requirement | ранг корпорации | [community-faq](../07-administration/community-faq.md) |
| Clan rename cost | `ClanChangeNameCost` | rename corp, clan rename cost | переименовать корпорацию | [xml-schemas](../05-configuration/xml-schemas.md) |
| Clan ship | `clan ship` | dreadnought, corp ship | дредноут, корабль корпорации | [cvar-defaults](../05-configuration/cvar-defaults.md) |
| Clan tag cost | `ClanChangeTagCost` | change corp tag | сменить тег корпорации | [xml-schemas](../05-configuration/xml-schemas.md) |
| Sector conquest | `sector conquest` | sector war, conquest | завоевание секторов, битва за сектор | [source-register](../sources/source-register.md) |

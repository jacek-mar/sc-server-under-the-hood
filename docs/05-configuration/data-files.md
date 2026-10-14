# Server data files (`cloud/data/*.xml`, `*.lua`, `*.gbin`)

> Status: **Stage 1 — first-pass catalogue** from reading file heads.
> Full schemas are a Stage 2 task. All XML here is **generated** from Lua
> definitions by `prepare_shared.bat`; edit the Lua source and regenerate
> unless noted.

| File | Root / structure | What it controls | Notes |
|------|------------------|------------------|-------|
| `store.xml` (15 MB) | `<Items><Item id price basePrice premiumPrice tokenPrice eventPrice tradePremiumPrice type requiredRank race requiredAccountAura …/>` | Complete store/item catalogue; prices in 5 currencies | `id` = *storeItemId* used by DB and loot tables |
| `store_rules.xml` | `<Rules><Rule type="def" defName newDefName credits silent …/>` | Item rewrite/migration rules (e.g. SpyDrone T1 → T2) | |
| `defmod_rules.xml`, `defmod_rules_new.xml` | rule list | Def modification rules; **both inert** (commented template / export output, no executable reads them); the live rule file is `store_rules.xml` - see [store-zones-rules-semantics](store-zones-rules-semantics.md) | `_new` is 162 KB |
| `autogen.xml`, `autogen_special_values.xml` | defs + `AutogenElementsNum=118` | Procedurally generated item defs | |
| `atlas_special_values.xml` | `AtlasVersion=1`, `AtlasElementsNum=1205` | UI atlas version/size sync | |
| `special_values.xml` | scalar elements | `GoldExchangeRate 400`, salvage factors, buyback modifiers, `MailTrading tax 0.1`, `NickNameChangeCost 3000`, `FactionChangeCostPerRank 30000`, credit packs… | **Economy knobs**, edit directly |
| `aux_limits.xml` | `ReputationRank` (18 thresholds), caps | `VesselExpPoolCap 5 000 000`, `CreditsCap 400 000 000`, `TokensCap 10 000`, `EventCreditsCap 300`, ship level XP table | Caps for editing DB values safely; **generated** by `prepare_shared` from `shared/reputation.lua` and other shared Lua (see [pipeline](../08-reverse-engineering/config-pipeline-and-limiters.md)) |
| `offers.xml` | `<Offers><Group><Offer offerId priority cooldown bundle/aura><Condition param compare value/>` | In-game promo offers; enabled via `cvars.sv_offerEnable` | |
| `battle_pass.xml` | `<battle_pass><stage><reward gold bundle cost/>` | Battle-pass reward ladder | Time windows from Lua (`battlePassStart`) |
| `loot_tables.xml` | `<LootTable defName><entry storeItemId dropChance/>` | Drop tables | Only 3 PvE tables (`PVE_T1_PassiveSet`, `PVE_T2_ActiveSet`, `PVE_T4_ActiveSet`); the `SetLootRules` names (`RareT1…`, `CommonRanks_*`) resolve against the Lua `LootTable` set, not this file (corrected 2026-10-12) |
| `quests.xml` (286 KB), `ship_quests.xml`, `clan_quests.xml` | `<QuestGroups><QuestGroup id cooldownInHours…><quest id/>` | Quest groups & cooldowns | clan quests empty |
| `skills.xml` | `<Talents><TalentGroup requiredShipRank talent0..2/>` | Pilot talent tree | |
| `achievements.xml`, `medals.xml`, `titles.xml`, `stickers.xml`, `account_auras.xml` | id lists | Meta-progression content | titles include "Developer", "Tester"… |
| `slot_machines.xml` | `<Machine name currency currency_amount><Combination><Reward type>` | Gamble machines (e.g. `SimpleSilver`) | |
| `zones.xml` (44 KB) | `<SpaceZones StartZoneForRace0..4 ClanShipZoneForRace…><Zone id name levelName minAccountRank maxPlayers universeType stellarSystem …><Reward …/>` | Open-world zone table | Start zones per faction |
| `universe.xml` | `conflictDurationTime=50 civilianZoneCost=1000 civilianZoneDuration=43200 moveCoefFar/Close` + `NewYearStages` (days 0,7,11,13,17,22,27) | Universe war timings | |
| `war.xml` | `warClanReviveCost=10000 warBaseReward=10000` | Clan war | |
| `karma.xml` | levels 1000/15000/50000/150000/500000 | Karma tiers | |
| `faction_rep.xml` | default rep `0,0,0,0,-50000`, max 50000 | Faction reputation defaults | 5th faction hostile |
| `tournaments.xml` | `enable=1 roundsNum=3 …`; two schedules (`d=0 h=17`, `d=6 h=16`), ranks 7–9, `BotsT3E` presets; round rewards ×0/0.5/1/2; finish gold 0/150/250/400 | Tournament calendar and rewards | Day/hour in server time |
| `starter_pack.xml` | `credits=0 goldCredits=0 tokenCredits=0`, vessel `Ship_Race1_M_T1` in battle slot | New-account grant | Combine with `gold_on_start` cvar |
| `regions.xml` | `RU`, `EU`, `US`, `AS` country lists | GeoIP country → matchmaking region | Used with `geo.gbin` |
| `geo.gbin` (379 KB) | binary | GeoIP DB (inferred) | format unknown |
| `league_equipment_lists.xml` | lists | League (competitive) allowed/forbidden equipment | |
| `clan_emblems.xml`, `clan_ship.xml` | | Clan emblems; clan dreadnought build data | |
| `vessel_custom_elements.xml` (1.4 MB), `…_rules.xml`, `vessel_presets.xml` | | Ship cosmetics, rules and prebuilt presets | |
| `bot_preset_exclusion_lists.xml` | `<ExclusionDefs><Def name/>` | Defs bots may not use | Mirrors `botPresetForbiddenDefs` |
| `cloud.xml` | see [config-system](config-system.md) | Topology | Hand-edited, not generated |
| `stat_server_cfg.xml` | `<Provider alias addr><Stream name/>` | StatServer metric providers on ports 4000–4008 | |
| `default_platform_config.lua` | Lua | Master policy | see [config-system](config-system.md) |
| `sstring.flog` | binary/log | string-table log (unknown) | |
| `chat/stop-list.txt`, `chat/white-list.txt` | word lists | Chat filter | |

## Lua sources consumed by the server (in `data/gamedata`)

`gamedata/shared/*.lua` (80 files) holds the tables that become XML:
`def_ids.lua`, `loot_tables.lua`, `quests*.lua`, `battle_pass.lua`,
`clan_*.lua`, `login_rewards.lua`, `module_presets.lua`,
`module_upgrade_chain.lua`, `league_equipment_lists.lua`, `account_rank.lua`,
`karma.lua`, `faction_rep.lua`, `adventures.lua`, `adventure_stages.lua`,
`green_nodes_price.lua`, `lobby_settings.lua`, `pve_missions/`, …
`gamedata/def/*.lua` (169 files): ship/module/effect/AI definitions,
`gameplaysettings.lua`, `designers_constants.lua`, `client_lua_rpc_allowlist.lua`.

**Who reads which file (static, 2026-10-13):** the per-file table is
generated in [gamedata-readers.md](gamedata-readers.md)
Summary:

* Only the client (`game.exe`) and the battle server (`DedicatedServer.exe`,
  also the `prepare_shared` tool) load `data/gamedata` directly;
  `ScriptsServer.exe` reads `shared/zones.lua` and `designers_constants.lua`
  and `AdventureServer.exe` reads `shared/adventures.lua` through their pak
  scripts. **The other 19 service executables never touch `data/gamedata`** -
  they get game data from the `cloud/data` XML files, which is why a Lua edit
  needs `prepare_shared` before the Shard, MatchMaker etc. see it.
* `def/`, `spell/` and `shared/` (255 files) are definition trees read by
  client and battle server (*inferred*); 188 of them also feed a generated
  XML. Their definition *names* are part of the battle server's entity-defs
  check ([hub-protocol-and-framing](../08-reverse-engineering/hub-protocol-and-framing.md) §6a).
* Client-presentation files (tooltips, `ui_properties2.lua`, slides, `eula.lua`,
  `role_descriptions.lua`, `shop_info.lua`) are used only by the client;
  server-only edits there have no effect, client-only edits are harmless to
  the server.
* 27 files have no static evidence (mostly the 22 `cam_ship_*.cfg` camera
  presets, plus `automats.lua`, `developer.lua`, `test_balance.lua`,
  `materials/samples.lua`, `materials/material_list.mel`).
* The generated-XML pairing is *observed* since the `prepare_shared` run in
  [verification-log V-11](../04-installation/verification-log.md).

## Search roots (`datasources*.txt`) *(file, 2026-10-13)*

The engine opens game files through a virtual file system whose roots are
listed in plain-text `datasources*.txt` files next to the executables; the
`.pak` archives in `data/` are mounted into the same tree, so a path such as
`gamedata/def/ex/ship.lua` or `platform_config.cfg` is looked up in every
root (and pak) in turn.

| File | Roots (relative to the executable) |
|---|---|
| `win64/datasources.txt` (client) | `..\data`, `..\sys_data` |
| `cloud/datasources.txt`, `cloud/datasources_cloud.txt` | `.\data`, `..\data`, `..\sys_data`, `..\local_data` |
| `cloud/datasources_defs_build.txt` | used by `prepare_shared` (`-ds` switch) |

`sys_data/` (41 files) is a **second data root**: `sys_data/gamedata/def/`
holds base definitions (`base_defs.lua`, `logic.lua`, `joints.lua`,
`filters.lua`, `sounds.lua`), plus `properties.lua`, physics and material
tables. Definitions there are referenced from `data/gamedata` (for example
logic entities such as `Logic_JumpDockLocation`), so tools that index
definitions must read both roots. `local_data/` does not exist in the
shipped install (an optional override root for the cloud services,
*inferred*).

## Adding a ship (community guide, S11 O12) *(community, ⚠ not tested by us)*

A community guide (dated "checked in game, October 2026") describes a new
ship as a chain; a missing link crashes the client or shows a black hull.
Server-relevant links, with the reported symptom when one is missing:

| File | What | Reported symptom if missing |
|---|---|---|
| `data/gamedata/def/ex/ship.lua` | definition: model, `storeItemId`, `base_preset`, tree icon and position (`treeIco`, `ui_tree_x`, `ui_tree_y`; a unique ship uses `race = ai.Race.SPECIAL`) | no ship / in the atlas but not in the tree |
| `data/gamedata/def/ex/prices_ship.lua` | shop price, `is_atlas_entity = true` (a `premiumPrice` inside `ship.lua` is not the shop price) | not in the atlas |
| `data/gamedata/def/ex/ship_preset.lua` | client preset `Ship_Preset_...` | empty modules |
| `data/gamedata/shared/module_presets.lua` | `ModulePresets.<base_preset>`, name byte-for-byte equal to `base_preset` | `prepare_shared`: "has no ShipPreset" |
| `data/gamedata/shared/vessel_tree.lua` | `VesselTree.<def> = {}` with `ods_export = true` | warning "not in the VesselTree" |
| `cloud/data/vessel_presets.xml` | server preset (generated) | no loadout in hangar/battle |
| `data/strings/<language>/string.txt` | name and description | raw key shown |
| `data/ui/textures/common/ship_icons_230x150.txt` (+ `ship_icon.txt`, `ship_icon_small.txt`) | icon aliases pointing at DDS files; the tree icon is stored as DXT5 232x152 because 230x150 is not divisible by 4 | no icon |

Then run `prepare_shared` (MongoDB running) and **cold-start** the client.
The guide also covers the model package (4 meshes, DXT5 texture pairs,
skeleton bone positions, convex collision) and a community asset toolkit
that reads but does not write game assets; those details stay in the source
(S11, link only). Two claims are open questions: loose files under `data/`
override the pak, so no repacking is needed (**Q56**), and `storeItemId` must
be a free id (**Q58**: the store export skips a definition whose
`storeItemId` another definition already exported and logs
`storeItemId %d (def '%s') is already exported to the store!`). A hand-made
DB grant takes its vessel id from the `vid` counter
([mongodb §3a](../06-database/mongodb.md), Q57). Every added definition also
changes the battle server's entity-defs hash, so stock clients are locked
out ([hub-protocol-and-framing §6a](../08-reverse-engineering/hub-protocol-and-framing.md)).

## Definition display names (B-8) *(file, 2026-10-13)*

There is **no automatic rule that turns a definition name into a display
name**. A definition is shown with a localised name only when it (or a
parent reached through `inherit`) does one of the following, resolved against
the client's `strings/<language>/string.txt`:

* carries an explicit **`uiName`** (and usually `uiDesc`) field pointing at a
  string key — the normal case for store items (for example
  `item_<defname>_name`); or
* happens to match a key by name: **`<defname>_name`**, **`item_<defname>_name`**
  or a bare **`<defname>`** key.

Measured over the shipped `data/gamedata` definitions (23 866 `Def.*`):

| Name source | Definitions |
|---|---:|
| own `uiName` field (key present) | ~1 955 |
| own `uiName` field (key **missing** in english) | ~167 |
| own `<defname>_name` / bare `<defname>` key | ~1 930 |
| name **inherited** from a parent definition | ~1 550 |
| **no display name at all** | ~16 960 |

So only about **6 500 of 23 866** definitions resolve to a player-visible
name; the remaining ~71 % are internal mechanics components that are never
shown directly — passive sub-modules, projectiles, blast waves, effects, and
the per-mark engine/capacitor grade modules generated by
`def/objects/modules_engine.lua` (families `ModulePassive`, `Projectile`,
`BlastWave`, `Effects`, `ModuleEngine`, `ModuleCapacitor`, `Constructor`,
`SpaceMissile` are almost entirely nameless). They are referenced by the
visible ships and modules that own them.

**Operator consequence.** To give a new item a visible name, set its
`uiName`/`uiDesc` to new keys **and** add those keys to the string table of
**every** client (`strings/<language>/string.txt` inside `data/strings.pak`,
or the loose `strings/` folder — see "Search roots"). A missing key shows the
raw key text. Name strings are a **client** resource: the server does not
supply them (consistent with [gamedata-readers](gamedata-readers.md)). Counts
of the string tables themselves are in
[locale-catalogue](locale-catalogue.md).

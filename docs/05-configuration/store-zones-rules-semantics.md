# Store, zones and rule files - semantics

> Companion to the generated [xml-schemas.md](xml-schemas.md) (structure) and
> [quests-semantics.md](quests-semantics.md) (quests). This page explains what
> the attributes *mean*. Counts come from throw-away scripts run on the shipped
> build 1.99.0.167293 (2026-10-11); enum names/numbers are from the lifted
> `ai/cosmos_constants` (names and numbers only). Evidence tags as in the
> [source register](../sources/source-register.md): *(file)*, *(inferred)*, ⚠.

## 1. Which XML files are generated and which are hand-maintained

`DedicatedServer.exe -prepareSharedData` (`prepare_shared.bat`) is implemented in
`PrepareSharedData.cpp`; the binary contains `DumpStoreXML`, `DumpTournamentsXML`
and `CreateAtlasIdsLuaFile` *(file: strings)*. The executable also names these
XML files, which are therefore the plausible generator outputs *(inferred)*:
`store.xml`, `quests.xml`, `zones.xml`, `ship_quests.xml`, `vessel_presets.xml`,
`battle_pass.xml`, `achievements.xml`, `titles.xml`, `account_auras.xml`,
`autogen.xml`, `special_values.xml` (+ `tournaments.xml`).

* A string says that prepare "ran on client which can't connect to db. atlasIds
  won't be updated", i.e. **prepare talks to MongoDB** (atlas ids are persisted
  there). This matches the community advice to start Mongo before running the
  prepare scripts *(file + community)*.
* `store_rules.xml` is read by the cloud services (it appears in the strings of
  Shard, ClanServer, QuestServer, ...), **not** produced by DedicatedServer.
* `defmod_rules.xml` and `defmod_rules_new.xml` are **not referenced by any
  shipped executable** (no `defmod_rules` string in any of the 22 exes) *(file)*.

## 2. `store.xml` (15 MB, generated)

Top-level sections and the `type` of the matching `<Item>` row:

| `Items/Item@type` | Section | Entries | `cantBeBought=1` | Example |
|---:|---|---:|---:|---|
| 0 | `Vessels` (ships) | 659 | 5 | `Ship_Helicon_L_SNIPER_Rank10` |
| 1 | `Modules` | 9 738 | 9 347 | `AG_Base_Balanced` (chips/autogen) |
| 2 | `Munition` (`Ammo`) | 1 015 | 0 | `DestrMunition_AnomalyBot_T5_Mk3` |
| 3 | `Drugs` (consumable auras) | 15 | 0 | `Drug_ExpBoost15` |
| 4 | `Bundles` | 806 | 539 | `Bundle_9_may_2021` |
| 5 | resources/components | 328 | 328 | `AlienCompositeAlloy` |
| 6 | `Blueprints` | 1 018 | 424 | `BP_AchillesTargetingUnit_T5_Craft` |
| 7 | `Avatars` | 349 | 290 | `Avatar_067` |
| 8 | `Mottos` | 349 | 274 | `Taunt_1` |
| 9 | `Junks` | 155 | 155 | `Armor_parts` |

(The type-to-section mapping is *(inferred)* from identical counts; 14 432 items
in total, **12 269 carry `cantBeBought="1"`**. Of those, 11 766 have a non-zero
credits/gold price, so `store_allowAllItemsForBying = 1` would make a large
part of the catalogue purchasable - effect still ⚠ untested.)

### `Item` attributes

| Attribute | Meaning | Notes |
|---|---|---|
| `id` | numeric item id (used in the DB and in module lists on ships) | |
| `defName` | def name (key into the Lua defs) | |
| `price` / `basePrice` | price in **credits** | 11 797 items > 0; `base*` equals the current value everywhere (base = before sale rules) |
| `premiumPrice` / `basePremiumPrice` | price in **gold** (premium currency) *(inferred)* | 7 613 items > 0 |
| `tokenPrice` / `baseTokenPrice` | price in tokens | 1 270 items |
| `eventPrice` / `baseEventPrice` | price in event credits | only bundles (234), matches `BundleContent.EVENT_CREDITS` |
| `tradePremiumPrice` / `baseTradePremiumPrice` | gold price in the trade/exchange path ⚠ | 1 029 items |
| `requiredRank` | required account rank | 0 on every item (rank gating lives on vessels/modules) |
| `race` | 0 Empire, 1 Federation, 2 Jericho, 3 Crystal, 4 Special, 5 none/any (13 773 items) | `ai.Race` |
| `requiredAccountAura` | account aura that must be active to buy (battle-pass/donor sets) | 220 items |
| `cantBeBought` | not offered in the store | see above |
| `stacks` | stackable in inventory | 1 030 |
| `deleteFromInventory` | item is removed from inventory on a rule/expiry | 24 |
| `localizedName` | name key, often a category word (`chip`) | |

### `Vessel` attributes

`shipClass` is the `ai.ShipClass` bit (1 small, 2 medium, 4 large, 8 huge:
203 / 187 / 213 / 56 ships); `tier` 1-5; `rank` = ship rank (1-17); `role` is
`ai.ShipRoles` (1 ECM, 2 SCOUT, 3 RECON, 4 ATTACK, 5 COMMAND, 6 TACKLER,
7 SNIPER, 8 GUARD, 9 ENGINEER, 10 OVERSEER); `slotsMask` / `defaultSlotMask`
bit masks over `ai.SpaceShipModuleSlot` (up to 32 slots); `repairCost`;
`preset` default module preset (`vessel_presets.xml`); `nextShip` +
`evolutionCost` form the **evolution chain** (112 ships with a successor);
`defaultNodes` pre-unlocked progression nodes; `isPremium` (204),
`craftable` with `recraftCredits/Gold`, `maxCraftSlots`,
`defaultCraftSlotsMask` (70 craftable); `dependsOn`/`dependsOnLvl` prerequisite
ship; `resourceRequired`/`resourceCount` + `Ingr` list = resources needed to
obtain; `Progress/*` = progression nodes (`nodeId`, `evolution` %, `slot`,
`requiredRank`, `group`); `NodePrices/NodePrice` = cost per node count
(`credits`, `tokenCredits`, `exp`, `Resources/*@amount`); `SpecialGrade`,
`specialModuleVariant` (alternative special modules with `cost`).

### `Module` attributes

`type` = `ai.ModuleType` (0 weapon, 4 active, 6 engine mod, 8 capacitor mod,
10 shield mod, 12 armor mod, 14 CPU mod, 15 special, 16 autogen/chip);
`tier`, `mark` (0 base, higher = better mark), `itemSubtype`, `classMask`
(`ai.ShipClass` bits) and `raceMask` (255 = all), `rank_min`/`rank_max`
usable ship rank range, `enchantingPrice`, `cantBeEquipped` (861, shown but not
equippable - typically intermediate marks), `curUpgradeLevel` (1-3 = module
level), `uniqueEquip` (172: counted by `store_maxUniqueModules*`), `tagsMask`
(`ai.ModuleTagsMask`).

### Bundles, blueprints, other sections

* `Bundle/Content@type` is `ai.BundleContent`: 1 ITEM, 2 VESSEL, 3 EXP,
  4 EVENT_CREDITS, 5 ACCOUNT_AURA, 6 INVENTORY_EXT, 7 CRAFT_RESOURCE,
  8 BLUEPRINT, 9 VESSEL_BUDGET, 10 CUSTOM_ELEMENT, 11 TITLE, 12 AVATAR,
  13 MOTTO, 14 AUTOGEN, 15 PREMIUM (counts in the shipped file: 929 custom
  elements, 823 craft resources, 523 items, 194 avatars ...). `priceWeight`
  splits the bundle price among contents; `isRewardable` marks bundles usable
  as rewards.
* `Blueprint@craftResult` is produced from `Ingr` rows: `currency` 0 = item
  `def` x `count`, 1 = credits (empty `def`), 3 = a further currency without a
  def (18 rows, ⚠ unknown; probably gold/tokens).
* `Drug@accountAura` names the account aura applied when used.
* `Resources` lists stack sizes of craft resources; `Prestige` holds
  `vsslAmount` / `premVsslAmount` (217 / 94, number of ships counted for
  prestige) ⚠.

## 3. `zones.xml` (open-world / universe zones)

Root `SpaceZones` carries start zones per race (`StartZoneForRace0..4` =
1, 2, 3, 231, 0) and clan-ship zones (`ClanShipZoneForRace0..2` = 17, 26, 36).
130 `Zone` rows:

| Attribute | Meaning |
|---|---|
| `id`, `name`, `levelName` | zone id, internal name, level scene (see [level-catalogue](level-catalogue.md)) |
| `minAccountRank`, `maxPlayers` | entry rank and instance capacity (16 / 24 / 64) |
| `station`, `stationRace`, `clanShipRace`, `civilianZone` | hub/station zones (4 stations), clan ship zones, civilian (no PvP) zones (109) |
| `universeType` | 1 or 2 (69 zones; `UT_ARENA`/`UT_BFS` in the master-server enum - numbering not confirmed) |
| `stellarSystem`, `dbgPosX/Y` | system id and map position (debug coordinates) |
| `raceDefault` | faction owning the zone at start (0 Empire, 1 Federation, 2 Jericho) |
| `factorPressure` | pressure multiplier (1.0-3.0) of the zone conflict |
| `tier` | 3-5, loot/difficulty tier |
| `universeMinShipRank`, `universeMaxShipRank` | ship rank window for entry |
| `conflictIntervalStart` / `conflictIntervalLong` | epoch ms start and period (86 400 000 = 1 day, 604 800 000 = 1 week) of the sector conflict cycle |
| `allowedJump`, `onlyForWing` | jump gate / wing-only restrictions |
| `Link@id` | graph edge to another zone (218 links; home worlds have 5) |
| `Reward@type/value/def` | reward of holding/clearing the zone: `type=6` = item `def` x `value` (resources such as `Iridium_monocrystall`, `AlienCompositeAlloy`, `Aliens_ship_part`), `type=3`/`1` = amounts without def (⚠ meaning; `RewardType` names are in [masterserver-enums](../08-reverse-engineering/masterserver-enums.md)) |

Dynamic ownership/conflict runtime state is not in this file; see
[zone-events](zone-events.md) and [open-world-and-services](open-world-and-services.md).

## 4. Rule files

| File | Status | Semantics |
|---|---|---|
| `store_rules.xml` | **live** (read by cloud services); 1 477 rules, 77 families | `type="def"` rewrite rule: players' inventory entries `defName` are replaced by `newDefName` (1 476 rules, e.g. Spy Drone T1 -> T2, Shield Vampire T1 -> T3); `silent="1"` = no notification. One rule (`BP_FakeBlueprint`) uses `credits="1"` = pay out credits instead of a replacement |
| `defmod_rules.xml` | **inert** (everything inside XML comments; no executable references it) | Contains only the rule *template* (author's Russian comment, translated): `<Rule type="def" defName="[source def]" goldCredits="[give gold]" credits="[give credits]" newDefName="[replace by def]" silent="[do it quietly]"/>`, plus commented historical examples (swap ship defs, compensate `credits="10000"` for weapons); one note says blueprints moved from resources to blueprints and the checker fails without the replacement |
| `defmod_rules_new.xml` | **inert, not XML** | export script output ("generated by Targem Export script from export_subtypes.ods"), Lua-style `--` header, rows terminated with `>` instead of `/>`, 1 431 rules of the same shape as `store_rules.xml` (T1 -> T2/T3 module migrations). Never read by a service, which explains its parse error (Q21) |

Operational meaning: a rule file migrates *existing* inventories when a def
is removed or renamed. A custom server that deletes or replaces defs should add
rules here (store_rules) instead of leaving dangling ids in player documents
*(inferred, untested)*.

## 5. Related generated references

* Quest semantics: [quests-semantics.md](quests-semantics.md).
* Structure of every XML file: [xml-schemas.md](xml-schemas.md).
* Which cvars change store behaviour: [tuning-recipes.md](tuning-recipes.md)
  (`store_allowAllItemsForBying`, `store_maxUniqueModules*`).

# Item names - how the game resolves a display name

How the client turns an internal definition name (`defName`, e.g.
`ModulePassive_AccelerationCoil_T1_Mk1`) into the name a player sees, and
how variants are told apart. Useful when you grant items in the database,
read a log, or build a tool that shows readable names.

Evidence: key names and short values are *(file)* from the client string
tables in `data/strings.pak` (`strings/english/string.txt`,
`strings/russian/string.txt`, Hub 1.99.0.167293) and from the definitions
under `data/gamedata/`. Counts per rule come from the maintainers' item
registry *(observed, 2026-10-19)*; they cover the 14 973 definitions that can
be on an account. No name tables are reproduced here.

## 1. Where the name text comes from

The string tables hold one `"key"<TAB>"text"` pair per line. An item's name
is found under one of these keys, in roughly this order:

| Source | Key | Share of account items | Example key |
|---|---|---:|---|
| the item's own key | `<defName>` or `<defName>_name` | ≈10 % | `Ship_Race1_S_T4_Glass` |
| a key named by a field of the definition | value of `uiName`, `ship_name` or `default_icon` | <1 % own, more through inheritance | `item_TreasureMap_name` |
| a **type prefix** + `defName` (ship paints, decals, stickers) | `sticker_<name>`, `shipChild_<name>`, `shipPreset_<name>` | ≈12 % | `sticker_Jericho_dream` |
| the **category** of the item (`item_subtype` field) | `itemSubType_<Subtype>` | **≈56 %** | `itemSubType_AccelerationCoil` |
| a pattern filled with another item's name | e.g. `blueprintNamePattern` | ≈18 % | see §3 |
| none found | - | ≈3 % (388 definitions) | mostly bundles, boosters, test items |

* **Most modules, weapons and munitions only have a category name.** Every
  acceleration coil, whatever its tier or mark, is named from
  `itemSubType_AccelerationCoil` (2 145 `itemSubType_` keys in the English
  table). The game tells the variants apart by tier, mark and rank range
  (§2), not by the name.
* **The prefix follows the custom-element type** *(file)*: elements of type
  `ai.VesselCustomElementType.STICKER` (`shared/vessel_stickers.lua`) use
  `sticker_`, `CHILD` uses `shipChild_`, `MPRESET`
  (`shared/vessel_mpresets.lua`) uses `shipPreset_`. The English table has
  1 113 `sticker_`, 204 `shipChild_` and 413 `shipPreset_` keys.
* **Rank variants of the progression ships** (Ellydium, Tester's Agony, …)
  take the name of their base definition through `ship_name`, e.g.
  `Ship_Race5_S_SCOUT_Rank9_7` uses `Ship_Race5_S_SCOUT_Rank5`.

## 2. Telling variants apart: tier, mark, rank

The client builds the variant label from separate keys *(file)*:

| Part | Keys | Text (EN / RU) |
|---|---|---|
| tier | `tier_1` … `tier_5` | `I` … `V` (both languages) |
| mark | `mark_<n>` | see the mark table below |
| rank range | `itemTooltip_rankRange` | `For ranks:` / `Для рангов:` + the definition's `rank_min`-`rank_max` |
| ship rank | `shipTooltip_rank` | `Rank $rank$` / `Ранг $rank$` |

The tier and mark values come from the definition's own `tier` and `mark`
fields (e.g. `def/ex/passive.lua:11609-11610`), and the rank range from
`rank_min` / `rank_max`. The mark number in the field is an **enum**, not a
"Mk" number *(file: definitions and string tables)*:

| `mark` field | Typical name suffix | Key | Text (EN and RU) |
|---:|---|---|---|
| 1 | `_Mk1` | `mark_1` | `Mk.1` |
| 2 | `_Mk2` | `mark_2` | `Mk.2` |
| 3 | `_Mk3` | `mark_3` | `Mk.3` |
| 4 | `_Prem` | `mark_4` | **`Premium`** |
| 5 | `_Rel` | `mark_5` | **`Mk.5`** |
| 6 | `_Rare` | `mark_6` | **`Mk.2`** - the same text as mark 2 |
| 7 | `_Epic` | `mark_7` | **`Mk.4`** |

Example: `ModulePassive_AccelerationCoil_T1_Epic` has `mark = 7`, so the game
shows it as Mk.4; the `_Rare` variant (`mark = 6`) reads Mk.2 like the real
`_Mk2`, so a tool listing both needs an extra tie-breaker. Variants such as
`_RT` and `_ET` have no `mark` field. Caveat: some families (missiles) inherit
`mark = 1` for every variant; for them the `Mk<n>` in the definition name is
the reliable mark, not the field.

The client's own wiki-export scripts (inside `scripts.pak`) group modules
the same way: by `item_subtype`, with marks and tier as separate columns.

## 3. Names built from another item

* **Blueprints** (`BP_…`, `is_blueprint = true`, `craft_result = <item>`) are
  named with `blueprintNamePattern` = `Blueprint '$craft_result_name$'` /
  `Чертеж «$craft_result_name$»`, filled with the name of the item they
  produce. The English table also has 930 `BP_…` keys of their own; an own
  key takes priority over the pattern.
* **Variants without a category of their own** (module suffixes `_RT`, `_ET`,
  marked `cant_be_equipped = true`) take the name of their `_Mk1` sibling of
  the same stem and tier *(observed rule, unverified in the engine)*.

## 4. Practical notes

* **Look items up by `defName`, never by `storeItemId`** - the id is not
  unique ([Q58](../08-reverse-engineering/open-questions.md)).
* Player ships: 655 definitions in this build - the 301 in `def/ex/ship.lua`
  plus 354 progression ships and rank variants in `def/ex/ship_green.lua`
  that carry `fake = true` ([ship-defs](ship-defs.md) §5) *(observed)*.
* Descriptions follow the same pattern with suffixes `_desc`,
  `_short_desc` and `_desc_lore`; category descriptions
  (`itemSubType_<Subtype>_desc`) contain value placeholders such as
  `$projectile_speed_mul$%` that the client fills from the definition.
* A raw key or an empty name in game usually means the definition has no
  matching key: check §1 in order before assuming a broken file.

Related: [locale-catalogue](locale-catalogue.md) (key counts per language),
[ship-defs](ship-defs.md), [module-defs](module-defs.md),
[data-files](data-files.md).

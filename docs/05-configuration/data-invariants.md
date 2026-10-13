# Data invariants and dangling references

> For hosts and modders who edit `data/gamedata` Lua or `cloud/data` XML.
> Part 1 lists rules that edits must not break - most "my server broke after
> an edit" reports come down to one of them. Part 2 lists references in the
> **shipped** data (build 1.99.0.167293) that point at definitions nobody
> defines, so that you can tell inherited defects from your own.

## 1. Invariants

| # | Rule | Why | Evidence |
|---|------|-----|----------|
| I-1 | **Adding, renaming or removing a definition requires the same files on every client.** Value-only edits of existing definitions do not. | The battle server compares a hash over the definition *names* (entities, spells, auras) with each client's and refuses a different client with `DR_BAD_GAMEDATA_VERSION`; the check cannot be switched off by configuration. Stock hash: `71367FCA` | *(static)* [hub-protocol-and-framing §6a](../08-reverse-engineering/hub-protocol-and-framing.md); *(observed)* hash in the `prepare_shared` log, [verification-log V-11](../04-installation/verification-log.md) |
| I-2 | **Never rename or remove a definition that players may own** (ships, modules, items, account auras, custom elements). Disable it (`cant_be_bought`, remove it from bundles/rewards) instead. | Account documents store definition names: `vessels[].defName`, `items[].defName`, `auras[].defName`, `vessels[].customElements[].defName`. A renamed definition leaves those entries pointing at nothing | *(observed)* field names in [schema](../06-database/schema.md); effect on a running account *(inferred)*, untested |
| I-3 | **Do not insert or remove definitions in the positional store-id families** (`Bundles_*`, `Avatars_*`, `Mottos_*`, `Drugs_*`); append new ones at the end of their file. | These definitions get their store id from a load-order counter (`_GetNextStoreItemId()`: bundles from 210000, avatars from 130000, ...). Inserting or removing one shifts the id of every later item; `store.xml` and the client's cached store (`store_cache.dat`) refer to items by id | *(static)* [config-validation-tools §2a](../07-administration/config-validation-tools.md) (`tools/data_drift_check.py` checks the order); effect on existing inventories *(inferred)*, untested |
| I-4 | **Never remove an autogen (seed-chip) class.** Change its values instead. | Modules already rolled from a class become invalid and can no longer be re-rolled (comment in `data/gamedata/shared/autogen.lua`, translated from Russian); affix edits only affect new rolls | *(file)* [community-faq](../07-administration/community-faq.md) "seed-chip class" |
| I-5 | **Keep module definition names stable across `prepare_shared` runs on the same database.** | `prepare_shared` keeps an atlas-id table and an autogen-id table in MongoDB keyed by definition name; a new or renamed module gets the next counter value. A fresh database rebuilds the tables (whether the ids then match an older database is untested) | *(observed)* V-11; [config-pipeline-and-limiters §1a](../08-reverse-engineering/config-pipeline-and-limiters.md) |
| I-6 | **Edit the Lua source, then regenerate; never hand-edit the 29 generated XML files.** | `prepare_shared` rewrites them from Lua (byte-identical on stock data); hand edits are lost on the next run, and a stale XML silently keeps old values | *(observed)* V-11; `tools/data_drift_check.py` flags stale and hand-edited files |
| I-7 | **Every name a reference points to must exist** - loot tables in the loot rules, modules in `default_modules`, spells, projectiles, bundles in account auras and quest rewards, `inherit` parents. | Unresolved references fail silently at run time: the shipped loot rules name eight loot tables that do not exist, which empties the arena reward search | *(file)* Q45, part 2 below; [open-questions](../08-reverse-engineering/open-questions.md) |
| I-8 | **Server-only edits of shared definitions change battles, not the hangar.** | The battle server decides stats in battle; the hangar shows the client's own file values | *(observed)* V-10 (hull 10 -> HUD 11) |
| I-9 | **Never renumber, reorder, comment out or delete titles; add new ones at the end.** | Titles are referenced by numeric id (achievement ranks, mail, accounts) | *(file)* comment in `data/gamedata/shared/titles.lua`, translated; [progression-xml-semantics](progression-xml-semantics.md) §1 |
| I-10 | **Never change an `offerId` once players have seen it.** | Accounts remember offers by id | *(file)* comment in `data/gamedata/shared/login_rewards.lua`, translated; §3 there |
| I-11 | **One custom element (sticker, paint, decor) per achievement reward.** | With several, only the last one is granted | *(file)* comment in `data/gamedata/shared/sc_achievements.lua`, translated; §2 there |

Before restarting after an edit: run `tools/data_drift_check.py` (I-3, I-6),
`tools/ref_lint.py --reference <untouched copy>` (I-7), `tools/queue_lint.py`
and `tools/defname_check.py` for queue and name typos
([config-validation-tools](../07-administration/config-validation-tools.md)),
and compare your definition names with the list your players have (I-1).

## 2. Dangling references in the shipped data

`tools/ref_lint.py` on the shipped build *(file, 2026-10-13)* indexed about 70 000 defined
names (every `<Registry>.<name> =` table in `data/gamedata` and
`sys_data/gamedata` - the second data root that holds base definitions - `Def`,
`Spell`, `LootTable`, `AccountAura`, `DefItemPrice`, `ModulePresets`, ... -
the item names in `store.xml`, and identifiers compiled into the battle
server and client, which covers engine built-ins such as `TriggerHurt`) and
checked about 80 reference keys whose values name a definition. 184
key/name pairs resolve to nothing. Impact is *(inferred)* unless stated;
none of these blocks a node from starting.

| Area | Unresolved names (file) | Likely effect |
|------|-------------------------|---------------|
| **Loot rules** (`lt`) | `CommonRanks_1_3`, `_4_6`, `_7_8`, `_9_10`, `_11_12`, `_13_15`, `NeodiumDrop`, `LezortiumDrop` (`cloud/data/default_platform_config.lua` lines 1318-1332) | **Observed:** empty arena reward search; fix = point the rules at the `_v3` tables (Q45, V-10) |
| Store rules | 104 names of module tiers that no longer exist (96 rows in `cloud/data/store_rules.xml`, the live rule file) (`Module_ShelterField_*`, `Module_ExternalCooler_T1/T2_*`, `Weapon_SuppressingFire_*`, `Module_HackSystems_*`, `Module_FakeShips_*`, `Module_GuidedDronRL_*`, `Ship_Race*` placeholders, `BP_FakeBlueprint`); the same names recur in the export files `defmod_rules*.xml` | Rule rows for items that cannot exist; no effect expected |
| Quest rewards | `Bundle_RoP2025HintMeter_1..4` (`shared/quests.lua` ~2943-3020, `reward_account_aura`) | Reward of those quests not granted; the quests are marked `disabled` |
| Account-aura discounts | `Bundle_GreenScoutAbility_1..4_T5`, `Bundle_GreenEngineerCabine_T3`, `Bundle_Parts_T3_Reaper_Unique` (`shared/account_auras.lua`, `discounted_def`) | Discount aura with nothing to discount |
| Clan-war rewards | custom elements `rank_1` .. `rank_7` (`shared/war.lua`, `RT_CUSTOM_ELEMENT`) | Reward element not granted |
| Module spells | `EcmHack`, `Spell_SpyBeaconAnalyse`, `EnlargeActiveCooldown0`, `AdaptiveBigShieldBoost_T1_Mk1` (`spell`), `DivineSave_`, `Spell_CinquedeaBlackout2` (`additional_spell`), `HoloSpy_End` (`deactivate_spell`) in `def/objects/modules.lua`; seven `target_spell`/`spell_on_*` names in `spell/spell.lua` and `def/objects/modules_special.lua` | Spell effect missing when the module/spell fires (most rows belong to old or unused modules) |
| Munitions and blast waves | `WeaponMod_{Laser,Plasma,Rail}Up1_Basic_T` (`def/designersdefs.lua`), `SpaceMissile_DoomDay_T3_Mk3` (three open-world police presets, `def/ex/ow_preset.lua`), `Blastwave_RocketMine`, `BlastWave_Missile_test`, `xBlastWave_SM_Standart_Raid_M_Spam` | Missing ammunition/explosion for those AI or test rows |
| Child parts and wrecks | `Pirate_Barge_Engine`, `Turret_Pirate_Barge_JerTurret`, `Turret_Pirate_Barge_Rocket`, `Pirate_Barge_Wreck*` (`def/objects/cargoship.lua`), `Destroyer_Life_Small_Wreck01..17` (`def/objects/misc.lua`), `Menu_model_hangar_sfincter_Ship` | Missing turrets/debris on a pirate barge and a boss wreck |
| Other single names | `Projectile_Return_5`, `Effects_Nebula_SlowSpeed3000`, `BigEvade` (AI behaviour), `Drug_ExpBoost10wide`, `xSpaceMissile_ThermalDamageZone_Raid_Pve_t3` | Local effect in the owning object |

**Limits of the scan.** Names built at run time (loops, string
concatenation) are only seen when they appear in `store.xml`, so a few
reported names may exist at run time. Keys that hold textures, models, UI
strings or engine class names (`tex`, `model`, `hangarIco`, `uiName`,
`class`, ...) are not checked. Disabled entries are reported like active ones.

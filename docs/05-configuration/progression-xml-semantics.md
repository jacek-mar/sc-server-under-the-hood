# Titles, achievements, offers, account auras, vessel presets, seed chips

> Semantic notes for six generated `cloud/data` files that the other
> reference documents do not cover. Element/attribute structure:
> [xml-schemas](xml-schemas.md). Counts are from the shipped build
> 1.99.0.167293 *(file, 2026-10-13)*. All six are rewritten by
> `prepare_shared` from their Lua source - edit the Lua, then regenerate
> ([config-pipeline-and-limiters](../08-reverse-engineering/config-pipeline-and-limiters.md)).
> Russian source comments quoted here are our translations.

| XML (`cloud/data`) | Lua source (`data/gamedata`) | Content |
|---|---|---|
| `titles.xml` | `shared/titles.lua` | 343 player titles |
| `achievements.xml` | `shared/sc_achievements.lua` | 250 achievements |
| `offers.xml` | `shared/login_rewards.lua` (`Offers`) | 3 offer groups, 17 offers |
| `account_auras.xml` | `shared/account_auras.lua` | 397 account auras |
| `vessel_presets.xml` | `def/ex/ship.lua` + `shared/module_presets.lua` | 361 ship loadouts |
| `autogen.xml` | `shared/autogen.lua` | seed-chip (autogen) classes, affixes, pricing |

## 1. Titles (`titles.xml`)

`<Title id name durationInHours>`; `durationInHours="0"` = permanent (338 of
343). A title is referenced by its **numeric id** - achievement ranks
(`rewardTitle`), the `LAT_TITLE` mail attachment (`tid`) and the account.

**Rule (comment at the top of `titles.lua`):** "Do not change the numbers or
the order of titles, and do not comment out or delete them. New titles may
only be added at the end." The same comment says "127 is the limit for now";
the shipped file has 343 titles, so that limit is outdated.

## 2. Achievements (`achievements.xml`)

`<Achievement id valueType>` with `numericalParam` conditions and one or
more `<rank value points gold [rewardTitle]>` steps. `id` comes from the
`ai.AchievementId` enum.

| Lua field | Meaning (from the source comments) |
|---|---|
| `value_type` (`valueType`) | `CUMULATIVE` = 1: progress advances every time the action happens; `HIGHEST` = 2: advances only when the previous record is beaten; `LIST` = 3: advances when one of up to 32 listed actions happens |
| `gameplays` | game modes in which the achievement can be earned (values from `ai.GameplayMask` in `constants.lua`); without it, every mode except training/tutorial counts |
| `coop_vs_ai = false` | cannot be earned in the "vs AI" mode |
| `numerical_conditions` | `comparison` (`ai.Comparison`) + `value` per counted parameter |
| ranks | `points`, `gold` (Galactic Standards) and optional title per step |

**Rule:** a reward may carry **only one custom element** (sticker, paint,
colouring or decor); with several, only the last one is granted (repeated
"IMPORTANT" comment in `sc_achievements.lua`).

## 3. Offers (`offers.xml`)

`<Group groupId>` -> `<Offer offerId priority cooldown bundle|aura>` with
`<Condition param compare value>`. Group 1 is the **daily login reward**
(`Bundle_DailyChest_T1` on days 1-3; a T5 secret chest on later days);
groups 2-3 are targeted shop offers that grant a discount aura (for example a
starter pack at rank 5, booster packs at rank 8, split by
`UID_DIVISIBLE_BY_TWO` for A/B testing). `cooldown` is in days *(inferred
from the values 0/5/9999)*.

`param` values (`MasterServer.OfferConditionParam`, see
[masterserver-enums](../08-reverse-engineering/masterserver-enums.md)):
0 `CREDITS`, 1 `GOLD_CREDITS`, 2 `TOKEN_CREDITS`, 3 `EVENT_CREDITS`,
4 `COUNT_GOLD_PAYMENT`, 5 `TOTAL_BOUGHT_GOLD`, 6 `LAST_BOUGHT_GOLD`,
7 `LAST_GOLD_PAYMENT_DAYS`, 8 `FIRST_LOGIN_DAYS`, 9 `LAST_LOGIN_DAYS`,
10 `COUNT_LOGIN_DAYS`, 11 `DAILY_LOGIN_LEVEL` (0..4), 12
`UID_DIVISIBLE_BY_TWO`, 13 `PLAYER_RANK`.

**Rule (comment in `login_rewards.lua`):** "offerId must not be changed after
it has been deployed to live" - accounts remember offers by id.

## 4. Account auras (`account_auras.xml`)

Timed account-wide effects: discounts, boosters, event and DLC bonuses.
`<AccountAura defName category [durationInHours] [isResetBundleContent]
[strParam]>` with optional `<NumericalParams ...>` (multipliers such as
`gold_credits_mul="-0.500"` = 50 % discount) and `<AltDiscountDef defName>`
(the bundle the discount applies to). 374 of 397 auras use `category="0"`
(`NONE`). Auras are granted by bundles, quests (`reward_account_aura`),
offers (`aura`), the `LAT_ACCOUNT_AURA` mail attachment and DLC crediting;
accounts store them in `auras[].defName`
([schema](../06-database/schema.md)). Six discount auras point at bundles
that do not exist ([data-invariants](data-invariants.md) part 2).

## 5. Vessel presets (`vessel_presets.xml`)

`<Preset name>` = a complete loadout: `<Module slot def>` (4 080 rows; `slot`
= `ai.SpaceShipModuleSlot`) and `<Munition ...>` (721 rows). Presets are the
`ModulePresets` tables of `shared/module_presets.lua`, referenced by ships
through `base_preset` and `testdrive_preset` (`def/ex/ship.lua`); they give a
ship its modules when it is granted or test-driven *(inferred from the key
names)*. `shared/vessel_mpresets.lua` is a different thing: **material**
(paint) presets, whose names come directly from colour and material names,
not from `VesselCustomElements` (source comment).

## 6. Seed chips (`autogen.xml`)

`<Autogen>` holds the global coefficients and `<ClassDesc>` the four classes
`COMMON`, `BALANCED`, `SPECIAL`, `DOUBLE`, each with the affix groups it
rolls (`<Affix affixGroupId minModuleRank>`), plus spells and level
modifiers. Pricing formula (source comment, translated):

```
cost = base + ( (affix_sum * (1 + average_roll) * (1 + (average_rank / rank_coef) * base_coef))^2 / divide_coef ) * upgrade_coef
```

`average_roll` = mean roll, `average_rank` = mean affix rank, `affix_sum` =
sum of the affixes' `cost_coef`. Shipped coefficients: `rank_coef` 15,
`upgrade_coefs` 1/2/3/10 per upgrade level, `upgradeModPerLevel` 0.2 (each
rolled value grows 20 % per upgrade level), experience-price coefficients
0 / 0.3 / 0.05, dismantle-for-credits 500 000 / 150 / 0.5, dismantle-for-gold
10 / 1.5 / 0.5, `donate_coef` 0.2 (experience a chip gives as donor =
0.2 x its own upgrade cost), `sellCreditsPrice` 1.

**Rule (source comment):** classes must not be removed from this list,
otherwise already-rolled modules become invalid and cannot be re-rolled.
`autogen_special_values.xml` holds two values: `AuogenVersion` 0 (sic) and
`AutogenElementsNum` 118 (a version/element counter written with the
autogen id table, *inferred*).

## 7. Rules in one place

The "never renumber / never remove" rules above are collected with the other
data invariants in [data-invariants](data-invariants.md) (I-4, I-9, I-10,
I-11).

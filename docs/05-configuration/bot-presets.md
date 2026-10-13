# Bot presets - how bot ships and skill are chosen (static analysis)

> Answers the static part of **Q28** (why rank 1-3 bots appear in high-rank
> queues). Sources: `data/gamedata/shared/ai_settings.lua`,
> `data/gamedata/preparedvessels.lua`, `data/gamedata/def/ex/ship_preset*.lua`,
> `data/gamedata/def/ex/bot_preset.lua`, queue templates in
> `cloud/data/default_platform_config.lua`, strings of `DedicatedServer.exe`,
> hull tiers/ranks from `cloud/data/store.xml` (2026-10-11, build 1.99.0.167293).
> The *runtime* fallback order inside DedicatedServer is **not** verified
> (needs the DS cvar dump / a battle) - those parts are tagged *(inferred)*.

## 1. The three layers

| Layer | File | What it defines |
|---|---|---|
| **Skill / behaviour preset** `AiPreset.<Name>` | `shared/ai_settings.lua` | aim dispersion per weapon type, reaction/attack delays, module-use chance, rocket use, evasion, aggro hold times, **and `ships = <PreparedVessels list>`** |
| **Ship lineup** `PreparedVessels*` | `gamedata/preparedvessels.lua` | lists of triples (S, M, L) of *ship presets* a bot may fly (72 lists) |
| **Ship presets** `Ship_Preset_R<race>_<class>_T<tier>[_Faction1/2/Premium]`, `Ship_PresetE_*`, `Ship_Bot*` | `def/ex/ship_preset.lua`, `ship_preset_e.lua`, `bot_preset.lua`, `pvebot_preset.lua`, `ow_bot_preset.lua` | modules fitted (`default_modules`), rocket munition, `ship_def` (the real ship), `ship4bot=true`, optional stat multipliers |

DedicatedServer logs `Applying AiPreset.%s for %s`, and fails with
`No ships defined in AiPreset.%s` when `ships` is missing *(file: strings)*.

## 2. Hull tier decides the bot's rank

Ship rank follows hull tier *(file-verified from `store.xml`)*:

| Tier | Ranks |
|---:|---|
| T1 | 1-3 |
| T2 | 4-6 |
| T3 | 7-9 |
| T4 | 10-16 |
| T5 | 13-17 |

The tier is part of every ship-preset name (`..._T1`, `..._T5`). A preset's
lineup therefore fixes the rank range of its bots; the queue's rank band does
not filter it by itself *(inferred)*.

## 3. Presets and the lineups they use

| `AiPreset` | `ships` list (tier) | `modules_can_use_percentage` | Used by (file-verified) |
|---|---|---:|---|
| `Default` | `PreparedVessels` = **nine T1 `Ship_PresetE_*` triples** | 0.01 | base preset; no queue names it |
| `Easy` / `Medium` / `Hard` / `Harder` | `PreparedVessels_PVE1` / `_PVE23` / `_PVE45` / `PreparedVesselsTX` | 0.5 | PvE difficulty presets |
| `BotsT1` / `BotsT1E` | `PreparedVesselsT1` / `PreparedVessels` (T1) | 0.33 / 0.5 | |
| `BotsT2`, `BotsT2E`, `BotsT2G` | `PreparedVesselsT2`, `T2`, `T2G` | 0.5 | |
| `BotsT3`, `BotsT3E`, `BotsT3G` | `T3`, `T2EE`, `T3G` | 0.5 / 0.6 / 0.6 | tournaments use `BotsT3E` |
| `BotsT4`, `T4E`, `T4EG`, `T4G` | `T4`, `T4E`, `T4EG`, `T4G` | 0.66 / 0.75 / 0.8 / 0.75 | |
| `BotsT5`, `T5E`, `T5G`, `T5X_H` | `T5`, `T5E`, `T5G`, `T5X_H` | 0.75 / 0.9 / 0.9 / 0.9 | |
| `BotsTX` | `PreparedVesselsTX` | 0.9 | dispersion 0, no delays (hardest) |
| `BotsOW` | `PreparedVesselsTX` | 0.5 | open world |
| `BotsLobby1/2/3` | `T1`, `T23`, `T5EXH` | 0.5 | custom-game lobby |
| `BotsBZS`, `BotsBZS_T3/T4/T5` | `T5E`, `T3EG`, `T4EG`, `T5EX` | 0.5 | sector/league queues (`botPresetByTier`) |
| `Easy_AID` ... `Harder_AID`, `Bot_Tornado`, `BotsPortal_T5` | AID/portal lineups | 0.5-0.7 | PvE mission scripts |

Generated families: `BotsT2..T5` x suffix `_E,_F,_J,_S,_M,_L,_H,_P,_R`
(race/role variants), `BotsT35_R`, `BotsT1_E..L` - created by a loop at the
end of `ai_settings.lua`. A preset can be referenced by any of these names in a
queue's `special.botPresetNames`.

Stat scaling lives in the ship presets: `Ship_PresetE_*` rows carry
`hull_health_mul = shield_max_mul = laser/plasma/railgun_damage_mul = 0.1`
(244 rows). The comment next to `AiPreset.BotsT1E` (which uses the same
`PreparedVessels` lineup as `Default`) says it is "now not an elite but a
*weakened* preset" (ticket #67356). The PvE `Ship_Bot*`
rows use negative multipliers (e.g. `hull_health_mul=-10`) *(file-verified)*.

## 4. Why a high-rank queue can show rank 1-3 bots *(inferred)*

1. A coop/PvP queue template that sets **no** `botPresetNames` /
   `botPresetByTier` and uses `botPresetType = bpt_none` (or omits it) leaves
   the choice to DedicatedServer's default - and `AiPreset.Default` carries the
   **weakened T1 lineup** (ranks 1-3, damage and hull x0.1).
2. `bpt_adaptive` / `bpt_mirror_and_save` build bots from ships saved from
   *real players* (Mongo `botPresets*`, `botPresetStats`; both empty on a
   fresh node - [schema.md](../06-database/schema.md)). The saving rules are
   cvars in the shipped config: `sv_numBestPlayerToSave = 2`,
   `sv_minEfficiencyVesselToSave = 1500`, `sv_numAdaptivePresetsInDB = 32`,
   `sv_numUniqueAdaptivePresets = 20`, `sv_rangeRankAdaptivePresets = 3`
   (ranks `max-3..max` of the queue). With an empty database the server logs
   `GetBotPresets(): bot preset empty` and has to fall back (fallback order
   unverified) - on a new community node this is the normal state.

Community corroboration *(community, anonymised; S12/S15 digests)*: on 9-10
Oct several operators independently reported that coop and PvP bots were
always rank 1-3 even with 4v4 setups and rank-15/17 queues, and one asked for
bots "within three ranks below the player's ship". The answer given in chat
(overlay author) was to set `botPresetType` to a non-`none` value **or** name
presets via `special.botPresetNames`, which is exactly what the structure
above predicts. No chat statement describes the engine's fallback order.

## 5. Recipe for believable bots on a small server *(untested)*

* Per queue: `special = { ..., botPresetNames = { "BotsT5" } }` (or the tier
  that matches the queue band; for mixed tiers use `botPresetByTier` as the
  sector queues do) and keep `botPresetType = bpt_none` so the named preset is
  not replaced by an empty adaptive pool.
* Community example (batch 005, H4; syntax verified against
  `InstantiateQueueTemplate`, effect unverified): one template instantiated
  once per rank band, each time passing the preset through the last
  (`addMods`) argument, which is merged into the template:

  ```lua
  table.insert( queuesConfigLo, InstantiateQueueTemplate( arcadeQueueTemplate,  1,  6, 1, 11, 0, 99, { special = { arcade = 1, botPresetNames = { "Medium"     } } } ) )
  table.insert( queuesConfigLo, InstantiateQueueTemplate( arcadeQueueTemplate,  7, 11, 1, 11, 0, 99, { special = { arcade = 1, botPresetNames = { "BotsBZS_T4" } } } ) )
  table.insert( queuesConfigLo, InstantiateQueueTemplate( arcadeQueueTemplate, 12, 17, 12, 17, 0, 99, { special = { arcade = 1, botPresetNames = { "BotsBZS_T5" } } } ) )
  ```

  The three names exist in `ai_settings.lua`. Pitfalls reported: a typo or an
  invalid queue makes the matchmaker ignore the whole block silently; a match
  that "never starts" was cured by cancelling and re-queueing, and
  `maxTimeInQueue = 1` gives instant matches. The *shipped* arcade template
  lists levels as `{4,9,11}`; the community example used `{9,11}` (see
  [queue-reference](queue-reference.md)).
* Raise `modules_can_use_percentage`/lower `dispersion` only in
  `AiPreset.*` copies you own (edits go to a data overlay; see
  [tuning-recipes](tuning-recipes.md)).
* `botPresetForbiddenDefs` in `default_platform_config.lua` (and
  `bot_preset_exclusion_lists.xml`) lists defs bots must not use.
* Check the effect with `mm_decisionLog = 1` and a battle; record the bot rank
  in [verification-log](../04-installation/verification-log.md).

## 6. What is still open (runtime)

* DedicatedServer's actual choice when the MatchMaker passes an **empty**
  `botPresetName` and the adaptive pool is empty. Static facts (2026-10-11,
  [config-pipeline-and-limiters §3](../08-reverse-engineering/config-pipeline-and-limiters.md)):
  `sv_botPresetType` default is `0` (NONE); the MatchMaker prefers
  `botPresetByTier` over `botPresetNames` and picks one name of a
  `botPresetNames` list **at random**. Only the DS fallback for the empty
  name needs a run.
* Whether editing `AiPreset.*` on the node affects remote clients (bot
  presets are in `data/gamedata`, i.e. also in the client install, Q36).

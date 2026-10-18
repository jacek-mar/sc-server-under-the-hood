# Queue reference (every matchmaker queue shipped)

> Status: **Stage 2, complete for the shipped file** (`default_platform_config.lua`,
> `ConfigureMatchmaker()`, lines ≈330–995). Companion to the
> [matchmaking guide](matchmaking-guide.md) (concepts and formulas).

## 1. Two queue sets

| Set | Variable | Registered with | Used when |
|-----|----------|-----------------|-----------|
| Low online | `queuesConfigLo` | `MatchMaker_ReconfigureQueues(queuesConfigLo, true)` | online players `< mm_lowOnlineLo` (250) until they reach `mm_lowOnlineHi` (300) |
| Normal online | `queuesConfig` | `MatchMaker_ReconfigureQueues(queuesConfig)` | otherwise |

> **Operator consequence.** A private or community server will practically
> always have far fewer than 250 players, so it runs on **`queuesConfigLo`**.
> That is the set to edit first; keep `queuesConfig` in sync only if you also
> change the thresholds.

### Differences between the sets

| Feature | `queuesConfigLo` | `queuesConfig` |
|---------|:---:|:---:|
| Training, PvE | ✔ | ✔ |
| Arcade PvP / Coop | 6 + 6 bands | 10 + 10 bands |
| **Brawl queues** (football, gtdm, atdm, sentinel, capture_the_base, hunger_games, one_against_all, zombie, close_distance, autogen_dm, three_teams_dm, april_control) | **✔ (12)** | ✘ none in the shipped file |
| Sector battle (`sectorQueue`, qid 501) | ✔ | ✔ |
| League (`leagueQueue`, qid 502) | ✔ | ✔ |
| Raid (`raidQueue`) | ✔ | ✔ |
| Arcade template `levelsDesc` | 5 maps × `{4,9,11}` (control, sentinel, bomb the base) | **only `s1338_devilsjaw = {9}`** (others commented out) |
| Arcade query ranks | `mmRank 1..17` in instantiations | `mmRank 1..15` |

### How the function builds the sets

*(file: S3, `ConfigureMatchmaker()` lines 330-995; counts from a full
static parse, checked by hand)*

* The two sets are filled by **51 `table.insert` calls**. **32** of them
  insert an `InstantiateQueueTemplate(...)` band; the rest insert fixed
  queues.
* Templates are function-local tables: `arcadeQueueTemplate` (line 391) and
  `coopQueueTemplate`. The name `coopQueueTemplate` is declared **twice**
  (lines 429 and 763). The first instance feeds the low set (first coop band
  at line 448). The second is a fresh `local` for the normal set, so editing
  one does not change the other.
* Registration happens exactly twice, at the end:
  `MatchMaker_ReconfigureQueues(queuesConfig)` (line 878) and
  `MatchMaker_ReconfigureQueues(queuesConfigLo, true)` (line 881). Nothing
  is inserted after line 881. Add new queues before the registration calls.
  *(inferred: an insert after them is probably ignored, unless the engine
  re-reads the table later; ⚠ unverified)*
* Line numbers refer to the reference build (Hub 1.99.0.167293). Community
  packs shift them, so search by name.

## 2. Training, PvE (both sets)

| Queue | min/opt/max | regionLocalized / maxTime | levels | query | special |
|-------|-------------|---------------------------|--------|-------|---------|
| Training | 1 / – / 10 | 30 / 45 | `s1338_pandora_dreadnwreck`, `s1338_pandora_anomaly`, `s1420_ceres3_northmsite` (no gameplay list) | `mmParams.practice = 1` | `gameMode = 5, botsCount = 0` |
| PvE | 1 / – / 1 | 10 / 10 | `{}` (chosen from `MatchMaker_SetPveSchedule`) | `mmParams.pve = 1` | `pve = 1, gameMode = 7` |

## 3. Arcade PvP and Coop vs AI

Templates (see guide §5). Bands are produced by
`InstantiateQueueTemplate(template, rMin, rMax, sqMin, sqMax, mmvMin, mmvMax[, mods])`:

| Set | Template | Instantiations (`mmValue` `[min, max)`) |
|-----|----------|------------------------------------------|
| Lo | arcade 24/4/1, expand 30 s | `0–20` (ranks 1–17, mods: `queueFlags.newbie`, `maxPlayers 16`), `19–24`, `24–31`, `31–39`, `39–51`, `51–99` (squad ranks 1–15) |
| Lo | coop 12/4/1 | `0–21` (mods: `newbie`, `coop_vs_ai`, `maxPlayers 8`), `19–24`, `24–31`, `31–39`, `39–51`, `51–99` (ranks 1–15) |
| Normal | arcade | `0–21` (newbie, `maxPlayers 16`), `20–24`, `23–28`, `26–31`, `30–35`, `33–38`, `37–42`, `40–45`, `44–51`, `51–99` (ranks 1–15) |
| Normal | coop | same ten bands (newbie `maxPlayers 8`) |

Map pools per band in the low set (from the commented `levelsDesc` lines, which
show the intended progression: harder/larger maps at higher MMV):

| `mmValue` band | Maps → gameplay ids (as written in comments) |
|---------------|-----------------------------------------------|
| 19–24 | devilsjaw `4,9,10`; aliendestsatation `4,10`; thar_gasgiant `4,9`; ceres3_northmsite `4,9,10` |
| 24–31 | ceres3_asteroidcity `4,9,10,11`; northmsite `4,11`; barrierdebris `4,9,11`; threshold `4,9,10`; livestation `4,10` |
| 31–39 | pandora_anomaly `3,4,9,11`; dreadnwreck `3,9,10,11`; asteroidcity `4,10`; northmsite `3,9,11`; lavastone `4,10` |
| 39–51 | pandora_anomaly `3,4,10`; dreadnwreck `3,4,9,11`; aliendestsatation `3`; aliendebris13 `3,4,9,10`; threshold `3,4,9` |
| 51–99 | devilsjaw `3,4,9`; aliendestsatation `3,4,9,10`; gasgiant `3,4`; northmsite `9`; lavastone `3,10,11`; threshold `3,11` |

*(analyst note)* These comment lines are **not active**: the live template
uses the single list `{4,9,11}` on five maps for every band. They document the
retired per-band rotation and are a ready recipe for restoring it by setting
`levelsDesc` on each instantiated queue via the `addMods` argument.

## 4. Brawl queues (low-online set only)

All: `regionLocalizedTimeInQueue 10`, `maxTimeInQueue 10`, `maxExpandTime 0`.

| Queue (`query` flag) | Map | Gameplay id | min/opt/max | `special` |
|----------------------|-----|:-:|-------------|-----------|
| football | `football` | 21 | 2/6/6 | `brawl = 1` |
| gtdm | `da_prototype` | 13 | 2/2/2 | `brawl = 1` |
| atdm | `paper_airplanes` | 26 | 2/8/8 (template) and 2/8/24 (second definition) | `brawl = 1` |
| sentinel | `s1420_ceres3_asteroidcity` | 9 | 4/8/24 | `brawl = 1` |
| capture_the_base | `s1338_devilsjaw` | 3 | 4/8/24 | `brawl = 1` |
| hunger_games | `s1338_hg_pandora_anomaly` | 24 | 2/6/24 | `hunger_games = 1` |
| one_against_all | `s1338_hg_pandora_anomaly` | 25 | 2/3/24 | `one_against_all = 1, botsCount = 7` |
| zombie | `da_deathstar` | 27 | 5/10/24 | `zombie = 1` |
| close_distance | `allidium_yard` | 28 | 2/8/24 | `close_distance = 1` |
| autogen_dm | `s1338_pandora_anomaly` | 29 | 2/6/24 | `hunger_games = 1` *(sic — reuses the hunger_games flag)* |
| three_teams_dm | `s1340_thar_alienruins` | 30 | 3/6/24 | `three_teams_dm = 1` |
| april_control | `paper_airplanes` | 31 | 2/8/8 | `brawl = 1` |

Which brawl is *open* at a given time is decided by the Shard's brawl schedule
(see [game modes §4](game-modes.md#4-brawl-schedule)), not by the queue
existing.

## 5. Universe / sector, league, raid (both sets)

| Queue | qid | maxPlayers | Notable `special` / `query` |
|-------|----:|-----------:|------------------------------|
| `sectorQueue` | 501 | 20 | `universe = 1, minSizeWing = 5, minSizeTeam = 4, withBots = true, botPresetType = bpt_none, botPresetByTier = {BotsBZS_T3×3, T4, T5}, queueFlags = {universe = 1, rank = 15}`; maps `dreadnoughtbattle_map_01…` gameplay 14 (clanship); query `mmParams.universe` + `universe_bfs`; `regionLocalizedTimeInQueue 1` |
| `leagueQueue` | 502 | 12 | `minSizeWing = 3, minSizeTeam = 1, withBots = false`; maps `s8256_thar_barrierdebris, s1338_devilsjaw, s1338_pandora_dreadnwreck, s1340_thar_aliendebris13, s1340_thar_gasgiant, s1420_ceres3_asteroidcity, s1338_pandora_anomaly, s8256_thar_concourse, s8256_thar_lavastone, desttown` gameplay 3; query `universe` + `universe_arena` |
| `raidQueue` | – | 12 (min 1, opt 12) | `special = { pve_raid = 1, gameMode = 7 }`, query `mmParams.pve_raid`; composition via `mm_raidSquadFilter` (the per-queue `squadFilter = 4` is commented out) |

Bot preset types (`bpt_*`): `0 none`, `1 mirror`, `2 adaptive`,
`3 mirror_and_save`. `botPresetByTier` lists preset names per tier
(`BotsBZS_T3/T4/T5`).

## 6. Reward-rate schedule and PvE rotation

* `MatchMaker_SetRewardRates(reward_mult)` — table keyed by weekday
  (`0` = Monday) of `{ hourBegin, hourEnd, rateExp, rateCred, goldReward }`
  windows. Shipped: all-ones rates, `goldReward = 50` Monday 02–05 h and
  `goldReward = 100` Sunday 10–13 h (server time).
* `MatchMaker_SetPveSchedule` — see [game modes §3](game-modes.md#3-maps-referenced-by-the-shipped-queues).

## 7. Editing checklist for a small server

1. Work in `queuesConfigLo` (see §1).
2. To make every band use the same easier rules, collapse bands (e.g. one
   instantiation `0–100`) — fewer players are then split across fewer queues.
3. For quick matches with bots: `minPlayers 1`, `optimalPlayers` low, coop
   template with `special.botsCount`.
4. Keep `levelsDesc` map names in sync with `data/levels` (names such as
   `s1338_devilsjaw` are level ids).
5. Restart the cloud after saving (MatchMaker reads the file at start).

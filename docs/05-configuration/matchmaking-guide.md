# Matchmaking guide

> Status: **English adaptation** of the official Russian document shipped as
> `star conflict/docs/matchmaking.md` (Gaijin/Targem), reorganised and
> annotated. Where this page adds something not in the original it is marked
> *(analyst note)*. Values shown are the shipped defaults.

## 1. Where it is configured

`cloud/data/default_platform_config.lua`:

* `cvars.*` inside `ConfigureShard()` (MMV maths, squad rules) and
  `ConfigureMatchmaker()` (thresholds, defaults, logging).
* `queuesConfig` (normal/high online) and `queuesConfigLo` (low online) tables
  inside `ConfigureMatchmaker()`, registered with
  `MatchMaker_ReconfigureQueues(queuesConfig)` and
  `MatchMaker_ReconfigureQueues(queuesConfigLo, true)`.

The matchmaker first decides which queue a player/group fits (via the queue's
`query`), then tries to assemble a battle by that queue's rules.

## 2. Concepts

| Term | Meaning |
|------|---------|
| **MMV** (`mmValue`) | Internal balance weight of a player/group. Higher = stronger. Queues usually filter on `mmValue`. |
| **mmRank** | Balance rank used to split players into queue groups; not always equal to the visible rank of one ship. |
| **mmSquadRank** | Rank check *across the ships of a squad*; keeps squads with mismatched ranks out of a queue. |
| **queue `query`** | Mongo-style filter (`$gte`, `$lte`, `$gt`, `$lt`) over `mmParams.<mode>`, `mmRank`, `mmSquadRank`, `mmValue`. |
| **`queueFlags.newbie`** | Marks the resulting battle as a newbie battle (e.g. no respawn-time penalty). It does **not** select players — the `query` does. |
| **KPM** | Kills per match on the current ship rank. |
| **Efficiency** (`effMod3`) | Server-side aggregated performance rating per rank. |

Mode flags in `mmParams`: `arcade` (PvP), `pve`, `coop_vs_ai`, `practice`,
and brawl flags `football`, `gtdm`, `atdm`, `capture_the_base`, `hunger_games`,
`one_against_all`, `zombie`, `close_distance`, `autogen_dm`, `three_teams_dm`,
`april_control`.

## 3. MMV calculation

### Inputs

| Name | Source |
|------|--------|
| `numBattles` | PvP battles played |
| `losStreak` | current losing streak |
| `isSingleUidOnPC` | only one account seen on this PC fingerprint |
| `highestRank` → `idx = highestRank − 1` | player's highest ship rank |
| `battles[idx]`, `penalty[idx]`, `mmvMin[idx]`, `uniqFingerprintClamp[idx]` | lists `mm_mmvMdBattles`, `mm_mmvMdPenalty`, `mm_mmvMin`, `mm_mmvMdUniqFingerprintClamp` |
| `losStreakDecrease[]` | `mm_losStreakMMVDecrease` (regular battles only) |

### Formulas

```
mmvMod = (numBattles >= battles[idx]) ? penalty[idx] : 0
mmvMod -= losStreakDecrease[ clamp(losStreak-1, 0, len-1) ]       # if losStreak > 0
mmvMin = (numBattles >  battles[idx]) ? mmvMin[idx] : 0
mmvMax = (isSingleUidOnPC and numBattles < battles[idx]) ? uniqFingerprintClamp[idx] : +inf

kpmMmValue     = clamp((kpm     - mm_kpmMMVBase)       / mm_kpmMMVStep,       0, mm_kpmMMVCap)
effModMmValue  = clamp((effMod3 - mm_effRatingMMVMdBase)/ mm_effRatingMMVMdStep, 0, mm_effRatingMMVMdCap)
winLoseMmValue = clamp((max(win/lost,0) - mm_winLoseMMVBase)/mm_winLoseMMVStep, 0, mm_winLoseMMVCap)
                 # only if numBattles > mm_winLoseMMVMinBattles

skill   = max(kpmMmValue, effModMmValue, winLoseMmValue)
mmValue = clamp(skill + mmvMod, mmvMin, mmvMax)

# group
squadMMValue = max(member mmValue);  squadSkill = max(member skill)
# arcade only
mmValue = clamp(mmValue + squadPenalty(size), -mm_totalMMVMdCap, +mm_totalMMVMdCap)
# squadPenalty: size 2 -> mm_squad2MMVPenalty, 3 -> mm_squad3MMVPenalty, 4 -> mm_squad4MMVPenalty, else 0

skilled = single ? (skill >= mm_skilledPlayer) : (squadSkill >= mm_skilledSquad)
```

`skilled` influences join-in-progress into the losing team.

*(analyst note, verified 2026-10-11 via the SSH console)* The shipped file does
**not** set `mm_losStreakMMVDecrease`, `mm_squad{2,3,4}MMVPenalty`,
`mm_skilledPlayer` or `mm_skilledSquad`; their **engine defaults** are:
`mm_squad2/3/4MMVPenalty = 0`, `mm_skilledPlayer = mm_skilledSquad = 35`,
`mm_losStreakMMVDecrease = ""` (no decrease). Full list:
[engine-cvars.md](engine-cvars.md).

## 4. Global cvars (shipped values)

| CVar | Value | Meaning |
|------|------:|---------|
| `mm_lowOnlineLo` / `mm_lowOnlineHi` | 250 / 300 | Enter low-online mode below 250 players online, leave at ≥ 300 (hysteresis) |
| `mm_totalMMVMdCap` | 2 | Cap on total MMV modification (arcade) |
| `mm_effRatingMMVMdBase/Step/Cap` | 0 / 25 / 50 | Efficiency contribution |
| `mm_kpmMMVBase/Step/Cap` | 0 / 0.0325 / 50 | KPM contribution |
| `mm_winLoseMMVMinBattles/Base/Step/Cap` | 2000 / 0.75 / 0.012 / 50 | Win/lose contribution |
| `mm_mmvMdBattles` | `200×7,100,0×10` | Newbie-protection battle thresholds per rank (18 values) |
| `mm_mmvMdPenalty` | `30×18` | Modifier per rank |
| `mm_mmvMin` | `30×18` | Floor per rank |
| `mm_mmvMdUniqFingerprintClamp` | `30×7, 80×11` | Ceiling for single-PC new players |
| `squad_maxNonPremiumSize` | 12 | Squad size not needing premium |
| `squad_maxNonWingSize` / `squad_maxWingSize` | 4 / 12 | Regular squad max / wing max |
| `mm_squad1AsSquad` | 0 | Treat solo as squad of one |
| `mm_notArcadeSquadRankDiff` | 17 | Allowed rank spread in a squad (non-arcade) |
| `mm_sectorMinWingSize` / `mm_sectorMaxWingSize` | 5 / 8 | Universe/sector wing size |
| `mm_enablePveRaids` | 1 | PvE raids on |
| `mm_raidMinWingSize` | 10 | Min wing size for a raid queue |
| `mm_raidSquadFilter` | 0 | 0 any · 1 solo only · 2 solo+squads · 3 squads+wings · 4 wings only |
| `raid_lootAuraInterval` | 1 | Days between raid loot-aura grants |
| `mm_botsCount` | 6 | Default bots (0..31); queue `special.botsCount` overrides |
| `mm_defaultGameplay` | 3 | Default gameplay id (see [game modes](game-modes.md)) |
| `mm_timeInQueueAveragingCf` | 200 | Smoothing of average queue time (10 dev, >100 live) |
| `mm_decisionLog` | 0 | Bitmask: 1 PvP · 2 PvP JIP · 4 PvP candidates · 8 coop · 16 coop JIP · 32 PvE · 64 universe · 128 brawl · 256 brawl candidates · 512 hunger games · 1024 one against all · 2048 zombie · 4096 three teams · 8192 close distance · 16384 general (all = 32767) |
| `mm_decisionDbg` | 0 | 0 buffer into info log · 1 write each line immediately to debug log |

**Rule:** the MMV-list cvars must all have the same length (18 = number of
ranks).

## 5. Queue definition

> Every shipped queue is catalogued in [queue-reference.md](queue-reference.md).
> A small server runs on `queuesConfigLo` (low-online set) — edit that first.

```lua
{
  minPlayers = 1, optimalPlayers = 4, maxPlayers = 24,
  maxTimeInQueue = 10,              -- s before starting an incomplete-but-valid battle
  regionLocalizedTimeInQueue = 10,  -- s to keep region-local matching before widening
  maxExpandTime = 30,               -- s after creation during which players can be added (0 = never)
  maxSquadTimeInQueue = 0x7FFFFFFF, -- wait limit where mmSquadRank is checked
  levelsDesc = { s1338_devilsjaw = {4,9,11}, ... },  -- map -> allowed gameplay ids
  query   = { ["mmParams.arcade"]=1, mmRank={["$gte"]=1,["$lte"]=15},
              mmSquadRank={["$gte"]=1,["$lte"]=15}, mmValue={["$gte"]=0,["$lt"]=100} },
  special = { arcade = 1 },         -- passed to the created battle (mode, botsCount, queueFlags …)
}
```

`InstantiateQueueTemplate(template, minMMRank, maxMMRank, minMMSquadRank,
maxMMSquadRank, minMMValue, maxMMValue, addMods)` deep-copies a template,
rewrites the query ranges and merges `addMods`:

```lua
table.insert(queuesConfig,
  InstantiateQueueTemplate(arcadeQueueTemplate, 1,15, 1,15, 0,21,
    { special = { queueFlags = { newbie = 1 } }, maxPlayers = 16 }))
```

### Shipped PvP/coop ladders (`mmValue` bands, upper bound exclusive)

| Set | Bands (`mmValue`) | rank / squad rank |
|-----|-------------------|-------------------|
| `queuesConfigLo` arcade (6 queues) | 0–20 (newbie, `maxPlayers 16`), 19–24, 24–31, 31–39, 39–51, 51–99 | 1–17 / 1–15 |
| `queuesConfigLo` coop (6) | 0–21 (newbie, `maxPlayers 8`), 19–24, 24–31, 31–39, 39–51, 51–99 | 1–15 / 1–15 |
| `queuesConfig` arcade (10 queues) | 0–21 (newbie, `maxPlayers 16`), 20–24, 23–28, 26–31, 30–35, 33–38, 37–42, 40–45, 44–51, 51–99 | 1–15 / 1–15 |
| `queuesConfig` coop (10) | same ten bands (newbie `maxPlayers 8`) | 1–15 / 1–15 |

Normal-online bands are narrower and overlap by 1–3 points (smoothing);
check the overlap before adding bands. Each band also carries its own
`levelsDesc` (harder maps at higher MMV, see source comments).

### Template defaults

| Queue | max/optimal/min | regionLocalized / maxTime | Other |
|-------|-----------------|---------------------------|-------|
| Arcade PvP | 24 / 4 / 1 | 10 / 10 | `maxExpandTime 30` |
| Coop vs AI | 12 / 4 / 1 | 10 / 10 | |
| PvE | 1 / – / 1 | 10 / 10 | `special = { pve = 1, gameMode = 7 }` |
| Training | 10 / – / 1 | 30 / 45 | `gameMode 5`, `botsCount 0` |
| Brawl (generic) | per mode | 10 / 10 | `maxExpandTime 0`, `special = { brawl = 1 }` |

## 6. Tuning recipes

| Goal | Do |
|------|----|
| Faster matches | Lower `minPlayers`, `optimalPlayers`, `maxTimeInQueue`, `regionLocalizedTimeInQueue`; widen `mmValue`/`mmRank`/`mmSquadRank`; add wide queues to `queuesConfigLo` |
| Better balance | Opposite; raise effect of efficiency/KPM/win-lose (smaller `*Step`) |
| Protect newbies | Narrow the newbie `mmValue` band; smaller `maxPlayers`; raise `mm_mmvMdBattles`; lower `mm_mmvMdUniqFingerprintClamp`; don't make `maxTimeInQueue` tiny |
| Squads wait too long | Widen `mmSquadRank` & `mmValue`; check `maxSquadTimeInQueue`; relax `mm_notArcadeSquadRankDiff` |
| Region quality | Raise `regionLocalizedTimeInQueue` (training uses 30) |
| More bots | Queue `special.botsCount`; `maxPlayers` (see community notes) |

**Order of work:** diagnose → find the queue by `query` → change queue fields →
only then global MMV cvars → re-test neighbouring queues.

Checklist before saving: correct table (`queuesConfig` vs `queuesConfigLo`);
no gaps/over-wide overlaps in `mmValue`; equal list lengths; `levelsDesc`
matches the mode; `special` flag present; sane `minPlayers`/`maxPlayers`.

## 7. Community findings

| Topic | Finding (source: community wiki, unverified by project) |
|-------|----------------------------------------------------------|
| More bots in a coop queue | Add `botsCount = 9` to `special` and set `maxPlayers = 8` → "4 vs 4 with one player + 3 bots vs 4 bots". Templates exist **twice** (low-online and normal) — edit both. |
| `maxPlayers` in presets | Several preset configs use 128/128/128; keep `optimalPlayers` at 50–75 % of `maxPlayers`. |
| Mode selection | Edit `levelsDesc` values in `arcadeQueueTemplate` / `coopQueueTemplate`, e.g. `s1338_devilsjaw = {4,9,11}`. |
| Squad/wing "forever loading" in PvP arena, and squads missing in full-bot lobbies after edits | Unresolved. |

## 8. Why a squad (or a high-rank player) may find no queue - static analysis (2026-10-11)

Derived from the shipped `queuesConfigLo` (the set a small server uses, Q35).
Everything below is file-verified *configuration*; whether a given account
really falls outside the bands needs a runtime check.

| Queue family | Rank bands in the query | Squad specifics |
|---|---|---|
| Arcade / PvP arena (`mmParams.arcade`) | `mmRank` **1-17**, `mmSquadRank` **1-15**, `mmValue` 0-99 (six bands) | A squad is matched on `mmSquadRank`; a squad containing ranks above 15 matches **no** queue |
| Coop vs AI / "random mission" (`mmParams.coop_vs_ai`) | `mmRank` **1-15**, `mmValue` 0-99 | no `mmSquadRank` clause; any rank-16/17 participant fails `mmRank <= 15` |
| Sector / league / raid | see [queue-reference](queue-reference.md) | wing size cvars `mm_sectorMinWingSize/MaxWingSize` = 5/8, `mm_raidMinWingSize` = 10, `mm_raidSquadFilter` |

Checklist for "squad cannot start a PvP arena / random mission":

1. **Rank band:** accounts edited to own rank 16-17 hulls (T4/T5) exceed
   `mmSquadRank <= 15` (arcade) or `mmRank <= 15` (coop). Widen the bands in your
   `queuesConfigLo` instantiations (e.g. `InstantiateQueueTemplate(..., 1, 17, 1, 17, ...)`).
2. **mmValue band:** squad MMV = max member MMV plus the squad penalty,
   clamped; a DB-edited `mmValue`/skill outside 0-99 leaves every band.
3. **Squad size:** `squad_maxNonWingSize = 4`, `squad_maxWingSize = 12`; larger
   groups must be wings, and ordinary queues do not take wings
   (`mm_notArcadeSquadRankDiff = 17` only limits the rank spread).
4. **Premium gate:** `squad_maxNonPremiumSize = 12` (not a limit at the shipped
   value).
5. **Region/timeouts:** `maxSquadTimeInQueue` is effectively unlimited
   (`0x7FFFFFFF`), so a never-ending search is a missing match, not a timeout.
6. Enable `mm_decisionLog = 1` and read the MatchMaker log to see which
   queue rejected the squad.

The "forever loading" symptom after a squad is formed in a PvP arena stays a
runtime question: the queue can match while the battle start fails (Q30 /
DedicatedServer address handling).

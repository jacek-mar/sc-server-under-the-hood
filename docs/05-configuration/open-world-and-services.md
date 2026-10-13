# Open world, universe, quests, leaderboards — service-level configuration

> Status: **Stage 2.** Covers `ConfigureZoneInstance`, `ConfigureUniverse`,
> `ConfigureQuestServer`, `ConfigureLobbyServer`, `ConfigureLeaderboardServer`,
> `ConfigureScriptsServer`, `ConfigureTournament`, `ConfigureClanServer`
> of `default_platform_config.lua`. Per-cvar meanings:
> [cvar-reference](cvar-reference.md) (English column).

## 1. Open world (ZoneInstance + ZoneCoordinator)

*Open world (OW) / free space* zones are separate processes (ZoneInstance)
started by the ZoneCoordinator. Zones are defined in `cloud/data/zones.xml`
(ids, level names, min account rank, max players, universe type, rewards).
Level names end in `_ow` (e.g. `wreck_generic_rock_03_r_ow`).

| Topic | Key settings (shipped) |
|-------|------------------------|
| Instance lifetime | `sv_instanceLifeTime 720` s — an empty instance closes after 12 min |
| Server FPS | `cl_maxFps 18` (ZI and DS) — "restart cloud after changing these cvars" |
| Damage vs. mobs by rank difference | `sv_ranksDiff = -5,-2,0,2,5,10` with `sv_ranksDiffCoeff = -0.5,0.2,0.5,0.6,0.7,0.8,1` (7 coefficients for 6 breakpoints → 7 intervals); `dbg_logRankDiffScaling` |
| Faction relations | NPC damage accumulates per faction: enemy after `sv_enemyMinFactionNPCDamage 6`, capped by `…Max 100` and `…MaxPerSec 1`, decays `0.2`/s, hostile for `sv_factionBadRelationshipTime 45` s; friendly-faction damage ×`0.25` |
| Aggressor flag | after `sv_aggressorMinNPCDamage 3000`, timer max `30` s |
| Resurrection | `sv_resurrectionCreditsPrice 100000` credits |
| XP in Free Space | `sv_freeSpaceExpRewards 2` (all players), `sv_freeSpaceExpMastery` per-rank list 1.95…4.1, `sv_expForDamageFreeSpace 0` |
| Loot | `sv_randomLootDef` (random crate), `sv_pickedLootRateToClanResource 0.1` per picked loot → clan iridium, sent every 6 h |
| Station portal | `sv_spaceStationPortalTimer 3` |
| Iterative loot | `DedicatedServerServices_SetIterativeLoot{ [levelName] = { [n] = { lootCrate = "LootCrate_Loot_<id>_ranks_a_b", dropCounter = 1 } } }` — one crate per OW location, graded by ship ranks (≈ 45 locations, ranks 2–17) |
| Raid zone blocks | `zc_enableZoneBlocks 0` (ZoneCoordinator) |
| Event objects | respawn 60–420 s; `sv_eventObjectEndTime` (ISO time after which the object is no longer created; shipped value is in 2026-04) |
| AI | `ai_logSquads 5`, `ai_kiteDistance 5000`, `ai_convoyDefendRadius 300` |

The ZoneInstance shares the first-win multipliers (`x3fw = 3`) and
`sv_freeSynergyRewardCf*` with the DedicatedServer.

## 2. Universe (global war / sector conflicts)

Server: `Universe.exe`; data: `universe.xml`, `war.xml`, `zones.xml`.

| Setting | Shipped | Meaning |
|---------|--------:|---------|
| `universe_unid` | 2 | Universe id |
| `universe_factorOwnerInReward` | 0.4 | Owner's share of the zone reward |
| `universe_decayOwner` / `universe_decayRival` | 0.25 / 0.1 | Influence decay at conflict start |
| `universe_takeOwnerCoeffA/B` | 2 / 3 | Rival contribution = influence / (A·place + B), place from 0 → 1/3, 1/5, 1/7… |
| `universe_decayIdle` | 0.5 | Decay when a conflict brought no new influence |
| `universe_raceFactorStellar` / `…Zone` | 0.1 / 0.1 | +10 % influence when clan race matches system / zone |
| `universe_allowExternalControl` | 1 | External service may drive zone logic; `0` = server never starts/ends conflicts itself |
| `universe_*KillsCF` | 0 | Faction kill counters growth (disabled) |
| `universe_newYearStartTime` | 2018-12-17 | New-year event stages (`universe.xml` stages at days 0,7,11,13,17,22,27) |
| `war_coeffAssist` / `Neutral` / `Bot` | 0.2 / 0.1 / 0.05 | Global-war score multipliers |
| `war_coeffRivalA/B` | 1 / 2 | Rival target multiplier = A·victimRank + B |
| `war_damageRawRateToMilitaryExp` / `…ToDamage` | 10 / 100 | Raw points → military rank progress / corporation damage |
| `war_decayCostBase` | 0.1 | Periodic reduction of the war base cost (×(1−v)) |
| `universe.xml` | `conflictDurationTime 50`, `civilianZoneCost 1000`, `civilianZoneDuration 43200` s, `moveCoefFar 95`, `moveCoefClose 45` | Timings and move coefficients |
| `war.xml` | `warClanReviveCost 10000`, `warBaseReward 10000` | |

"Green" (alien) global events are driven by `ScriptsServer:ConfigureGlobalEvents`
(§5).

## 3. Quests, achievements, lobby

| Service | Settings |
|---------|----------|
| QuestServer | `quests_enable 1`, `quests_readWaveMaxUids 100`, `quests_dbgLog 31` (bitmask: 1 caching, 2 availability, 4 user state, 8 selection, 16 progress), seasonal toggles `event_summer`, `event_summerShip`, `event_halloween`, `event_newYear` (start 2030-12-17 → effectively off), `event_custom`, imaginary-quest reward decay `A = 25, B = 0.17` → `floor((A−1)(1−tanh(B(n−1)))+1)`; also `QuestServer_SetupBattlePassActivation` |
| AchievementServer | `achievements_enable 1`, `achievements_readWaveMaxUids 100`, `achievements_dbgLogEnable 0` |
| LobbyServer (custom games) | `lobby_enabled 1`, `lobby_rewardRates 1`, PvE lobby 3–4 players, `store_maxUniqueModules 3/2`, `Lobby_SetupLeagueForbiddenEquipment(leagueForbiddenDefs)` |

Imaginary-quest reward by completion count (A=25, B=0.17): 25, 20, 17, 13, 10, 8, 6, 5, 3, 3, 2, 2, 1, 1, … (computed from the formula).

## 4. Leaderboards (needs Redis)

`ConfigureLeaderboardServer()` builds two Lua tables and passes them to
`Leaderboards_Configure(lbrds)` / `Leaderboards_Routes(routes)`:

* **lbrds** — boards: `{ name, entityType, dir, decayInterval, decayPower,
  expiresAt, expAction, renewalInterval, rewards }`
* **routes** — `{ event, target, update }`: which game event feeds which board.

| Enum | Values |
|------|--------|
| entity type `LET_*` | 0 player, 1 clan, 2 clan member, 3 race, 4 league team |
| expire action `LEA_*` | 0 reset, 1 delete, 2 no-op |
| reward type `LRT_*` | 0 credits (mail reward), 1 leaderboard event |
| update `LUT_*` | 0 increment, 1 set, 2 set if greater, 3 set if lesser |

Shipped boards (active):

| Group | Boards (event → board) |
|-------|------------------------|
| Permanent players | prestige, pvp/pve effectiveness (daily decay 10 %), battles (`gover`), wins (`gwin`), kills, karma good/bad, football goals, hunger-games kills, pressure (influence), PvE raid completion times (`time_pve_raid*`, set-if-lesser, `dir = 1` presumably means ascending order — lower is better), unlimited-PvE wave level, wave-PvE wave |
| Weekly with rewards (renew 7 d) | `player_kills_weekly`, `player_pvp_eff_max_weekly`, `player_pve_eff_max_weekly`, `player_pve_win_weekly` — top-3 get 400/200/100 token credits (Iridium); `player_eff_rating_weekly` — top 1–3 / 4–20 / 21–50 tiers by title id 31/32/33 |
| Clan members | pvp/pve effectiveness, pressure, military rank, war damage, war losses |
| Clans | `CLS_PVP_RATING`, `CLS_PVE_RATING` (1 %/h decay), `CLS_WAR_DAMAGE`, `CLS_ZONE_CAPTURE`, `CLS_WAR_RATING`, `CLS_WAR_RATING_MAX` |
| Events | `event_green_war_{empire,federation,jericho,total}`, `player_april_win`, `player_cd_win` (close distance), `player_kills_marathon` (expires 2022-05) |

Without Redis (`db_redisHost`) the LeaderboardServer cannot persist these;
other services run normally ([quick start §6](../04-installation/quick-start.md#6-optional-leaderboards-redis)).

## 5. ScriptsServer global events

`ConfigureScriptsServer()` sets `sv_enableCommunticationWithSS 1` and calls
`ScriptsServer:ConfigureGlobalEvents{ forceEvents = {…} }` — **all examples are
commented out** in the shipped file, followed by
`ScriptsServer:SetTimerScale(1)` (1 s real = 1 s event time; the commented
`OnSetTimerScale(3600)` would make 1 s = 1 h, "not all parameters support
acceleration").

`forceEvents` entry fields (from the comments): `eventDefName` (event type id;
created if absent, modified if present), `eventLocation` (zone id),
`newEventState` (numeric state / timer; `-100501` = TIMEOUT_EVENT),
`eventParams`, `disableCreate`, `removeEvent`.

Event ids: **use the table in [zone-events.md](zone-events.md)** (generated from the ScriptsServer bytecode: e.g. EMPIRE_OWNERSHIP = 3, GREEN_OWNERSHIP = 23, ATTACK_GREEN_CHINABOSS = 41).

> ⚠ The numbers written in the *commented examples* of default_platform_config.lua (1 invasion, 2 ownership, 6/7 pre-event, 8 counter-attack, 9, 12) are from an **older numbering** and do not match this build.

Zone ids mentioned: 11 (wreck lab, Empire–Federation), 213 (abandoned
complex, behind Jericho), 224 (north mining station, Federation–Jericho),
104 ("Wasteland"), 234, 212, 231 (starting zone), 247, 25 (PvP reservoir).
These are examples of how to restart open-world campaigns on a private server.

## 6. Tournament and clan servers

| Cvar | Shipped | Meaning |
|------|--------:|---------|
| `tournament_levels` | 9 maps | Tournament map pool (`s1338_pandora_anomaly` excluded: "glitchy") |
| `tournament_battleRank` / `tournament_gamemode` / `tournament_teamSize` | 17 / 12 (TDM) / 8 | |
| `tournament_gameInterval` | 2000 ms | Spacing of game creation |
| `clan_shipPartsCanBuild` | 4 | Dreadnought build stages 0–4 |
| `clan_shipUpgradeCanBuild` | 3 | Upgrade stages (T3, T4, T5) |
| `clan_shipBuildHighRanks` | 3 | Rank-9 members needed |
| `clan_warWinRewardAura` | `Bundle_ClanWar_Win` | |

Schedule and rewards of tournaments: [data-files](data-files.md) (`tournaments.xml`).

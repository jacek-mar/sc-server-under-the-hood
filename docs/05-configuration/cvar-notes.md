# CVar notes — curated English annotations

> Status: **started (Stage 1).** The full generated list is in
> [cvar-reference.md](cvar-reference.md) (original Russian comments). This page
> collects *English* explanations and practical effects for the cvars that
> matter most to a server operator. Add entries as they are verified.
> "(file)" = value shipped in `default_platform_config.lua`.

## Accounts, economy (Shard)

| CVar | (file) | Effect |
|------|-------:|--------|
| `auth_allowInternalAutoCreate` | 1 | Auto-create an account on first login. Set `0` to forbid new accounts |
| `auth_infinitePremiumForRoles` | `"gm;support"` | `admRole`s with infinite premium |
| `gold_on_start` / `credits_on_start` / `premium_on_start` | 300 / 0 / 0 | Starting Galactic Standards / credits / premium time for new accounts |
| `store_allowAllItemsForBying` | 0 | `1` lets items flagged `cant_be_bought` be bought — community: "unlocks everything in the store" |
| `store_vesselPriceMod`, `store_modulePriceMod`, `store_munitionPriceMod` | 1 | Price multipliers (0.001…100) |
| `store_maxTransactionSum` | 20000 | Max single transaction/mail |
| `store_maxUniqueModules` / `…OnPremium` | 3 / 2 | Max identical unique modules per ship |
| `store_vesselExpExtractionCost` | 0.00667 | Cost to extract ship XP |
| `sv_tokenCreditsDailyLimit` | 1000 | Daily Iridium (token credits) earn cap |
| `sv_offerEnable` | `"6,7,17,18,19"` | Enabled `offerId`s from `offers.xml` (empty disables all) |
| `premiumTimeForAccountRank` | 86400 | Premium seconds granted per account rank |
| `shard_minAntibotCounterForMailSending` | 50 | Anti-bot gate for mail |
| `sm_sandboxAccess` | 4 | Sandbox function access level (meaning unverified) |
| `steam_useMicroTxnSandbox` (shard.cfg) | 1 | Steam microtransactions in sandbox mode |

Currency names ↔ DB fields (community): `credits` = credits, `goldCredits` =
Galactic Standards (GS), `tokenCredits` = Iridium, `accountExpPool`/
`vesselExpPool` = synergy/free XP. See [database](../06-database/mongodb.md).

## Battle rules (DedicatedServer / ZoneInstance)

| CVar | (file) | Effect |
|------|-------:|--------|
| `sv_lootEnabled` | 1 | Post-battle loot on/off |
| `sv_lootFailChance` | 0 | Chance (0..1) to find nothing; community: values > 0 cause "loot not found" |
| `sv_lootScanTime` / `sv_lootDuration` | 1 / 120 | Scan time / duration of the loot phase (s) |
| `sv_salvageTokenConversion` | 0.2 | Salvage refund = tokenPrice × this |
| `sv_salvagePremiumTokenConversion` | 0.6 | Premium-salvage refund factor |
| `sv_afkCheckDuration` | 120 | Seconds idle before AFK kick (3600 ≈ off) |
| `sv_respawnTimePenalty` | −1 | Override respawn penalty (−1 = use gameplay settings; newbie queues set 0) |
| `sv_dailyWin{Pvp,Pve,Coop,Brawl}ExpRewardCf` | 3 (`x3fw`) | First-win-of-day XP multiplier |
| `sv_freeSynergyRewardCf` / `…PremiumVessel` | 0.05 / 0.2 | Free synergy reward factors |
| `sv_leaveFineRewardCoef` | 0.8 | Reward multiplier after leaving previous battles |
| `sv_leaverBanTime` | 0 | Battle-ban seconds for leavers (0..1800; engine default 300) |
| `sv_leaverReputationAdd/Decay`, `sv_leaveCounter…` | | Leaver counter model (see comments in reference) |
| `sv_kickExcessiveBotsEnabled` | 1 | Kick players when bots outnumber players |
| `sv_numAdaptivePresetsInDB`, `sv_numUniqueAdaptivePresets`, `sv_rangeRankAdaptivePresets`, `sv_numBestPlayerToSave`, `sv_minEfficiencyVesselToSave` | 32 / 20 / 3 / 2 / 1500 | Adaptive bot presets: best players' ships are saved and replayed by bots |
| `cl_combatLog` | 0 | Combat log verbosity 0–4 (kills → modules → all damage → aura coefs) |
| `sv_shipWeaponDamageCoef` | 1 | Global weapon damage multiplier (ZoneInstance) |
| `sv_autorecordReplaysTo` | `""` | Directory for dedicated-server replays; empty = off |
| `cl_maxFps` | 18 (DS/ZI) | Server simulation frame cap |

## Rewards (GameRewardDispencer / Matchmaker)

| CVar | (file) | Effect |
|------|-------:|--------|
| `reward_bonusGoldForWinner` / `…Looser` | 0 / 0 | Bonus GS per battle (community: set 15 / 5 for a "gold per match" server) |
| `reward_eventGoldTimePeriod` | `"2025-09-02T12:00:00Z;2025-09-11T06:00:00Z"` | Window of the "gold for first/fifth win" event; **must contain the current date** for the event to run |
| `reward_eventGoldTimeValue` | 20 values | Gold per win slot |
| `rate_exp` / `rate_cred` | `1×18` | XP/credit multipliers per rank (18 ranks) |
| `MatchMaker_SetRewardRates` | schedule | Day-of-week/hour windows overriding rates and gold |

## Chat

Anti-spam model: *awareness* grows by `antispam_awarenessIntervalNumerator/dt`
per message plus `K·similarity^P`, decays by `antispam_awarenessDecay`/s;
notify at 450, auto-ban at 500 for 60 s (trade chat: 150/200). Word lists:
`cloud/data/chat/stop-list.txt`, `white-list.txt`.

## Load balancer

`lb_limitPlayersOnShardTo = 800`, `lb_disallowAccess = 0` (set `1` to refuse
all logins — handy for maintenance), `lb_maxTaskQLenOnShard = 500`.

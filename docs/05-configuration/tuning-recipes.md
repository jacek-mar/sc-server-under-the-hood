# Tuning recipes — where to change gameplay values

> Status: **first draft (2026-10-11).** Collects the places an operator can
> change economy, loot, bots, events and store content on a *local* server.
> Origin: community leads from Discord batch 002 (anonymised, see
> [source register](../sources/source-register.md), S12) **cross-checked against
> the shipped files**. Each row carries its evidence level:
>
> * **file-verified** — the file/key exists in the depot as described; the
>   *effect* has not been tested by us.
> * **lead** — community claim only, not yet confirmed. ⚠
>
> Paths relative to the depot root `star conflict/`.

## Golden rule: edits only affect the server you run

*(community, consistent with architecture)* Game-data and `cloud/data` edits
are read by the services of **your own node**. A client connecting to someone
else's server gets that server's data; client-side edits of server data do
nothing. Restart the node after editing (data is loaded at start-up).

## Economy and progression

| Goal | Where | Evidence |
|------|-------|----------|
| Currencies / XP / resources of one account | MongoDB `accounts` collection of the node DB (credits, free XP, gold, craft/PvE resources); use a Mongo GUI | file-verified ([schema.md](../06-database/schema.md)); field names `craftResource`, `pve_resource` reported by community ⚠ (arrays: add fields if absent) |
| Allow buying every store item | `cvars.store_allowAllItemsForBying = 1` in `cloud/data/default_platform_config.lua` (shipped value **0**, line ~83) | file-verified |
| Add a ship/pack to the store for testing | `cloud/data/store.xml` — shipped file contains `Bundle_For_Testers` (2 occurrences) and ship "part" bundles such as `Ship_Race5_S_RECON_part`; community recipe: copy a bundle's contents to the desired item name | file-verified (names exist), recipe ⚠ lead |
| Post-battle junk drops (tokens) | `data/gamedata/def/ex/junk.lua` — Targem-exported defs `Token_drop_T<n>` with `tokens`, `drop_weight`, `item_lvl` | file-verified |
| Asteroid yield (rocks per asteroid) | `data/gamedata/def/objects/openworld_entities.lua` | file-verified (file exists), effect ⚠ lead |
| What asteroids/containers drop | `data/gamedata/def/objects/ow_loot_tables.lua` (1 961 lines) | file-verified (file exists), effect ⚠ lead |
| Heat limit of a ship | key `overheat_temperature`; the only literal occurrence in `data/gamedata` is in `def/objects/openworld_entities.lua` (one def, value 0.90) — player-ship values are probably inherited/derived elsewhere ⚠ | file-verified (key exists), player-ship location open |

Caveat from the community: copying an alien ship definition from
`gameplay_leviathan.lua` into `ship.lua` did **not** work (missing
properties) ⚠ — NPC defs are not drop-in player ships. A later community
recipe (S17) claims the opposite for weapons only: a snippet in the ship's
`ship.lua` entry plus emptied weapon slots in the hangar makes the ship fire
the alien gun ⚠ - test proposal **Q55**.

## Events, battle pass, xenochips

* **Xenochips and other event currencies exist only while the matching event is
  active.** Event windows are set in `default_platform_config.lua` and are dated
  2023–2025 (see CLAUDE.md gotchas) — move the dates (or the clock) to make an
  event active. *(community + file-verified: dates are in the past)*
* Reported symptom: first event phase completes, the next phase is rejected
  with "wrong phase" — consistent with phase windows tied to dates ⚠.
* **Battle pass** is defined in `data/gamedata/shared/battle_pass.lua`.
  *(observed)* In the shipped file **stage 1 is active and stages 2–4 are
  wrapped in `--[[ … ]]` comments**; premium/VIP DLC keys are commented out and
  some paid bundles are commented. Community explanation for the error seen
  when finishing stage 1: rewards that reference bundles removed together with
  monetisation ⚠. Fix idea: re-enable stage 2 and replace invalid bundle names
  with ones that exist in `store.xml`.

## Bots and PvE

| Goal | Where | Evidence |
|------|-------|----------|
| Queue-wide bot preset mode | queue `special.botPresetType` = `bpt_none` (0) / `bpt_mirror` (1) / `bpt_adaptive` (2) / `bpt_mirror_and_save` (3) — constants declared in `default_platform_config.lua` ~line 353 | file-verified |
| Fixed preset per queue | `special.botPresetNames = { "BotsBZS_T5" }` | lead ⚠ (key used by community overlay) |
| Preset by tier | `special.botPresetByTier = { "BotsBZS_T3", … }` — used by the sector/league queues (qid 501/502) in the shipped file; community says the "Sec Con" queues accept only `botPresetType` **or** `botPresetByTier` | file-verified (key), exclusivity ⚠ |
| Why rank 1-3 bots appear / how rank follows tier | see [bot-presets.md](bot-presets.md) | file-verified (inference ⚠) |
| Available preset names | `data/gamedata/shared/ai_settings.lua`: `BotsT1…T5` (+`E`/`G`/`EG` variants), `BotsBZS`, `BotsBZS_T3/T4/T5`, `BotsLobby1–3`, `BotsOW`, `BotsPortal_T5`, `BotsT35_R`, `BotsT5X_H`, `BotsTX` | file-verified |
| Number of bots / team size in PvE | queue `special = { pve = 1, gameMode = 7, botsCount = N }`, `maxPlayers`, `minPlayers`; query `mmParams.pve = 1` | file-verified (shape), effect ⚠ |
| Allied bots in **Special Operations** (PvE raids) | **No configuration route** (V-12): the raid queue's `special.botsCount` is replaced by 0, `botsInTeam1` reaches the battle server but needs a non-zero total, DS cvars `sv_numBots`/`sv_botsInTeam1`/`sv_forceBotTeam` had no effect, PvE custom games list missions only | observed; open Q50 |
| Special Operations access | account rank 7 (client `UI.rankLocks.raid`), ship rank picks the operation (`aux_limits.xml` `/PVEMissions raid="1"`), weekly `RaidSchedule` (even hours of the week), solo allowed by `mm_raidSquadFilter = 0` | file-verified + observed (V-12) |
| Mission difficulty level | **not** a queue setting as far as known: PvE mission levels unlock by completing a mission (stock behaviour per community); still open how to force a level | ⚠ open |
| Bots don't carry the bomb (bomb mode) | same on the live service — meta was letting enemy bots hold it | community, ⚠ |

**Duplicate queue blocks are expected.** Queues are defined for both
`queuesConfig` and `queuesConfigLo` (some are inserted into both tables, some
are written twice) because the server switches between them
by online count: `cvars.mm_lowOnlineLo = 250`, `cvars.mm_lowOnlineHi = 300`
*(file-verified)*. A small server always uses the *Lo* set — edit **both** when
unsure (see [queue-reference.md](queue-reference.md)).

## Reported client-side issues (leads)

* Second-PC LAN test: client on the main PC fails to connect to a node on
  another PC although the node's windows are open ⚠ — feeds Q2/Q3
  ([open-questions](../08-reverse-engineering/open-questions.md)). Firewall
  rules per executable path and bind addresses are the first suspects
  ([verification-log](../04-installation/verification-log.md) V-8).
* First start of a fresh local node: after the tutorial the client returned to
  the login page ⚠ (not reproduced).
* Reported "server time might be bugged" for event timers ⚠ — see event dates.
* Matchmaking in public community servers described as "still wonky" ⚠ (see Q11).

## Additions from the Russian channel (batch 003, S15; 2026-10-11)

File-verified before inclusion (depot copy, `default_platform_config.lua`):

| Lead | Check | Result |
|------|-------|--------|
| `cvars.store_allowAllItemsForBying` toggles purchase of items hidden by the "cannot be bought" flag | grep | shipped `0`; comment confirms semantics |
| Cap of identical unique modules per ship | grep | `store_maxUniqueModules = 3`, `store_maxUniqueModulesOnPremium = 2` (separate limits; comment mentions a backlog item to allow one experimental module on premium/DLC ships) |
| Starting values for new accounts | grep | `gold_on_start = 300`, `premium_on_start = 0`, `credits_on_start = 0` |
| Bot counts sit in `coopQueueTemplate` instances (Lo and normal queue sets) | read | yes, `maxPlayers = 8`, newbie flag on the first |
| Battle pass stages enabled by removing comment markers | S12 digest | consistent |

Community behaviour reports (⚠ untested by us):

* Content-unlock recipe seen repeatedly: copy the depot, ask an AI assistant
  to "make everything available" (items free/purchasable, slot and class
  restrictions removed, unique-module limit raised), regenerate with
  `prepare_shared`. Users report it works but that **invalid ids written into
  the DB make the server refuse to start** — back up Mongo first.
* Ships are stored in `accounts.vessels` (array of ship documents) with module
  ids as numbers; foreign-faction ("alien") ships taken from special game
  modes can be placed in a slot but then fail on launch or module fitting.
* Premium time: unit unclear (Q27).
* Stat edits: speed/energy/manoeuvrability changed, damage/hull/radar did not
  (Q29).
* Empty loot points after battle on community nodes (Q12): low drop chance
  suspected, `sv_lootFailChance` is the known lever.

## Additions from batch 004 (2026-10-11; S12/S15 partial exports)

Leads only; see the "batch 004" digest in the
[source register](../sources/source-register.md).

* **Quest rewards.** Reported: change both `data/gamedata/shared/quests.lua`
  and `cloud/data/quests.xml` (both exist; the XML holds QuestGroups and
  cooldowns). Claimed order: Lua first, start Mongo + run the prepare `.bat`s,
  then the XML; repeat the XML step after every modification. The quest UI
  shows only one reward but several can be granted. Example reported:
  credit-reward quests also pay gold (1 gold per 1 000 credits). ⚠ Untested
  (Q36).
* **Seeing DB edits.** A client must log in again to see edited account data;
  no refresh trigger is known (Q32). Do edits with the client logged out.
* **Ship speed.** Raising a ship's speed value works (800 sent a ship almost
  across the map); a ship-specific 60 s respawn and the warp speed cap were
  reported removable ⚠ (consistent with Q29).
* **Per-player customisation.** Slot count / special module of a single
  player's ship can be changed in that player's DB document; whether the
  client accepts a special-module choice it does not have in its own files is
  unknown (Q36).
* **Friends joining.** Virtual-LAN tools (ZeroTier reported working) put the
  node address on a host interface; a spoofed/foreign address is what
  reportedly crashes the DedicatedServer (Q30).

## Additions from batch 005 (2026-10-11; S12/S15 partial exports)

Leads only; see the "batch 005" digest (H1-H19) in the
[source register](../sources/source-register.md).

* **Iridium limit.** `cvars.sv_tokenCreditsDailyLimit` (shipped 1000, set
  twice in `default_platform_config.lua`) is the *daily* iridium cap; one
  operator runs 100 000. Conquest rewards alone hit 1 000. Effect untested.
* **Hard currency caps**: edit the Lua globals `ai.event_credits_cap`,
  `ai.vessel_exp_pool_cap`, `ai.credits_cap`, `ai.tokens_cap` in
  `data/gamedata/shared/reputation.lua` (lines 39-42), then run
  `prepare_shared`; `cloud/data/aux_limits.xml` is **generated** from them and
  is overwritten (Q38 solved, [pipeline](../08-reverse-engineering/config-pipeline-and-limiters.md)).
  A stock client shows its own copy of the cap.
* **Bots by rank band.** See the example in [bot-presets](bot-presets.md) section 5:
  several `InstantiateQueueTemplate` calls, each with its own
  `special.botPresetNames`. Pitfall: an invalid block is ignored silently.
* **Instant matches.** `maxTimeInQueue = 1` in the queue template (reported).
* **Kicked for frequent actions.** Shard cvars `sm_overloadCounterLimit`
  (shipped 20), `sm_reqFreqOverloadLine` (0.8), `sm_reqFreqCalculationSamples`
  (15) in `cloud/data/shard_local.cfg` (static, effect untested; Q41 solved).
* **Check before restart:** [config-validation-tools](../07-administration/config-validation-tools.md)
  (`defname_check.py`, `queue_lint.py`).
* **Squad in PvE missions.** Raise the PvE queue's max players to 4 (reported,
  Q35).
* **More asteroid loot.** Add entries to `asteroid_loot_crate` in
  `data/gamedata/def/objects/openworld_entities.lua` (one line per crate, one
  entry per possible drop). Premium vs. free drops reportedly differ in the
  files (not checked).
* **Event ship parts** (Helicon/Salyut). Write the defs straight into the
  account (DB) instead of the store: `HeliconCorpse`/`HeliconModule` exist as
  type-5 store items (`cantBeBought`, price 100 000). Not buyable in the UI,
  no usable prices, 99 pieces per craft; changing the **craft recipe**
  (`def/ex/craft.lua`) is judged easier than the store. `unreachable_activator`
  (`amount=99`) in one recipe is the intentional blocker. A typo in a def name
  stops the server from starting.
* **Details** for event-ship parts, mail limits (`shard_minAntibotCounterForMailSending`) and the clan
  ship (`clan_shipBuildHighRanks`, `ClanShipKF`): [event-ships-mail-and-clan-ship](event-ships-mail-and-clan-ship.md).
* **Store experiments** that stop the server from starting: remove the added
  items, or keep a backup of the file; Steam "verify files" resets *all* edits.

## Additions from batch 006 and the community mod manager (2026-10-12)

Leads and file checks; see the "batch 006" digest (I1-I20) in the
[source register](../sources/source-register.md) and the tool review
[community-mod-manager](../07-administration/community-mod-manager.md) (S18).

* **Arena "search" rewards (shipped bug, file-verified).** The rank table in
  `DedicatedServcerServices_SetLootRules` (`default_platform_config.lua`
  lines 1315-1335) uses `common = { lt = "CommonRanks_<band>" }`, while
  `shared/loot_tables.lua` defines only `CommonRanks_<band>_v3`; ranks 8 and 11
  also use undefined `NeodiumDrop` / `LezortiumDrop` as `epic`. Fix by aliasing
  (`LootTable.CommonRanks_1_3 = LootTable.CommonRanks_1_3_v3`, ...) or by
  renaming the references in the config (server-only file). Q45.
* **Iridium from the search:** `Def.Iridium_Junk_r1..r15.tokenPrice` in
  `data/gamedata/def/ex/junk.lua` (32 ... 239, r15 = 500); still capped by
  `sv_tokenCreditsDailyLimit` and `TokensCap`.
* **Arena fill with bots:** `mm_botsCount`, `sv_kickExcessiveBotsEnabled` (shipped 1; the
  Russian comment reads "kick players from battle if there are more bots than
  players", the name suggests excess bots are removed - ⚠ unclear) and the two `arcadeQueueTemplate`
  blocks (`optimalPlayers 4`, `maxExpandTime 30`, `maxTimeInQueue 10`,
  `special = { arcade = 1 }`); the mod manager sets 23 bots / 0 / 12 / 60 / 15
  and `botsCount` in `special` (effect reported by the community, untested).
* **Open-world loot:** canister tables `OW2_GoodJunk1..6` and ore tables
  `OW3_Ore{Poor,Normal,Rich,UltraRich}` in `def/objects/ow_loot_tables.lua`
  (credit items carry the developers' comment "серебро" = silver/credits);
  crate counts per asteroid in the 20 `asteroid(_premium)_loot_crate` blocks of
  `def/objects/openworld_entities.lua`; enemy drop rarity in
  `OW3_autogen_rnd_poor_13/18` (`str_param` COMMON/BALANCED/SPECIAL/DOUBLE).
* **Anti-flood kick:** `cloud/data/shard.cfg` line 6 `set sm_overloadCounterLimit 20`.
* **Dreadnought:** gate `clan_shipBuildHighRanks` (3) rank-9 members; a host
  saw the unlock only after a restart (Q32).
* **Service windows:** `hub_detachChildProcesses` in `cloud/data/hub.cfg` (1).
* **Remember:** anything under `data/gamedata/**` is also client data; hosted
  servers that change it lock out stock clients (b006 I4, Q3).

## Additions from batch 007 and the first LAN test (2026-10-12)

Leads and file checks; see the "batch 007" digest (J1-J12) in the
[source register](../sources/source-register.md) and
[verification-log V-9](../04-installation/verification-log.md).

* **Battle pass stages 2-4 (file-verified).** Uncommenting the stages in
  `shared/battle_pass.lua` is not enough: the shipped `cloud/data/battle_pass.xml`
  holds only stage-1 bundles. Regenerate it with `prepare_shared` (*inferred*;
  MongoDB running) or use an XML with the later `Bundle_Battle_Pass_*` entries.
* **Seed chips / autogen (file + translation).** `shared/autogen.lua` sets
  storage sell price, per-level growth of rolled values (`upgradeModPerLevel`
  0.2), upgrade price multipliers per level (`{1, 2, 3, 10}`), curve
  coefficients for experience and credit costs and the donor-experience
  factor; its class table must **not** lose classes (already rolled modules
  would become invalid). `cloud/data/autogen.xml` maps `affixId` to `name`.
* **Granting ships (community, unverified).** Add a full vessel element with
  a unique `vid` to `accounts.vessels`; alien/brawl hulls also need
  `def/objects/gameplay_leviathan.lua` for tree position and icons - a file
  the clients read too.
* **Small-server matchmaking (observed V-9).** The MatchMaker reports LOW
  online mode, merges players who queue at the same moment, avoids the
  group's most-played map, and sends no bot preset (DS falls back to
  `AiPreset.Default`, bots carry `mmValue 17`). Use the decision log
  (`mm_decisionLog = 1` in the platform Lua, both assignments) to tune.
* **Anti-flood** `sm_overloadCounterLimit` in `cloud/data/shard.cfg` - confirmed
  again by hosts (b007 J7).

## Additions from batch 008 (2026-10-12 evening)

* **Alien bosses in an open-world hub** *(reported by a host; files
  verified)*: the hub `data/levels/global_world/_campaign/hub_jer_rock_terramorph_e_ow/zone_mission.lua`
  already defines an alien boss group that uses `AlienCruiser_EventDestroyer`
  (`boss = true`); hosts edit this mission script to spawn bosses. The
  destroyer's `health = 1000000000` in `data/gamedata/def/objects/cargoship.lua`
  is the **live-event value** (comment "100M test, 1G live"; the def is a copy
  of a raid ship for the open-space event) - lower it only if a small player
  base cannot finish the event. Battle stats come from the server's Lua (V-10
  test V-10); the client still needs the models and defs it already has.
* **Granting resources and ships without editing documents by hand**: use the
  Shard admin-task queue (V-10: `give` with `value` = `credits` /
  `goldCredits` and `amount`; documents need `pickedBy: 0`; requester with
  `admRole` `root`) - see [admin-tasks-howto](../07-administration/admin-tasks-howto.md).

## Additions from batch 010 (2026-10-13)

| Goal | Where | Evidence |
|------|-------|----------|
| Start a PvE **custom game** (lobby) with fewer than 3 players | `cvars.lobby_reqPlayersPvEMin = 3` (and `lobby_reqPlayersPvEMax = 4`) in `ConfigureLobbyServer()`, `cloud/data/default_platform_config.lua` lines 1832/1834. Set in the platform Lua, so `lobby_server_local.cfg` cannot override it; edit the Lua and restart (whether a live console assignment takes effect for this cvar is untested, see [settings-reload-map](settings-reload-map.md)) | file-verified; reported by a host: `1` lets one player start a PvE lobby, but no allied bots join ⚠. Static (2026-10-13): custom-game bots are a lobby setting - the client's advanced options (`data/ui/scripts/windows/gameplaycustomwnd.lua`) offer 0/8/12/16/20/24 bots and a bot skill preset (`botsCount`, `botPresetName`), the LobbyServer counts `botsInTeam1`/`botsInTeam2`; the older per-lobby bot picker is commented out. **Observed (V-12):** the bot selector appears for PvP custom games only; a PvE lobby (capacity 1/4) has none, and the PvE list offers missions, not Special Operations (raids) |
| Change **craft recipes** (blueprints, parts) | `data/gamedata/def/ex/craft.lua`: `BP_*` definitions with `craft_result` and `craft_ingredients[n]` (`def`, `count`); ships built from parts: `craftable_reagents` in `def/ex/ship.lua`. `cloud/data/store.xml` holds the compiled recipes (`<Ingr resource=... amount=...>`) - regenerate it with `prepare_shared` instead of editing it | file-verified; `Iridium_plate` is the "Metal blank" resource, not iridium |
| Change **ship prices** | `data/gamedata/def/ex/prices_ship.lua` (stats, special module and recipe are in `def/ex/ship.lua`) | file-verified (files exist); edit order Lua -> `prepare_shared` |
| Put a different model on a hull | The hull class binds each module slot to a **named bone** of its model (`slot_bones` in `data/gamedata/def/objects/ships.lua`, e.g. `PRIMARY_WEAPON_01 = "gun"`, `ACTIVE_01 = "gun_1"`), plus `weapon_slots` and `fire_sectors`. A model without the expected bones cannot mount those weapons or modules | file-verified fields; consequence *(inferred)*, matching a host's report (dreadnought model on a destroyer: flies, no weapons or modules) |
| Alien/boss hulls as player ships | AI hulls are in `def/ex/ow_bot_preset.lua` and `def/ex/pvebot_preset.lua` (`ship4bot = true`, `_Mob` modules, `avtomat` AI behaviour). Reported: some move, others (e.g. `Ship_OW_Boss_Manta`) neither move nor turn although speed and engine values are set | lead ⚠ -> Q49 |

## Additions from the community guide update (S11, 2026-10-14)

| Goal | Where | Evidence |
|------|-------|----------|
| Raise how much of a resource a player may hold | `.player_stock_limit` per resource in `data/gamedata/def/ex/prices_tradegoods.lua` (148 entries; e.g. `ow_Impure_iridium` = Vanadium, `iridium_monocrystall`, `processor_block`, `resource_zeta`); edit the Lua, then `prepare_shared` | file-verified key; effect reported ⚠ |
| Insignias / the "mole" event | Asteroid drop tables in `data/gamedata/def/objects/openworld_entities.lua`: each line `[chance] = { crate, crate, ... }` is one crate, the bracketed number its chance, the list the possible crate types; every asteroid type follows the generic table but has its own table per controlling faction. The mole crates (`LootCrate_OW2_MoleShipPart`, `..._MoleShipPartNormal`) are present only in trailing comments of those lines; moving them into the lists is the reported way to enable them | file-verified layout and comments; effect reported ⚠ |
| Battle pass window and stages | `battlePassStart` and `battlePassEndTable = { {stage, "end time"}, ... }` at the top of `cloud/data/default_platform_config.lua` (passed to `Shard_SetupBattlePassActivation`); xenochip window `creditsEventStart` / `creditsEventEnd`. File comments (translated from Russian): an **empty end time** means the stage has no end; player progress is stored for **one** event only and is **lost when `battlePassStart` changes**; keep the end times of stages 1 and 2 of one battle pass equal | file-verified comments; reward errors after enabling stages -> Q59 |
| Seed-chip generation | `shared/autogen.lua` (classes, effect counts, minimum ranks, prices) and the effect groups `def/ex/autogen_common.lua`, `autogen_balanced.lua`, `autogen_special.lua`; `cloud/data/autogen.xml` is generated from them - run `prepare_shared`, do not edit the XML ([progression-xml-semantics §6](progression-xml-semantics.md)) | file-verified file roles; class composition reported (COMMON 4 common; BALANCED 1+3; SPECIAL 1+3; DOUBLE 2 special + 3 common) |
| Bot behaviour presets | PvE `def/ex/bot_preset.lua`, open world `def/ex/ow_preset.lua` (AI hulls: `ow_bot_preset.lua`) | files exist; see [bot-presets](bot-presets.md) |
| Battle-pass rewards fail after enabling stages | No server-side DLC check exists (the `premium_dlc*` keys are read only by the client UI); the reward must be an existing `Def` bundle with `is_rewardable`, otherwise the Shard logs `cannot find store item` / `is not bundle`. Shard console command for tests: `dbg_testBattlePassUnlockPremium <uid> <eventStart> <stage> [<unlockLevels>]` | static (2026-10-14), Q59 |
| Currency caps | `ai.credits_cap`, `ai.tokens_cap`, `ai.event_credits_cap` in `shared/reputation.lua` (-> `aux_limits.xml`); maximum accepted value 2 147 483 647 (signed 32-bit) | static (2026-10-14), Q52 |
| Alien weapon on a player ship | Put the weapon (`Weapon_AlienGun_Prec`, `Weapon_AlienGun2_Prec`, `Weapon_ReaverGun_Prec`, `Weapon_ScoutGun_Prec`) into the hull's `default_modules[ ai.SpaceShipModuleSlot.PRIMARY_WEAPON_01 ]` in `def/ex/ship.lua` and empty the slot in the hangar; the battle server spawns ships with their `default_modules` | mechanism static (2026-10-14), effect reported (S17) ⚠, Q55 |
| Allied bots in Special Operations (raids) | Not configurable: the MatchMaker writes `botsCount = 0` for every raid game | static (2026-10-14) + V-12, Q50 |
| Add a new ship | Chain of definitions, presets and assets - see [data-files](data-files.md) "Adding a ship (community guide)"; ship id for a DB grant -> Q57; `storeItemId` -> Q58 | community guide (S11 O12) ⚠ |

## Additions from batch 011 (2026-10-14)

| Goal | Where | Evidence |
|------|-------|----------|
| Starter kit of new accounts (ships, currencies, items) | `data/gamedata/shared/starter_pack.lua`: `StarterPackBase` (`credits`, `goldCredits`, `tokenCredits`, `resources`, `items`) and `StarterPack.Vessels` (`<hull> = { [slot] = module, munition = {...}, put_in_battle_slot = n }`); `prepare_shared` writes `cloud/data/starter_pack.xml`, which the Shard reads. Stock: `Ship_Race1_M_T1` in battle slot 1, all currencies 0; three more T1 ships commented out on 2025-09-04 (file comment, translated) | file-verified; reported by a host: new accounts with rank-10/11 ships ⚠ |
| Free synergy for new accounts | cvar `synergy_on_start` (int, default 0, all services; not assigned by the platform Lua, so a `*_local.cfg` should work) | static ([cvar-defaults](cvar-defaults.md)); effect reported ⚠ |
| Fewer "kicked for spending" | `set sm_overloadCounterLimit 20` in `cloud/data/shard.cfg` line 6 (or `shard_local.cfg`); hosts use 999 | file-verified, Q41 |
| Remove a mode from co-op vs AI (e.g. Detonation) | edit the map lists in `coopQueueTemplate.levelsDesc` (shipped `{4,9,11}` on five maps) in `cloud/data/default_platform_config.lua` | file-verified key; bots and mode 11 -> Q61 |
| Post-battle loot with iridium | loot rules in `DedicatedServcerServices_SetLootRules` (platform Lua), tables in `data/gamedata/shared/loot_tables.lua`; use the `_v3` table names (Q45) | file-verified layout; a host's tweak reported |
| Grant cosmetic items (paints, decals, stickers) | custom elements in `shared/vessel_custom_elements.lua`, stickers in `shared/vessel_stickers.lua`; admin mail attachment type 16 `LAT_CUSTOM_ELEMENT` or a bundle with `ai.BundleContent.CUSTOM_ELEMENT` | static ⚠ untested |

## Additions from the Steam forum (S19, 2026-10-14)

| Goal | Where | Evidence |
|------|-------|----------|
| Co-op PvE missions for 2-4 players | both `-- PVE QUEUE` blocks in `cloud/data/default_platform_config.lua` (lines 376 and 701) ship with `maxPlayers = 1`; set 4. Allied bots: `botsCount = <n>` in that block's `special` | file-verified key; effect reported by several players ⚠ |
| Rank 16-17 ships in vs-AI battles | the co-op vs AI queue queries accept `mmRank` 1-15; widen the ranges (and add queues per tier) | file-verified; hosts report it works |
| Loot search for rank 16-17 | `DedicatedServcerServices_SetLootRules` has rows `[1]`-`[15]` only; add `[16]` and `[17]` (tables are case-sensitive names from `shared/loot_tables.lua`, e.g. `_v3`) | file-verified; effect reported |
| More bots in PvP | `cvars.mm_botsCount` (shipped 6, range 0-31), `cvars.sv_kickExcessiveBotsEnabled` (1 -> 0), queue `optimalPlayers`, `maxExpandTime`; `botsCount` in a queue's `special` worked for some and caused endless "heavy load" for others | keys file-verified; mixed reports ⚠ |
| Stronger bots / bots by tier | queues set no bot preset, so the default `AiPreset.Default` (weakened T1) is used; set `botPresetByTier` / `botPresetNames` per queue ([bot-presets](bot-presets.md)); the adaptive presets copy fits from players and stay empty on a fresh database | static; hosts confirm |
| Squads with bots | make each queue's `mmSquadRank` range equal its `mmRank` range | reported ⚠, Q35 |
| Gold for battle wins | `cvars.reward_bonusGoldForWinner` / `reward_bonusGoldForLooser` in `ConfigureGRD()`, window `cvars.reward_eventGoldTimePeriod` | keys file-verified; effect reported |
| Iridium after battles | in `shared/loot_tables.lua` replace un-salvageable `Iridium_Junk_r<n>` entries by `Token_drop_T1`-`T5` (defined in `def/ex/junk.lua`) (converted to iridium automatically); daily quests can give `reward_tokens` (`BP_DAILY_*` in `shared/quests.lua`, UI does not show it) | reported ⚠ |
| Infinite premium for everyone | `cvars.auth_infinitePremiumForRoles = "gm;support;player"` (shipped `"gm;support"`) | file-verified key; effect reported (24-hour display that refreshes) |
| Clan ship (dreadnought) for one player | `clan_shipBuildHighRanks` is set twice in the platform Lua (inside `LoadBalancer_SetGreetingMessageCVars` and as a cvar); rank requirements also in `clan_upgrades.lua` / `aux_limits.xml`; costs and times in `shared/clan_ship.lua` -> `cloud/data/clan_ship.xml` (edit the Lua and regenerate) | reported; files exist |
| Do not touch | `cvars.sm_sandboxAccess` (shipped 4 = "allow all", built-in description: 0 forbid all … 4 allow all); lower values lock players out of sandbox features such as the open world | static + reported |

## Still to verify (candidates for Stage 3 experiments)

1. Does `store_allowAllItemsForBying = 1` make *every* def purchasable?
2. Do ore/loot edits require editing only the Lua defs, or also generated XML
   (`prepare_shared`)? (links to B-5)
3. Which key controls PvE mission level / bot tier in PvE queues?
4. Do `botPresetNames` actually override the default tier presets, or is the
   `botPresetByTier` default re-applied?

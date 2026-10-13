# Config pipeline, request limiter and bot-preset selection (static analysis)

> Analysis of 2026-10-11. **Static** disassembly/strings analysis of the
> 32-bit service executables (method in section 5). Nothing
> was executed. Evidence tags: *(file)* verified in the shipped depot,
> *(disasm)* read from machine code, *(inferred)* conclusion drawn from both.
> Closes Q38 and Q41, gives a static answer to part of Q28.
> Addresses are virtual addresses of the depot build (Hub 1.99.0.167293); they
> change with every rebuild and are given only so the claims can be re-checked.

## 1. `aux_limits.xml` is generated, not hand-written (Q38)

**Pipeline** *(file + disasm)*:

```
data/gamedata/shared/*.lua          (Lua globals; also part of the client install)
        │  DedicatedServer.exe -prepareSharedData   (PrepareSharedData.cpp, needs MongoDB)
        ▼
cloud/data/aux_limits.xml           (+ store.xml, quests.xml, ... see xml-schemas.md)
        │  read once at start by Shard.exe (AuxiliaryLimits.cpp) and DedicatedServer.exe
        ▼
runtime limits in the services
```

* The writer is the `PrepareSharedData` function of `DedicatedServer.exe`
  (the string `aux_limits.xml` is referenced at `0x4a5001` inside it,
  surrounded by Lua-table readers and `PrepareSharedData.cpp` error sites).
* The readers are `Shard.exe` (function at `0x4d0630`, source file
  `AuxiliaryLimits.cpp`) and `DedicatedServer.exe`.
* **Consequence:** editing `aux_limits.xml` directly works only until the next
  `prepare_shared`; the durable edit is in the Lua source below. The community
  statement "the file is overwritten by prepare_shared" is therefore correct.

**Where the four hard caps come from** *(file, `data/gamedata/shared/reputation.lua`
lines 39-42)*:

| Lua global | Shipped | Written as (`aux_limits.xml`) | Guard in `PrepareSharedData` |
|------------|---------|-------------------------------|------------------------------|
| `ai.vessel_exp_pool_cap` | 5 000 000 | `<VesselExpPoolCap value=…>` | error `vessel_exp_pool_cap is too big. Max value: %d` |
| `ai.event_credits_cap` | 300 | `<EventCreditsCap value=…>` | error `event_credits_cap is too big…` |
| `ai.credits_cap` | 400 000 000 | `<CreditsCap value=…>` | error `credits_cap is too big…` |
| `ai.tokens_cap` | 10 000 (comment `#98284`) | `<TokensCap value=…>` | error `tokens_cap is too big…` |

The caps are 64-bit values in the output (`%I64u`); the maximum accepted
value is a compile-time constant printed in the error text and was not
extracted (shipped values are far below any plausible limit).
**Client side:** `data/ui/scripts/work/uigamefuncs.lua` reads
`ai.credits_cap` / `ai.event_credits_cap` from the *client's own copy* of the
shared Lua to display limits, so a server-only edit shows the old maximum in a
stock client *(file)* - the "client keeps its own copy" claim is correct and
supports Q36.

**Other sections written by the same function** (Lua source → XML section;
names from the executables, the Lua files exist in `data/gamedata/shared`):

| Lua global / file | XML section(s) in `aux_limits.xml` |
|-------------------|-------------------------------------|
| `ai.ReputationByRank` (`reputation.lua`) | `ReputationRank` / `Rank rep=` (must be sorted ascending; the Shard rejects `newRep < lastRep`) |
| `VesselExpPerLevel`, `VesselMaxLvl`, `VesselMaxLevel` (`vessel_grades_progression.lua`) | `VesselLvl` / `Rank` / `Level exp=`, `VesselMaxLevel` |
| `AvailableLobbySettings` (`lobby_settings.lua`) | `LobbySettings` / `Setting levelName gameMode forbiddenOnLive` |
| `UnlimitedPvE` (`unlim_pve.lua`) | `UnlimPve` (credits/resource A, Z, min, max for buffs 1 and 2) |
| `LockRank`, `ClanHighRank`, `AccountAura(s)`, `clan_upgrades.lua` (pairing by name, *inferred*) | `LockRank`/`Race_%d`, `ClanHighRank`, `DailyAuras`, `ClanUpgrades` |
| (further: `PVEMissions`, `ReferralsSettings`, `TutorialRewards`, `Teaching`, `RaidSchedule`, `LeagueTeamSettings`, `FootballSettings`, `TradingLimits`, `TradingTax`, `FreeSpace`, `MilitaryRank`, `Rewards`) | present in the Shard loader; their Lua origin is not listed here |

Validation messages worth knowing (*disasm*, operators see them in the log
when `prepare_shared` fails): `Too many elements in 'ReputationByRank' table`,
`Incorrect amount of elements in 'VesselExpPerLevel' table, must be %d`,
`VesselExpPerLevel[%d] is not a table`, `Invalid ClanHighRank %d. Should be: 1
<= ClanHighRank <= %d`, `Failed to locate 'UnlimitedPvE.player_buff_N_cost.*'`,
and, on the Shard side, `AuxiliaryLimits: ReputationRank error: newRep <
lastRep`, `VesselLvl error: newExp < lastExp`, `AccountRank error: newExp <
lastExp`, `RaidSchedule: Found intersected periods`.

**Not the same thing:** the *daily* iridium cap is the cvar
`sv_tokenCreditsDailyLimit` (default 1000, `default_platform_config.lua`
lines 269/1622) and is independent of `ai.tokens_cap` (10 000, the absolute
holding cap).

## 1a. What a `prepare_shared` run writes *(observed, V-11, 2026-10-13)*

Stock run on the lab node copy (`prepare_shared.bat` command line, Hub
stopped, MongoDB running): 9 s, exit code 0.

* **Files:** 29 `cloud/data` XML files rewritten - `account_auras`,
  `achievements`, `atlas_special_values`, `autogen`,
  `autogen_special_values`, `aux_limits`, `battle_pass`,
  `bot_preset_exclusion_lists`, `clan_emblems`, `clan_quests`, `clan_ship`,
  `faction_rep`, `karma`, `league_equipment_lists`, `medals`, `offers`,
  `quests`, `ship_quests`, `skills`, `starter_pack`, `store`, `titles`,
  `tournaments`, `universe`, `vessel_custom_elements`,
  `vessel_custom_elements_rules`, `vessel_presets`, `war`, `zones` - all
  **byte-identical** to the shipped files. So the shipped XML is exactly the
  generator's output for the shipped Lua, the run is deterministic on this
  data, and hand edits in these 29 files are lost on the next run.
  `special_values.xml` and `regions.xml` (named in the binary) were not
  written; hand-maintained: `loot_tables.xml`, `store_rules.xml`,
  `slot_machines.xml`, `stickers.xml`, `defmod_rules*.xml`, all cfg files.
* **Database:** the run reads and writes two id tables: the **atlas id
  table** `atlas_<db>.ids` (one document `{modules: {<def>: <id>}, counter,
  version}`, 1 205 entries = the 1 205 `atlasId` values in `store.xml`) and
  the autogen id table. These ids persist in MongoDB - a new module def gets
  the next counter value; a node started on a fresh database rebuilds the
  table (whether the ids then match an old database is untested).
* **Log:** `prepare_shared.log` in the profile's `StarConflict
  DedicatedServer` log folder; it prints `Entity Defs hash 71367FCA` for the
  stock build (the value the battle server compares, see
  [hub-protocol-and-framing](hub-protocol-and-framing.md) §6a) and
  warnings about lootable defs without `source_desc`.
* Use `tools/data_drift_check.py` to see which generated files are stale
  after a Lua edit.

## 2. Shard request-flood limiter (Q41)

*(strings + disasm, `Shard.exe`)* The "kick on frequent actions" that
operators complain about exists in the **Shard**, per client channel
(`ShardChannel`), and is configurable by three cvars registered at
`0x5fbc20..0x5fbc7a`:

| Cvar | Engine default | Shipped `shard.cfg` | Meaning (engine description) |
|------|----------------|---------------------|------------------------------|
| `sm_reqFreqCalculationSamples` | `15` | - | "Amount of samples being averaged to calculate request frequency" |
| `sm_reqFreqOverloadLine` | `0.8` | - | "Amount of requests per second considered harmful" |
| `sm_overloadCounterLimit` | `10` | **`20`** (`cloud/data/shard.cfg`) | "Having this much requests over the allowed frequency will induce disconnect" |

Behaviour *(disasm, inferred)*: per channel the request rate is smoothed over
the sample window; each measurement above the overload line increments a
counter, a measurement below it resets the counter to 0 (the counter counts
**consecutive** overloads); when the counter exceeds `sm_overloadCounterLimit`
the channel is disconnected and the log shows
`ShardChannel: Disconnecting <user> due to request spam ( x.xxx rps )`;
at 0.9 × the limit (float constant `0.9` at `0x6082c8`) it logs
`... is close to be disconnected due to request spam`. Rates below
`0.0001` are ignored. `Task_UserProfileGet` has an additional per-user cap
(`Task_UserProfileGet: Too many requests (%d/%d)`); `sm_ignoreRequests`
(default 0) exists in the same cvar family. The numeric unit of the overload
line follows the engine description; the exact comparison direction was not
proven, so tune empirically.

*Operator use:* raise `sm_overloadCounterLimit` / `sm_reqFreqOverloadLine`
in `cloud/data/shard_local.cfg` (the shipped `shard.cfg` already doubles the limit).
Chat flooding is a different mechanism (`ChatServer.exe`, `AntiSpam.cpp`,
cvar family `antispam_*`; DedicatedServer shows the "stop spamming the chat"
warning).

## 3. How the MatchMaker picks the bot preset (Q28, static part)

*(disasm, `MatchMaker.exe`, game creation in `MMQueue.cpp` near `0x419800`)*
The queue's `special` table is copied into the game document. When the game
needs bots, the MatchMaker:

1. looks for `special.botPresetByTier` - if present it is used first and the
   preset is chosen by the tier of the game;
2. otherwise looks for `special.botPresetNames` (an array of names): **one name
   is chosen at random** (`rand() % size`), so a list is a uniform random pick;
3. otherwise uses the empty string;
4. removes `botPresetByTier` and `botPresetNames` from the copied `special`
   and stores the result as the single field **`botPresetName`** (plus
   `queueSpec`, `botsCount`, `botsInTeam1/2`, `coop_vs_ai`, …) in the
   game-session document that the DedicatedServer reads (K5 in
   [implementation-options](../09-community-edition/implementation-options.md)).

So **`botPresetByTier` beats `botPresetNames` when both are set** (the
open point in [bot-presets §6](../05-configuration/bot-presets.md)), and an
unknown preset name is not validated by the MatchMaker (the string is only
copied) - whatever consumes `botPresetName` later has to cope with it
(community reports: typos give matches that never start, not verified here).
The linter [queue_lint](../07-administration/config-validation-tools.md)
catches unknown names before a restart.

**DedicatedServer side** *(disasm)*: `sv_botPresetType` is registered with
default **`0`** (NONE; description string `0 - NONE, 1 - MIRROR, 2 - ADAPTIVE,
3 - MIRROR_AND_SAVE_PRESET`). Together with a non-empty `botPresetName` the
named `AiPreset` is used; with the empty string and type NONE no preset is
selected by this mechanism and the engine falls back to its own default
lineup (the weakened T1 list, `AiPreset.Default`; see
[bot-presets](../05-configuration/bot-presets.md) §4). What exactly the DS
does for an empty name remains a runtime question (Q28 stays open on that
point only).

## 4. Why this matters for a re-implementation (language-neutral)

* The three concerns above are **pure data/contract facts**, independent of
  any implementation language: (a) `prepare_shared` is a *build step* from
  Lua to XML that both Shard and DS consume; (b) client and server read the
  same Lua (`shared/`) so limits/presets edited on one side only create
  display or behaviour mismatches; (c) bot-preset choice is made by the
  matchmaking component and passed as a plain string, so any replacement
  matchmaker only has to provide `botPresetName` (+ counts) in the session
  document.
* The request limiter shows that the Shard defends itself per channel; a
  replacement gateway has to implement an equivalent (or accept stock clients
  being disconnected by nobody and flooding the DB).
* Build-time validation (`PrepareSharedData`) holds many data invariants
  (sorted rank tables, array sizes, non-overlapping schedules) that a
  replacement data pipeline must reproduce or knowingly relax.

## 5. Method notes (so the results can be re-checked)

* String cross-references: the 32-bit images have no ASLR and no
  RIP-relative addressing (S-20), so code that uses a string pushes its
  absolute address; the string literals a function references are
  effectively "the XML keys and messages this function touches".
* Cvar registrations are a constructor call
  `ecx = &static_cvar; push flags; push name; push default; push description;
  call register` - the pushed constants give name, default string and
  description without running anything. The same pattern gives defaults for
  every cvar of every executable (candidate for a generated table).
* Everything above is reproducible on the stock install with any
  disassembler; no decompiler output is quoted.

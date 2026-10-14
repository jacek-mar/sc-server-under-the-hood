# Config validation tools (def names, references, queue block, data drift)

> Small **read-only** helpers for operators who edit the shipped files.
> They address the most frequent failure reports in the community channels
> (see the "demand and problem signals" in the
> [source register](../sources/source-register.md), batch 005): a server that
> no longer starts after a store/quest/loot edit, and a matchmaker block that
> is silently ignored ("match never starts"). They are analysis aids that
> belong to this documentation project; they do not modify any file and do
> not start any service.

Run them inside the project venv, from the repository root:

```
.venv\Scripts\python.exe -X utf8 -I tools\defname_check.py NAME [NAME ...]
.venv\Scripts\python.exe -X utf8 -I tools\queue_lint.py [path\to\default_platform_config.lua]
```

Both default to the private depot copy `sc-server-files/star conflict`; use
`--depot DIR` for another copy (for example the node you edit).

## 1. `tools/defname_check.py`

**Purpose:** tell whether a definition name exists before you write it into
the store, the account (DB), a recipe, a quest or a loot table.

* Index (about 24 500 names): `cloud/data/store.xml` (`defName`, the element
  names used in `<Resources>`/`<Ingr>`) and every `Def.<name> =`,
  `Def["<name>"] =`, `DefItemPrice.<name>`, `AiPreset.<name>` assignment in
  `data/gamedata/def/**` and `data/gamedata/shared/*.lua`.
* Modes: names on the command line, `--names-file`, `--xml <edited store.xml>`
  (checks `defName`, `def`, `resource`, `preset`, `nextShip`,
  `discounted_def`, `requiredShip`, `<Ingr resource=>`), `--lua <edited .lua>`
  (checks `def|defName|resource|item|reward|preset = "Name"` and `Def.Name`
  references).
* Output: `ok` with the defining place (`store.xml:line Item id= type=` or
  `file.lua:line`), `UNKNOWN` with up to three near matches
  (`did you mean: …`). Exit status 1 when anything is unknown.

Example (the names from the batch-005 chat about event ship parts):

```
ok       HeliconCorpse  <- store.xml:2333 Item id=3151 type=5
ok       SalyutCorpse   <- store.xml:10236 Item id=2259 type=5
ok       unreachable_activator <- data/gamedata/def/ex/craft.lua:14763
UNKNOWN  Salyut_Corpse   did you mean: SalyutCorpse, BP_SalyutCorpse, SalyutCorpse_part
```

Limits: a name can exist in the index but still be the wrong *kind* of
definition for the field you put it in (a bundle where a module is expected);
the tool reports the store item `type` to help (0-9 = vessels, modules,
munition, drugs, bundles, resources, blueprints, avatars, mottos, junks - see
[store-zones-rules-semantics](../05-configuration/store-zones-rules-semantics.md)).
Names created at run time by Lua loops (for example the generated `Bots<T>_<sym>`
bot presets) are not in the static index unless the tool lists them
explicitly (the queue linter knows that family).

## 2. `tools/queue_lint.py`

**Purpose:** catch mistakes in the matchmaker block before a restart, using
only the text of `default_platform_config.lua` (no Lua interpreter).

| Code | Class | Check |
|------|-------|-------|
| E1 | error | unbalanced `{ } ( ) [ ]`, unterminated string or long comment |
| E2 | error | `InstantiateQueueTemplate` argument count (must be 7 or 8), non-numeric rank/value |
| E3 | error | min > max (rank, squad rank), `mmValue` min >= max (max is **exclusive**), ranks outside 1..17, values outside 0..100 |
| E4 | error | queue template variable not defined |
| E5 | error | `botPresetNames` / `botPresetByTier` name not in `ai_settings.lua` (generated families `BotsT2..5_{E,F,J,S,M,L,H,P,R}`, `BotsT1_{E,F,J,S,M,L}`, `BotsT35_R` included) |
| W1 | warning | level in `levelsDesc` not in `data/levels/active_maps.list` |
| W2 | warning | `(level, mode)` pair without a `Setting` row in `aux_limits.xml` LobbySettings |
| W3 | warning | missing comma between two `levelsDesc` entries |
| I1 | info | rank × `mmValue` coverage per (queue list, template): ranks and values no queue accepts |
| I2 | info | queues whose `mmSquadRank` range differs from their `mmRank` range (squads are filtered by the squad range; players report squads with bots matched only when both are equal, Q35) |
| I3 | info | a co-op (vs AI) template whose `levelsDesc` includes mode 11 (bomb the base / Detonation); bots are reported not to carry the bomb (Q61) |
| L1 | warning | loot rules (`DedicatedServcerServices_SetLootRules`): a ship rank 1..17 without a row - ships of that rank silently get no loot search after battles |
| L2 | error | loot rules row syntax: each row needs `common`, `rare`, `epic`, each with `lt = "<table>"` and a numeric `iter = {...}`; rank outside 1..17, a rank defined twice (the later row wins), missing comma between rows |
| L3 | info | loot rules summary: which ranks share which tables (printed with the coverage block) |

Reading the coverage block (I1): an account whose `mmRank`/`mmValue` falls
into an uncovered cell is accepted by **no** queue of that template - the
static counterpart of the "squad cannot start" reports (Q35).

Reading the loot checks (L1-L3, added 2026-10-14): each row
`[rank] = { common = { lt = "Table", iter = {...} }, rare = ..., epic = ... }`
picks the after-battle loot tables for one ship rank; the battle server
finds no row for a missing rank and gives no loot search, without an error
line. L1/L2 check the shape and the rank coverage only; whether each table
name exists in `data/gamedata/shared/loot_tables.lua` (including the case
of `_v3`) is checked by [`ref_lint.py`](#2b-toolsref_lintpy) - run both.

### Result on the shipped config (2026-10-11)

```
0 errors, 6 warnings
W1 paper_airplanes (atdm / april team DM / april control templates) and
   s1338_hg_pandora_anomaly (hangar games / one against all): not in active_maps.list
W2 (s1338_pandora_anomaly, mode 29): no LobbySettings row
I1 queuesConfigLo / arcade: ranks 1-17 served; mmValue 99 not served
I1 queuesConfigLo / coop:   ranks 16-17 have no queue; mmValue 99 not served
I1 queuesConfig   / arcade: ranks 16-17 have no queue; mmValue 99 not served
I1 queuesConfig   / coop:   ranks 16-17 have no queue; mmValue 99 not served
```

Interpretation (all *(file)*; the consequences are static inferences):

* **Ranks 16/17 are not served** by the coop templates (both lists) nor by
  the arcade template of the normal-online list; only the low-online arcade
  list accepts them (squad rank still 1-15). Since a small server always uses
  the low-online lists, rank-16/17 accounts can enter arcade but not coop
  queues (matches Q35 / matchmaking-guide §8).
* **`mmValue` 99 is never served** because the last queue uses
  `InstantiateQueueTemplate(…, 51, 99)` and the template's upper bound is
  `$lt`. A player at exactly the clamp maximum (if the MMV can reach 99) is in
  no queue; the shipped intent (queue "51-99") suggests an inclusive upper
  bound was meant. Whether MMV can reach 99 is a runtime question.
* The April/paper-airplane and hangar-games templates reference levels that
  the active-map list does not contain - they are inactive event modes.

### I2 / I3 on the shipped config (2026-10-14)

```
I2 queuesConfigLo / arcadeQueueTemplate: 6 queue(s) with mmSquadRank range != mmRank range (rank 1-17 / squad 1-15)
I3 coopQueueTemplate (line 429): mode 11 (bomb the base / Detonation) on 5 map(s) of a vs-AI template
I3 coopQueueTemplate (line 763): mode 11 (bomb the base / Detonation) on 5 map(s) of a vs-AI template
```

Both are information only (no effect on the exit status): they point at the
places community hosts change for squads with bots and for vs-AI battles
without the bomb mode.

### Loot rules on the shipped config (2026-10-14)

```
L1 line 1315: loot rules: no row for rank(s) 16-17 - ships of these ranks get no loot search after battles

L3 loot rules by rank (common / rare / epic table):
      1-3: CommonRanks_1_3 / RareT1 / RareT1
      4-6: CommonRanks_4_6 / RareT2 / RareT2
        7: CommonRanks_7_8 / RareT3Mono / RareT3
        8: CommonRanks_7_8 / RareT3Mono / NeodiumDrop
        9: CommonRanks_9_10 / RareT3Mono / RareT3
       10: CommonRanks_9_10 / RareT4Mono / RareT4
       11: CommonRanks_11_12 / RareT4Mono / LezortiumDrop
       12: CommonRanks_11_12 / RareT4Mono / RareT4
    13-15: CommonRanks_13_15 / RareT5Mono / RareT5
```

The L1 finding matches the community report that rank 16-17 ships find no
loot (source register S19 SF12). The summary also shows the names
`ref_lint.py` reports as undefined (all `CommonRanks_*` without `_v3`,
`NeodiumDrop`, `LezortiumDrop`; Q45). Tested on modified copies: rows 16 and
17 added -> no L1; a missing comma, a missing `epic` entry, a duplicate
rank, a non-numeric `iter` value and a row `[18]` each give one L2 and exit
status 1.

### Not checked (known limits)

* Lua semantics (the file is parsed textually); a queue built in a loop or via
  a helper other than `table.insert( list, InstantiateQueueTemplate(…) )` is
  not analysed.
* Whether the engine accepts a field value (for example `maxPlayers`) - only
  syntax, arity, names and ranges are checked.
* The mode ids' meaning; see [game-modes](../05-configuration/game-modes.md).
* Loot rules: the `iter` numbers' meaning and balance, and whether a table
  name exists (that is `ref_lint.py`).

## 2a. `tools/data_drift_check.py`

Compares a node's `cloud/data` and `data/gamedata` (more with `--scope`)
with an untouched reference depot and reports, without printing contents:

```
.venv\Scripts\python.exe -X utf8 -I tools\data_drift_check.py <reference "star conflict"> <node "star conflict"> [--out report.md]
```

| Section | What it flags | Why it matters |
|---|---|---|
| File diff | changed / added / missing files (SHA-256) | know exactly what a node differs in before asking for help |
| Generated XML vs Lua | **stale**: a Lua source changed but its generated XML did not (or is older); **hand-edit**: a generated XML changed while its Lua sources did not | the server reads the XML; `prepare_shared` rewrites it from Lua ([config-pipeline-and-limiters](../08-reverse-engineering/config-pipeline-and-limiters.md)) |
| Positional store ids | definitions that take their store id from a load-order counter (`Bundles_`, `Avatars_`, `Mottos_`, `Drugs_` `_GetNextStoreItemId()`), compared in order per file and per family | inserting or removing one shifts every later id |

Pairing rules: same base name (`battle_pass.lua` -> `battle_pass.xml`),
plus `reputation.lua` -> `aux_limits.xml`, `quests_base.lua` -> `quests.xml`
and `data/gamedata/def/**` -> `store.xml`. The set of generated XML files is
the **29 files a stock `prepare_shared` run rewrote** in lab V-11 (*observed*;
`special_values.xml`, `regions.xml`, `loot_tables.xml`, `store_rules.xml`,
`slot_machines.xml`, `stickers.xml` and `defmod_rules*.xml` are
hand-maintained).

Counter parsing understands `Def.Name = {...}` and numeric loops
`for i = a, b do Def["Prefix" .. i] = {...}` including an offset variable
(`nn = 39 + i`); on the shipped build it finds 349 avatar and 349 motto
definitions - the same numbers as the avatar and motto entries in
`store.xml` - 847 bundles and 15 drugs. Family-level order uses sorted file
paths, which may differ from the engine's load order; per-file results are
exact.

Results (2026-10-13): lab node copy (V-9 state) vs depot -> only
`cloud.xml` and `default_platform_config.lua` changed plus their `.orig`
backups, no generated-XML or store-id findings. Synthetic test (scratch
copy: one bundle inserted, `battle_pass.lua` touched, `aux_limits.xml`
edited) -> 2 stale, 1 hand-edit, `Bundles_` order shift reported at the
inserted definition. Exit code 1 whenever files differ.

## 2b. `tools/ref_lint.py`

```
.venv\Scripts\python.exe -X utf8 -I tools\ref_lint.py --depot "<game>"
.venv\Scripts\python.exe -X utf8 -I tools\ref_lint.py --depot "<edited copy>" --reference "<untouched copy>"
```

Finds **dangling references**: a value that should name a definition but
names nothing. Such references fail silently at run time - the stock loot
rules name eight loot tables that do not exist, which empties the arena
reward search (Q45).

| Indexed as defined | Checked as references |
|---|---|
| every `<Registry>.<name> =` / `<Registry>["<name>"] =` table in `data/gamedata` and `sys_data/gamedata` (`Def`, `Spell`, `LootTable`, `AccountAura`, `DefItemPrice`, `ModulePresets`, `VesselTree`, `Materials`, `AiPreset`, ...); `<Item defName>` in `store.xml` (covers names Lua builds in loops); identifiers compiled into `DedicatedServer.exe` and `win64/game.exe` (engine built-ins; `--no-exe` skips them) | `<key> = "Name"` for about 80 reference keys in the game-data Lua (`inherit`, `default_modules`, `spell`, `projectile`, `item`, `bundle`, `loot_table`, `discounted_def`, `reward_account_aura`, ...; texture, model, UI-string and engine-class keys are excluded); loot tables (`lt = "..."`) in `cloud/data/default_platform_config.lua`; `defName=` / `resource=` in `cloud/data/*.xml` |

With `--reference` only findings that the untouched copy does not have are
printed - the ones your edits introduced. `--key` limits the check to some
keys, `--limit 0` prints every location. Exit code 1 when findings are
printed.

**Result on the shipped build** *(file, 2026-10-13)*: about 70 000 defined
names, **184 unresolved key/name pairs** - listed and classified in
[data-invariants](../05-configuration/data-invariants.md) part 2. None of
them stops a node from starting.

**Limits:** names created at run time that are not in `store.xml` are
reported (check by hand); disabled entries are reported like active ones;
values that are not definition names but use a checked key (for example
beacon ids `_first_1` in `shared/adventures.lua`) are skipped only when
they start with `_`.

## 3. Suggested workflow for an operator

1. Keep the edit in `*_local.cfg` / an overlay file where possible
   ([config-system](../05-configuration/config-system.md)).
2. Run `queue_lint.py` on the edited `default_platform_config.lua`; fix
   E-class findings; read the I1 block once.
3. After editing `store.xml`/Lua defs run `defname_check.py --xml …` /
   `--lua …`, then `ref_lint.py --reference <untouched copy>` (nothing new
   may appear).
4. Only then run `prepare_shared` and restart. Back up Mongo before inserting
   defs into accounts.
5. Run `data_drift_check.py` against an untouched copy of the same build:
   no **stale** or **hand-edit** lines, and no store-id family that
   "differs" unless you meant it (then every client needs the same files -
   see [hub-protocol-and-framing](../08-reverse-engineering/hub-protocol-and-framing.md) §6a for the
   battle server's entity-defs check).

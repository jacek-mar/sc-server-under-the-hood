# Config validation tools (def names, queue block, data drift)

> Two small **read-only** helpers for operators who edit the shipped files.
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

Reading the coverage block (I1): an account whose `mmRank`/`mmValue` falls
into an uncovered cell is accepted by **no** queue of that template - the
static counterpart of the "squad cannot start" reports (Q35).

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

### Not checked (known limits)

* Lua semantics (the file is parsed textually); a queue built in a loop or via
  a helper other than `table.insert( list, InstantiateQueueTemplate(…) )` is
  not analysed.
* Whether the engine accepts a field value (for example `maxPlayers`) - only
  syntax, arity, names and ranges are checked.
* The mode ids' meaning; see [game-modes](../05-configuration/game-modes.md).

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

## 3. Suggested workflow for an operator

1. Keep the edit in `*_local.cfg` / an overlay file where possible
   ([config-system](../05-configuration/config-system.md)).
2. Run `queue_lint.py` on the edited `default_platform_config.lua`; fix
   E-class findings; read the I1 block once.
3. After editing `store.xml`/Lua defs run `defname_check.py --xml …` /
   `--lua …`.
4. Only then run `prepare_shared` and restart. Back up Mongo before inserting
   defs into accounts.
5. Run `data_drift_check.py` against an untouched copy of the same build:
   no **stale** or **hand-edit** lines, and no store-id family that
   "differs" unless you meant it (then every client needs the same files -
   see [hub-protocol-and-framing](../08-reverse-engineering/hub-protocol-and-framing.md) §6a for the
   battle server's entity-defs check).

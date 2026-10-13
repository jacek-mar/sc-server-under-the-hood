# Community mod manager "SCPatcher" (Star Conflict Mod Manager v0.1)

> Status: **static review of a third-party tool (2026-10-12).** We read every
> file (about 1 500 lines of Python plus three text files) and checked each
> assumption the tool makes against our copy of the shipped depot with a
> read-only script. We have **not run** the tool against a game folder, so
> its runtime effects stay *(community)*/⚠ until reproduced. Source register
> entry: **S18**.

**Credit.** SCPatcher / "Star Conflict Mod Manager" was written by
**Furebel** (the author's handle, as given in the tool's own README), with
patches the author credits partly to "the SCPP Discord" (the community
preservation project). It was released as `SCModManager_v0_1.zip` in the
community `#general-eng` channel on 2026-10-11 through a temporary download
link. There is no repository yet; the author plans one ("will dive into GitHub
eventually"). No licence is stated. That is why this page quotes only short
excerpts for analysis, with attribution, and does not redistribute the tool.
Get the tool from its author's channel.

## 1. Verdict

| Question | Answer |
|----------|--------|
| What is it? | A small Python/Tkinter **text patcher** for a *local* Star Conflict install (client and server in one Steam folder). It applies "mods" (Python files) to 8 Lua/XML data files, runs `prepare_shared.bat` in the right order and keeps backups. It does **not** touch executables, the database or the network. |
| Is it safe? | **No malicious behaviour found.** No network access, telemetry, obfuscation or binary payloads; standard library only. The risks are by design: **every mod is arbitrary Python** that runs on each start, and a few correctness edges (section 5). Treat third-party mods like executables. |
| Is it useful? | **Yes, for single-player/local nodes.** It packages six community fixes and tweaks in a reversible way. It also contains the first **file-verified explanation of the "empty arena search" bug** (section 4.2). For *hosted* servers it is a reference for edit order and backup discipline, not a deployment tool (client/server data must match, see section 6). |
| What does it tell this project? | (a) The edit order **Lua → `prepare_shared` → generated XML** is what operators need automated. (b) A shipped data defect: 8 of 16 loot-table names referenced by the stock loot rules do not exist. (c) The "patch from the pristine backup, never twice" pattern with SHA-256 fingerprints is a good model for any downstream tooling. |

## 2. Inventory of the release

| File | Lines | Role |
|------|------:|------|
| `patcher.py` | 72 | Entry point: GUI by default; `--cli list/apply/restore` with `--no-bats --dry-run --enable/--disable ID --set ID.key=value` |
| `sc_engine.py` | 448 | Engine: mod discovery, settings, backups, patch pipeline, build-script runner |
| `sc_gui.py` | 347 | Tkinter window (tabs Mods / Tweaks / Advanced, log box, progress bar) |
| `sc_lua.py` | 62 | Text helpers for loot tables (`table_spans`, `strip_loot_entries`, CRLF-safe line handling) |
| `mods/*.py` | 8 files, 471 | The bundled mods (section 4) |
| `README.md`, `MODDING_GUIDE.md`, `IF DOESNT WORK.txt` | | User and mod-author docs |

Requirements: Python ≥ 3.9 with Tkinter, Windows (the build step is skipped
on other OSes). `MODDING_GUIDE.md` refers to `mods/_template_mod.py`, which is
**missing from the v0.1 zip**.

## 3. How it works

### 3.1 Mod format

A mod is one Python file in `mods/` that defines a `MOD` dictionary and an
`apply(files, values, log)` function. `MOD["files"]` maps keys to depot-relative
paths with a **stage**:

* `stage: 'lua'` (default) — written **before** the build scripts;
* `stage: 'xml'` — written **after** `prepare_shared.bat`, "because
  `prepare_shared.bat` regenerates XML" (author's statement; it matches our
  static finding that `PrepareSharedData` writes the generated XML,
  [config-pipeline-and-limiters](../08-reverse-engineering/config-pipeline-and-limiters.md)).

Tweakables (`int`, `float`, `bool`, `choice`, `text`) carry `min/max/step`.
The engine clamps them and stores them in `settings.json` next to the tool.

### 3.2 Pipeline (excerpt, `sc_engine.apply_patches`, abridged)

```python
# 1. back up every target once (game/_SCPatcher_backups/<rel>), record sha256
# 2. patch in memory, always starting from the BACKUP (the original)
work = {rel: read_text(backup_dir / rel if (backup_dir / rel).exists() else game / rel)
        for rel in targets}
for m in active:                      # sorted by MOD['order'], then id
    m.apply(FileView(work, m.files), values, log)   # any exception aborts, nothing written
# 3. write 'lua'-stage files; restore files no enabled mod uses any more
# 4. launch_mongodb.bat (if 27017 closed) -> prepare_shared.bat -> write 'xml'-stage files
```
*(excerpt from SCPatcher v0.1 by Furebel, abridged)*

Properties worth copying into any downstream tool:

* **Idempotent:** a multiplier is always applied to the original value, so
  re-applying never multiplies twice; switching a mod off restores the original.
* **All-or-nothing in memory:** a failing mod aborts before any write.
* **Byte-exact round trip:** files are decoded as UTF-8 with
  `surrogateescape` and split on `\n` only, so CRLF line endings and odd bytes
  survive. In the shipped depot, the 4 loot/def files and the 2 config files
  use CRLF, `quests.lua`/`quests.xml` use LF.
* **Fingerprints:** `KNOWN_ORIGINALS` holds the SHA-256 of 8 pristine files. A
  mismatch is only a warning ("probably edited by hand; verify via Steam").

**Verified:** all 8 fingerprints **match our depot copy** (build
1.99.0.167293), so the tool targets exactly the final build we analyse. The
list includes `data/gamedata/designers_constants.lua`, which no bundled mod
edits (leftover or reserved).

### 3.3 Files it can change

`cloud/data/default_platform_config.lua`, `cloud/data/quests.xml`,
`data/gamedata/shared/{loot_tables,quests}.lua`,
`data/gamedata/def/objects/{ow_loot_tables,openworld_entities}.lua`,
`data/gamedata/def/ex/junk.lua`. Backups and a `manifest.json` go to
`<game>/_SCPatcher_backups/`.

## 4. The bundled mods, checked against the depot

All counts below come from a read-only script run against our copy of the
shipped files. "Match" means the mod's search patterns find exactly what the
mod expects.

| Mod (id) | Default | What it changes | Our check |
|----------|:------:|-----------------|-----------|
| Full arena matches (`arena_bots`) | on | `mm_botsCount` → 23, `sv_kickExcessiveBotsEnabled` → 0; in both `arcadeQueueTemplate` blocks `optimalPlayers` 4→12, `maxExpandTime` 30→60, `maxTimeInQueue` 10→15, `special = { arcade = 1, botsCount = N }` | **Match:** 1 + 1 cvar lines, 2 templates, each `optimalPlayers = 4`, `maxExpandTime = 30`, `maxTimeInQueue = 10`, `special = { arcade = 1 }`. Note: the shipped range of `mm_botsCount` is 0..31 (2026-10-11); "24 players per arena" is the author's statement. Background: [bot-presets](../05-configuration/bot-presets.md), [matchmaking-guide](../05-configuration/matchmaking-guide.md) |
| Arena search fix (`arena_search_fix`) | on | Appends aliases `LootTable.CommonRanks_<r> = LootTable.CommonRanks_<r>_v3` for 6 rank bands to `shared/loot_tables.lua` | **Match, and the bug is real**, see 4.2 |
| More iridium (`iridium_multiplier`) | on, ×10 | Multiplies `Def.Iridium_Junk_r<N>.tokenPrice` in `def/ex/junk.lua` | **Match:** 15 lines (r1 = 32 ... r14 = 239, r15 = 500). Iridium per day is still capped by `sv_tokenCreditsDailyLimit` (1 000) and `TokensCap` ([config-pipeline-and-limiters §1](../08-reverse-engineering/config-pipeline-and-limiters.md)); the mod does not raise those |
| Hidden canisters: no credit junk (`canister_loot`) | on | Removes `ow_*` entries (optionally also `ow_Rare_*`) from `OW2_GoodJunk1..6` in `ow_loot_tables.lua`; never empties a table | **Match:** all 6 tables exist |
| More ore (`ore_drops`) | on, ×5 | Repeats the crate names inside every `asteroid(_premium)_loot_crate` entry in `openworld_entities.lua`; removes credit items from `OW3_Ore{Poor,Normal,Rich,UltraRich}`, recognised by the developers' Russian comment "серебр…" ("silver" = credits) | **Match:** 20 crate blocks, 4 ore tables, 43 lines with the "silver" comment. Uses the developers' Russian comments as data, which is clever but fragile |
| Enemy loot engoodener (`enemy_rarity`) | on, experimental | Rewrites `drop_weight` of `COMMON/BALANCED/SPECIAL/DOUBLE` entries in `OW3_autogen_rnd_poor_13/18` (default 40/40/14/6) | Tables exist; effect not verified (the author is also unsure) |
| GS from missions (`quest_rewards`) | on | Adds `reward_gold_credits` to quests in `quests.lua` (card display) **and** `rewardGoldCredits` to `<Quest>` tags in `quests.xml` (server payout), 3 GS per 1 000 credits; multiplies xenochip rewards ×20 and also converts them to GS | **Match:** 820 `Quests[QuestId.X]` blocks (26 already pay gold), 49 xenochip lines; `quests.xml` has 912 `<Quest>` tags (6 with `rewardGoldCredits`, 12 with `rewardEventCredits`). The 92 XML-only quests ([quests-semantics](../05-configuration/quests-semantics.md)) get gold only from the xenochip/fallback rules, because the mod looks up their credits by name in the Lua. It edits both files on purpose, which is the edit-order question **Q36** |
| Buy everything! (`store_unlock`) | **off**, experimental | `store_allowAllItemsForBying` → 1 | **Match:** 1 line (shipped 0). Author warns: obsolete/dev items can break a save; see [tuning-recipes](../05-configuration/tuning-recipes.md) |

### 4.1 Why the quest mod also says "Xenochips vanish"

The mod description reports that xenochips "disappear from the account in the
offline game". That is consistent with the event-currency cap
`EventCreditsCap` = 300 in `aux_limits.xml` (generated from
`reputation.lua`, [config-pipeline-and-limiters §1](../08-reverse-engineering/config-pipeline-and-limiters.md))
and with Q33 (xenochip balance). It is **not verified**. A ×20 multiplier
would run into that cap at once.

### 4.2 Shipped defect: loot rules reference undefined tables (file-verified)

`default_platform_config.lua` (lines 1315-1335, function
`DedicatedServcerServices_SetLootRules` — the misspelling is in the shipped
file) defines, for each rank 1-15, the loot tables for the post-battle
"search" (`common`, `rare`, `epic` with `lt = "<table>"`). We checked every
referenced name against all `LootTable.<name> =` definitions under
`data/gamedata`, in `cloud/data` and in the extracted pak scripts:

| Referenced table | Ranks | Defined? |
|------------------|-------|----------|
| `CommonRanks_1_3`, `_4_6`, `_7_8`, `_9_10`, `_11_12`, `_13_15` (`common` slot) | 1-15 | **No.** Only `CommonRanks_<band>_v3` exist in `shared/loot_tables.lua` |
| `NeodiumDrop` (`epic` slot) | 8 | **No**, defined nowhere |
| `LezortiumDrop` (`epic` slot) | 11 | **No**, defined nowhere |
| `RareT1`..`RareT5`, `RareT3Mono`..`RareT5Mono` | all | yes |

So on a stock node the `common` reward of every rank and the `epic` reward of
ranks 8 and 11 point at nothing. The community calls this the empty arena
"search" (*(community)* symptom). Two equivalent repairs:

* alias the `_v3` tables under the old names (SCPatcher's way, in
  `loot_tables.lua`, which the client also reads), or
* change the six `lt = "CommonRanks_<band>"` strings in
  `default_platform_config.lua` to the `_v3` names (server-only file, so no
  client change is needed: this is our inference, not tested).

`NeodiumDrop`/`LezortiumDrop` stay undefined either way. Whether the
DedicatedServer logs a warning for a missing table, and what the client shows,
is a runtime question (**Q45**).

## 5. Security and robustness review

| # | Severity | Observation | Advice |
|---|----------|-------------|--------|
| M-1 | High (by design) | **Mods are arbitrary Python.** `discover_mods()` imports *every* `mods/*.py` on each start, so module-level code of **disabled** mods also runs. "Import mod..." runs the selected file (`exec_module`) to validate it *before* the user confirms the copy. The README says so ("pythons can bite you") | Only run mods you have read; never import a mod file just to "look at it"; review the `.py` like an executable |
| M-2 | Low | The path check in `MOD["files"]` blocks only `..`. On Windows, `Path(game) / "C:/x"` resolves to `C:\x`, so a mod's *declared* targets can lie outside the game folder (verified with Python's path rules). The declaration is therefore not a sandbox, though M-1 already implies that | Do not treat the "Changes: ..." line in the GUI as a guarantee |
| M-3 | Medium | **Build step.** It finds `launch_mongodb.bat` and `prepare_shared.bat` by **name** (first match, depth ≤ 3 under the chosen folder, skipping its backup dir). The shipped root `launch_mongodb.bat` only runs `start "" ... launch.bat`, so MongoDB starts **detached**. The later `taskkill /PID <cmd> /T /F` therefore targets a `cmd` that has already exited, and MongoDB most likely **keeps running** after patching (inferred from the batch file, not executed). If it did kill mongod, that would be an unclean stop; our clean-stop recipe is `db.shutdownServer()` ([verification-log](../04-installation/verification-log.md)) | After patching, close MongoDB cleanly. Keep only one depot copy below the chosen folder, so the name search cannot pick a stray or planted `.bat` |
| M-4 | Medium | **Build against a live node.** If port 27017 is already open, it reuses that MongoDB and runs `prepare_shared` while a Hub may be running | Stop the node first (README: "close the game") |
| M-5 | Low | Backups and the manifest live **inside** the Steam folder. "Verify integrity" restores originals but leaves `_SCPatcher_backups`; the next run warns "changed outside the patcher" and still uses the stored backup (correct) | Expected; delete the backup folder only after a full restore |
| M-6 | Low | Several mods report pattern mismatches only as **log lines** (for example `arena_bots` expects "1, 1, 2"). A later game build would be patched partially without an error | Read the log after every apply; a downstream tool should fail on count mismatch |
| M-7 | Info | `IF DOESNT WORK.txt` suggests **disabling the antivirus** as step 3 | Do not; check which file the AV flags and why (no part of this tool needs it) |
| M-8 | Info | `settings.json` stores the game path (can contain the Windows user name) | Do not share `settings.json` |
| M-9 | Info | No network, no registry, no elevated rights, no executable patching, no DB writes | Good: smaller footprint than binary patchers ([docker.md](../04-installation/docker.md) section 3) |

Overall: a careful hobby tool. Backups, idempotence and all-or-nothing writes
are better than most hand-edit recipes in the chat. Its trust model is "you
trust every mod author".

## 6. Usefulness and applications

* **Single-player / local node (target use).** One click applies the common
  quality-of-life fixes in the correct order and can undo them. That covers the
  pain point "edits applied by hand in the right order are error-prone"
  (batch 005 signals).
* **Hosted servers.** Changes to `data/gamedata/**` are client-visible data.
  Several hosts report that clients with **unmodified** data are refused
  (cannot enter battles or the server) after the host changed shared Lua
  (batch 006 I4/R5; Q3). The Shard hash gate is open on a stock node, so the
  cause is data disagreement ([hub-protocol-and-framing](../08-reverse-engineering/hub-protocol-and-framing.md) §6a). A host using these mods therefore has to ship the
  same files to players: the "launcher with manifest" approach other hosts are
  building. Server-only edits (`default_platform_config.lua`, generated
  `cloud/data/*.xml`) do not have that problem.
* **For downstream projects (comparison input, not a recommendation):**
  * the mod format (`MOD` metadata + `apply(files, values, log)`) is a working
    example of a *declarative-target, scripted-edit* plugin model; a safer
    variant would use data-only patch descriptions (regex/table operations) and
    no executable code;
  * the two-stage order (Lua → build → XML) and the SHA-256 baseline match our
    [config-pipeline](../08-reverse-engineering/config-pipeline-and-limiters.md)
    findings and could become a conformance check;
  * the loot-rule defect (4.2) belongs in any "known shipped data bugs" list.
* **For this repository:** confirms Q36 edit order in practice, adds Q45, and
  gives a concrete second producer of the "edit order" demand signal.

## 7. Follow-ups

* Q45 (runtime effect of undefined loot tables) and a proposed test:
  apply only `arena_search_fix` to a lab copy, run one arena battle, and
  compare the search result and DS log before/after.
* Proposed: run `patcher.py --cli apply --dry-run --game <lab copy>` from a
  scratch location (`-I`, separate directory) to confirm the counts above
  match the tool's own log.
* Watch for a public repository and licence; re-run the fingerprint check on
  new versions.

## 8. Reuse policy

Third-party code with **no stated licence**: link to the author's release,
quote only short excerpts with attribution (as above), never copy files into
this CC0 repository. Our verification script stayed in the session scratchpad.
The counts in section 4 can be reproduced with `grep` against the files named
there.

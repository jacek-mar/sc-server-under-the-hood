# Source register

Every claim in the docs should be traceable to one of these. Reliability:
**A** = shipped by Gaijin/Targem (authoritative), **B** = directly observed
by the project (logs/behaviour), **C** = community statement (unverified).

| ID | Source | Location (private) | Rel. | Used for |
|----|--------|--------------------|:---:|----------|
| S1 | Official "Local Game Launch" page + end-of-service notice (saved HTML, 9–10 Oct 2026) | `random-materials/STAR CONFLICT — MMO SPACE ACTION … .html` | A | Architecture list, launch methods, DB handling, language switch, legal terms, mode names |
| S2 | `star conflict/docs/matchmaking.md` | `sc-server-files/star conflict/docs/` | A | Matchmaking guide |
| S3 | `cloud/data/default_platform_config.lua` (+ original comments) | `sc-server-files/…/cloud/data/` | A | cvar reference, queues, schedules |
| S4 | `cloud/data/*.cfg`, `cloud.xml`, `*.xml`, `datasources*.txt`, bat files | same | A | Config system, ports, data catalogue |
| S5 | `win64/local_server.xml`, `launch_server_and_db.bat` | `…/win64/` | A | Local server control by the client |
| S6 | `cloud/mongodb/*` | `…/cloud/mongodb/` | A | DB version, bind, tools |
| S7 | Hub & service logs (2026-10-10-09/10) | `sc-server-files/Targem/StarConflict/cloud/Hub/logs/` | B | Startup order, service ids, DB name rewriting, build id |
| S8 | Client logs | `…/Targem/StarConflict/logs/` | B | Client↔shard ports (3802), shutdown behaviour |
| S9 | ASCII strings of `Hub`, `Shard`, `MatchMaker`, `DedicatedServer`, `Authenticator`, `LoadBalancer`, `ScriptsServer`, `game.exe` | scratch only | B | Console commands, cvar names, LuaJIT |
| S10 | MongoDB data directory listing | `…/Targem/StarConflict/cloud/mongodb/data/` | B | Database names |
| S11 | Community wiki "STAR CONFLICT COMMUNITY EDITION" (editable Google document; local snapshot 2026-10-10, online version re-read 2026-10-14: `https://docs.google.com/document/d/1FVFKNYQdCZJGlXSTMVnP4IPsPz9fFg5pZaMj2B4lx1w`) | `random-materials/STAR CONFLICT COMMUNITY EDITION.md` (snapshot); online: link only | C | Account fields, config tips, Linux, bots; 2026-10-14 delta: battle pass, seed chips, resource limits, new-ship guide (O1-O14) |
| S12 | Discord export `#general-eng` of the "Preservation Project" (batch 001: 5 717 messages, 2026-04-17 → 2026-10-10; batch 002: 5 900 messages, **superset** of 001 +183 from 2026-10-10 13:05–22:03 UTC) | `random-materials/Star_Conflict_Preservation_Project_00{1,2}.1*/` | C | RE leads (pak, RakNet), operator experiences |
| S14 | **Star Conflict game wiki** reference copy (5 381 pages, 3 313 media files, 696 MB; captured 2026-10-10 from the community wiki mirror, historical archive 2026-06-04). *Game* documentation, not server documentation | `random-materials/sc-media-wiki/` | C | Gameplay background (ships, modes, economy, currencies); **not** evidence of server behaviour. Rights unresolved (see its `ATTRIBUTION.md`) → keep private, cite page title/revision only |
| S13 | `files.list` | `…/star conflict/files.list` | A | Depot manifest |
| S15 | Discord export `#general-ru` of the same server, **Russian-language channel**, HTML (Discrub) export: 9 323 messages, 100 authors, 2026-04-20 → 2026-10-11 02:47 (batch 003) | `random-materials/Star_Conflict_Preservation_Project_003.ru-html/` | C | Release-day operator experience (RU community), RE leads, Docker announcement; **not** a superset of S12 (different channel) |
| S16 | Community project "Star Conflict — Unofficial Server in Docker" (GitHub, MIT; scripts/configs only, no game files); local snapshot of 2026-10-10/11 | `random-materials/starconflict-community-edition-docker-master/` | C (claims) / B (byte-pattern check we ran) | Linux/Wine hosting analysis: [docker.md](../04-installation/docker.md) |
| S17 | Fan site "The Outpost" - Server Guide Modules (snippet collection); evaluated page: `default_platform_config.lua` with comments translated to English (`https://www.graviton.at/outpost/server-guide-module/defaultplatformconfiglua-translated-to-english`, seen 2026-10-11); whole Knowledge Base (17 articles) and the Server Setup Guide reviewed 2026-10-14 (`https://www.graviton.at/outpost/base`) | web, link only (not copied) | C (spot-checked against S3: faithful; KB: unnamed or Discord-credited authors, average trust) | Reading aid for the Russian comments; operator how-tos; leads Q51-Q55; see digest below |
| S12/S15 b004 | Batch 004: partial JSON exports `Star_Conflict_Preservation_Project_004.eng-json-part` (23 msgs) and `...004.ru-json-part` (248 msgs, 213 new), both 2026-10-11 | `random-materials/Star_Conflict_Preservation_Project_004.*-json-part/` | C | Digest "batch 004" below; Q32-Q36, S-19 |
| S12/S15 b005 | Batch 005: partial JSON exports `Star_Conflict_Preservation_Project_005.eng-json-part` (155 msgs, 132 new) and `...005.ru-json-part` (389 msgs, 219 new), 2026-10-10 23:26 → 2026-10-11 18:47 (EN) and 12:07 → 13:48 (RU) | `random-materials/Star_Conflict_Preservation_Project_005.*-json-part/` | C | Digest "batch 005" below; Q38-Q40, Q28/Q34 amended |
| S12/S15 b006 | Batch 006: partial JSON exports `Star_Conflict_Preservation_Project_006.eng-json-part` (302 msgs incl. a 2-message release thread, 147 new, 2026-10-11 19:13 → 2026-10-12 09:05) and `...006.ru-json-part` (951 msgs, 485 new, 2026-10-11 13:52 → 2026-10-12 09:15) | `random-materials/Star_Conflict_Preservation_Project_006.*-json-part/` | C | Digest "batch 006" below; Q44-Q46, Q3/Q32/Q36 amended |
| S12/S15 b007 | Batch 007: partial JSON exports `Star_Conflict_Preservation_Project_007.eng-json-part` (64 msgs, 54 new, 2026-10-12 09:19 → 16:15) and `...007.ru-json-part` (229 msgs, 222 new, 09:16 → 16:10); continue batch 006 without a gap | `random-materials/Star_Conflict_Preservation_Project_007.*-json-part/` | C | Digest "batch 007" below (J1-J12); Q24, Q36, Q40, Q46 amended; S-07 note |
| S12/S15 b008 | Batch 008: partial JSON exports `Star_Conflict_Preservation_Project_008.eng-json-part` (83 msgs, 73 new, 2026-10-12 16:50 → 21:03) and `...008.ru-json-part` (255 msgs, 205 new, 16:12 → 21:18); both overlap batch 007 (no gap) | `random-materials/Star_Conflict_Preservation_Project_008.*-json-part/` | C | Digest "batch 008" below (K1-K14); security S-07 note, S-29, S-30; Q47 |
| S12/S15 b009 | Batch 009: partial JSON exports `Star_Conflict_Preservation_Project_009.eng-json-part` (63 msgs, 31 new, 2026-10-12 21:20 → 2026-10-13 06:11) and `...009.ru-json-part` (374 msgs, 199 new, 2026-10-12 21:19 → 2026-10-13 07:38); continue batch 008 without a gap | `random-materials/Star_Conflict_Preservation_Project_009.*-json-part/` | C | Digest "batch 009" below (M1-M9) |
| S12/S15 b010 | Batch 010: partial JSON exports `Star_Conflict_Preservation_Project_010.eng-json-part` (11 msgs, 11 new, 2026-10-13 08:44 → 16:21) and `...010.ru-json-part` (348 msgs, 327 new, 07:46 → 16:16); continue batch 009 without a gap | `random-materials/Star_Conflict_Preservation_Project_010.*-json-part/` | C | Digest "batch 010" below (N1-N13); Q49 amended |
| S19 | Steam community discussions of the game (app 212070): General discussions (56 threads active 2026-10-09 → 10-14) and comments under the official announcements (5 threads); 627 posts, 262 authors; includes the pinned official setup guides (same content as S1) and the forum's rules for unofficial-server posts | `https://steamcommunity.com/app/212070/discussions/` (private local copy) | C (official pins: A) | Digest "S19" below (SF1-SF24); Q62-Q63; Q35/Q45/Q52/Q59 amended ; **re-crawl 2026-10-16** (14 threads, 69 posts newer than the first crawl) -> SF25-SF35 |
| S20 | Public community host's configuration overlay (Git repository `star-conflict-overlay` of the `cosmosim-infra` organisation on the host's own Gitea; 27 commits 2026-10-09 → 10-17; no licence). Sibling repos: `ansible` (Gitea/SSO deployment, not game-related, not read), `doc` (empty) | `https://git.cosmosim.dev/cosmosim-infra` (private local clone) | C (one host's settings) | Store/quest HTTP patch channel (Q72); host tuning examples |
| S21 | Community tool **sc-proxy** ("Star Conflict Shard and Chat Proxy"): Python man-in-the-middle proxy for client ↔ load balancer / Shard / chat with Kaitai packet schemas (`client.ksy`, `server.ksy`), a 249-entry client-message dispatch table (`ac_dispatch_table.json`: id, handler address, `AC_*` name), body decoders and a Qt inspector; Unlicense (public domain); "heavily vibe coded" per its README; last updated 2026-06-25 (captures made against the official servers) | linked from The Outpost (S17) resources; private local copy `random-materials/sc-proxy-2026-10-19/` | B (names verified in our binaries) | Protocol catalogue, Q73 |
| S12/S15 b011 | Batch 011: partial JSON exports `Star_Conflict_Preservation_Project_011.eng-json-part` (99 msgs, 98 new, 2026-10-13 16:45 → 2026-10-14 07:32) and `...011.ru-json-part` (786 msgs, 783 new, 2026-10-13 17:42 → 2026-10-14 11:45); EN continues batch 010, RU leaves a gap of about 90 minutes (16:16 → 17:42) | `random-materials/Star_Conflict_Preservation_Project_011.*-json-part/` | C | Digest "batch 011" below (P1-P15); Q60-Q61, Q49 amended |
| S12/S15 b012 | Batch 012: partial JSON exports `Star_Conflict_Preservation_Project_012.eng-json-part` (286 msgs, all new, 2026-10-14 13:00 → 2026-10-15 21:36; a gap of about 5.5 hours after batch 011) and `...012.ru-json-part` (1 067 msgs, 1 016 new, 2026-10-14 11:46 → 2026-10-15 21:08, continues batch 011) | `random-materials/Star_Conflict_Preservation_Project_012.*-json-part/` | C | Digest "batch 012" below (R1-R19); Q64-Q67; Q44, Q49, Q61 amended; security finding S-31 |
| S18 | Community tool **SCPatcher / "Star Conflict Mod Manager" v0.1** by Furebel (Python/Tkinter text patcher with 8 bundled mods; released 2026-10-11 in `#general-eng` as `SCModManager_v0_1.zip`, temporary download link, no repository, **no licence stated**) | `random-materials/SCPatcher/` | C (claims) / B (fingerprints and patterns checked against S3/S4 by us) | Review: [community-mod-manager.md](../07-administration/community-mod-manager.md); loot-rule defect (Q45) |
| S22 | Discord forum channel `#mod-releases` of the same server (one thread per release; batch 001: 11 threads, 290 messages, 2026-10-11 → 2026-10-20; EN with some RU) | `random-materials/Star_Conflict_Preservation_Project_001.mod-releases-json-part/` | C | Digest "S22" below (MR1-MR9); Q74; Q71 amended |

## Digest of S11 (community wiki)

Contents: process (NoSQLBooster 4.7.5 "or anything that supports MongoDB 2.6"), "INTRO" (Steam launch
spawns two CMD windows = Mongo + Hub), DB property list, Linux/Proton recipe,
and Q&A items: loot-not-found (`sv_lootFailChance`), gold per match
(`reward_bonusGoldFor*`, event period), more bots (`botsCount`), game modes
(`levelsDesc` numbers). All integrated into
[mongodb.md](../06-database/mongodb.md), [matchmaking-guide](../05-configuration/matchmaking-guide.md),
[cvar-notes](../05-configuration/cvar-notes.md), [linux-proton](../04-installation/linux-proton.md).
The wiki has 5 embedded screenshots (Mongo GUI, gameplay-id comment block,
queue template) — extracted copies are not retained.

### S11 update (online version, read 2026-10-14) - delta only

The document roughly tripled since the 2026-10-10 snapshot. Contributors are
named in the document; they stay anonymous here. Code shown only as
screenshots and a chat-attachment link were not followed. Average trust:
recipes from individual hosts. One section (the new-ship guide) is detailed,
dated "checked in game, October 2026", and gives byte layouts.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| O1 | Linux: Proton **9.0-4** works as well as 11.0-2 (tested on Debian 13 with an integrated Intel GPU); the DB can be edited on Linux with **NoSQLBooster 5.2.12** (AppImage, needs the FUSE 2 library); procedure: start the game, close the game and the Hub window, keep `mongod` running, connect to `localhost:27017` | Added to [linux-proton](../04-installation/linux-proton.md) and [mongodb](../06-database/mongodb.md) (our earlier "NoSQLBooster ≤ 4.7.5" was too strict) ⚠ untested by us |
| O2 | Loot not found: `cvars.sv_lootFailChance` (find by name, the line number varies) | Already covered ([cvar-notes](../05-configuration/cvar-notes.md), Q45) |
| O3 | Insignias via the "mole" event: inject the mole crates into the asteroid drop table of `openworld_entities.lua`; each asteroid table line is one crate, the bracketed number its chance, the braces the possible crates; every asteroid type copies the generic one but has its own table per controlling faction | **File-verified:** the asteroid tables have lines `[0.88] = { "LootCrate_OW3_OreUltraRich", ... }`, and the mole crates (`LootCrate_OW2_MoleShipPart`, `..._MoleShipPartNormal`) sit in trailing comments of those lines in the shipped file -> [tuning-recipes](../05-configuration/tuning-recipes.md) |
| O4 | **Tester's Agony** (`Ship_ST_Rank5`): node tree like the Ellydium ships, any basic special module, rank 5-15, model changes with the special module; crafting it always fails with "not enough credits"; workaround: insert a `vessels` entry (with `unlockedMask` / `activeMask` values) | "Not enough credits" matches our file finding: the recipe needs `unreachable_activator` (price 1 000 000 000) as an intentional blocker ([event-ships](../05-configuration/event-ships-mail-and-clan-ship.md)). Grant recipe ⚠; vid handling -> **Q57** |
| O5 | Vessel ids: one author takes "highest `vid` + 1" and is unsure; the new-ship section says take `vid` from collection `counters` (`_id: "vid"`) and increment the counter, because the next purchase consumes the counter; duplicate `vid`s "sometimes cause problems" | Consistent with the schema (`counters` = `{_id: string, c: int64}`); exact behaviour untested -> **Q57** (matters for every hand-made ship grant and for admin tools) |
| O6 | A Lua table fails without a trailing comma (`{{1,"..."} }` breaks, `{{1,"..."}, }` works) | **Contradicted by the stock file:** `battlePassEndTable` in the shipped `default_platform_config.lua` ends with `}}` and no trailing comma; Lua accepts both forms. The breakage was most likely another syntax error -> FAQ (syntax check) |
| O7 | Resource holding limits: `.player_stock_limit` in `prices_tradegoods.lua` (examples: `ow_Impure_iridium` = Vanadium, `iridium_monocrystall`, `processor_block`, `resource_zeta`) | **File-verified:** 148 occurrences in `data/gamedata/def/ex/prices_tradegoods.lua` -> tuning-recipes |
| O8 | Seed chips: `shared/autogen.lua` holds the base class, prices, upgrade costs, effect counts and minimum ranks; effect groups in `def/ex/autogen_common.lua`, `autogen_balanced.lua`, `autogen_special.lua`; classes COMMON (4 common), BALANCED (1 balanced + 3 common), SPECIAL (1 special + 3 common), DOUBLE (2 special + 3 common); `cloud/data/autogen.xml` must change too; owned chips: ids in `autogen_defs.lua` | Consistent with [progression-xml-semantics §6](../05-configuration/progression-xml-semantics.md): `autogen.xml` is **generated** from `shared/autogen.lua` - regenerate with `prepare_shared` instead of editing it by hand (explains the author's inconsistent results) |
| O9 | Battle pass: `creditsEventStart`/`creditsEventEnd` decide when xenochips can be earned and shown; `battlePassStart`/`battlePassEndTable` the event window and active stages; stages must also be uncommented in `shared/battle_pass.lua` and match `cloud/data/battle_pass.xml`; some stages still error because the game checks DLC ownership before giving rewards | Consistent with tuning-recipes (batch 007). New from the file comments (translated from Russian): an empty stage end time means "no end"; player progress is kept for **one** event only and is lost when `battlePassStart` changes; stage 1 and 2 end times must be equal. `premium_dlc` keys are already commented out in the shipped `battle_pass.lua`; the DLC-check claim -> **Q59** (with Q44) |
| O10 | Bot presets: PvE `def/ex/bot_preset.lua`, open world `def/ex/ow_preset.lua` | Files exist (plus `ow_bot_preset.lua` for the open-world AI hulls); covered in [bot-presets](../05-configuration/bot-presets.md) |
| O11 | "How to find the admin-role field": guesses (`role`, `admin`, `gm`, ...) marked as unconfirmed | Answered here: the field is `accounts.admRole` *(observed, V-10)*; privileges come from `web_adm.admRoles` ([admin-tasks-howto](../07-administration/admin-tasks-howto.md) §4a) |
| O12 | **New-ship guide**: a ship is a chain - Lua def (`def/ex/ship.lua`: model, `storeItemId`, `base_preset`, tree icon and position), `prices_ship.lua` (`is_atlas_entity`), client preset (`ship_preset.lua`), `ModulePresets.<base_preset>` (`shared/module_presets.lua`), `VesselTree.<def>` (`shared/vessel_tree.lua`), server preset (`cloud/data/vessel_presets.xml`), strings, icons; model package with 4 meshes, DXT5 texture pairs, skeleton bone records, convex collision; "loose files under `data/` override the pak (`win64/datasources.txt`)", so no repacking; a community asset toolkit reads paks, meshes and textures but does not write them | Server-relevant chain added to [data-files](../05-configuration/data-files.md) (paraphrased; asset byte layouts stay in the source). Loose-file override -> **Q56** (consistent with N1, contradicts F11). `storeItemId` claim -> **Q58** |
| O13 | The client picks up a new model only on a cold start; `Hub.exe` does not exit on its own and the next launch attaches to the old cluster - kill both `game.exe` and `Hub.exe` | Consistent with the client-started local node (`win64/local_server.xml`) leaving the Hub running ⚠ -> FAQ |
| O14 | Client logs in `%LOCALAPPDATA%\Targem\StarConflict\logs\`, crash dumps in `...\exceptions\` | Consistent with S8 -> FAQ |

**Re-read 2026-10-19** (linked again in the RU chat, b014): no new sections
since 2026-10-14; every part maps to O1-O14 or the earlier snapshot. Two
minor points: a shared `battle_pass.lua` with "four passes, DLC requirement
off" (chat attachment, not followed; DLC check: Q59), and the new-ship guide
states that rams and hits use the convex `.mdp` collision hull, not the
visible mesh (client asset; context for b014 U6).

**Re-read 2026-10-20:** the text export is byte-identical to the
2026-10-19 read; no delta.

#### Demand and problem signals (S11 update)

* Hosts want **generous accounts** (currencies, insignias, resources above
  the holding limit) without breaking them - the type-limit warning in the
  document matches Q51/Q52.
* **Special and test ships** (Tester's Agony, custom hulls) are the most
  detailed topic; the shared pain is ship grants by hand (`vid`, masks).
* **Events on demand:** battle pass, xenochips and timed gold rewards all
  hinge on dates in the platform config.
* **Custom content** is moving to the client side (models, textures, icons);
  this raises the client-compatibility questions of Q3/Q36 and the loose-file
  question Q56.

#### Not adopted

Contributor names and credits; the chat-attachment link to a modified
`battle_pass.lua`; screenshot-only code; asset byte layouts (left in the
source, link only).

## Digest of S12 (Discord, anonymised summary of server-project work)

> **Reliability warning.** Statements from chat users are *leads, not facts*.
> Many community members are, however, actively working to understand the
> server and share findings — useful hypotheses and tools come from there.
> Promote a claim into the docs as verified only after checking it against
> files, logs or experiments. Further Discord batches are expected and are to
> be digested here in the same anonymised, summary-only form.

| Period | Theme |
|--------|-------|
| 2026-04-17 → May | Channel for a "preservation project" opened after the shutdown announcement; discussions on packet capture, reverse engineering, legal risk, "no monetisation" |
| May–Jul | Pak unpacking, models/audio extraction, who can host, wishes for a server list; debate "preserve SC vs build a new game" (consensus: make SC1 work without official support) |
| Aug–Sep | Hardware for hosting, Linux/ARM questions, account-migration ideas (ship-preset import) |
| 2026-10-06 | Statement that Gaijin will publish a "distributed version" of the server to run locally; no peer-to-peer |
| 2026-10-09 → 10 | Release day: Mongo GUI version issues, `store_allowAllItemsForBying`, event config in `default_platform_config.lua`, Proton hosting, Docker plans |

Contains personal data (names, avatars, IPs shared by users). It is never
published; only anonymised technical facts are summarised here.

### Batch 002 (2026-10-11) — delta only

Batch 002 is a re-export containing all 5 717 messages of 001 plus **183 new
ones** (no deletions, no edits). Release-day+1 activity by local-server operators:

* Many users now run a local node and tweak it: economy multipliers, loot,
  store bundles, bots, events. Technique: edit Lua/XML in the depot, restart.
  Consolidated, file-cross-checked in
  [tuning-recipes.md](../05-configuration/tuning-recipes.md).
* Recurring questions: where Xenochips come from (events must be active), why
  battle-pass stage 2 errors (commented out / bundles removed), how to raise
  bot tier/aggressiveness, how to pick a PvE mission level (answer: unlocked by
  clearing the previous one).
* Shared mini-findings: `mm_lowOnlineLo/Hi` explain the duplicated queue
  blocks; `botPresetType` / `botPresetNames` / `botPresetByTier` selection
  keys; PvE queue shape (`pve=1`, `gameMode=7`, `botsCount`).
* Networking reports: LAN client → server on a second PC failed for one user
  (feeds Q2/Q3); a community-run public server with its own configuration
  overlay repository exists (matchmaking still described as unreliable); a
  shared "how to run a localhost" document circulates (not part of our sources).
* Statement that local edits cannot affect remote servers — consistent with the
  architecture.

## Digest of S15 (Discord `#general-ru`, batch 003; anonymised summary)

> Same reliability warning as for S12: **leads, not facts.** Names, ids, IPs,
> server addresses and chat quotes are deliberately not reproduced; statements
> are paraphrased and translated into English.

**Scope.** HTML pages of one channel (plus two tiny side threads), messages
2026-04-20 → 2026-10-11. Busiest days: 21 Apr (channel opening, 665), 28 May
(670), 3 Jun (658), 21 Sep (982), **9 Oct (1 076)** and **10 Oct (693)**. About
85 % of the channel is gameplay/balance talk, memes and interpersonal disputes
(out of scope, not recorded). Technically relevant material sits in a few
windows:

| Window | Theme | Class | Value |
|--------|-------|-------|-------|
| 20–21 Apr | Mobilisation, "who can host / pay", legal worries | context | low |
| 14–15 May | First protocol claims by one individual using an AI-assisted emulator: master-server channel is TCP (the LoadBalancer port), RakNet only in battles, booleans bit-packed, AES only for the password, file-hash check server-side; "hangar reached" | RE lead ⚠ (mixed with LLM-generated text in the same thread, e.g. "XOR deobfuscation", "PostgreSQL") | medium |
| May–Jul | Pointers to community repositories: a Go master-server re-implementation (reaches the hangar) and a capture proxy | RE lead ⚠ | medium |
| 3–7 Sep | Pre-release work on the **local battle instance** (loopback UDP 35000), an undocumented multi-instance client flag, RakNet *security layer* patched in a private test client, need for a client patcher and its patch groups (`security` vs. `maxconn/vesselhash/launchconfig/dock_actor`), PvE/open world partly working in a prototype, cost of one instance per open-world location | RE lead ⚠ | **high** |
| 21–24 Sep | Gameplay/meta chat; official statement quoted that every custom server has its own account DB | context | low |
| 9–10 Oct | **Release-day operations:** Mongo GUI versions, `store_allowAllItemsForBying`, DB editing recipes, stat tweaks, bot/rank questions, empty loot points, LAN/remote connection failures, region-specific disconnects, public servers, **Docker image announcement** | operations | **high** |
| 10–11 Oct | Docker project update (reverse-proxy scenarios), client-version question, Linux/reverse-proxy attempts, content-editor ideas | operations | medium |

### Findings worth keeping (with our classification)

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| F1 | A community Docker image runs the node on Linux; stock binaries do not start under Wine without an address-assertion patch | **Cross-checked:** pattern present once in 20/22 exes ([docker.md](../04-installation/docker.md) §3.1) |
| F2 | DedicatedServer crashes at battle start when the node address is not a genuine local address; fixed by a null-call guard | Patch patterns **match** the shipped exe (13/13); *behaviour* ⚠ → DK-3/DK-4 |
| F3 | Mongo must be 2.6 (newer versions break `aggregate` and `system.indexes`) | Plausible; consistent with bundled 2.6.12 |
| F4 | Mongo GUI: only old versions connect (NoSQLBooster 5.2.x and MongoBooster 3.5.x reported) | Consistent with S11/S12 (we had 4.7.5 / 3.x) |
| F5 | Gold/credits/ships/modules are given by editing the account document in Mongo; modules on ships are stored as numeric ids, not names | Consistent with [schema.md](../06-database/schema.md) ✔ |
| F6 | Premium time unit: users disagree (seconds vs. days); a 365-day grant "in seconds" did not take | **Resolved 2026-10-13 (Q27):** `premiumTill` = expiry as Unix epoch **milliseconds** (maintainers + `Shard.exe` static check) - a seconds value lands in 1970, i.e. expired; `give premiumTill` takes hours |
| F7 | `store_allowAllItemsForBying = 1` lifts the "cannot be bought" flag for items; ships may carry the same flag but need a separate check | File-verified for the cvar (shipped `0`); ship effect ⚠ |
| F8 | Identical unique modules per ship are limited by `store_maxUniqueModules` (shipped **3**) and `store_maxUniqueModulesOnPremium` (shipped **2**) | **File-verified** |
| F9 | Bot count lives in the coop queue templates and the starting coop queues; bot rank selection not found | Consistent; rank open (Q28) |
| F10 | Battle-pass stage blocks are commented out in `battle_pass.lua`; removing the markers enables them; some bundles contain other ships' parts | Consistent with S12 digest ✔ |
| F11 | *(+JSON re-export, 11 Oct 05:28-06:00)* Ship stats live in the Lua ship definitions with `inherit` chains (editing a base def changes heirs); base `hull_health`, `shield_max`, `max_speed` are not the final in-battle numbers (modules, bonuses, progression apply); loose Lua files are not read by the client, a **override .pak** is needed for client-visible changes. Lua stat edits: **speed, energy, manoeuvrability** took effect on the user's own server; **damage, hull, radar** did not; others disagree | Mixed ⚠ → Q29 |
| F12 | Extreme damage values crash a battle (overflow of a stored type) | ⚠ plausible, untested |
| F13 | Players from one country were disconnected ~20 s after login on some community servers; a VPN avoided it | Unresolved; regional network path suspected ⚠ (Q26); no server defect shown |
| F14 | "Network error" at connect, `OnDisconnect reason 0` on the console; remote players fail while the node works locally; firewall/AV prompts block first start | Matches Q2/Q3/Q25 and V-8; no new root cause |
| F15 | Client login screen: choose the **server** entry (not *localhost*) and give the IP; the Hub port is the default, a trailing LoadBalancer-style port confused users | *(community)* ⚠ test (Q2) |
| F16 | Loot search points are often empty after battles on community servers | Q12 unchanged; "low chance", not zero |
| F17 | One zone instance per open-world location; a host operator estimates ≈ 1.5–2 GB RAM per instance; shard capacity "32, limited to 24 clients" | ⚠ unverified capacity figures (DK-8) |
| F18 | The tutorial grants permanent premium on a fresh account | ⚠ unverified |
| F19 | A hidden multi-instance flag lets several clients run on one PC | ⚠ not tested |
| F20 | Paks are usable; models are low LOD; hangar assets were ported to another engine by one person | context |
| F21 | Claims that the code base is dangerous/insecure; no concrete vulnerability given | Not evidence; see our audit in [security.md](../07-administration/security.md) |
| F22 | Operators mention reverse-proxy publication, ~USD 40/yr VPS class hosting, donation/monetisation debate | context; terms forbid monetisation ([legal](../09-community-edition/legal-and-licensing.md)) |

### Re-export of the same channel as JSON (2026-10-11)

`random-materials/Star_Conflict_Preservation_Project_003.ru-json/` is the same
channel as the HTML batch, exported later: 9 338 messages (HTML: 9 323), range to
2026-10-11 05:59. All HTML messages are contained; **15 new messages**
(05:28-05:59) were diffed with a scratch script. Content: banter plus one
how-to for changing ship characteristics, summarised in F11 and in
[community-faq.md](../07-administration/community-faq.md). The only
file-checkable part was verified: `data/gamedata/def/objects/ships.lua` exists
with 73 `inherit` entries and the `hull_health` / `shield_max` / `max_speed`
fields. The JSON export replaces the HTML one as the primary S15 source.

### Statements we explicitly do **not** adopt

* Packet-layout details from the May AI-generated summaries (XOR layer,
  AES-128 session keys, PostgreSQL mapping): no evidence; the same thread
  contradicts parts of them.
* "A local battle instance does not use RakNet": rebutted later in the thread
  (the *security layer* is disabled, not RakNet itself).
* Statements about cheating on foreign servers: consistent with server-side
  damage authority (architecture), not tested.

## Digest of batch 004 (partial exports of S12 and S15, 2026-10-11)

> Same reliability warning as for S12/S15: **leads, not facts**; anonymised,
> paraphrased, no names/ids/addresses.

**Scope.** Two *partial* JSON exports (one page each, avatars/emojis only
otherwise): `Star_Conflict_Preservation_Project_004.eng-json-part`
(`#general-eng`, 23 messages, 2026-10-11 00:02 → 11:50, all newer than batch
002) and `Star_Conflict_Preservation_Project_004.ru-json-part` (`#general-ru`,
248 messages, 06:38 → 12:12; 213 not in the 003 JSON re-export, 35 overlap).
There is a gap between the end of the older exports and the start of these
slices (EN: 10 Oct 22:03 → 11 Oct 00:02; RU: 05:59 → 06:38), so a later full
export is still welcome. Both are one-day slices of release-weekend chatter.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| G1 | The Docker project was announced in the EN channel. One operator runs the stock binaries **unpatched under Wine** on a host whose local interface carries a publicly routed address; the Docker author reports crashes only when the advertised address does not belong to the host (dummy/loopback aliases did not help) and none when running via Steam Proton bound to 127.0.0.1; a macOS-Wine run hit an engine-rejected memory address | Supports the Q30 hypothesis (trigger = address not owned by the host), still ⚠; consistent with README of S16 |
| G2 | DB edits are easy but the client only shows them after a **re-login**; no known way to make the server push fresh data; a "hot reload of config" was judged not to help | **Open (Q32)** |
| G3 | Quest rewards can be edited: both `quests.lua` and `quests.xml` must be changed; claimed order: Lua first, then start Mongo and run the prepare `.bat`s, then insert the XML (re-apply the XML after every change). Only one reward is displayed in the quest UI although several can be granted. One operator converted credit rewards to also give gold (1 gold per 1 000 credits) | **File-verified:** both files exist (`data/gamedata/shared/quests.lua` 22 601 lines, `cloud/data/quests.xml` 5 838 lines, QuestGroups). Order/procedure ⚠ untested (Q36) |
| G4 | Xenochips: missions completed but the balance stays 0; nobody could say how to activate them | Matches earlier reports ([tuning-recipes](../05-configuration/tuning-recipes.md), events); **Q33** |
| G5 | Ship parts for event/premium ships can only be obtained through events; two ships with unique craft activators (Salut, Helicon) could not be assembled by any path found | ⚠ Q34 |
| G6 | "Squad cannot start a PvP arena / random mission" asked, no answer | **Q35** |
| G7 | Operators claim to have filled PvP with T5 bots of level 14-15 (screenshots only) | Consistent with Q28; recipe not given |
| G8 | Changing a ship's speed worked (a 800 speed value sends it nearly across the map; a 60 s respawn and the warp speed cap were also removed for one ship); a ship build with three drone types and wide shields was made by file edits | Consistent with Q29 (speed works); ⚠ no files shown |
| G9 | Virtual-LAN tools (Radmin, Hamachi, ZeroTier, port-forward helpers) were tried to let friends join; one operator reports ZeroTier working | Consistent with G1 (address belongs to a host interface); supports Q2/Q25 |
| G10 | Entity (e.g. projectile) definitions are a short list of fields: model ref, effect ref, direct/splash/effect damage, damage type, effect type, speed, lifetime/range | Plausible, generic ⚠ (B-7 will confirm) |
| G11 | Per-player ship customisation without client changes: change slot count / special module of **one player's** ship in the DB (BSON); website-driven ship constructor idea; battle-pass progress to be moved from client to server/website | Idea; feasibility depends on Q36 |
| G12 | Custom content that the client reads from its own `data/gamedata` (battle pass, bot presets, special-module choice) needs files on every player's machine or a custom launcher; `cloud/data` is server-only | Partly file-verified (`battle_pass.lua`, `ai_settings.lua` live in `data/gamedata/shared`); client-side use ⚠ **Q36** |
| G13 | **Password handling criticism** (one person writing an account website for their own server): the client stores a *hash* of the password locally for "remember me", the salt is embedded in the client in clear, and that hash is what is sent as the password, so a leaked server DB allows login without cracking anything ("pass-the-hash"); suggested mitigations: server-side second hashing or session tokens. The transport is believed (not tested) to be TLS; other participants disputed | **⚠ unverified single-source claim**, plausible design; recorded as S-19 in [security.md](../07-administration/security.md), Q24 amended, SV-10 added. Earlier S15 leads: password is AES-protected on the master channel; on 9 Oct a participant noted the client's local data holds login + an "encrypted" password and asked which algorithm is used (no answer) |
| G14 | Fragmentation worry: every operator builds a private server with different goals (stock, rebalance, unlocker); "pirate WoW without an official realm" analogy | context; supports a shared, documented baseline |
| G15 | Open-world pirates activation and removing the timer of the "reconnaissance in force" mode asked, no answer | open; see [zone-events](../05-configuration/zone-events.md) PIRATE event ids and mode ids in [game-modes](../05-configuration/game-modes.md) |

Not adopted: balance opinions (nerf/buff lists, debuff for >9 modifier slots
on green ships, three special-module presets) — design ideas, no technical
content; personal disputes.

## Digest of batch 005 (partial exports of S12 and S15, 2026-10-11)

> Same warning as before: **leads, not facts**; anonymised and paraphrased, no
> names/ids/addresses/quotes.

**How to read this digest.** Most items below describe what *one host*
configured on *their* node (their limits, queue bands, edited defs), not
general server behaviour, and chat is not an infallible source. The recipes
are kept as leads; the main value is the **demand and problem signals**
summarised after the table.

**Scope.** Two *partial* JSON exports, one page each:
`...005.eng-json-part` (`#general-eng`, 155 messages, 132 new, 2026-10-10
23:26 → 2026-10-11 18:47; it closes most of the gap before batch 004 and
extends it by ~7 h) and `...005.ru-json-part` (`#general-ru`, 389 messages,
219 new, 12:07 → 13:48; overlaps the end of batch 004). The RU slice is a
single ~1.5 h window; **both slices end mid-conversation**, so a later
continuous export is still welcome.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| H1 | Players hit a **1 000 iridium limit**; one operator raised it to 100 000 per day with `cvars.sv_tokenCreditsDailyLimit` in `default_platform_config.lua` and a second operator confirmed it worked. Conquest rewards alone reach the limit; the lever is also suggested for rock-mining servers (about 500 iridium per hour of mining reported) | **File-verified:** `sv_tokenCreditsDailyLimit = 1000` appears twice (lines 269 and 1622) in the shipped config; documented in [cvar-reference](../05-configuration/cvar-reference.md). "Daily" matches the cvar name; the effect of raising it is a community report (⚠ untested) |
| H2 | RU operators asked where **currency caps** live in Lua; answer given: `cloud/data/aux_limits.xml` lines 22-25 (experience pool, xenochips, credits, iridium "it seems"); counter-claim: that file is overwritten by `prepare_shared.bat`, so a Lua source must exist; also that the client keeps its own copy and would display old limits | **File-verified (partly):** lines 22-25 are `VesselExpPoolCap 5 000 000`, `EventCreditsCap 300`, `CreditsCap 400 000 000`, `TokensCap 10 000`; both `DedicatedServer.exe` and `Shard.exe` contain the strings `aux_limits.xml`, `CreditsCap`, `TokensCap`. **Answered statically (2026-10-11, Q38 closed):** the caps are Lua globals `ai.event_credits_cap` / `vessel_exp_pool_cap` / `credits_cap` / `tokens_cap` in `data/gamedata/shared/reputation.lua` (lines 39-42); `PrepareSharedData` writes `aux_limits.xml` from them, so "overwritten by prepare_shared" is correct, and the client UI reads the same globals from its own copy - see [config-pipeline-and-limiters](../08-reverse-engineering/config-pipeline-and-limiters.md) |
| H3 | Mail: spam/"letters" caused by caps was a motivation; ships cannot be sent by mail, ship **parts** can | **Answered statically (2026-10-11, Q43 closed):** ships are not a mailable content type (resources/parts are); mail sending is gated by `shard_minAntibotCounterForMailSending` = 50; see [event-ships-mail-and-clan-ship §2](../05-configuration/event-ships-mail-and-clan-ship.md) |
| H4 | **Per-rank bot presets in the queue template.** Recipe shown (one operator, two others used it): call `InstantiateQueueTemplate` several times with different rank bands and pass `{ special = { arcade = 1, botPresetNames = { "<Preset>" } } }` as the last argument; example bands: ranks 1-6 `Medium`, 7-11 `BotsBZS_T4`, 12-17 `BotsBZS_T5`. A second operator saw "match never starts" until a typo/invalid queue was fixed; suggested `maxTimeInQueue = 1` for instant matches; a mistyped config makes the matchmaker silently ignore it | **File-verified:** `InstantiateQueueTemplate(template, minMMRank, maxMMRank, minMMSquadRank, maxMMSquadRank, minMMValue, maxMMValue, addMods)` merges `addMods` with `sys.mergeTable`; `AiPreset.Medium`, `AiPreset.BotsBZS_T4`, `AiPreset.BotsBZS_T5` exist in `data/gamedata/shared/ai_settings.lua` (lines 83, 1137, 1176). **Static result (2026-10-11):** `MatchMaker.exe` checks `botPresetByTier` first, then picks one name of `botPresetNames` at random, then passes a single `botPresetName` to the game session ([config-pipeline-and-limiters §3](../08-reverse-engineering/config-pipeline-and-limiters.md)). **Not verified:** the stuck-match symptom (Q39) and the DS behaviour for an empty name. Example added to [bot-presets](../05-configuration/bot-presets.md) §5 |
| H5 | Squad matchmaking in a mission (PvE) reportedly needs **max players of the PvE queue raised to 4** | Plausible for the squad failure in Q35 (see [matchmaking-guide §8](../05-configuration/matchmaking-guide.md)); the PvE queue's `maxPlayers` was not re-checked here; ⚠ untested |
| H6 | More **asteroid resources**: add entries to the `asteroid_loot_crate` table - each line is a crate, each entry inside the brackets one possible drop; the question came from someone who wanted to know what to write into `openworld_entities.lua`. RU side: premium vs. non-premium players have different asteroid drops "visible in the files" | **File-verified:** `asteroid_loot_crate` appears in `data/gamedata/def/objects/openworld_entities.lua` (first at line 5732, repeated per asteroid class). Premium vs. free split ⚠ not checked |
| H7 | **Event ship parts.** The "Salyut" and "Helicon" parts can be found as store defs `SalyutCorpse`/`SalyutModule` and `HeliconCorpse`/`HeliconModule` (take the `defName` from `cloud/data/store.xml`); writing them directly into the account in the DB works, a typo in the name makes the server crash at start; `store_allowAllItemsForBying = 1` (shipped line 83 = 0) reportedly does not help for those two because **no UI exists to buy them** and **no prices are set** (99 pieces needed per craft); a third ship's final part is `unreachable_activator` in its recipe, so craft recipes (not the store) are the place to change | **File-verified:** `HeliconCorpse` (id 3151) and `HeliconModule` (id 3152) exist as type-5 items, `cantBeBought="1"`, price 100 000; `SalyutCorpse` (id 2259) and `SalyutModule` (id 9271) are also type-5, `cantBeBought` items (price 100 000; checked with [defname_check](../07-administration/config-validation-tools.md)), next to `BP_SalyutCorpse`, `BP_SalyutWing` and the `Bundle_SalyutEvent_*` bundles; `unreachable_activator` is `Def.unreachable_activator` in `def/ex/craft.lua` (price 1 000 000 000, `cant_be_bought`) and appears as `<Ingr ... amount="99">` at `store.xml` line 115297. Q34 answered statically in [event-ships-mail-and-clan-ship §1](../05-configuration/event-ships-mail-and-clan-ship.md) (Helicon parts have no producer in the shipped data) |
| H8 | "All ships complete" achieved on one node through DB edits + admin panel (Mongo-based); templates/decals/paints cannot be granted in bulk except by writing the rows into the account document; an *admin panel* in Mongo is mentioned | Consistent with the account schema ([schema.md](../06-database/schema.md)); no procedure published; **Q40** |
| H9 | Account/regional facts for custom servers: every community server needs its **own registration** (no shared accounts); the operator is responsible for stored passwords; the original server is gone, so the Steam client without patches is "just the client"; "wrong password" after reinstall = different server/registration | Consistent with S-19 and the architecture; no new evidence |
| H10 | **Operator tooling in progress** (no files shown): (a) a Python *mod manager* that takes small edit scripts, lets the operator tweak values and, with one button, runs the batch files and applies Lua/XML in the correct order; first test reported "does not work", then "works but needs changes"; (b) a call-graph/auto-documentation tool for the shipped Lua (parsed with tree-sitter, linked deterministically, per-function summaries written by an LLM - experimental, "hallucination" risk); (c) account/shop websites written in Rust (Dioxus) or similar; registration through a website instead of the in-game form | Context only. (b): any LLM summary is *not evidence* - verify against code. Fits the [implementation options](../09-community-edition/implementation-options.md) "operator tooling" thread |
| H11 | RU debate on **client/server data sync**: `shared` folder = data both sides need; the original developers synced it with game updates; with community servers it is manual, or via a custom launcher (idea: launcher with integrity check + file-system watcher; counter: no protection against memory patching/injection or against players who skip the launcher; real fix would be a server-driven settings import like in sandbox games). A launcher would also allow free client modification | Matches Q36 and the Linux/portable analysis; no evidence about integrity checks in the client binary (⚠, the claim "there are probably none in the binary" is a guess) |
| H12 | RU: "there is an anti-spam/anti-flood limiter on frequent actions" - kick on rapid actions; believed to be compiled into binaries (not Lua/config); an operator plans a Python patcher that NOPs the kick in the binary if no config key is found | **Answered statically (2026-10-11, Q41 closed):** it is in the **Shard**, not Lua: per-channel request-rate limiter, cvars `sm_reqFreqCalculationSamples` (15), `sm_reqFreqOverloadLine` (0.8) and `sm_overloadCounterLimit` (10; shipped `shard.cfg` sets 20); log text `Disconnecting <user> due to request spam` - no binary patch needed, see [config-pipeline-and-limiters §2](../08-reverse-engineering/config-pipeline-and-limiters.md) |
| H13 | RU: a **store edit made the server stop starting**; fixed by removing the added items; suggestions: keep the edited file open to undo, or "verify game files via Steam" (resets all edits) | Matches the established failure mode "invalid ids/defnames make the server refuse to start" (tuning-recipes) |
| H14 | RU: where are the parameters (including loot visibility) of asteroids/containers of the open world? Answer: depends on which; see H6 | see H6 |
| H15 | RU: persistent presence of event ships (like Nagelfar) in the open world asked, no answer; corp **dreadnought build requirement** ("10 rank-9 players") asked in EN, no answer | **Dreadnought requirement answered (2026-10-11):** shipped `clan_shipBuildHighRanks` = 3 (not 10), `ClanHighRank` = 9 - [§3](../05-configuration/event-ships-mail-and-clan-ship.md); persistent event ships still open (Q42/Q10) |
| H16 | RU/EN: the stock "evil" daily/conquest timings are outside some time zones → suggestion to make conquest always available and to update conquest stats hourly; counter-thought: always-available conquest favours players with more hours (zerg effect); ideas: daily conquest point limit or a debuff after a threshold | Design opinions, not adopted (conquest time windows live in `default_platform_config.lua`, see [zone-events](../05-configuration/zone-events.md)) |
| H17 | EN: servers are "much less active than before the game died"; one server named by a user is the most visited; a market-population idea: a *bot account* that posts offers into the market every hour via the DB | Context; market idea idea only; the market storage was not analysed (no verification) |
| H18 | Several requests for premium licence / gold / "how to add money" on a node answered with "farm" or "see the Steam store" | Context; the relevant levers are `gold_on_start`, `premium_on_start`, `auth_infinitePremiumForRoles` (all file-verified earlier, see [tuning-recipes](../05-configuration/tuning-recipes.md)) |
| H19 | EN: a question "how to set a special module in active module slots" (no answer); RU: "how to launch any event on localhost" (no answer); RU: step-by-step single-player guide asked → pointed to the fan site (S17) | open; events: see [zone-events](../05-configuration/zone-events.md) |

### Demand and problem signals (batch 005)

What users were *looking for* or *stuck on*, regardless of whether an answer
given in chat was right. Each signal points at the doc or question that
should serve it.

| Signal | Kind | Where we help / gap |
|--------|------|---------------------|
| Caps feel too low: daily iridium (1000), conquest hits it at once, mining about 500/h; "where are the currency limits in Lua?" | wanted setting | [cvar-reference](../05-configuration/cvar-reference.md), tuning-recipes; answered: [config-pipeline-and-limiters §1](../08-reverse-engineering/config-pipeline-and-limiters.md) (Lua source = `reputation.lua`, regenerated by `prepare_shared`) |
| PvP/PvE bots are rank 1-3 on a small server; want ranked/believable bots | wanted feature | [bot-presets](../05-configuration/bot-presets.md); precedence now known (ByTier > Names, random pick), **gap Q28** (DS behaviour for empty name) / Q39 |
| Matches that never start or start after leaving the queue after a queue edit; Lua brace/comma errors | config problem | bot-presets §5 pitfalls; [queue_lint](../07-administration/config-validation-tools.md) (syntax, arity, names, coverage); **gap Q39** (runtime symptom) |
| Squad cannot enter PvE/PvP | config problem | matchmaking-guide §8; **gap Q35** |
| Server will not start after a store edit (mistyped def names) | config problem | tuning-recipes, FAQ; [defname_check](../07-administration/config-validation-tools.md) |
| Event-ship parts (Helicon, Salyut, a third ship) cannot be obtained; all-ships/all-cosmetics unlocks | wanted feature | tuning-recipes; **gap Q34/Q40** |
| Persistent event ships, launching an event on localhost, special module in active slots, corp dreadnought requirement | wanted feature, unanswered | **gap Q42**, [zone-events](../05-configuration/zone-events.md) |
| Anti-flood kick on frequent actions annoys operators | wanted setting | answered: [config-pipeline-and-limiters §2](../08-reverse-engineering/config-pipeline-and-limiters.md) (Shard `sm_*` cvars) |
| Edits do not reach clients / need relogin / client keeps old limits; no server-driven settings sync | architecture limit | **gap Q32/Q36**; [implementation-options](../09-community-edition/implementation-options.md) |
| Edits applied by hand in the right order (Lua, bat files, XML) are error-prone; operators build mod managers | operator pain | [administration](../07-administration/administration.md); idea: documented, scripted apply order |
| Newcomers ask for a short "what to open, what to edit" single-player guide; "how to add money / premium" | onboarding gap | [quick-start](../04-installation/quick-start.md), FAQ; levers `gold_on_start`, `premium_on_start` |
| Accounts do not carry between servers; password storage is the host's job | expectation gap | [security](../07-administration/security.md) S-19 |
| Remote friends joining a localhost node (ports, firewall) | config problem | [verification-log V-9](../04-installation/verification-log.md), Q2/Q25 |

Not adopted: server naming/branding talk, website and domain plans, personal
account-recovery disputes (a progress-recovery request on one operator's
server), opinions on the original developers' architecture (summary: "two
binaries on an old Mongo" - consistent with our own findings, no new facts),
jokes and screenshots.

## Digest of batch 006 (partial exports of S12 and S15, 2026-10-11/12)

> Same rules as before: **leads, not facts**; anonymised and paraphrased; no
> names, ids, addresses (several public server IPs were posted - not copied),
> server names or quotes. The only name used is the tool author's,
> because it is the attribution of a released tool (S18).

**Scope.** EN: 147 new messages, 2026-10-11 19:13 → 2026-10-12 09:05,
including the mod-manager release thread. RU: 485 new messages, 2026-10-11
13:52 → 2026-10-12 09:15; it closes the RU gap after batch 005 and runs into
the morning. A large part is off-topic (hardware/AI chat, banter).
As before, most recipes describe **one host's** node.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| I1 | A host added ten rank-9 accounts to the DB and to their corporation, but the **dreadnought build** stayed locked until the DB/services were restarted | Consistent with the shipped gate `clan_shipBuildHighRanks` = 3 at rank `ClanHighRank` 9 ([event-ships-mail-and-clan-ship §3](../05-configuration/event-ships-mail-and-clan-ship.md)): ten were more than needed. "Effective only after restart" supports **Q32** (no live refresh of DB edits) |
| I2 | **Mod manager released** (the "Python mod manager" from b005 H10a): GUI, sliders, backups, runs the batch files, bundled community patches | Reviewed statically: [community-mod-manager.md](../07-administration/community-mod-manager.md) (S18). Benign code; all 8 file fingerprints match our build |
| I3 | Arena "search" after a match gives nothing; a community fix aliases the `CommonRanks_*_v3` loot tables | **File-verified root cause:** the stock loot rules reference 8 undefined tables (6 × `CommonRanks_<band>`, `NeodiumDrop`, `LezortiumDrop`) - [community-mod-manager §4.2](../07-administration/community-mod-manager.md); runtime effect **Q45** |
| I4 | **Balance edits on the server lock out unmodified clients.** EN: after "balance tweaks" players could no longer join matches with the standard Steam client. RU: removing ships from craft/purchase through Lua flags made the host's own client unable to enter the server; adding a third weapon slot server-side and removing it again made the client crash on entering battle | Strong runtime signal for the **data-hash / version gate (Q3)** and client-side data (Q36). Static basis: the Shard checks `game version` and a data-hash list ([hub-protocol-and-framing §6](../08-reverse-engineering/hub-protocol-and-framing.md)). Which files are hashed is still open. **Follow-up (same session):** the Shard gate is open while its hash list is empty (stock), so the cause is data disagreement; positional store ids and the battle server's entity-definition check explain it - [hub-protocol-and-framing](../08-reverse-engineering/hub-protocol-and-framing.md) §6a |
| I5 | **Launchers to distribute modified clients.** Two hosts are building one: multiple download sources, a manifest regenerated after each file change ("generate" command), a small file server (one in Rust), English localisation, open source planned; reason given: "otherwise players are not let into battle". Hashing ~12 GB for the manifest was mentioned | Context/demand: the operator-side answer to I4. Not evaluated (no code yet). Note the official warning that clients trust servers (S-17): a launcher that downloads executables increases that trust |
| I6 | Legal: "risk of distributing a modified client and server?" - answer in chat: the community manager's guideline is "do not make money with it"; RU host plans **donations** ("tip the admin") alongside registration rewards (6 months premium on sign-up, 7-day premium for daily log-ins via a website) | Our [legal-and-licensing](../09-community-edition/legal-and-licensing.md) records the official terms (no monetisation, "Unofficial Server"); whether voluntary donations are compatible is **not** decided here (downstream/legal question). Website-driven rewards = more demand for an admin plane (Q40) |
| I7 | **Anti-flood auto-kick** "for doing too many actions": raise the value in `Shard.cfg` from 20 to e.g. 900 | **File-verified:** `cloud/data/shard.cfg` line 6 `set sm_overloadCounterLimit 20` - exactly the cvar of Q41 ([config-pipeline-and-limiters §2](../08-reverse-engineering/config-pipeline-and-limiters.md)). The effect of 900 is untested; a very large value effectively disables the limiter |
| I8 | **Crediting DLCs** to restored accounts is the missing piece for one host's account-restoration effort; "all battle-pass cosmetics are in test mode" | **Static (this session):** DLC ownership is checked by the Shard (`Task_UpdateDLCOwnership`) through `SteamWebAPI_GetPublisherAppOwnership`, which needs the empty publisher key; DLC prices/contents come from collections `steamDlcPrices`/`yupDlcPrices`/`arcDlcPrices` (`LoadDlcPrices`), and bundles are in `data/gamedata/def/objects/bundles_dlc.lua` (`Bundle_DLC_*`, "used in DLC, do not change"). A cvar `dbg_simulatedSteamDlcOwnership` (string, Shard) exists. New **Q44** |
| I9 | Giving yourself a special ship: copy the DB data of a *similar* ship (manufactured from manufactured, non-customisable from non-customisable) and change `defName` - written up in a community document | Consistent with Q40/schema; recipe unverified |
| I10 | **Custom seed chips** live in `autogen.xml` | **File-verified:** `cloud/data/autogen.xml` and `autogen_special_values.xml` exist; `AUTOGEN` contents with grades `BALANCED/SPECIAL/DOUBLE` appear in DLC bundles. Semantics not documented yet (B-4 rest) |
| I11 | The Outpost fan site (S17) has a new **server setup guide** page; one university firewall blocked the site | **Resolved 2026-10-14:** guide read; its content (port 3850, `hub_detachChildProcesses`, Redis via `db_redisHost`, `auth_allowInternalAutoCreate`, `-lang`, mode names, shutdown order, `cosmosim_<user>`) matches our docs; nothing new - see [S17 KB review](#s17-knowledge-base-review-2026-10-14) |
| I12 | RU: **local server "authorisation error"**; both batch files open and close at once; fix reported by one host: in `cloud/mongodb/launch.bat` set `MONGO_DATA_PATH` to a folder next to `launch.bat` instead of the `%LOCALAPPDATA%` path. Another suggestion: use the Docker project | **File-verified:** shipped `launch.bat` uses `%LOCALAPPDATA%\Targem\StarConflict\cloud\mongodb\data` and creates it if missing. The cause is unknown (⚠ hypothesis: a profile path that MongoDB 2.6 cannot use, e.g. non-ASCII user names, or permissions). Added to the FAQ as a diagnostic |
| I13 | RU: "there was a setting that shows the windows of **all services** on Windows" | **File-verified:** `cloud/data/hub.cfg` line 6 `set hub_detachChildProcesses 1`; binary description "launch server applications without a window". Setting 0 should show the service consoles (⚠ untested) - FAQ |
| I14 | RU: wish for the client to **start in "server" mode and remember the address**; answers: "patch the exe" or put a short name for the server's IP into the Windows `hosts` file | **Static lead (this session):** the client's `config.cfg` (in `misc.pak`) runs `exec address.cfg`, but no `address.cfg` ships and `game.exe` does not name it; the client has `net_masterServerAddress` ("master server load balancer network address", default empty). Whether a user `address.cfg` with that cvar presets the server is **Q46** |
| I15 | RU: a heavily modified client can join *any* server; one user says only energy (maybe speed) changes took effect, another that speed does not | Unverified; relevant to [security §4.2](../07-administration/security.md) "Cheating in battle" (DS assumed authoritative). Lab item, not a fact |
| I16 | RU: the client's resource **links** (forum etc.) are easy to redirect to one's own | Consistent with `net_masterServer*Url` cvars (news feed, status, version, addresses) commented out in the client `config.cfg`; see [binary-endpoints-and-options](../08-reverse-engineering/binary-endpoints-and-options.md) |
| I17 | RU: connection to a community server failed with a network error; worked through a VPN, or after toggling UPnP on the home router (not reproducible) | Q2/Q25 context; client-side NAT behaviour unknown; no conclusion |
| I18 | RU: request for the **password-hash algorithm** (salt, iterations) so that admins can reset forgotten passwords; also a 2FA wish | Demand signal for Q24/S-19. **Not pursued** (maintainer decision, 2026-10-11: the key-derivation thread stays closed); recorded as demand only |
| I19 | Hidden/test ships surface on modded nodes (alien "Biomorph" hulls flown by players, a premium "Palom" `Ship_Race2_L_T1_Premium`, a rank-15 "decor" test ship); alien hulls pull their default loadout and crash if it is removed | Context; `store.xml` ships with `cantBeBought` are the source ([ship-defs](../05-configuration/ship-defs.md)); stability claims unverified |
| I20 | Ecosystem: at least four community servers in RU alone, with different philosophies (classic progression vs. heavily rebalanced); an automated Lua documentation generator (tree-sitter + LLM summaries, b005 H10b) shown again; ReShade works with the client, DLSS injection did not | Context only (LLM summaries are not evidence) |

### Demand and problem signals (batch 006)

| Signal | Kind | Where we help / gap |
|--------|------|---------------------|
| Hosted servers with edited shared Lua lock out stock clients; hosts build launchers | architecture limit | **Q3** (which files are hashed?), Q36; [community-mod-manager §6](../07-administration/community-mod-manager.md); edit server-only files where possible |
| Arena search gives nothing | shipped bug | answered: [community-mod-manager §4.2](../07-administration/community-mod-manager.md); runtime Q45 |
| Anti-flood kick annoys players | wanted setting | answered: `sm_overloadCounterLimit` in `shard.cfg` (Q41) |
| DLC content for restored accounts | wanted feature | **Q44** (static start in this digest, I8) |
| Local node "authorisation error", batch windows close immediately | config problem | FAQ (MongoDB data path, service windows via `hub_detachChildProcesses`) |
| Client should default to a server and remember its address | wanted feature | **Q46** (`address.cfg` hook) |
| Dreadnought build, DB edits needing restarts | config problem | event-ships §3, **Q32** |
| Password reset for forgotten passwords, 2FA | wanted feature | Q24/S-19 (not pursued); admin-plane requirement for downstream projects |
| Custom seed chips, special/alien ships, all-cosmetics | wanted feature | I10 (`autogen.xml`), Q40 |
| Donations / registration rewards on hosted servers | legal/demand | [legal-and-licensing](../09-community-edition/legal-and-licensing.md) (official terms only) |

Not adopted: hardware and AI-model chat, firewall product opinions, store
platform opinions, server advertising (addresses not copied), personal
banter, balance opinions about individual ships.

## Digest of batch 007 (partial exports of S12 and S15, 2026-10-12)

> Same rules: **leads, not facts**; anonymised and paraphrased; no names, ids,
> addresses or quotes.

**Scope.** EN: 54 new messages, 2026-10-12 09:19 → 16:15. RU: 222 new
messages, 09:16 → 16:10. Both follow batch 006 directly. A large part of the
RU slice is ship talk and banter.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| J1 | **Password storage:** the stored value is a single SHA-256 pass, lowercase hex, over a fixed prefix that is the same for every account plus the password as typed (UTF-8, no trimming, no case folding - a stray trailing space matters) | **Confirmed by a value-free check** (2026-10-12, [verification-log V-9 addendum](../04-installation/verification-log.md)): two independent test passwords MATCH as typed, lower-cased variants do not; trimming untested. The constant is deliberately not reproduced. Consequences in [security S-07](../07-administration/security.md) |
| J2 | A host plans a **web password reset** for its server | Demand signal: with J1 an admin could compute the value; V-9 confirms that copying a known value is a possible reset path |
| J3 | **Battle pass stages 2-3:** after uncommenting them in Lua, completing a stage of phase 2 errors; fixed by using a `battle_pass.xml` that contains `Bundle_Battle_Pass_2_X` entries | **File-verified:** shipped `cloud/data/battle_pass.xml` names only stage-1 bundles (41×), `data/gamedata/shared/battle_pass.lua` stages 1-4 (2-4 commented out) -> the XML must be regenerated (`prepare_shared`) or replaced after enabling stages ([config-pipeline-and-limiters](../08-reverse-engineering/config-pipeline-and-limiters.md)) |
| J4 | How to start an event / the battle pass: "`default_platform_config.lua` lines 6-19" | Pointer only; see [zone-events](../05-configuration/zone-events.md) and the battle-pass notes in [tuning-recipes](../05-configuration/tuning-recipes.md) |
| J5 | **Seed chips:** `autogen.xml` holds `affixId` + `name`; editing the affix defs only affects newly generated chips; request for a translation of the Russian comments in `autogen.lua` | **File-verified + translated** (comments are cp1251 shown as mojibake): `data/gamedata/shared/autogen.lua` - "description of how many affixes, and from which groups, each autogen class contains"; "**classes must not be removed from here, otherwise already rolled modules become invalid and can no longer be re-rolled**"; further comments: sell price from storage, per-upgrade-level growth of each rolled value, cost formula from average roll / average affix rank / summed affix cost coefficients, upgrade price multipliers per level `{1,2,3,10}`, donor-experience coefficient |
| J6 | **Granting ships** through Mongo: add an element to the account's `vessels` array (a large JSON object per ship; each needs a **unique `vid`**); some ships are invisible in the tree unless granted; alien (brawl) ships appear in the tree only if `data/gamedata/def/objects/gameplay_leviathan.lua` (tree position and icons) is also in place | Consistent with schema (`accounts.vessels`, Q40); **file-verified** location of `gameplay_leviathan.lua` (game data the client also reads) -> such edits must reach clients |
| J7 | `sm_overloadCounterLimit 20` in `cloud/data/shard.cfg` is "the limit on requests to the server" | Already documented (Q41, b006 I7) |
| J8 | "`store.xml` is not synchronised by the script" | Unverified; relevant to Q36 (`prepare_shared` writes store XML from the DB according to our static analysis) -> V-11: `prepare_shared` rewrites `store.xml` (byte-identical on a stock install) |
| J9 | Brawl "Hunter" ship flown in the open world yaws randomly (probably AI logic of its PvE origin) | Context; no action |
| J10 | Moving progress from the official servers is impossible (the official database stayed with the developers); on one's own server items can be granted by hand or via huge resource amounts | FAQ |
| J11 | Ecosystem: a **generic module for the AMP hosting panel** is in progress; hosts plan to add items to drop tables; opening a local server to the internet "took 5-10 minutes" | Packaging context ([linux-native-and-portable-server](../09-community-edition/linux-native-and-portable-server.md) L4); Q25 now answered for LAN |
| J12 | **Player-base fragmentation:** concern that many servers scatter the small community; ideas: a public server list and a client-side app that reads it | Demand signal; static lead Q46 (`address.cfg` preset) and login-screen behaviour (V-9: the `server` entry takes a free address) |

### Demand and problem signals (batch 007)

| Signal | Kind | Where we help / gap |
|--------|------|---------------------|
| Password reset / password handling on hosted servers | wanted feature | J1/J2 + V-9 (no salt, copy-reset path) |
| Enabling later battle-pass stages fails | config problem | J3 answered (regenerate or replace `battle_pass.xml`) |
| Understanding seed-chip (autogen) data | knowledge gap | J5 translation; B-4 rest (`autogen.xml` semantics) |
| Granting ships, alien ships in the tree | wanted feature | J6; Q40; client-side file requirement |
| Player-base fragmentation, server discovery | ecosystem | J12; Q46; downstream topic (server list is outside this repository) |
| Hosting panels (AMP), quick internet exposure | packaging | J11; security profile C, minimal ports (V-9) |

Not adopted: ship balance opinions, wishes for new factions, banter,
AI-assistant tool recommendations.

## Digest of batch 008 (partial exports of S12 and S15, 2026-10-12 evening)

> Same rules: **leads, not facts**; anonymised and paraphrased; no names, ids,
> addresses, server names or quotes.

**Scope.** EN: 73 new messages, 2026-10-12 16:50 → 21:03. RU: 205 new
messages, 16:12 → 21:18. Large parts are screenshots without text, nostalgia
and banter. The EN slice is dominated by a launcher/file-distribution thread
and its security debate; the RU slice by new players asking how to join
private servers and by hosts talking about progression design.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| K1 | A **community launcher** (public repository, same author as the Docker project S16) lists servers and downloads per-server client files from a host's file server (hashed manifest); today it ships a modified client for one server; planned: fetch the unmodified Steam client and take only Lua/assets from third-party servers | Ecosystem context (watch list); a launcher/server list is a downstream product, outside this repository. Relevant inputs here: minimal client file set, [S-29](../07-administration/security.md) |
| K2 | Review of that launcher: do not recommend running its service as `root`; serving unsigned code over plain HTTP is risky; trust-on-first-use with a self-signed certificate suggested; counter-view: fine on a LAN/VPN | Security guidance for any distribution channel -> S-29 recommendations |
| K3 | **The game's Lua runtime is not sandboxed**: shell execute, arbitrary file write and the FFI library would give third-party Lua full code execution on the player's PC; mitigation ideas: strip FFI/shell/file functions from the interpreter, Windows process-mitigation policies, AppContainer or restricted tokens; Wine/CrossOver as a "sandbox" was disputed | **Partly supported statically** (2026-10-12): FFI library names (`cdef`, `metatype`), `package.loadlib`, `loadstring`/`dofile` are compiled into `game.exe` **and** `DedicatedServer.exe`; `game.exe` imports `ShellExecuteA`; names `os.tmpname`/`io.popen` are absent (os/io libraries possibly trimmed); no shipped Lua uses `ffi`/`os`/`io`. Whether `ffi` is reachable from scripts is open (Q47). -> **S-29** |
| K4 | "There are two version checks in the client and one in the server; the server one can be bypassed by hard-coding the client's values" | Unverified; related to Q3 (stock data-hash gate is open) and V-10 (client version string sent in clear in the first login frame) **Static check (2026-10-13): partly right** - one client check (HTTP version URL, warning only, off on stock clients), server checks at the Shard (build + data-hash list) and the battle server (protocol 14, build, entity-defs hash); the build checks need no patch (`net_checkVersion 0`, build `local`, last version part may differ), the entity-defs hash cannot be disabled by config - [hub-protocol-and-framing.md](../08-reverse-engineering/hub-protocol-and-framing.md) §6a |
| K5 | Alien bosses and an "unreleased" alien destroyer can be spawned in an open-world hub by editing that hub's `zone_mission.lua`; the destroyer has 1 000 000 000 HP, "fixed" by editing `def/objects/cargoship.lua` | **File-verified, framing corrected:** `Def.AlienCruiser_EventDestroyer` (`data/gamedata/def/objects/cargoship.lua`) is commented "for the open-space event - a copy from raid `pve_raid_waterharvest`", `health = 1000000000 --100M test, 1G live` - an intended live-event value, not a bug; the stock `data/levels/global_world/_campaign/hub_jer_rock_terramorph_e_ow/zone_mission.lua` already references it as an alien boss (`boss = true`). Server-side Lua decides battle stats (V-10) |
| K6 | Boss and alien models made flyable for players; a creature given a special module from another def ("is it only a texture?" debate) | Modding demand; client must have the same defs/models |
| K7 | A host broke `autogen.xml` and asked for a copy | `cloud/data/autogen.xml` is a shipped (generated) file: restore it from the Steam depot (verify files) or regenerate; keep backups before hand edits (`tools/data_drift_check.py` finds such edits) |
| K8 | How to change the stats of xenochips one already owns | Owned chips are per-item records; affix edits only affect new rolls (b007 J5); Q33 |
| K9 | **Joining a private server:** start `win64\game.exe` directly (a Steam start also launches the local server and its windows); on the login screen switch the bottom-left selector from `localhost` to the server entry, paste the address every time, log in with a name (not an e-mail); the old pre-Steam launcher is useless | Consistent with V-9 (`local_server.xml` auto-start, `server` entry takes a free address, port pre-filled 3801) and V-10 (no address preset) -> FAQ |
| K10 | Old official accounts cannot be used (the database was not released); advice not to type official credentials into private servers - one new player already did; every server needs its own account | Security note added to **S-07** (unsalted fast hash + global prefix: a host can test guesses offline) -> FAQ |
| K11 | "The local server accepts connections from any address" | Consistent with V-1 (services bind 0.0.0.0) -> **S-30** (client-started local node on player PCs) |
| K12 | A second, independent Docker build: native Linux MongoDB container + a Wine container for the services ("the shipped DB schema saves the reverse-engineering"); the S16 author mentions Wine on macOS mis-handling addresses -> crashes that needed patches | Linux/Docker labs LX/DK, Q30; [linux-native-and-portable-server](../09-community-edition/linux-native-and-portable-server.md) |
| K13 | Several public community servers run; a host restarts every ~15 min while tuning; hosts soften the grind with rank-up bonuses; a host plans an **admin panel to hand out resources**; demand for full grants and unlocked ships | Admin-task interface verified in **V-10** (`give`, `mute`, `playerInfo`; documents need `pickedBy: 0`) -> [shard-admin-tasks](../08-reverse-engineering/shard-admin-tasks.md); restart churn -> [settings-reload-map](../05-configuration/settings-reload-map.md) |
| K14 | Design wishes: fuel in the open world, full-PvP open world; T5/T6 craft parts are hard to get because the player market is dead on small servers | Demand signal; Q34 (part producers); design decisions are downstream |

### Demand and problem signals (batch 008)

| Signal | Kind | Where we help / gap |
|--------|------|---------------------|
| How to join a private server, where to find servers | onboarding | K9 -> FAQ "Multi-user / hosting"; server list = downstream (K1) |
| Credential reuse from the official game | security | K10 -> S-07 note, FAQ |
| Trust in launcher-distributed client files and Lua | security | K1-K3 -> S-29, Q47 |
| Resource/ship grants without DB hand-editing (admin panel) | wanted feature | K13 -> V-10 admin tasks |
| Restart-heavy tuning | operations | K13 -> [settings-reload-map](../05-configuration/settings-reload-map.md) |
| Restoring a broken generated file | config problem | K7 -> FAQ |
| Boss/event content in the open world | modding | K5 -> tuning-recipes |
| Craft parts unobtainable without a market | economy | K14 -> Q34 |
| Hosting on Linux (Docker) | packaging | K12 -> LX/DK labs |

Not adopted: server recommendations, UE5 remake debate, nostalgia about
older game versions, banter.

## Digest of batch 009 (partial exports of S12 and S15, night of 2026-10-12/13)

> Same rules: **leads, not facts**; anonymised and paraphrased; no names, ids,
> addresses, server names or quotes. A public server address posted in the
> chat was not copied.

**Scope.** EN: 31 new messages, 2026-10-12 21:20 → 2026-10-13 06:11. RU: 199
new messages, 2026-10-12 21:19 → 2026-10-13 07:38. Low signal: most of the RU
slice is nostalgia about old balance (implants, bosses) and banter; several
messages are screenshots without text.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| M1 | The S17 page with the translated platform config was briefly unreachable (unpublished while its markup was fixed); the site renders Lua/XML/config snippets with display problems and asks for snippets or screenshots | Link still valid (S17); link-only policy unchanged |
| M2 | "How do I unlock the **Experimental Destroyer**?" | **File-verified:** "Experimental destroyer" is the display name of the open-world pirate-event **boss** `Def.Ship_OW_Boss_PirateEvent` (`data/gamedata/def/ex/ow_bot_preset.lua`, `inherit = "Ship_Gen_Boss_Empire_Destroyer"`, `ship4bot = true`, hull 40 000 000, shield 8 000 000, `max_speed` 23, boss modules, hangar icons `icon_error`). It is an AI ship, not a player ship - there is nothing to unlock. Community figures of "50 M hull / 10 M shield" refer to similar boss hulls; battle values are decided by the server Lua (V-10) |
| M3 | Ellydium (alien) ships on community servers: the first three are "relatively obtainable" but need **"gs"** for the starter pack; hosts add "gs" to PvE/PvP rewards | "gs" = **Galactic Standards**, the premium currency (`goldCredits` in `accounts`; string table: "not enough Galactic Standards"). Hosts can grant it with the verified `give` admin task (`value: "goldCredits"`) - [admin-tasks-howto](../07-administration/admin-tasks-howto.md); reward edits -> [tuning-recipes](../05-configuration/tuning-recipes.md) |
| M4 | A "hidden" alien ship added to an account directly in MongoDB **cannot move**; its modules look like destroyer modules | Unverified. Lead: AI and boss hulls (`ship4bot = true`; 1 800+ such definitions across the bot/NPC preset files) carry AI-only modules and boss models; whether such a hull is flyable by a player, and what stops it moving, is open -> **Q49** |
| M5 | Several hosts have already added alien ships and an alien boss creature as playable ships; requests for a **step-by-step guide "what to add where"** for non-programmers; reply: it has to be added on the server **and** the client | **Supported by static analysis:** the battle server compares an entity-definitions hash over definition names with the client's and refuses a client with different definitions (`DR_BAD_GAMEDATA_VERSION`, not switchable) - [hub-protocol-and-framing](../08-reverse-engineering/hub-protocol-and-framing.md) §6a; only the client and the battle server read `data/gamedata` - [gamedata-readers](../05-configuration/gamedata-readers.md) -> FAQ |
| M6 | A host built a launcher to distribute client files after four days of work ("on localhost it is easy, for remote players it is hard") | Same demand as b008 K1; security S-29 |
| M7 | A host clears Redis before opening the server ("junk left in it") | Redis is used by the LeaderboardServer ([service-summaries-static](../08-reverse-engineering/service-summaries-static.md)); **Static answer (2026-10-13):** Redis is disabled on a stock node (`db_redisHost` commented out in `common.cfg`); when enabled it holds only leaderboard sorted sets (`<leaderboard>` and `<leaderboard>:<cid>`) and optional logger lists - [service-summaries-static](../08-reverse-engineering/service-summaries-static.md) §4 |
| M8 | Wish for a "classic" server: no dreadnoughts, no open world, only 15 ship ranks and the commander (captain) mode; a guess that drop rates are set in the matchmaker | Queue set and modes are server configuration ([queue-reference](../05-configuration/queue-reference.md), [game-modes](../05-configuration/game-modes.md)); loot is set by the loot rules in the platform Lua and the Lua loot tables (Q45), not by the matchmaker |
| M9 | A host wants to **load-test** a public node to know whether the machine is big enough | No load data yet; known figures: idle node ~1.2 GB RAM, 19 processes; CPU starvation on 2 cores (V-1, V-5). Lab idea: bot-only battles on a node copy |

### Demand and problem signals (batch 009)

| Signal | Kind | Where we help / gap |
|--------|------|---------------------|
| Adding ships/content: what goes on the server, what on the client | modding | M5 -> FAQ "Modding"; a full guide is a gap |
| Alien ships, premium currency | economy | M3 -> FAQ, admin tasks |
| Boss hulls as player ships | modding | M2, M4 -> Q49 |
| Capacity planning | operations | M9 -> gap (no load figures) |
| Classic queue set | configuration | M8 -> queue reference |

Not adopted: nostalgia about old balance (implants, boss fights), AI-art,
streaming chatter, insults.

## Digest of batch 010 (partial exports of S12 and S15, 2026-10-13 daytime)

> Same rules: **leads, not facts**; anonymised and paraphrased; no names, ids,
> addresses, server names or quotes. A server web address posted in the chat
> was not copied.

**Scope.** EN: 11 new messages, 2026-10-13 08:44 → 16:21 (videos, thanks to
a community host, one economy question). RU: 327 new messages, 07:46 →
16:16. The RU slice is mostly modding: alien and boss hulls as player
ships, craft recipes, and a host announcing a public server with its own
launcher and reward website. Many messages are screenshots without text,
or banter.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| N1 | Localised text does not have to be packed back into a `.pak`; the client reads it from a folder | Consistent with the virtual file system: the `datasources*.txt` roots and the mounted `.pak` archives form one tree, and the shipped client already reads loose `data/gamedata` files ([data-files](../05-configuration/data-files.md), "Search roots"). The string tables are `strings/<language>/string.txt` inside `data/strings.pak` *(observed in an extraction)*. **Static (2026-10-14, Q56):** for an equal path the packed copy wins; a loose `string.txt` therefore does not replace the one in `strings.pak` - the report may describe a client whose packed copy was changed or removed |
| N2 | Where are the module parameters of the alien ships and the biomorph hull? | Module definitions live in `data/gamedata/def/ex` (weapon → projectile → spell chain) - [module-defs](../05-configuration/module-defs.md). AI-only boss modules are separate definitions with an `_Mob` suffix (for example `Module_BossHealManta_Mob`) *(file)* |
| N3 | Craft recipes: one player first looked in `store.xml`; another pointed to `craft.lua`; the "iron plates" are called `Iridium_plate` internally; destroyers used to be built from resources and faction parts that are still in the files | **File-verified:** blueprint recipes are `BP_*` definitions with `craft_ingredients` in `data/gamedata/def/ex/craft.lua` (36 765 lines, exported from a designer spreadsheet; 1 346 definitions); ship recipes are `craftable_reagents` in `def/ex/ship.lua`; `store.xml` holds the compiled form (`<Ingr resource=... amount=...>`), generated by `prepare_shared`. `Iridium_plate` is the "Metal blank" resource (store id 3546, type 5), not iridium. Edit the Lua, then regenerate. Whether every old destroyer part still has a producer was not checked (Q34) |
| N4 | Xenochips are generated automatically and saved chips are stored in the account; overwriting an existing chip is hard, copying it and editing the copy is easier | Consistent with the seed-chip model: classes in `autogen.xml`, rolled items in `accounts.autogenItems` - [progression-xml-semantics](../05-configuration/progression-xml-semantics.md), invariant I-4 in [data-invariants](../05-configuration/data-invariants.md) |
| N5 | A host found how to start a **PvE custom game alone**: change the minimum player count from 3 to 1; there are no allied bots then | **File-verified:** `cvars.lobby_reqPlayersPvEMin = 3` and `lobby_reqPlayersPvEMax = 4` in `ConfigureLobbyServer()` of `cloud/data/default_platform_config.lua` (lines 1832/1834; comment "minimum/maximum players to start a PvE lobby" - our translation). The platform Lua assigns it, so a `lobby_server_local.cfg` cannot override it ([settings-reload-map](../05-configuration/settings-reload-map.md)). Bots in custom games are a lobby option (advanced options: 0 or 8-24 bots + skill preset; LobbyServer `botsInTeam1/2`); **V-12 (observed):** the bot selector is shown for PvP custom games only, PvE lobbies have none and list no raids; raid games always get `botsCount 0` from the MatchMaker (Q50) -> [tuning-recipes](../05-configuration/tuning-recipes.md) |
| N6 | Adding a ship takes at least four files (ship definition, ship tree, ship prices, server store) plus models. A dreadnought model on a destroyer definition flew, but took no weapons or modules and its special module did not work; the number of guns is tied to the model ("hardpoints in the model"); the ship did not appear in the ship list. A special module placed in an ordinary slot works only partly | **Supported statically:** every hull class maps each module slot to a **named bone of its model** (`slot_bones`, for example `PRIMARY_WEAPON_01 = "gun"`, `ACTIVE_01 = "gun_1"`), together with `weapon_slots` and `fire_sectors` (`data/gamedata/def/objects/ships.lua`) *(file)*. A model without these bones has nowhere to mount weapons and modules *(inferred)*. Prices are in `def/ex/prices_ship.lua`; stats, special module and recipe in `def/ex/ship.lua` *(file)*. The ship-list cause is not checked. New definitions also need the same client files (entity-definitions hash, see M5) |
| N7 | Boss and alien hulls as player ships: the "Manta" alien boss can be added and has a gun and three active modules but **neither moves nor turns**; one alien guard definition "has no model"; a scripted alien boss is only a model moving along a path; bot tiers exist for a large biomorph hull | **Static facts for Q49:** `Ship_OW_Boss_Manta` (`def/ex/ow_bot_preset.lua`) inherits `Ship_Manta` → `Ship_Precursor_Predator` → `Ship_Large_Precursor`; it inherits `max_speed` 19, has its own engine grade table, a physics mass of 50 000 (the same as the player destroyer base class `Ship_HUGE`), `ship4bot = true` and an AI behaviour `avtomat = "BossEasyPatrol"`. Speed, engine and mass values therefore do **not** explain why it does not move. `Ship_OW_Alien_Guard` has no model line of its own and takes the model of `Ship_Precursor_Interceptor_Big`. `Ship_Biomorph_Large_T1..T3` are PvE bot presets (`def/ex/pvebot_preset.lua`, `bot_rank` 17). Runtime cause still open -> **Q49** |
| N8 | A host opened a public server: some ships removed for balance, slower progression, rewards (daily, rank-up, starter) handed out by a **website that writes into the game database**, statistics read from the database; adding a resource crate to the store required modified client files; joining from an unmodified Steam client fails for quick battles, so players use the host's launcher; the host plans to patch the client to preset the server address and has removed the request limiter | Consistent with the entity-definitions rule (M5, I-1) and the open Shard data-hash gate on stock nodes; a database-writing website is a product outside this repository - the supported write path for grants is the admin-task queue ([admin-tasks-howto](../07-administration/admin-tasks-howto.md)); address preset = Q46; request limiter = `sm_overloadCounterLimit` (FAQ). Security of launcher-distributed files: S-29 |
| N9 | Review of that launcher: it installs into the user profile without a folder choice, then modifies the game folder the player selects; "download threads" = parallel file downloads | Ecosystem context (watch list). A launcher that rewrites the selected install changes the client files for every server; keep a separate copy for servers that need modified files |
| N10 | "What can the GM and support roles do? I set one on my account and saw nothing in the game" | `accounts.admRole` is checked by the Shard for admin tasks (privileges from `web_adm.admRoles`; `root` always allowed) and by `auth_infinitePremiumForRoles` (shipped `gm;support` = infinite premium) - [admin-tasks-howto](../07-administration/admin-tasks-howto.md) §4a, [masterserver-enums](../08-reverse-engineering/masterserver-enums.md) (`Privilege`). **Static answer (2026-10-13):** the only client privilege checks are in the chat moderation UI (punishment entry with Mute/Ban for `mute`/`ban` holders); no script checks `gmView`/`observeGames`; on a stock node `web_adm.admRoles` is empty, so `gm`/`support` hold no privileges - which matches "saw nothing" |
| N11 | Why split the small player base over many servers? Answer: every host has a different idea of the game; others want an unchanged game with balance votes. A backend rewrite in another language and a hardened Lua runtime for client mods are discussed | Demand signal (server list, fragmentation); option analyses in [09-community-edition](../09-community-edition/) compare trade-offs only; Lua runtime surface: S-29, Q47 |
| N12 | On a community server iridium is the bottleneck: "at least some iridium after battles?" | Iridium = `tokenCredits` with a daily cap `sv_tokenCreditsDailyLimit` (FAQ); battle rewards are server Lua/config. Demand signal for currency-source tuning |
| N13 | The client reportedly refuses to run in a Remote Desktop session | **Confirmed statically (2026-10-13):** at start-up `win64/game.exe` calls `GetSystemMetrics(SM_REMOTESESSION)` and, in a remote session, shows "Sorry, this application does not support remote session!" and exits; no command-line switch skips it (`-multiCopies` only skips the single-instance check that follows) -> FAQ |

### Demand and problem signals (batch 010)

| Signal | Kind | Where we help / gap |
|--------|------|---------------------|
| Adding ships: which files, why weapons do not mount | modding | N6 -> tuning-recipes, FAQ "Modding"; an end-to-end guide is still a gap |
| Boss/alien hulls as player ships that do not move | modding | N7 -> Q49 (static half done, runtime open) |
| Craft recipe edits | modding / economy | N3 -> FAQ, tuning-recipes |
| Solo PvE custom games | configuration | N5 -> tuning-recipes |
| What admin roles do in-game | administration | N10 -> FAQ |
| Iridium and credit sources on small servers | economy | N12 -> FAQ (daily cap); reward tuning is a gap |
| Rewards from an external website writing into the DB | operations | N8 -> admin-task queue as the supported write path |
| Server fragmentation, server lists | community | N11 -> downstream |

Not adopted: unreleased alien modules with odd effects (curiosities, no
server relevance), videos and screenshots without text, server naming
jokes, insults.

## Digest of batch 011 (partial exports of S12 and S15, 2026-10-13 evening → 2026-10-14 noon)

> Same rules: **leads, not facts**; anonymised and paraphrased; no names, ids,
> addresses, server names or quotes. Server and video addresses posted in the
> chat were not copied.

**Scope.** EN: 98 new messages (loot-table and ship-modding tips, a public
host's change list, game-mode mix, an updated community knowledge base, a
long chat about PvP tactics). RU: 783 new messages, most of them a flame
war and off-topic talk; the useful part is about database editing for
newcomers, alien and boss hulls, imported 3D models, the request limiter,
game modes for bots, karma, seed chips and multi-region hosting.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| P1 | Newcomers: "how do I edit the database?" - start `cloud/mongodb/launch.bat`, connect a MongoDB GUI (NoSQLBooster **5.2.12**, the version the community recommends for the bundled MongoDB 2.6) to `127.0.0.1:27017`, edit, close everything, stop the database with Ctrl+C, **then** start the game. Another player edits while playing and only relogs; a third saw errors when starting the game from Steam while the database window was open. A Linux how-to for the same tool was added to a community guide | Consistent with our rules: write while the Hub is stopped or through the admin-task queue; the Shard holds online accounts in memory (Q32, [mongodb §3a](../06-database/mongodb.md)). The Steam errors match the client's **local-server autostart**: a Steam start runs `win64/game.exe -launchLocalServer`, which starts MongoDB on the same data folder and port, plus the Hub, from `win64/local_server.xml` *(observed V-5; Steam launch entries, static)* - a second `mongod` on a data folder already in use fails *(inferred)* -> FAQ |
| P2 | A host pushed a post-battle "search" loot table that now includes iridium and may tune the chances | Loot rules are set in the platform Lua (`DedicatedServcerServices_SetLootRules`), tables in `data/gamedata/shared/loot_tables.lua`; the shipped rules reference undefined tables (Q45, fixed by the `_v3` names) *(file)* |
| P3 | Alien weapon on any ship: one line in `ship.lua` (the boss hull's weapon, with the hull name replaced) and the weapon slot emptied in the hangar - in battle the ship fires the alien gun | **Corroborates the static answer to Q55** (`default_modules` are applied at spawn when the slot is empty) - [tuning-recipes](../05-configuration/tuning-recipes.md) S11 table. Second independent report; still not run by us |
| P4 | Two players ask how to get bots into Special Operations | Answered statically: the MatchMaker writes `botsCount 0` for every raid game; no configuration route (Q50, V-12) |
| P5 | The "Manta" boss hull still neither moves nor turns. Workarounds: put the ESM warp-jump module on the weapon buttons and "teleport"; or copy the parameters of a working alien hull ("Zeta") and keep only the Manta model. A player also listed the alien hulls now flown on community servers ("Woodlouse" - internal name `multiped` per the chat - four biomorph hulls, the Manta) | Q49 stays open (runtime). **New static fact:** the biomorph (7 definitions), open-world boss (13), open-world alien (10) and alien predator hulls declare **no seed-chip slots** of their own (`default_slot_mask` / `slot_bones` without `AUTOGEN_0n`), while crafted rank-14/15 hulls declare 4/5 (`def/ex/ship_green.lua`) *(file; checked along the inheritance chains 2026-10-14 - no parent declares them either)* - matches P9 |
| P6 | A public host lists its changes: a "dreadnought speedrun" (a corporation with one level-10 player builds a basic dreadnought in seconds), new accounts get rank-10/11 ships and some free synergy, and fewer kicks "for spending money" | Clan-ship requirements: `clan_shipBuildHighRanks` and `ClanShipKF` ([event-ships](../05-configuration/event-ships-mail-and-clan-ship.md)). **New-account kit (file):** `data/gamedata/shared/starter_pack.lua` (`StarterPack`: currencies, resources, items, `Vessels` with modules and `put_in_battle_slot`) -> `cloud/data/starter_pack.xml` via `prepare_shared`, read by the Shard (string in `Shard.exe`); stock kit = one T1 ship, zero currencies (three more T1 ships commented out on 2025-09-04, per the file's Russian comment); free synergy = cvar `synergy_on_start` (default 0, all services). The kicks = Shard request limiter (P7) |
| P7 | "Kicked while buying/crafting": set the request limit from 20 to 999 in the file next to the platform config | **File-verified:** `cloud/data/shard.cfg` line 6 `set sm_overloadCounterLimit 20` (Q41 solved; [config-pipeline-and-limiters](../08-reverse-engineering/config-pipeline-and-limiters.md)). The platform Lua does not assign it, so `shard_local.cfg` also works *(static)*. 999 effectively disables the per-channel spam protection - a trade-off for public servers (Q41) |
| P8 | Game modes: PvP shows only "bomb" and "captain" modes; it is "configured in the matchmaker"; a host reduced Detonation in PvP and removed it from co-op vs AI because **bots do not handle the bomb**; another found the mode lists `4,9,11` in the platform config and a fix for bots stuck with the bomb | **File-verified:** both the arcade and the **co-op vs AI** templates of the low-online queue set list `{4,9,11}` (control, sentinel = "recon", bomb the base = "Detonation") for five maps ([queue-reference](../05-configuration/queue-reference.md)). Whether AI bots carry and plant the bomb is untested -> **Q61**; the bot fix is not described |
| P9 | Newly added hulls cannot take seed chips, only crew changes | Consistent with the static fact in P5 (no `AUTOGEN` slot declarations on alien/boss hulls) |
| P10 | A player changed their **karma** and now "is not let in anywhere"; others suspect a ship/module tier mismatch ("tech level") after adding ships | **File (karma, translated comments):** `data/gamedata/shared/karma.lua` - five levels each way (thresholds 1 000 / 15 000 / 50 000 / 150 000 / 500 000; the comments give ranges such as `[10;19]`, so the stored value is probably the displayed one ×100 *(inferred)*), `KarmaLevelOfPoliceEnemy = -1` (below that level a player is a "very dangerous criminal" for police NPCs), police raids triggered by fast karma drops (`designers_constants.lua`); karma reset costs 500 GS (`KarmaResetCost` in `special_values.xml`). Nothing found that blocks entry by karma; the actual refusal is unexplained -> **Q60** |
| P11 | How to grant tournament paints? How to edit seed-chip values? | **Static answer:** paints, patterns and decals are *custom elements* (`data/gamedata/shared/vessel_custom_elements.lua`, e.g. `4cb_tournament`) and stickers (`shared/vessel_stickers.lua`, group `TOURNAMENT`); bundles grant them as `ai.BundleContent.CUSTOM_ELEMENT` with the element name, the admin task `giveVesselCustomElement` (fields `uid`, `item`; privilege propertyEdit) grants one directly, and the admin mail has attachment type 16 `LAT_CUSTOM_ELEMENT` ([admin-tasks-howto](../07-administration/admin-tasks-howto.md) §4b) ⚠ untested; tournament reward sets and schedule: `shared/tournaments.lua`. Seed chips: rolled chips are stored in the account (N4), classes in `shared/autogen.lua` ([progression-xml-semantics §6](../05-configuration/progression-xml-semantics.md)) |
| P12 | Custom 3D models: "all paks can be unpacked, so models can be changed"; a player showed a ship model from a TV series added to the game; others warn that copyrighted designs risk a takedown even without money involved | Archive format: [tpak-format](../08-reverse-engineering/tpak-format.md); mounting needs the named bones (N6) and the same client files (entity-definitions hash, M5). Legal note: third-party designs are a separate risk from the publisher's terms ([legal-and-licensing](../09-community-edition/legal-and-licensing.md)) |
| P13 | Multi-region hosting "in miniature": one database with several nodes in different places, like the official service; today players need a separate account per server. For players in one country, traffic filtering can raise ping from 30 to 300 ms for hours - a regional server would help. Testing such setups in virtual machines was suggested | `cloud.xml` allows several `<Node>` elements, each with its own `address`, `region` and `dediServerHost` *(file; topology notes in [architecture](../03-architecture/architecture.md))*; a real multi-node run is untested (lab backlog). Accounts per server: each node has its own database (`cosmosim_<user>`). Demand signal for shared accounts and regional battle servers |
| P14 | A community member is rebuilding the game with AI help on Unreal Engine 5, as "another game" to avoid legal trouble; heated debate | Context for [09-community-edition](../09-community-edition/) (option E, full clean-room); nothing adopted |
| P15 | Modding "feels like black magic" for non-coders; the chat is unsearchable - mods should go to a mod site; the community knowledge base (S17) added comments and an editor beta | Demand signal: end-to-end guides and a mod catalogue; S17 stays link-only |

### Demand and problem signals (batch 011)

| Signal | Kind | Where we help / gap |
|--------|------|---------------------|
| Safe database editing for newcomers (tool, order, game closed?) | operations | P1 -> FAQ; admin-task queue as the safe path |
| Kicked while spending (request limiter) | configuration | P7 -> FAQ (file-verified) |
| Starter kit for new accounts, free synergy | economy | P6 -> tuning-recipes |
| Mode mix per queue; bots and the bomb mode | configuration / AI | P8 -> queue-reference; Q61 |
| Boss/alien hulls: movement, seed chips | modding | P5, P9 -> Q49 |
| Account refused after edits (karma, tiers) | modding / support | P10 -> Q60 |
| Cosmetic rewards (tournament paints) | administration | P11 -> FAQ |
| Shared accounts across servers, regional servers | hosting | P13 -> architecture; multi-node lab is a gap |
| Mod distribution and beginner guides | community | P15 -> downstream / gap |
| Bots in Special Operations | configuration | P4 -> Q50 (not configurable) |

Not adopted: PvP tactics and nostalgia, the flame war, hardware and phone
debates, image-generation talk, film-ship wish lists beyond the legal note.

## Digest of batch 012 (partial exports of S12 and S15, 2026-10-14 noon → 2026-10-15 evening)

> Same rules: **leads, not facts**; anonymised and paraphrased; no names, ids,
> addresses, server names or quotes. Server, site and file-host addresses
> posted in the chat were not copied.

**Scope.** EN: 286 new messages - playable boss and pirate hulls, "all ships"
account arrays, public servers and their mode lists, Wine start-up times,
a community re-implementation of the services, and an undisclosed security
report. RU: 1 016 new messages, again mostly a flame war and off-topic talk
(operating systems, hardware, personal disputes); the useful part repeats the
hull-modding recipes and adds a community launcher and toggle-mode modules.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| R1 | **Security:** a host reports an attack vector that lets a game client run **administrative console commands** (such as entering maintenance mode) and through them **arbitrary Lua, including shell calls**, on the server; details are withheld until a fix exists; the host keeps the node in an isolated virtual network | ⚠ **unverified, single source, no details.** Static context: the client and the battle server contain a full cheat command set (`cheat_*`, `GameStore_Cheat*`), gated by `net_allowCheats` (default 0, observed 0 on the battle server, not set by the shipped configs); service Lua is not sandboxed (S-29). Recorded as **S-31** in [security](../07-administration/security.md); test idea Q65 |
| R2 | A community registration page allows only lower-case letters and digits for logins because "the game server sometimes rejects players whose login contains upper-case letters" | Not documented; static probe inconclusive (no login-specific case handling found by string search). New **Q64** |
| R3 | **Linux/macOS start-up:** most of the start time under Wine is spent on timeouts; with a recent Wine every `cloud/*.exe` stalls about 10 s in `StartServiceCtrlDispatcher`. Tips: run the Hub as a Windows service inside Wine, or patch that call; a recent kernel with `ntsync` and a recent Wine help (one host: 40 s → about 10 s). The S16 maintainer measures about 20 s with Wine 8 (Debian bookworm) and calls the README figure outdated | Plausible and **consistent with the imports**: the services import `StartServiceCtrlDispatcherA` and the other service-control functions ([pe-imports](../08-reverse-engineering/pe-imports.md)). Added to [linux-proton](../04-installation/linux-proton.md) as a host-reported tip ⚠ |
| R4 | A community developer is re-implementing the server applications with AI help: a partial Hub already lets a client log in and reach the hangar; the code is to be published later. Others: Hub and Shard are the interesting parts, the LoadBalancer is simple, a new DedicatedServer is a multi-month effort; estimate for a full replacement 6-12 months | Effort indicators for [09-community-edition](../09-community-edition/); not verified |
| R5 | **Playable boss, alien and pirate-destroyer hulls** (both channels): add a vessel with an **unused `vid`**, then grant it (it appears in the tech tree) or put it in a battle slot; the clone needs edits in four or five client files for the tech tree; if the launch fails with "ranks too low", one value in the vessel's equipment array (reported as 45 000 or 54 000) must be set to 0; removing a cruise missile fixed a hull that could not launch; the Manta hull still does not move (warp module as workaround); one alien hull behaves as if the AI took over | Host-reported recipes. `vid` must be unique per database; new ids come from `counters` ([mongodb](../06-database/mongodb.md) §3a). The equipment values are not verified → **Q49 amended** |
| R6 | **"All ships" account:** `vessels` and `items` arrays pasted into an empty account with a MongoDB client give every ship, aliens included, fully equipped; storage capacity must be raised; some unique module slots stay empty; a shared table maps ship ids to names; names via `cloud/data/store.xml` | Host-reported. Database edits only with the Hub stopped ([mongodb](../06-database/mongodb.md) §3a); demand for a ship id ↔ name list ([ship-defs](../05-configuration/ship-defs.md)) |
| R7 | Starter pack with every ship plus currencies by replacing `cloud/data/starter_pack.xml`; given when a new account registers, so the first login takes longer | Consistent with the batch 011 finding; `starter_pack.xml` is generated from `data/gamedata/shared/starter_pack.lua` ([data-files](../05-configuration/data-files.md)), so edit the Lua source or a regeneration overwrites the XML |
| R8 | **Toggle-mode active modules:** a timed module can be made to run until pressed again (ship Lua), but its visual and sound effects still end after the original ~2 s; looping them reportedly needs repacked game files. Four landing-platform modules on one destroyer by adding four active-module rows in `ship.lua` and emptying the hangar slots | Host-reported modding; effects live in the client paks ([pak-contents](../02-inventory/pak-contents.md)) |
| R9 | Module data: player modules in `active.lua` (very large); alien, PvE and open-world bot modules in separate files | Consistent with [module-defs](../05-configuration/module-defs.md) |
| R10 | Question: where are **ship respawn times** and the **battle-start countdown** defined? One answer points to ship definition files | No such folder in the shipped loose data; the `respawn_time` fields in `def/objects` belong to world objects (bonuses, cargo ships, adventure objects); respawn cvars `sv_respawnTime*` are documented ([cvar-notes](../05-configuration/cvar-notes.md)). **Static (file):** the countdown is `countdown_duration` and the per-death penalty `spawn_time_penalty_per_death` in `data/gamedata/gameplaysettings.lua`, per mode → **Q66** (partly solved) |
| R11 | Question: how to make **asteroids easier to see** in open space | Unanswered → **Q67** |
| R12 | Events: "how do I start the second and third phase of an event - the page stays empty"; how to open earlier battle-pass archives | Gap; related to Q59 (DLC checks on rewards) |
| R13 | **Public servers and their modes:** one offers beacon capture, control and team battle and has removed Detonation and the captain mode for now; another runs "old-style" progression without PvE attack/defence levels and seed chips and says its bots **now plant the bomb**; a third keeps the original progression | Host-reported; the bomb claim contradicts SF30 → **Q61 amended** |
| R14 | Request to a host: sector conquest in more time zones | Demand; conquest schedules: [game-modes](../05-configuration/game-modes.md) |
| R15 | **Account restoration and DLC:** a host plans an archive server that restores accounts by hand from players' screenshots; the missing piece is crediting DLC; a community admin panel (several languages) reportedly credits DLC; another player built an AI-assisted panel that grants all bot ships | Demand for admin tooling; DLC crediting → **Q44 amended** |
| R16 | Community launcher (RU): play without Steam or VPN; installs into the user's local programs folder without shortcuts; the installer fails on Windows 7; full client about 13 GB; its server has temporarily removed the biomorph ships and the rank-17 destroyers for rebalancing | Information; third-party client files are code (S-29) |
| R17 | A player thinks the client sends a password **hash** instead of the password to protect players from scam servers | Our captures: the login frame carries an encrypted-looking block, the stored hash is not sent in clear ([verification-log](../04-installation/verification-log.md) V-10, Q24); the "hash as credential" claim stays ⚠ (S-19) |
| R18 | Steam starts restore modified client files ("the client updates everything back") | Known: Steam file verification replaces changed depot files; keep mods outside the depot or use a launcher |
| R19 | The community mod manager (S18) has a new version (dark mode, Russian translation) | Watch item |

Not adopted: the flame war and personal disputes, operating-system and
hardware debates, server advertisements (no names or addresses copied),
balance opinions, 3D-model talk.

### Demand and problem signals (batch 012)

| Signal | Kind | Where we help / gap |
|--------|------|---------------------|
| Client-side attack on the console / Lua (undisclosed) | security | R1 -> S-31, Q65; isolate the node |
| Login names with upper-case letters refused | support | R2 -> Q64 |
| Slow start under Wine (Linux, macOS, Docker) | hosting | R3 -> linux-proton |
| Boss, alien and pirate hulls as player ships | modding | R5 -> Q49 |
| Every ship on an account; ship id ↔ name list | administration | R6, R7 -> FAQ |
| Respawn times, battle-start countdown, asteroid visibility | configuration | R10, R11 -> Q66, Q67 (gaps) |
| Event phases and battle-pass archives | economy | R12 -> Q59 context |
| Bots and the bomb mode | AI | R13 -> Q61 |
| Restoring old accounts, crediting DLC | administration | R15 -> Q44 |
| Replacement services, community launchers | downstream | R4, R16 -> 09-community-edition |

## Digest of batch 013 (partial exports of S12 and S15, 2026-10-15 evening → 2026-10-17 evening)

> Same rules: **leads, not facts**; anonymised and paraphrased; no names, ids,
> addresses, server names or quotes. Server, repository and file-host
> addresses posted in the chat were not copied.

**Scope.** EN: 160 new messages - forced faction ownership of open-world
sectors, a public host's start-up and ship-ban troubles, seed chips outside
open space, hull models and unpack tools. RU: 908 new messages, mostly a
flame war and off-topic talk (another space game, hardware, guild history);
the useful part is a registration-rules dispute, a "settings do nothing"
support case, storage limits and model/texture tooling.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| T1 | **Pirate ownership of open-world sectors:** in `ConfigureScriptsServer()` of `cloud/data/default_platform_config.lua` call `ScriptsServer:ConfigureGlobalEvents{ forceEvents = { { eventDefName = 18, eventLocation = <zone id>, newEventState = 1000 }, ... } }` (one entry per sector, the middle sectors listed) after `cvars.sv_enableCommunticationWithSS = 1`; the host's full function replaces the shipped one | **Consistent with the file:** the shipped function sets `sv_enableCommunticationWithSS = 1` and calls `ConfigureGlobalEvents` with commented `forceEvents` examples (one with `eventDefName = 4, eventLocation = 247, newEventState = 998`). Event ids: [zone-events](../05-configuration/zone-events.md); mechanism: [open-world-and-services](../05-configuration/open-world-and-services.md). Value 18 = pirate ownership and the state 1000 are host-reported ⚠ |
| T2 | "Server under heavy load" right after a fresh install: the client was started before the node had finished starting; it connects once start-up completes | Known start-order symptom ([troubleshooting](../04-installation/troubleshooting.md)) |
| T3 | A public host shortened its boot time; the change used up file descriptors and left the server locked; reverted. Separately, `DedicatedServer.exe` stopped launching after a binary patch, so the host plans an unpatched server with other service management | Host-specific (Linux/Wine node); supports keeping binaries stock and changing behaviour through configuration ([linux-proton](../04-installation/linux-proton.md)) |
| T4 | **Banning ships from PvP only:** the host blocked rank-16/17 and unique ships, which removed them from every queue (players could not queue at all with them); wish: keep them for PvE, open space and vs-AI | Gap → **Q69** |
| T5 | **Seed chips** work only in open space; to enable them elsewhere set `sv_autogenModulesEnabled = 1` and `sv_dbgAutogenDefs = 2` in `ConfigureZoneInstance()`, `ConfigureDediServer()` and `ConfigureDediServerFlags()` (Steam answer, SF41); a host notes vs-AI would then need seed-chip bots | **Contradiction:** the engine default of `sv_autogenModulesEnabled` is 0 and the shipped config sets 0 (and `sv_dbgAutogenDefs` 0) in `ConfigureZoneInstance()` *(file)*, yet players see chips in open space → **Q68** |
| T6 | Check the Hub logs in the runtime profile (`...\Targem\StarConflict\cloud\Hub\logs\`) to find errors after a config edit | Consistent with [administration](../07-administration/administration.md) (runtime profile, logs) |
| T7 | Hosting behind an unclear address: a guild bound the node to a virtual loopback adapter with a static address to have a stable `cloud.xml` address (Windows Server guide published by the host) | Same family as Q62 (NAT, announced address); host-reported workaround |
| T8 | **"My edits change nothing"** (RU): the player edited the platform Lua but MongoDB kept running after the game closed, so the node never restarted; a full stop (MongoDB included) and start fixed it; then a "data error" until game and node were restarted together | Confirms the restart rule in [settings-reload-map](../05-configuration/settings-reload-map.md); FAQ candidate |
| T9 | Storage full after granting many items: purchases blocked; one player spent a day deleting about a thousand modules; no bulk select beyond Ctrl+click | Demand: storage limit and bulk cleanup through the database (Hub stopped, [mongodb](../06-database/mongodb.md) §3a) |
| T10 | A community registration page requires lower-case logins; the dispute is about whether the password rule is digits only (it is "characters", per the page) | Context for **Q64** |
| T11 | Ship models: attachment points (guns, engines, modules) are bones in the model skeleton (`.mdl-skl`); a definition only names the bone; skins use three colour masks; textures tested only as DXT5; a public tool set for unpacking and model conversion exists and a pack/edit SDK is being written | Client-asset modding; out of scope beyond [pak-contents](../02-inventory/pak-contents.md) |
| T12 | Account-starter kit: a new player at clearance level 14 asks how to get the starter pack | Known: given at registration only (b012 R7) |
| T13 | Hosts discuss one shared community server versus many small ones, donations, and a long-term "new content" project; a host claims to manage 22 servers | Context for [09-community-edition](../09-community-edition/) and the [legal notes](../09-community-edition/legal-and-licensing.md) (no monetisation) |

Not adopted: the flame war and personal disputes, another game's mechanics,
hardware, guild history, server advertisements (no names or addresses
copied), balance opinions, film-ship wish lists.

### Demand and problem signals (batch 013)

| Signal | Kind | Where we help / gap |
|--------|------|---------------------|
| Faction ownership of open-world sectors | configuration | T1 -> zone-events (recipe) |
| Ship bans per mode (PvP only) | configuration | T4 -> Q69 (gap) |
| Seed chips outside open space | configuration | T5, SF41 -> Q68 |
| Edits without effect (node not restarted) | support | T8 -> settings-reload-map, FAQ |
| Storage full after grants | administration | T9 -> database edit with the Hub stopped |
| Detonation mode removed, campaign mission needs it | configuration | SF44 -> Q61 |
| Model and texture tools | modding | T11 -> out of scope |

## Digest of batch 014 (partial exports of S12 and S15, 2026-10-17 evening → 2026-10-19 morning)

> Same rules: **leads, not facts**; anonymised and paraphrased; no names, ids,
> addresses, server names or quotes. Links to file hosts, videos and private
> documents posted in the chat were not copied.

**Scope.** EN: 95 new messages - post-battle loot for rank 16/17, a welcome
letter with synergy through `adminMail`, Glass-ship collision damage, a map
material fix, an admin panel announced, item-list and icon requests. RU: 231
new messages, mostly talk about AI tools; the useful part is the storage
limit, a "client files error" on a foreign server, where the logs are, and a
Docker-based admin panel.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| U1 | **No post-battle loot for rank-16/17 ships:** add rows for ranks 16 and 17 to `DedicatedServcerServices_SetLootRules`; the asker reports it works | **File-verified:** the shipped rules have rows 1-15 only (`queue_lint` L1, [config-validation-tools](../07-administration/config-validation-tools.md)); the `_v3` table names still apply (Q45). Recipe already in [tuning-recipes](../05-configuration/tuning-recipes.md) |
| U2 | **Free synergy for every account:** a public host inserts a letter into `adminMail` (`amid` larger than any before, `sentAt`, `expTime` +7 days, `important`, `source`, `goldCost`, attachments type 2 = subject/body and type 7 = `vesselExpPool`); a second host warns that it silently does nothing when run in the wrong database | **Consistent with the static layout** in [admin-tasks-howto §4b](../07-administration/admin-tasks-howto.md); first field report of delivery *(community)*. Wrong database = the account database, not the game database |
| U3 | **Storage limit:** more than 4 096 slots is "a technical limit"; a host shared a storage guide; the same applies to the number of ships | Same value reported on the Steam forum (SF47) → **Q71** ⚠ |
| U4 | "Client files error" when joining a battle on someone else's server; answer: game file hashes differ (the host's community launcher had updated files) | Known mechanism: data-version check ([pak-contents](../02-inventory/pak-contents.md), Q3, b008 K4) |
| U5 | Where the logs are: `%LOCALAPPDATA%\Targem\StarConflict\logs\<newest>\game.log` (Lua errors and crash cause); crash reporter logs in `...\Targem\Targem Crash Reporter\logs`; Proton path under `compatdata/212070/pfx/.../AppData/Local/...` | Consistent with [administration](../07-administration/administration.md) (runtime profile); the crash-reporter folder is new to us ⚠ |
| U6 | Glass (GS) ships take very high collision damage at low speed | **File-verified:** `def/ex/ship.lua` gives the `_T4_Glass` hulls `contact_damage_cf` 250 / 400 / 900 (S / M / L) against 20-160 for most hulls, and `contact_damage_min_speed = 20` (most hulls 3-5). Stock data, not a host setting |
| U7 | A public host's new-account kit: free basic T3 dreadnoughts, rank-10/11 ships, all crew and ship slots, e-sports weapons for credits, large starting balances | Host-specific; levers: `starter_pack.lua` (b012 P6), [event-ships](../05-configuration/event-ships-mail-and-clan-ship.md) |
| U8 | Fort Muerto map: black flickering (Z-fighting) fixed by restoring two `UserParam` lines of the asteroid material in `s1515_piratebay.mdf`, dropped in map version `1.6.5c.138647` | Client asset; out of scope beyond [pak-contents](../02-inventory/pak-contents.md) |
| U9 | Range chips on a weapon show no effect on range or heat | Report only; no test |
| U10 | A Docker-based admin panel (Docker Desktop + WSL, about 15 GB archive with the game) with seed-chip generation from containers; another panel announced in the EN channel | Downstream tools; distributed archives contain game files (not adopted, rule 1) |

Not adopted: talk about AI tools and prompting, video-like requests, memes,
another game, offers of paid or like-gated tools.

### Demand and problem signals (batch 014)

| Signal | Kind | Where we help / gap |
|--------|------|---------------------|
| Loot for rank 16/17 | configuration | U1 -> tuning-recipes (known) |
| Granting currency to all accounts | administration | U2 -> admin-tasks-howto §4b |
| Storage and hangar caps | administration | U3, SF47, SF48 -> Q71 (gap) |
| Joining foreign servers fails | support | U4 -> data-version check |
| Where are the logs | support | U5 -> administration |
| More trade offers; picking up several items at once in open space | configuration | gap (not researched) |
| Full item list; uploading corporation icons | administration | gap; item names: `def/ex` + [locale-catalogue](../05-configuration/locale-catalogue.md) ⚠ |
| A stats HTTP API for a fan site | downstream | gap; no such service in the shipped node |

## Digest of batch 015 (partial exports of S12 and S15, 2026-10-19 → 2026-10-20 morning)

> Same rules: **leads, not facts**; anonymised and paraphrased; no names, ids,
> addresses, server names or quotes. Links to file hosts, videos and private
> documents posted in the chat were not copied.

**Scope.** EN: 75 new messages (2026-10-19 12:32 → 2026-10-20 08:08; a gap
of about five hours after batch 014) - a paid-mod proposal, an item-index
tool, icon extraction for a fan site, invite links. RU: 171 new messages
(2026-10-19 08:00 → 2026-10-20 10:45, continues batch 014) - the same
paid-mod proposal, a hangar limit, AI-tool talk, NPC alien ships as
playable ships.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| W1 | A modder proposes a **paid subscription** for a large single-player mod (full version; a higher tier adds an admin panel with cheats); says it contains only own files. Most replies object (paid mods, a barrier to entry for servers); one notes that the published terms name servers, not mods | Out of scope: this project does not cover payment or financial rules; our [legal notes](../09-community-edition/legal-and-licensing.md) cover servers only (no monetisation, "Unofficial Server"). Demand signal only |
| W2 | **320 ships per account** is "the technical limit": adding the remaining ships needed selling others; above it the client reportedly crashes at start | No 320 in the shipped config or data files *(file: `cloud/data/*.xml`, `*.cfg`, `default_platform_config.lua`)*; the item registry has 655 account ships, so a cap below that would bite → **Q71** amended ⚠ |
| W3 | Currency added through a third-party admin panel shows only after a re-login | Consistent with the Shard's account cache (Q32; live changes go through the admin-task queue) |
| W4 | One host's admin panel is built for Docker; on Windows that means WSL and the Windows binaries under Wine/Proton | Known ([docker](../04-installation/docker.md), b014 U10) |
| W5 | A player-kit generator gives every player gun ordinary munitions; to keep an NPC ship's own projectile the modder needed an exception; NPC alien hull figures quoted (very high hull, shield and resists) | Lead for the new-ship chain (S11 O12); munition defaults not checked |
| W6 | Removing low-rank ships from the tree breaks the progression dependencies | Consistent with the `VesselTree` links (`shared/vessel_tree.lua`) *(inferred)*; same family as invariant I-12 |
| W7 | A player reports an account taken over by password guessing (which service is unclear) | Context for [security](../07-administration/security.md) §4.1 (passwords stored verbatim, V-13); no detail ⚠ |
| W8 | A fan site cut item icons out of icon sheets defined by rectangles in text files and mapped them to internal names (no English names in the client locale) | Consistent with `data/gamedata/atlas_defs.lua` *(file exists)* and the naming rules in [item-names](../05-configuration/item-names.md) |
| W9 | An item-index tool with a search site was announced (SC Scrap Metal Index) | Related project; built from the same static data |
| W10 | How to add custom ships - unanswered in the channel | S11 O12 new-ship chain ([data-files](../05-configuration/data-files.md)) |

Not adopted: AI-tool and prompting talk, memes, other games, invite links,
screenshots without text.

### Demand and problem signals (batch 015)

| Signal | Kind | Where we help / gap |
|--------|------|---------------------|
| Hangar cap (ships per account) | administration | W2 -> Q71 (gap) |
| Paid mods and paid admin panels | community | W1 -> out of scope |
| NPC and alien ships as playable ships | configuration | W5, S22 MR3 -> lead; Q74 |
| Account takeover by guessed passwords | security | W7 -> security §4.1 |
| Item names and icons | downstream | W8, W9 -> item-names |

## Digest of S22 (`#mod-releases` forum channel, batch 001)

First export of this channel. Most threads repeat recipes already digested
from The Outpost (S17) and earlier batches; only the deltas are listed.
Attachments (XML, JSON, Lua, archives, executables) were not opened.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| MR1 | **Starter pack with almost every ship** (`cloud/data/starter_pack.xml`, or `starter_pack.lua` + `prepare_shared`; new accounts only; the first login is slow). Six ships cannot be included - they cause a "network error": the four `Ship_Leviathan_*` hulls, `Ship_OW_Boss_PirateEvent1` and `Ship_ST_Rank17` | **File check:** the first five have no row in `store.xml`; `Ship_ST_Rank17` has one (`<Item>` type 0, `<Vessel>` rank 17, premium) → **Q74** (new) |
| MR2 | "Ultimate ship collection" (OP3): after pasting, `vid`s start at 1000 and `iid`s at 100000; open-space missions show "wrong contract type" for a while; a high-rank hull gets no co-op matches, PvE works | Hand-made ids bypass `counters` ([mongodb](../06-database/mongodb.md) §3a); unlocks and ranks are separate account fields; matchmaking by rank ([matchmaking-guide](../05-configuration/matchmaking-guide.md)) ⚠ |
| MR3 | Playable alien hulls: the Hunter/Predator conversions get the open-space NPC weapons when their slots name `Weapon_AlienGun_T4` / `Weapon_AlienGun2_T4`; "ship rank too small" until fixed; one hull cannot move | **File-verified names:** both are `default_modules` of open-world presets (`def/ex/ow_preset.lua`, `ow_bot_preset.lua`). The conversions edit `gameplay_leviathan.lua` |
| MR4 | Localisation: rename `data/strings.pak` and unpack the strings into `data/strings/<language>/`; the game reads the loose files | Consistent with the loose-file override (**Q56**, S11 O12); not tested |
| MR5 | Store unlock through `store_allowAllItemsForBying = 1` and the `store_*PriceMod` cvars in `default_platform_config.lua`; one user saw no change | Known cvars ([cvar-reference](../05-configuration/cvar-reference.md)); does not unlock every ship (MR1 is the ship route) |
| MR6 | Mod manager (S18) 0.2+: iridium cap removal, easier crafting, premium booster (warns that large day counts overflow), a GS mod that works only when the server has the same mod | S18; premium overflow = **Q63**; client/server pairing = data-version check |
| MR7 | A server-list mod replaces the client's login-window Lua to keep several servers and a default | Client file replacement; same caution as other unsigned client mods ([security](../07-administration/security.md)) |
| MR8 | A launcher downloads game files from each server's patch server (SHA-256), with a malware warning | Known (b008 K1, **S-29**) |
| MR9 | A Russian "extended account panel" (executable + Python scripts): the database name `cosmosim_<name>` must be edited in its script | Downstream tool; database naming as in [mongodb](../06-database/mongodb.md) ⚠ |

## Digest of S17 (The Outpost, fan site: Server Guide Modules)

* A community-run site that collects short snippets (XML, Lua, MongoDB,
  screenshots) with a title each as a "Server Guide Modules" collection; the
  maintainers asked in the EN channel (2026-10-11) for contributions so that
  the material stays reachable without Discord and is turned into an open
  handbook with a setup guide. Login not required to post.
* Page evaluated: **`default_platform_config.lua` (translated to English)** —
  the shipped `cloud/data/default_platform_config.lua` with its Russian
  comments translated; one large Lua code block, no author named, dated
  2026-10-11. See [evaluation](#s17-evaluation).

### S17 evaluation

* **Matches our file.** Spot checks against the local file (2 207 lines, 512
  of them with Cyrillic): the same duplicated assignments
  (`store_maxTransactionSum` ×2, `mm_decisionLog` ×2), the same ticket tags
  (`#0098493`, `SC-112207`), `brawlSchedule` with `three_teams_dm` as the only
  active entry, `ConfigureLobbyServer` starting with `lobby_enabled = 1`. The
  translated comments checked were faithful. Some translated wording is
  clumsy and leftovers stay (e.g. "Balanse rule").
* **Completeness unknown.** Our fetch read ~100 000 of 126 093 characters; the
  truncation marker may belong to the fetch tool, not the page. Re-check in a
  browser before relying on the tail (lobby, event, dispatch sections).
* **Value:** a reading aid for the comments (what each cvar is for, units,
  ranges) and a cross-check for our [cvar-reference](../05-configuration/cvar-reference.md)
  (which already carries our own English column for 243 cvars). It is not
  structured and adds no information beyond the file itself.
* **Rights/policy:** unnamed translator, derivative of Gaijin's file, terms
  unknown → **link only**; do not copy it or publish our own full translation
  of the file (it would be a derivative of shipped code, contrary to the
  "no Gaijin code" rule). Short paraphrases of individual cvars with our own
  wording remain fine.
* **Watch:** the collection may grow into a practical handbook; re-check
  periodically (listed in CLAUDE.md watch list).

### S17 Knowledge Base review (2026-10-14)

All 17 "Server Guide Modules" articles and the Server Setup Guide were read
(text only; code shown only in screenshots was not read). Trust: average -
short recipes, mostly credited to Discord users, rarely with evidence.

**Already covered** (no change needed): loot aliases for the
`CommonRanks_*_v3` tables (Q45, V-10); matchmaker bot presets and
`maxTimeInQueue` ([bot-presets](../05-configuration/bot-presets.md)); the
auto-kick limit "20" in `shard.cfg` = `sm_overloadCounterLimit` (I7);
starting balances `gold_on_start` etc., battle pass dates and
`battle_pass.xml`, asteroid yield files, alien boss HP in `cargoship.lua`
([tuning-recipes](../05-configuration/tuning-recipes.md)); pirate destroyer
names ([pirate-destroyers](../05-configuration/pirate-destroyers.md)); DB fields
`goldCredits`, `credits`, `tokenCredits`, `accountRank` (useful maximum 25 per
the site), `unlimPve_playerLevel1/2`; `prepare_shared.bat` workflow; the setup
guide (I11).

**New leads → test proposals** (all ⚠, community):

| Site article | Claim (paraphrased) | Open question |
|--------------|---------------------|---------------|
| Setting PvE Attack/Defense Levels | Very high levels: invincible ship, `nan` hull/shield bars, level-1 damage | [Q51](../08-reverse-engineering/open-questions.md) |
| Setting GS, Iridium and Credits | Balances set too high turn negative and cannot be spent | Q52 |
| Unlocking the experimental destroyer | Insert a vessel record with `defName: Ship_OW_Boss_PirateEvent1` (name not found in shipped data) | Q53 (and Q49) |
| Setting the Resources | Buy one of each resource first, then edit its amount; "special parts" crafts may stay blocked | Q54 |
| Import the alien weapons of gameplay_Leviathan | Snippet in `ship.lua` + emptied weapon slots = ship fires the alien gun (contradicts an earlier report) | Q55 |

Player and host interest behind them: generous test accounts without
breaking the account, PvE progression by hand, special ships and weapons.

### S17 re-read (2026-10-19) - delta only

The site now also runs under a new domain (b014). Knowledge Base: about 30
modules (17 on 2026-10-14); Resources: about 35 entries over five pages,
mostly fan-kit media (sounds, wallpapers, fonts, screenshots). This
repository is listed there as a documentation link. Code in screenshots and
download archives with game files were not opened.

| # | Item (paraphrased) | Our status |
|---|--------------------|------------|
| OP1 | **Respawn times:** `spawn_timeout` in `data/gamedata/def/objects/ships.lua`, different per ship type | **File-verified:** `Ship_Base` 15, `Ship_Small` 13, `Ship_Medium` 15, `Ship_Large` 17, `Ship_HUGE` 60, `Ship_ST` 3 (seconds per the file comment) → **Q66 solved** (static) |
| OP2 | Pirate control of open-space zones with `forceEvents` (`eventDefName = 18`, `newEventState = 1000`, one entry per zone) | Same recipe as b013 T1 and S20 |
| OP3 | "Ultimate ship collection": two JSON files with every ship and item, pasted into an account's `vessels` / `items` arrays | Risky: pasted vessels need unique `vid`s from `counters` ([mongodb](../06-database/mongodb.md) §3a); asked about in b014 |
| OP4 | All-ships CSV sheet; English translations of `ships.lua`, `default_platform_config.lua`, `dediserver.cfg`, `special_values.xml`, `gameplay_leviathan.lua`, the shipped `docs/matchmaking.md`, and of all `shared` and `objects` Lua files | Translations of shipped files: research aid only, cite the install ([translations](#s17-evaluation)) |
| OP5 | Higher-rank bots: `botPresetType` (`bpt_mirror`, `bpt_adaptive`, `bpt_mirror_and_save`) or `special.botPresetNames` per queue | Known ([bot-presets](../05-configuration/bot-presets.md)); same host as S20 |
| OP6 | Alien bosses in the terramorphing open-space location via its level Lua | Lead only; [level-catalogue](../05-configuration/level-catalogue.md) |
| OP7 | New tools: **sc-proxy** (packet-capture proxy, see S21), an in-game "instance launcher" (proxy `d3d9.dll` that hooks client Lua functions to run maps locally), a config table editor, a chat translator (online translation service), a long community "science" document | sc-proxy → S21; the d3d9 hook injects code into the client (not reviewed; treat like any unsigned DLL, [security](../07-administration/security.md)); others context only |
| OP8 | A "capture coverage" site of a player who recorded server traffic before shutdown | Not reachable on 2026-10-19 (site and forum thread); watch list |

### S17 re-read (2026-10-20) - delta only

Checked because the site owner announced Knowledge Base updates. The 30
modules and their dates are unchanged (newest 19 October). Changes:

| # | Item (paraphrased) | Our status |
|---|--------------------|------------|
| OP9 | Site renamed to "Star Conflict CE: The Outpost"; the download page points to the Community Edition on Steam | Naming only |
| OP10 | New **"Game Items (in progress)"** section: one page per item with the source string keys (`ItemSubtype_*`) and an icon; pages "still being styled" | No values to check yet; compare with [item-names](../05-configuration/item-names.md) when the pages carry data |
| OP11 | Resources: an item-index tool added (W9); the capture-coverage entry (OP8) removed | OP8 dropped from the watch list |

### S21 evaluation (sc-proxy, 2026-10-19)

* **Matches our build:** 246 of the 249 `AC_*` message names in
  `ac_dispatch_table.json` occur as strings in both `win64/game.exe` and
  `cloud/Shard.exe` of Hub 1.99.0.167293 *(static)*; our docs named 25 of
  them ([protocol-observed](../08-reverse-engineering/protocol-observed.md)).
* What it adds: per-message body layouts (Kaitai schemas checked against its
  own captures), server notification ids, a load-balancer and chat proxy.
  Not run here; captures are not in the archive.
* Use for us: a cross-check source for a message catalogue built from our
  own binaries (Q73); not copied into this repository.


## Digest of S19 (Steam community discussions, 2026-10-09 → 2026-10-14)

> Same rules as for Discord: **leads, not facts**; anonymised and
> paraphrased; no names, ids, addresses, server names, repository or file-host
> links. A local copy (raw pages, parsed threads) is kept privately.

**Scope.** Steam forum of the game (app 212070): 56 threads of the General
discussions with activity since 9 October and 5 comment threads under the
official announcements; 627 posts by 262 authors (EN, RU, a few DE/ES/ZH).
Compared with the Discord slices the forum is more technical and more
beginner-oriented: setup failures, step-by-step recipes, shared
configuration packs, unofficial-server announcements.

**Official material on the forum.** The pinned "Community Edition - Official
instruction" threads (EN, RU; 12 October) link Steam guides that repeat the
official website page S1 (architecture, launch methods, database handling,
mode names, `-lang`, logs, the termination notice) and add a "Before you
start" section *(official, compared with our 9 October copy of S1)*: Redis
is needed only for leaderboards; the default address 127.0.0.1 "does not
necessarily prevent the server from accepting connections through other
network interfaces" (our S-30); "only connect to servers you trust - a
malicious server may exploit vulnerabilities in the game client" (our
S-29); and "passwords are stored in hashed or otherwise protected form"
(compare S-07: one unsalted SHA-256, confirmed value-free). The pinned unofficial-server list states the forum's moderation rules:
one post per server, the "Unofficial Server" label, no monetisation, no use
of software vulnerabilities ([legal-and-licensing](../09-community-edition/legal-and-licensing.md)).

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| SF1 | "MongoDB does not start / the window flashes and closes" and "localhost: cannot connect to the server": fixed by starting `mongod.exe --dbpath "<game>\cloud\mongodb\data"` by hand (some add `--smallfiles`), or by correcting `MONGO_DATA_PATH` in `launch.bat`; reported mostly by players whose earlier non-Steam installation kept the data in the game folder | `launch.bat` uses `%LOCALAPPDATA%\Targem\StarConflict\cloud\mongodb\data` *(file, [mongodb](../06-database/mongodb.md))*. Other causes that fit: a second `mongod` on the same folder (client autostart, batch 011 P1), unclean `mongod.lock`; `--smallfiles` reduces MongoDB 2.6 preallocation, so low free disk space is a plausible cause *(inferred)*. Windows 11 compatibility of MongoDB 2.6.12 untested |
| SF2 | Which MongoDB GUI works: NoSQLBooster 3.5.7 (supports MongoDB 2.2-3.4) or 5.2.12; current versions (11.x) fail to connect | Consistent with the bundled MongoDB 2.6.12 being too old for current drivers (FAQ) |
| SF3 | The data is in `cosmosim_<Steam account name>`; `cosmosim_Admin` is empty | The official guide and our observation: `cosmosim_<Windows user name>` *(official S1, observed)*; the services import `GetUserNameA` *(static)*. The report most likely shows a Windows user named like the Steam account ⚠ |
| SF4 | Shell guide to "top-tier" accounts: stop the server, then `$set` `credits`/`goldCredits` (`NumberLong(999999999)`), `accountExpPool`, `accountRank` (max 25), `premiumTill` (milliseconds), `raceRep` (five values), `prestigeBonus`, `vessels.<n>.exp`; resources via `craftResources` (Zeta parts `resource_zeta_final_*`) | Field names match [schema](../06-database/schema.md); balances stay below 2 147 483 647 (Q52); write only with the Hub stopped (Q32) |
| SF5 | Premium: far-future `premiumTill` shows **no** premium - a host found the client keeps the remaining premium time in **seconds as a 32-bit number** (overflow beyond about 68 years); other reports: +10 years or "until 2063" works, "until 2068/2100" fails. Alternatives: add `player` to `auth_infinitePremiumForRoles` (shows a 24-hour counter that refreshes), or premium by welcome mail | `cvars.auth_infinitePremiumForRoles = "gm;support"` shipped *(file)*; premium attachment `LAT_PREMIUM` in admin mail ([admin-tasks-howto](../07-administration/admin-tasks-howto.md) §4b). Overflow limit -> **Q63**; **static (2026-10-14): confirmed** - the client display keeps 32 bits of the seconds left, the expiry check uses the full value |
| SF6 | "Server under heavy load" after config edits (often with `botsCount` in a queue's `special`) or while a client-started server still runs | **Static:** the text is the client string `login_connecting_desc` (English string table) shown while the login waits in the queue - it reports a login that does not complete, not a measured load. Causes reported: lingering Hub, broken queue edits, services not started |
| SF7 | "Fatal error: can't initialize file server. Two or more files within packages are the same" | **Static:** the message is in `game.exe` and in every service executable (engine file system); it points to duplicate paths across `.pak` archives (leftover or added packages) *(inferred)* - see Q56 |
| SF8 | Dialog "LobbyServer: Memory leak detected. Amount: 6, size: ..." and the Hub crashes | **Static:** the message exists in all 21 service executables; it is a modal `MessageBoxA` (only without a debugger, `MB_SERVICE_NOTIFICATION`) from the engine's memory-statistics routine - the service blocks until the dialog is closed. Trigger not pinned down -> [troubleshooting](../04-installation/troubleshooting.md) |
| SF9 | Hosting for friends abroad: ports TCP 3801/3802/3815 and UDP 35000+ (up to 35050 on one host); the node address in `cloud.xml` must be one the PC owns, so the public IP behind a router gives `there is no my node in xml`; workaround: a virtual network adapter (or VM) carrying the public IP, after which battles needed a VPN; CGNAT prevents port forwarding; routers may not loop back to the public IP | Ports and the error match V-9 *(observed)*. The node address is used both to bind and to announce -> **Q62**. Static (2026-10-14): "override external host" cvars exist (`net_overrideShardAddr`, `net_overrideChatServerAddr`, `net_overrideDedicatedServerAddr`; host only); the LoadBalancer pair seems to apply only with two or more Shard/chat candidates ⚠ |
| SF10 | More bots: `mm_botsCount` 6 -> 23, `sv_kickExcessiveBotsEnabled` 1 -> 0, `optimalPlayers` 4 -> 12, `maxExpandTime` 30 -> 60, mode 12 (TDM) added to `levelsDesc`; `botsCount` in a queue's `special` works for some and causes endless "heavy load" for others; PvE missions get allied bots with `botsCount = 3` in the PvE queue's `special`; arcade/vs-AI bots are always T1 because the queues set no bot preset; bots that copy fits from the leaderboard are weak on an empty database | Keys exist *(file)*; the T1 fallback matches the static finding (`AiPreset.Default`, [bot-presets](../05-configuration/bot-presets.md)); adaptive pools empty on a fresh DB *(static)*. Special Operations stay at 0 bots (Q50) |
| SF11 | PvE missions with a friend fail; setting both `-- PVE QUEUE` blocks from `maxPlayers = 1` to `4` fixes it and adds allied bots; some missions stay grey ("needs a squad of 4") | **File-verified:** both PvE queue blocks (platform Lua lines 376 and 701) ship with `maxPlayers = 1`, `special = { pve = 1, gameMode = 7 }`. The "squad of 4" missions are not explained (`lobby_reqPlayersPvEMin` 3 applies to lobbies, batch 010 N5) |
| SF12 | Rank 16-17 ships: endless search in vs-AI battles and no loot search after battles | **File-verified:** the co-op vs AI queues accept `mmRank` 1-15, and `DedicatedServcerServices_SetLootRules` has rows `[1]`-`[15]` only - both gaps were in our queue coverage check ([config-validation-tools](../07-administration/config-validation-tools.md)); hosts extend the ranges and add rows `[16]`, `[17]`. `tools/queue_lint.py` now reports missing loot rows (L1, 2026-10-14) |
| SF13 | Loot: add `_v3` to the common tables (a host quotes the battle-server log line `got common loot table 'CommonRanks_1_3_v3'`); `NeodiumDrop` and `LezortiumDrop` are still missing; `_V3` (wrong case) breaks it; un-salvageable "iridium junk" (`Iridium_Junk_r<n>`) lands in the mailbox as an illegal item and blocks other trophies - replaced by `Token_drop_T1..T5` entries; daily quests `BP_DAILY_*` can reward iridium (`reward_tokens`) although the UI does not show it | Q45 independently reproduced, including the two missing epic tables *(file, V-10)*; table names are case-sensitive Lua keys. The mailbox bug is new ⚠ |
| SF14 | Squads cannot find PvP or vs-AI battles with bots unless `mmSquadRank` ranges equal the `mmRank` ranges | Matches Q35 (squad queue failure) - amended |
| SF15 | Battle pass: stage 1 works, stages 2-3 show rewards but claiming fails with a "wrong stage" error; 45 rewards enabled in Lua but 41 in the XML show as N/A; reports disagree whether `battle_pass.xml` is regenerated | `battle_pass.xml` is written by `prepare_shared` *(V-11)*; reward checks are bundle checks (Q59) - amended |
| SF16 | `store_allowAllItemsForBying = 1` shows everything (test-only items at 999 999, orange parts, seed-chip packs) and "borks" accounts; do **not** change `sm_sandboxAccess` from 4 or the open world closes | **Static:** built-in description of `sm_sandboxAccess`: 0 forbid all, 1 privilege, 2 privilege or DLC, 3 privilege or achievement, **4 allow all** (shipped 4) - consistent |
| SF17 | Clan ship alone: `clan_shipBuildHighRanks` is set twice (inside `LoadBalancer_SetGreetingMessageCVars` and as a cvar), ranks also in `clan_upgrades.lua` / `aux_limits.xml`, costs and times in `clan_ship.xml` (from `shared/clan_ship.lua`); dreadnought battles with bots work, Conquest queues forever | Consistent with [event-ships](../05-configuration/event-ships-mail-and-clan-ship.md); edit the Lua and regenerate rather than the XML |
| SF18 | "Fatal error: cannot run another copy" when starting a second client | Client switch `-multiCopies` (Q31, static) |
| SF19 | Inventory extensions (`special_values.xml`): deleting rows between tiers stops the game from starting; more than 3 500 slots stalls at "heavy load"; a larger `baseSize` works, but the next upgrade resets the size to 75 | **File:** `InventoryExtensions baseSize="50"`, first row `size="75"` - the account stores an upgrade step, not a size *(inferred)*; another invariant for [data-invariants](../05-configuration/data-invariants.md) ⚠ |
| SF20 | A host lowered "trade after 50 battles" to 10 and removed "a check that blocked trading for players who played on more than one PC" | **Static:** mail/trade gate `shard_minAntibotCounterForMailSending` 50 (file); chat gate `chat_minAntibotCounterForSendMsg` default 0; the Shard keeps a per-PC flag (`isSingleUidOnPC`, admin tasks `setIsSingleUidOnPC`/`unsetIsSingleUidOnPC`) used at login and in matchmaking, not for trade; the multi-PC trade block fits the machine counter + `shard_is2StepAuthForMailSendingNeeded` (default 1; set 0 in `shard_local.cfg` on a server without 2-step authorisation) - [event-ships](../05-configuration/event-ships-mail-and-clan-ship.md) mail section, S-28 |
| SF21 | Steam achievements no longer unlock on local or community servers | **Static:** no Steamworks client library is shipped with the client or the services; the client cannot report achievements to Steam |
| SF22 | Linux: Steam shows a 0-byte install or "game.exe not found" unless a Proton version is selected | There is no native Linux build - [linux-proton](../04-installation/linux-proton.md) |
| SF23 | Quest edits: changing rewards works; making daily quests repeatable gives "wrong quest type"; extra evolution points on alien ships give an error when applied | Quest data rules: [quests-semantics](../05-configuration/quests-semantics.md); leads only |
| SF24 | Shared "solo configuration" packs (whole `default_platform_config.lua`, `ai_settings.lua`, batch files) on file hosts; one host publishes its server changes as a public repository | Third-party files that run as Lua with native-code access (S-29) - review before use; not copied |

### Demand and problem signals (S19)

| Signal | Kind | Where we help / gap |
|--------|------|---------------------|
| Database will not start, localhost cannot connect, wrong DB tool version | setup | SF1, SF2 -> FAQ; troubleshooting is a recurring gap |
| "Server under heavy load" / "file server" fatal error / memory-leak dialog | setup | SF6-SF8 -> FAQ |
| Bots everywhere (PvP, vs-AI, PvE missions, Special Operations) | configuration | SF10, SF11 -> tuning-recipes; raids not configurable (Q50) |
| Rank 16-17 matchmaking and loot | configuration | SF12 -> tuning-recipes |
| Squads with bots | configuration | SF14 -> Q35 |
| Hosting for friends behind NAT/CGNAT | hosting | SF9 -> Q62 |
| Premium, currencies and resources for solo play | economy | SF4, SF5 -> FAQ, Q52, Q63 |
| Battle pass, xenochips, DLC items | economy | SF15 -> Q59, Q44 |
| Steam Workshop, mod manifest, server-required mod list, TPAK/model/level/navmesh tools, mod validator | modding ecosystem | demand for downstream projects ([09-community-edition](../09-community-edition/)) |
| Server browser, saved server address, in-game admin console, one-click server launcher | usability | Q46, admin-task queue; downstream |
| Account recovery from the official service | support | impossible; do not reuse Gaijin passwords (FAQ, S-07) |

Not adopted: farewell messages, the achievement-hunting dispute beyond
SF21, PvP nostalgia, server advertisements (no names or addresses copied),
open-world design wish lists.

### S19 re-crawl (2026-10-16) - delta only

Second crawl of the same forum (threads active since 14 October): 14
threads, 69 posts newer than the first crawl.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| SF25 | **Repeatable quests - a working recipe:** in `quests.lua` add `intervalStartHour`, `intervalLongHours`, `intervalLongEnableHours` and `max_completions` (and raise `locks_on_account_rank`); the quest's active state and rewards must also be set in `quests.xml` (`maxCompletions`, reward attributes) | **Answers SF23** ("wrong quest type"): both layers must agree. Fields as in [quests-semantics](../05-configuration/quests-semantics.md); host-reported |
| SF26 | **Clans for solo players:** lower prices and build times of clan-ship products; one member of rank 9+ instead of ten; clan creation for 5 instead of 1 500 | **File-verified values:** `ClanRegistrationCost tokenCredits="1500"` in `cloud/data/special_values.xml`, `ClanHighRank` 9 in `aux_limits.xml` ([xml-schemas](../05-configuration/xml-schemas.md)); the host also plans bot clans for clan wars (idea) |
| SF27 | Confusion about "Lua versus XML": which one wins, entries that must exist in both, and the claim that Lua edits are picked up at the next start without the update step | Layer order and generated files: [config-system](../05-configuration/config-system.md) (`default_platform_config.lua` runs last for cvars; `cloud/data/*.xml` come from the shared Lua via `prepare_shared.bat`); reload behaviour: [settings-reload-map](../05-configuration/settings-reload-map.md). The forum statements partly conflict with each other |
| SF28 | Weapon and module stats live in `data/gamedata/def/ex` (one file per family: capacitor, armor, ...); the chip generator in `autogen_common.lua` | Consistent with [gamedata-catalogue](../05-configuration/gamedata-catalogue.md) |
| SF29 | A shared solo configuration fixes the brawl modes "Last Hero" and "Fight Club" so that they start and fill with bots | Host-reported; not documented yet ([game-modes](../05-configuration/game-modes.md)) |
| SF30 | Bots in Detonation stall after picking up the bomb, "since 2016"; the logic is probably in the binaries | Matches our static result (no bot-side bomb behaviour found, Q61); contradicts R13 |
| SF31 | MongoDB and the Hub do not start on some Windows 10 PCs from the shipped batch files (relative paths); workarounds: own batch files, starting `mongod --dbpath ...` by hand, adding `cloud/mongodb` to `PATH` | Start failures: [troubleshooting](../04-installation/troubleshooting.md); host-reported workarounds ⚠ |
| SF32 | Rank-1 bots for a rank-13 player in PvP, explained as cross-rank matching with hidden scaling to the highest ship in the player's slots | Explanation unverified; bot ranks: [community-faq](../07-administration/community-faq.md) |
| SF33 | Players expected their official accounts and got an empty new one | Known (S19): the local server has no official account data |
| SF34 | A shared configuration had calendar events (Halloween, "claws") switched on permanently by mistake; wish for a switch for event visuals | Shared configuration packs are code to review (SF24) |
| SF35 | Gold without purchases: small amounts added to end-of-battle salvage and to crafting for credits | Tuning idea; loot rules in [tuning-recipes](../05-configuration/tuning-recipes.md) |

Not adopted: a hardware stutter fix (monitor on another graphics card),
server advertisements, farewell posts, an AI-generated answer quoted as a
source.

### S19 re-crawl (2026-10-17) - delta only

Third crawl (threads active since 15 October): 22 threads, about 60 posts
newer than the second crawl.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| SF36 | Clan creation cost is `ClanRegistrationCost` in `cloud/data/special_values.xml` | **File-verified** (`tokenCredits="1500"`); same as SF26 |
| SF37 | A database guide uses `use cosmosim_Admin`; a reader finds the database name follows the local user name, and `mongo.exe` fails with "connection refused" when `mongod` is not running | Database naming and start order: [mongodb](../06-database/mongodb.md), [config-system](../05-configuration/config-system.md); the guide's `premiumTill` for 2100 shows no premium (Q63) |
| SF38 | **Linux:** with the Steam runtime the install shows 0 B and an empty folder; selecting a Proton version downloads about 10 GB (the old Linux client depot has no server files) | Repeat of the 2026-10-14 tip already in [linux-proton](../04-installation/linux-proton.md) *(community)* |
| SF39 | A shared solo pack now also fills brawls with bots and rotates the brawl mode daily, gives premium to new accounts, raises the daily credit limit; another pack mixes PvP presets into bot fits and plays 12 v 12 | Shared configuration packs are code to review (SF24) |
| SF40 | Bots on the player's side are much weaker than the enemy bots; a reader suspects a hidden skill value that the pack lets act from battle 0 instead of 2 000 | Unverified; bot settings: [community-faq](../07-administration/community-faq.md) |
| SF41 | Seed chips outside open space: set `sv_autogenModulesEnabled = 1`, `sv_dbgAutogenDefs = 2` in three config functions | See batch 013 T5 → Q68 |
| SF42 | Low-rank seed chips rarely drop for low-rank ships | Lead for Q68 (drop rules) |
| SF43 | A public server's bots fly a premium rank-13 ship in rank-2/3 battles | Bot ship pools per rank: [community-faq](../07-administration/community-faq.md) |
| SF44 | **A campaign mission requires Detonation**, but the pack removed that mode (bots cannot use the bomb), so the campaign stalls and fails after five days; the player asks how to back up the account before switching configs | **File-checked:** the story quest `CAMPAIGN_QUEST_23` requires planting a bomb (six more quests use bomb objectives) → **Q61 amended**; backup: database copy with the Hub stopped ([administration](../07-administration/administration.md) §4) |
| SF45 | Players ask for older game versions | **Checked 2026-10-17:** Steam lists only the `public` branch (build 25826043 of 2026-10-09, Hub 1.99.0.167293); no older branch is offered |

Not adopted: cheating complaints without detail, farewell posts, account-loss
complaints (known, SF33), server advertisements.

### S19 re-crawl (2026-10-19) - delta only

Fourth crawl (threads active since 17 October): 17 threads, about 35 posts
newer than the third crawl.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| SF46 | Iridium crystals are `tokenCredits` in the account document | Known ([community-faq](../07-administration/community-faq.md)) |
| SF47 | **Storage above 2 750:** raise the `InventoryExtensions` steps in `cloud/data/special_values.xml`; above 4 096 slots a host saw packet loss on bot connections and a stuck server at about 11-12 connections; suspects a cap in the database. Another player un-commented the shipped `size="3000"` step (developer comment: postponed "until spring 2026") and set 4 000. A third warns that deleting rows breaks the game start | Steps and the commented 3 000 step **file-verified**; never delete rows = invariant **I-12** ([data-invariants](../05-configuration/data-invariants.md)). The 4 096 limit and its symptom → **Q71** ⚠ |
| SF48 | Ships cannot be added without limit either (RU chat, U3) | → Q71 |
| SF49 | **Battle-pass stage price:** `cost` in `data/gamedata/shared/battle_pass.lua` (xenochips, `gold = false`); after editing the Lua the purchase failed until the generated XML was changed too | `cost = 100, gold = false` **file-verified**; matches the Lua → XML layer rule (`prepare_shared`, [config-system](../05-configuration/config-system.md)) |
| SF50 | Writing `craftResources.resource_xenochips` into an account made the xenochip counter vanish from the HUD; workaround: buy xenochips in the unlocked store (max 400) | Unsafe database edit; xenochips are not a craft resource ⚠. Lead for the Q52 balance family |
| SF51 | Premium "disappears" with `premium_on_start = 2147483647`; tip: add `player` to `auth_infinitePremiumForRoles` (shows 24 h, refreshes at login) | Overflow = **Q63**; shipped `auth_infinitePremiumForRoles = "gm;support"` *(file)* |
| SF52 | **Cyrillic profile path:** start `mongod --dbpath C:\SC_MongoData` and point `dataPath` in `win64/local_server.xml` to it | `dataPath` key and its comment *(file)*; Steam file verification may restore the XML ⚠. Troubleshooting candidate |
| SF53 | `mongod.exe --dbpath` without a folder fails with "required parameter is missing" | Usage error; [troubleshooting](../04-installation/troubleshooting.md) |
| SF54 | Friends cannot queue together for PvE skirmish with a solo pack (endless search); a co-op map without bots or beacon | Packs set `maxPlayers` 1 (SF8 family, Q35) |
| SF55 | Clan ship solo: auto-created extra accounts, level 9 and three members | Consistent with [event-ships](../05-configuration/event-ships-mail-and-clan-ship.md) |
| SF56 | Wish: offline simulation of the old player market to buy blueprints | Demand signal; the market service is not in the node ⚠ |

Not adopted: cheating complaints, farewell posts, language quarrels, AI-tool
advice, download links of configuration packs (code to review, SF24).

### S19 re-crawl (2026-10-20) - delta only

Fifth crawl (threads active since 19 October): 9 threads, 39 posts.

| # | Statement (paraphrased) | Our status |
|---|-------------------------|------------|
| SF57 | **Storage above 4 096:** comment out the `Extension` steps and raise `baseSize` (one player uses 20 000) - works; the error appears only when extension sizes go above about 4-5 000; buying an extension resets the size to that step. The same change on `AutogenInventoryExtensions` (seed-chip storage) fails | `InventoryExtensions baseSize="50"`, `AutogenInventoryExtensions baseSize="10"` *(file: `cloud/data/special_values.xml`)* → **Q71** amended ⚠ |
| SF58 | Seed chips work only in open space, and not in its PvP zones | Lead; the per-mode rule is not located |
| SF59 | Ship parts as drops: add craft parts to the end-of-match search loot, per rank range | Same lever as the loot rules (b014 U1, Q45); tuning-recipes candidate |
| SF60 | A modified `store.xml` + `craft.lua` pack for special parts (third-party download) | Not adopted (rule 1, code to review) |
| SF61 | Rare paint schemes: unlock the whole store | Known (S22 MR5) |
| SF62 | A pinned forum thread links an official Star Conflict Discord server | Pointer only; not followed |
| SF63 | "The server does not run on Linux; the client does under Proton" | Contradicts the Wine reports for the server ([docker](../04-installation/docker.md)); one player's view |

Not adopted: farewell and balance-history posts, AI-tool talk, requests for
step-by-step help.

## Digest of S20 (public host's configuration overlay, read 2026-10-19)

> Leads, not facts: one public host's settings. Addresses, database names,
> key paths and the patch-server address are not copied.

The repository holds only the files the host changed (diffed against the
reference build). It is the same host as b013 T1 (forced faction events) and
b014 U1/U7 (rank-16/17 loot, new-account kit); commit messages give the
order of changes.

| # | Statement / change | Our status |
|---|--------------------|------------|
| CO1 | **Live store patching over HTTP:** `shard_local.cfg` sets `store_patchItemsUrl`, `store_patchSpecialValuesUrl` (an XML on the host's web server) and `store_patchItemsInterval 60` | **New to us.** Static *(file, 2026-10-19)*: Shard and GameRewardDispencer log `GameStore: Failed to g_httpClient->Request( store_patchItemsUrl )` / `( store_patchSpecialValuesUrl )`; DedicatedServer has `StoreSvc::ApplyStorePatch`; QuestServer has a matching `quests_patchUrl`. Engine defaults: empty URL, interval 0 ([engine-cvars](../05-configuration/engine-cvars.md)). Format and effect decoded statically → [http-store-quest-patch](../05-configuration/http-store-quest-patch.md); lab test still open → **Q72** |
| CO2 | Split node: MongoDB and Redis on another host (`db_mongoHosts`, `db_redisHost`), database names and `db_dedicatedDbCollectionSuffix` set to a non-user name; the services run under Wine (`Z:\home\...` key paths) | Consistent with [config-system](../05-configuration/config-system.md) and [linux-proton](../04-installation/linux-proton.md) |
| CO3 | `bind_ip` commented out in `cloud/mongodb/config.cfg` so the database listens on all interfaces (needed for the split) | MongoDB 2.6 without authentication: reachable by anyone who can reach the port unless a firewall limits it → [security](../07-administration/security.md) (S-30 family) |
| CO4 | Hub SSH console enabled with the host's own key pair | Known risk area (S16 Docker config, [security](../07-administration/security.md)) |
| CO5 | Economy: infinite premium for the `player` role, start balances, store price multipliers 0.5, iridium daily limit 100 000, talent sets free (`skills.xml` + `talents.lua`), fourth battle slot from account rank 1, clan-ship parts price 0 / duration 1 in both `clan_ship.lua` and `clan_ship.xml`, `sm_overloadCounterLimit 200` | Levers all known ([tuning-recipes](../05-configuration/tuning-recipes.md), [event-ships](../05-configuration/event-ships-mail-and-clan-ship.md)); edits made in Lua **and** generated XML |
| CO6 | Matchmaking: reworked queue templates, bot presets `BotsBZS_T3..T5`, longer PvP map lists with mode ids 4/10/11/12/23 | Host tuning; check with `tools/queue_lint.py` before reuse |
| CO7 | `cloud.xml` node `region` 1 → 2 | Unexplained ⚠ |

Not adopted: the `ansible` repository (infrastructure secrets in vault files;
not opened), full copies of shipped files.


## Digest of S16 (community Docker project)

Full evaluation: [docker.md](../04-installation/docker.md). Summary: MIT
scripts that run the 17-service node under Wine, native Mongo 2.6 and Redis,
two binary patchers, documented ports and failure signatures; the author
claims LAN and DNAT battles verified on 2026-10-10. Our independent check
covered the patch byte patterns only.

## Media in S12

`avatars/` (user avatars), `emojis/`, `discrub_media/` — irrelevant, can be
ignored/deleted.

## S14 - game wiki (usage notes)

* Folder: `random-materials/sc-media-wiki/` - Markdown pages in `corpus/current/`, structured records in `corpus/*.jsonl`, media in `corpus/media/`; entry point `corpus/COMMUNITY_SERVER_INDEX.md`.
* It documents **how the game behaved/was described**; it does not specify server algorithms. Use it to understand terminology (ship classes, modes, currencies, sectors) and to sanity-check config values; never promote a wiki statistic to a server fact without testing.
* Reuse terms of the wiki text/media are unresolved - do not copy wiki text/images into this repository; cite title + revision.
* The folder's own MIT licence covers only its tooling/notes, not the wiki content.
* Page `SPECIAL_OPERATIONS` (online wiki, read 2026-10-13): terminology "Special Operations" = 10-12-ship PvE operations with rank bands and an hourly/day-of-week rotation; used to map the term to the config's PvE raids and to cross-check `RaidSchedule` (V-12).

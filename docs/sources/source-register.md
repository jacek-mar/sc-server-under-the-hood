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
| S11 | Community wiki "STAR CONFLICT COMMUNITY EDITION" | `random-materials/STAR CONFLICT COMMUNITY EDITION.md` | C | Account fields, config tips, Linux, bots |
| S12 | Discord export `#general-eng` of the "Preservation Project" (batch 001: 5 717 messages, 2026-04-17 → 2026-10-10; batch 002: 5 900 messages, **superset** of 001 +183 from 2026-10-10 13:05–22:03 UTC) | `random-materials/Star_Conflict_Preservation_Project_00{1,2}.1*/` | C | RE leads (pak, RakNet), operator experiences |
| S14 | **Star Conflict game wiki** reference copy (5 381 pages, 3 313 media files, 696 MB; captured 2026-10-10 from the community wiki mirror, historical archive 2026-06-04). *Game* documentation, not server documentation | `random-materials/sc-media-wiki/` | C | Gameplay background (ships, modes, economy, currencies); **not** evidence of server behaviour. Rights unresolved (see its `ATTRIBUTION.md`) → keep private, cite page title/revision only |
| S13 | `files.list` | `…/star conflict/files.list` | A | Depot manifest |
| S15 | Discord export `#general-ru` of the same server, **Russian-language channel**, HTML (Discrub) export: 9 323 messages, 100 authors, 2026-04-20 → 2026-10-11 02:47 (batch 003) | `random-materials/Star_Conflict_Preservation_Project_003.ru-html/` | C | Release-day operator experience (RU community), RE leads, Docker announcement; **not** a superset of S12 (different channel) |
| S16 | Community project "Star Conflict — Unofficial Server in Docker" (GitHub, MIT; scripts/configs only, no game files); local snapshot of 2026-10-10/11 | `random-materials/starconflict-community-edition-docker-master/` | C (claims) / B (byte-pattern check we ran) | Linux/Wine hosting analysis: [docker.md](../04-installation/docker.md) |
| S17 | Fan site "The Outpost" - Server Guide Modules (snippet collection); evaluated page: `default_platform_config.lua` with comments translated to English (`https://www.graviton.at/outpost/server-guide-module/defaultplatformconfiglua-translated-to-english`, seen 2026-10-11) | web, link only (not copied) | C (spot-checked against S3: faithful) | Reading aid for the Russian comments; see digest below |
| S12/S15 b004 | Batch 004: partial JSON exports `Star_Conflict_Preservation_Project_004.eng-json-part` (23 msgs) and `...004.ru-json-part` (248 msgs, 213 new), both 2026-10-11 | `random-materials/Star_Conflict_Preservation_Project_004.*-json-part/` | C | Digest "batch 004" below; Q32-Q36, S-19 |
| S12/S15 b005 | Batch 005: partial JSON exports `Star_Conflict_Preservation_Project_005.eng-json-part` (155 msgs, 132 new) and `...005.ru-json-part` (389 msgs, 219 new), 2026-10-10 23:26 → 2026-10-11 18:47 (EN) and 12:07 → 13:48 (RU) | `random-materials/Star_Conflict_Preservation_Project_005.*-json-part/` | C | Digest "batch 005" below; Q38-Q40, Q28/Q34 amended |
| S12/S15 b006 | Batch 006: partial JSON exports `Star_Conflict_Preservation_Project_006.eng-json-part` (302 msgs incl. a 2-message release thread, 147 new, 2026-10-11 19:13 → 2026-10-12 09:05) and `...006.ru-json-part` (951 msgs, 485 new, 2026-10-11 13:52 → 2026-10-12 09:15) | `random-materials/Star_Conflict_Preservation_Project_006.*-json-part/` | C | Digest "batch 006" below; Q44-Q46, Q3/Q32/Q36 amended |
| S12/S15 b007 | Batch 007: partial JSON exports `Star_Conflict_Preservation_Project_007.eng-json-part` (64 msgs, 54 new, 2026-10-12 09:19 → 16:15) and `...007.ru-json-part` (229 msgs, 222 new, 09:16 → 16:10); continue batch 006 without a gap | `random-materials/Star_Conflict_Preservation_Project_007.*-json-part/` | C | Digest "batch 007" below (J1-J12); Q24, Q36, Q40, Q46 amended; S-07 note |
| S12/S15 b008 | Batch 008: partial JSON exports `Star_Conflict_Preservation_Project_008.eng-json-part` (83 msgs, 73 new, 2026-10-12 16:50 → 21:03) and `...008.ru-json-part` (255 msgs, 205 new, 16:12 → 21:18); both overlap batch 007 (no gap) | `random-materials/Star_Conflict_Preservation_Project_008.*-json-part/` | C | Digest "batch 008" below (K1-K14); security S-07 note, S-29, S-30; Q47 |
| S12/S15 b009 | Batch 009: partial JSON exports `Star_Conflict_Preservation_Project_009.eng-json-part` (63 msgs, 31 new, 2026-10-12 21:20 → 2026-10-13 06:11) and `...009.ru-json-part` (374 msgs, 199 new, 2026-10-12 21:19 → 2026-10-13 07:38); continue batch 008 without a gap | `random-materials/Star_Conflict_Preservation_Project_009.*-json-part/` | C | Digest "batch 009" below (M1-M9) |
| S12/S15 b010 | Batch 010: partial JSON exports `Star_Conflict_Preservation_Project_010.eng-json-part` (11 msgs, 11 new, 2026-10-13 08:44 → 16:21) and `...010.ru-json-part` (348 msgs, 327 new, 07:46 → 16:16); continue batch 009 without a gap | `random-materials/Star_Conflict_Preservation_Project_010.*-json-part/` | C | Digest "batch 010" below (N1-N13); Q49 amended |
| S18 | Community tool **SCPatcher / "Star Conflict Mod Manager" v0.1** by Furebel (Python/Tkinter text patcher with 8 bundled mods; released 2026-10-11 in `#general-eng` as `SCModManager_v0_1.zip`, temporary download link, no repository, **no licence stated**) | `random-materials/SCPatcher/` | C (claims) / B (fingerprints and patterns checked against S3/S4 by us) | Review: [community-mod-manager.md](../07-administration/community-mod-manager.md); loot-rule defect (Q45) |

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
| I11 | The Outpost fan site (S17) has a new **server setup guide** page; one university firewall blocked the site | S17 update; link only. Re-check for content during the next S17 visit |
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
| N1 | Localised text does not have to be packed back into a `.pak`; the client reads it from a folder | Consistent with the virtual file system: the `datasources*.txt` roots and the mounted `.pak` archives form one tree, and the shipped client already reads loose `data/gamedata` files ([data-files](../05-configuration/data-files.md), "Search roots"). The string tables are `strings/<language>/string.txt` inside `data/strings.pak` *(observed in an extraction)*. Which copy wins when the same path exists both loose and in a `.pak` has not been verified |
| N2 | Where are the module parameters of the alien ships and the biomorph hull? | Module definitions live in `data/gamedata/def/ex` (weapon → projectile → spell chain) - [module-defs](../05-configuration/module-defs.md). AI-only boss modules are separate definitions with an `_Mob` suffix (for example `Module_BossHealManta_Mob`) *(file)* |
| N3 | Craft recipes: one player first looked in `store.xml`; another pointed to `craft.lua`; the "iron plates" are called `Iridium_plate` internally; destroyers used to be built from resources and faction parts that are still in the files | **File-verified:** blueprint recipes are `BP_*` definitions with `craft_ingredients` in `data/gamedata/def/ex/craft.lua` (36 765 lines, exported from a designer spreadsheet; 1 346 definitions); ship recipes are `craftable_reagents` in `def/ex/ship.lua`; `store.xml` holds the compiled form (`<Ingr resource=... amount=...>`), generated by `prepare_shared`. `Iridium_plate` is the "Metal blank" resource (store id 3546, type 5), not iridium. Edit the Lua, then regenerate. Whether every old destroyer part still has a producer was not checked (Q34) |
| N4 | Xenochips are generated automatically and saved chips are stored in the account; overwriting an existing chip is hard, copying it and editing the copy is easier | Consistent with the seed-chip model: classes in `autogen.xml`, rolled items in `accounts.autogenItems` - [progression-xml-semantics](../05-configuration/progression-xml-semantics.md), invariant I-4 in [data-invariants](../05-configuration/data-invariants.md) |
| N5 | A host found how to start a **PvE custom game alone**: change the minimum player count from 3 to 1; there are no allied bots then | **File-verified:** `cvars.lobby_reqPlayersPvEMin = 3` and `lobby_reqPlayersPvEMax = 4` in `ConfigureLobbyServer()` of `cloud/data/default_platform_config.lua` (lines 1832/1834; comment "minimum/maximum players to start a PvE lobby" - our translation). The platform Lua assigns it, so a `lobby_server_local.cfg` cannot override it ([settings-reload-map](../05-configuration/settings-reload-map.md)). Bots in custom games are a lobby option (advanced options: 0 or 8-24 bots + skill preset; LobbyServer `botsInTeam1/2`); whether they join PvE missions is not proven statically -> [tuning-recipes](../05-configuration/tuning-recipes.md) |
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

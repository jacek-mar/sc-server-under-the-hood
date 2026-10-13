# Operator FAQ — questions the community asked in the first days

> Status: **draft (2026-10-11).** Built from the anonymised digests of the
> Discord exports (S12 English channel, batches 001–002, period 2026-10-06 →
> 10-10; S15 Russian channel, batch 003, period to 2026-10-11) and the
> community Docker project (S16), with every answer cross-checked against files
> in the depot or our own run where possible.
> Chat statements are *leads*, not facts: each answer carries an evidence tag.
> No names, ids, IPs or quotes of chat messages are reproduced.

## Getting started

**Q: Do I need Steam to run the server/client?** *(community, plausible)* Steam
was only the download channel and the Steam login; the depot is a plain
directory. The local built-in server accepts any e-mail/username + password
and creates the account on first login. Our own test used a Steam copy
([verification-log](../04-installation/verification-log.md) V-5); running a
copied depot without Steam is still open (Q20).

**Q: The game says "this application does not support remote session".**
*(static, `win64/game.exe` start-up code)* The client refuses to start
inside a Remote Desktop session; no switch disables the check. Start it
on the machine's local (console) desktop. The server services are not
affected.

**Q: I log in on "localhost" and get a fresh level-1 account — where is my old
progress?** *(community; matches architecture)* The official database is gone;
every node has its own MongoDB and every account is created empty. Progress can
only be rebuilt by editing the node's DB (see below). Accounts do not carry
between servers.

**Q: First start is slow / "connection to server lost" a few times.**
*(observed)* A node needs < 90 s to reach 17 services on a decent PC; on a
2-core CPU the Hub stalls and services die. Wait until all services are up
before logging in ([verification-log](../04-installation/verification-log.md)
V-1, V-5). Closing the game while the server windows are still starting leaves
stale processes (stop Hub cleanly, then `mongod`).

**Q: MongoDB window closes or the DB tool cannot connect.** *(community +
file-verified)* The depot ships MongoDB **2.6.12**; modern GUI clients refuse
it. Community reports NoSQLBooster **3.x (≈3.5.7)** works, the current major
does not. `mongod` must be running; the game/server need not be, but do not
edit while the node is writing. The DB has no authentication on 127.0.0.1
([mongodb.md](../06-database/mongodb.md)). On Windows a per-exe firewall prompt
or a hidden `cmd /c launch.bat` can kill `mongod` — start it directly.

**Q: Which MongoDB GUI works?** *(community, S15)* Reports from the Russian
channel: NoSQLBooster **5.2.x** and MongoBooster **3.5.x** connect; recent
releases do not. Start `mongod` first and let the server finish starting
before connecting. The same constraint (server speaks the MongoDB 2.6 wire
protocol only) applies to any GUI or driver — see
[mongodb.md](../06-database/mongodb.md). In a container use the `mongo:2.6`
image ([docker.md](../04-installation/docker.md)).

**Q: How do I connect a client to my (or a friend's) node?** *(community, S15 +
official page)* On the client login screen pick the **server** entry instead of
*localhost*, enter the node's IP and any login/password (the account is created
on first login). Give the plain IP: the Hub port is the default (3850); users
who typed another port from the logs failed. ⚠ not verified by us (Q2).

**Q: "Network error" / "OnDisconnect reason 0" when connecting to another PC.**
*(community, S15)* Most reports are from first attempts across a LAN or the
Internet. Checklist, most likely first: (1) all firewall/AV prompts answered or
rules created for every `cloud\*.exe` ([verification-log](../04-installation/verification-log.md)
V-8); (2) `cloud.xml` `<Node address=…>` holds an address the *client* can
reach — not `127.0.0.1` — and the Hub restarted afterwards (but see Q30: a
non-loopback address is the suspected trigger of a battle crash); (3) the battle port
range (UDP/TCP 35000+) is reachable, otherwise lobby works and battles fail;
(4) same game build as the server; (5) remote players only: the node's
router/NAT forwards the Hub, LoadBalancer, Shard, chat and battle ports (the
full set is still being minimised, Q25). A DedicatedServer crash at battle
start with a non-loopback node address was reported by the Docker project
author (Q30). Region-specific disconnects after ~20 s were reported by players
in one country and avoided with a VPN (Q26) — not a server fault so far.

**Q: Client language is Polish/Russian though Steam says English.**
*(community)* Add `-lang ENGLISH` to the Steam launch options (`%command%` is
replaced by the stock command, so it may come first or last). ⚠ not tested by us.

## Accounts and economy

**Q: Which DB fields are the currencies?** *(field names file-verified in
[schema.md](../06-database/schema.md); mapping from community)*

| In-game | `accounts` field |
|---------|------------------|
| Iridium (token credits) | `tokenCredits` (+ `tokenCredits_earnedToday`) |
| Credits | `credits` |
| GS (gold) | `goldCredits` |
| Synergy (account XP pool) | `accountExpPool` (reported: the *free* synergy counter did not show and the value went negative when set by hand ⚠) |

**Q: Why does editing the Lua config not give me gold?** The balances live in
the DB, not in `default_platform_config.lua`. The config only holds *starting*
values (e.g. `premium_on_start`, cost multipliers) and rules. *(file-verified)*

**Q: Why can't I earn more iridium in a day?** `cvars.sv_tokenCreditsDailyLimit
= 1000` in `default_platform_config.lua` (two occurrences) caps token credits
per day; the DB tracks it in `tokenCredits_earnedToday`. *(file-verified;
effect untested)* — relevant to Q12.

**Q: Permanent premium for admins?** `cvars.auth_infinitePremiumForRoles =
"gm;support"` gives infinite premium to accounts whose `admRole` is in the list.
*(file-verified)* Setting `admRole` in the DB might also be what community
"GM command" experiments need ⚠.

**Q: How do I make everything purchasable / cheaper?**
`cvars.store_allowAllItemsForBying = 1`; price multipliers for ships/modules/
ammo are near the top of the config (lines ~110–114). *(file-verified)* See
[tuning-recipes.md](../05-configuration/tuning-recipes.md).

**Q: How do I grant premium for 365 days?** `accounts.premiumTill` is the
**expiry time as a Unix timestamp in milliseconds** (int64; maintainer statement
2026-10-13 that it is a Unix expiry timestamp, millisecond unit confirmed
statically in `Shard.exe`, the same clock as `bannedTill`/`chatMutedTill`).
A seconds value (the community's "365 days in seconds", S15) is read as a date
in January 1970 - already expired - which explains the report that it "did not
work". Two ways:

* admin task (preferred): `{cmd: "give", uid, value: "premiumTill",
  amount: <hours>, reason, ...}` - the Shard adds `amount` x 3 600 000 ms to
  the later of the current expiry and *now* (8 760 h = 365 days); negative
  amounts shorten it (`premium already expired` / `premiumTime underflow`
  guards) - see [admin-tasks-howto](admin-tasks-howto.md);
* direct edit: `premiumTill: NumberLong(<epoch ms of the expiry>)`, e.g.
  `NumberLong(Date.now() + 365*24*3600*1000)` in the mongo shell; the client
  shows it after re-login (Q32).

**Q: How many identical unique modules can a ship carry?** *(file-verified,
S15 pointer)* `cvars.store_maxUniqueModules = 3` (normal ships) and
`cvars.store_maxUniqueModulesOnPremium = 2` (premium ships) in
`default_platform_config.lua`; the preceding comments describe exactly this
limit. Raise both to allow more.

**Q: I changed ship statistics in Lua — why did only some take effect?**
*(community, ⚠ mixed)* Users on their own node report that speed, energy and
manoeuvrability changed in battle while damage, hull and radar did not (and one
user saw one-shot kills). Which values the DedicatedServer takes from where is
open (Q29). **Static finding (2026-10-11, file-verified):** the per-ship numbers (`hull_health`, `shield_max`, `max_speed`, `energy_*`, resistances, `repair_cost`) are *not* in `objects/ships.lua` (that file holds only the 63 base classes) but in the exported rows of `data/gamedata/def/ex/ship.lua` and `ship_green.lua` - see [ship-defs.md](../05-configuration/ship-defs.md). Practical method *(community, later message)*: find the ship there and check its `inherit` (a base def change affects heirs); the base `hull_health`, `shield_max`, `max_speed` are not the final battle values; change **one parameter at a time** and note ship, field, old and new value; client-visible numbers need the data in an override `.pak` (loose Lua files are not read by the client). If the UI number changes but battle behaviour does not, the server computes it elsewhere. Remember that **only the server you run is affected** and that the
generated XML (`prepare_shared`) may need regeneration after data (not config)
edits ([tuning-recipes](../05-configuration/tuning-recipes.md)). Extreme values
reportedly crash a battle (type overflow) ⚠.

**Q: Can I move an account to another server?** Not officially. The DB document
could in principle be exported/imported between nodes — untested (Q18).

**Q: Can I move my progress from the official servers to my own?** *(b007
J10)* No - the official account database stayed with the developers. On your
own server items and ships can be granted by hand in MongoDB (each ship is an
element of `accounts.vessels` with a unique `vid`; alien/brawl ships also need
`data/gamedata/def/objects/gameplay_leviathan.lua` on server **and** clients
for their place and icon in the tree - community recipe, unverified).

**Q: A player forgot the password - can the admin reset it?** *(observed V-9;
b007 J1/J2)* The client has no password-change function. The stored value
(`accounts.password`, 64 hex characters) does not depend on the account: two
accounts with the same password store the same value, so copying the value of
an account whose password you know sets that password (test V-10
pending). Passwords are used exactly as typed - a trailing space is part of
the password (community).

## Battles, bots, PvE

**Q: Bots are weak (T1–T3) / only one AI enemy / want more bots.**
`cvars.mm_botsCount` (file value **6**, range 0..31) is the base; each queue can
override with `special.botsCount`. The *newbie* queues (`queueFlags.newbie = 1`,
e.g. lines 412/448/734/782) are what low-level accounts land in, so edits to
other queues appear to "do nothing" until the account levels up. Bot quality is
the preset: `botPresetType` / `botPresetNames` / `botPresetByTier`
([tuning-recipes](../05-configuration/tuning-recipes.md)). *(file-verified keys;
effects ⚠)* Reported: very high bot counts make bots stutter (stop shooting for
seconds) — a possible AI-update limit of one DedicatedServer process ⚠.

**Q: Why do two copies of the same queue exist?** `queuesConfig` vs
`queuesConfigLo`, chosen by `mm_lowOnlineLo/Hi` (250/300 online).
*(file-verified)*

**Q: Respawn penalty?** Newbie queues set `sv_respawnTimePenalty = 0` through
`ConfigureDediServerFlags`. *(file-verified)*

**Q: PvE mission level stays 1.** Stock behaviour per community: clearing a
mission opens the next level. Whether a server key forces it is open.

**Q: After-battle loot says "Nothing found" / skips.** Several operators hit
this on local and public nodes. Reported partial cause: loot-table def names
with and without a `_v3` suffix (`_1_3` vs `_1_3_v3`) in
`data/gamedata/shared/loot_tables.lua`, plus rank-dependent behaviour. ⚠ Open —
investigate with `sv_lootFailChance` (Q12).

## Events, battle pass, special currencies

**Q: Xenochips?** They exist only while the matching event is active; leftover
chips are destroyed at event end (in-game text, per community). Event windows
are dates in `default_platform_config.lua`; the shipped ones are in the past.
Reported: events can be started, but chips bought were not shown/usable — so
the full recipe is **unknown** ⚠ (`battle_pass.lua` has stages 2–4 commented
out).

**Q: Local server says "authorisation error"; the batch windows open and close
at once.** *(community, b006 I12; cause ⚠ unknown)* First check that MongoDB
really runs: `cloud\mongodb\launch.bat` stores the DB in
`%LOCALAPPDATA%\Targem\StarConflict\cloud\mongodb\data` *(file)*. One host
fixed this error by pointing `MONGO_DATA_PATH` in that file to a folder next to
`launch.bat`. A profile path MongoDB 2.6 cannot use (permissions, unusual
characters) is our unconfirmed guess. Start `mongod.exe` from a console to see
its error text instead of a vanishing window.

**Q: How do I see the console windows of all services?** *(file; effect ⚠
untested)* `cloud/data/hub.cfg` line 6 sets `hub_detachChildProcesses 1`
("launch server applications without a window"). Setting it to `0`, preferably
in a `hub_local.cfg`, should make the Hub start each service with its own
console. Service logs are in the profile directory in any case
([administration](administration.md)).

**Q: I enabled battle-pass stages 2-3 in the Lua, but completing a stage of
phase 2 errors.** *(file-verified, b007 J3)* The game also needs the stages in
the generated `cloud/data/battle_pass.xml`. The shipped XML names only stage-1
bundles, while `data/gamedata/shared/battle_pass.lua` defines stages 1-4 (2-4
commented out). After enabling stages in the Lua, regenerate the XML
(`prepare_shared.bat` - *inferred* from the output names in the executable,
needs MongoDB running) or use an XML that contains the
`Bundle_Battle_Pass_2_*` / `_3_*` entries; restart the node.

**Q: Can I remove a seed-chip (autogen) class I do not like?** *(file, b007
J5)* No. The comment in `data/gamedata/shared/autogen.lua` (translated from
Russian) says classes must not be removed, otherwise modules that were already
rolled become invalid and can no longer be re-rolled. Change values instead;
edits to affix definitions only affect newly generated chips.

## Multi-user / hosting

**Q: After I changed balance/ships on my server, players with the normal client
cannot join (or crash entering battle).** *(community, b006 I4, two hosts)*
Edits in `data/gamedata/**` (shared Lua) are client data too. It is **not** the
Shard's data-hash gate (open on a stock node). The likely cause is data
disagreement: the client builds defs from its own files but receives the
store from the server, and bundle/avatar/motto/drug store ids are assigned by
load order, so inserting or removing such a def shifts ids (⚠ hypothesis;
`tools/data_drift_check.py` reports such shifts). Adding or renaming defs also
trips the battle server's entity-definition check
([hub-protocol-and-framing](../08-reverse-engineering/hub-protocol-and-framing.md) §6a).
Append new defs at the end of a family or give them explicit ids.
Either ship the same files to every player (hosts are building launchers for
this), or keep changes to server-only files (`cloud/data/*`, the platform
config) where possible.

**Q: Can players' clients start directly on my server address?** Not
documented. A lead: the client config runs `exec address.cfg`, a file that is
not shipped (Q46, untested). Players currently type the address. One host
suggests a short alias in the Windows `hosts` file.

**Q: Can friends join my server?** *(community, architecture)* Yes: they enter
the node's IP/port in the login screen; local edits apply to the host only.
Open ports in [architecture.md](../03-architecture/architecture.md); the Hub
HTTP status port and Mongo should not be exposed. A LAN attempt failed for one
user (cause unknown, Q2/Q3).

**Q: Can I host it in Docker / on a Linux VPS?** *(community, S16; analysed
by us)* Yes, with caveats: a community image runs the 32-bit services under
Wine and uses native MongoDB 2.6 + Redis; it patches the executables and
publishes a wide port range. Evaluation, risks and a hardened blueprint:
[docker.md](../04-installation/docker.md).

**Q: Hardware needed?** Community estimates: a modern 6–12 core PC with
16–128 GB can host a few hundred players ⚠ (no measurement). Our node: 19
processes, ~1.2 GB idle. A host operator (S15) estimates ≈ 1.5–2 GB RAM per
open-world zone instance, with one instance per open-world location, and says
a rented 3-core/28 GB VPS-class machine is enough for ~500 online ⚠ — neither
measured by us (DK-8).

**Q: Several regions / separate DB?** Community: the DB endpoint can be set via
an undocumented block in `common_local.cfg`, giving a single shard DB with
region-specific services ⚠ (Q4/Q9 open). The game does not secure the Mongo
connection (no password) — keep it on a private network/VPN.

**Q: Can I use an external login/auth?** No documented hook; accounts are
created on first login against the node DB ⚠.

**Q: Which ports must a LAN/remote player reach?** *(observed V-9)* TCP
3801 and 3802 (login, hangar), TCP 3815 for chat (without it chat fails
silently - no error on screen) and UDP 35000 upwards, one port per concurrent
battle. The Hub port 3850 is internal. On the login screen choose the
`server` entry and type the host's address; the port box defaults to 3801.
Details: [verification-log V-9](../04-installation/verification-log.md),
[security §6.2](../07-administration/security.md) (tested port list).


### Batch 008 additions (2026-10-12)

* **How do I join a community server?** Start `win64\game.exe` directly (a
  Steam start also launches the local server and its windows). On the login
  screen switch the bottom-left selector from `localhost` to the server entry,
  type the host's address (the port box is pre-filled with 3801) and log in
  with a **name**, not an e-mail - a new name creates an account on most
  servers. The address has to be typed every time; an `address.cfg` preset
  has no effect (test V-10). *(community, consistent with V-9)*
* **Can I use my official account?** No - the official database was not
  released. Every community server has its own accounts. **Never reuse the
  password of your official or any other account**: servers store an
  unsalted fast hash, so a host can test guesses ([security S-07](security.md)).
* **Is it safe to download client files from a server or launcher?** Treat
  them like programs: game Lua can probably run native code (S-29, Q47).
  Prefer unmodified Steam files and trusted sources.
* **I broke a generated file such as `autogen.xml`.** It ships in
  `cloud/data`; restore it from the Steam depot (verify game files, or copy
  from a clean install) or regenerate it with `prepare_shared`. Keep backups
  before editing generated files.

### Batch 009 additions (2026-10-13)

* **How do I unlock the "Experimental destroyer"?** You cannot: it is the
  open-world pirate-event boss (`Ship_OW_Boss_PirateEvent` in
  `data/gamedata/def/ex/ow_bot_preset.lua`), an AI ship with 40 M hull.
  *(file-verified)*
* **What is "gs"?** Galactic Standards, the premium currency, stored as
  `goldCredits`. Grant it with the `give` admin task
  ([admin-tasks-howto](admin-tasks-howto.md)).

### Batch 010 additions (2026-10-13)

* **What do the `gm` and `support` roles do in the game?** Setting
  `accounts.admRole` shows nothing new in the client. The role matters to the
  Shard: it decides which admin tasks the account may request (privileges
  from `web_adm.admRoles`; `root` is always allowed), and
  `auth_infinitePremiumForRoles` (shipped `gm;support`) gives those roles
  infinite premium ([admin-tasks-howto](admin-tasks-howto.md) §4a). In the
  client, only the chat moderation UI checks privileges: with `mute`/`ban`
  a player's chat context menu gets a punishment entry (Mute/Ban with a
  duration). There is no GM panel. On a stock node `web_adm.admRoles` is
  empty, so `gm` and `support` have no privileges until you assign them.
  *(static)*
* **Can I start a PvE custom game alone?** Lower
  `cvars.lobby_reqPlayersPvEMin` (shipped 3) in `ConfigureLobbyServer()` of
  the platform Lua. A host reports that `1` works but no allied bots join
  ([tuning-recipes](../05-configuration/tuning-recipes.md), batch 010).
  *(file-verified key; effect reported)*
* **Should a server's website write rewards straight into MongoDB?** Direct
  edits reach the player only after a new login (Q32), and a service that
  holds the account in memory might write its own copy back ⚠ (not tested).
  The admin-task queue (`give`, `adminMail`) is the interface the Shard
  itself applies ([admin-tasks-howto](admin-tasks-howto.md)). *(observed for
  the admin tasks, V-10/V-11)*

## Modding

**Q: I added a new ship or item. Do players need my files?** Yes. Adding or
renaming definitions changes the entity-definitions hash that the battle
server compares with each client's; a client without the same definitions is
refused with `DR_BAD_GAMEDATA_VERSION`, and this check cannot be switched off
([hub-protocol-and-framing §6a](../08-reverse-engineering/hub-protocol-and-framing.md)).
Changing only *values* of existing definitions (for example hull points) does
not change the hash; the battle server's values win in battle while the
hangar shows the client's own values (V-10). *(static analysis + observed)*

**Q: Does the client need my edits?** Server-data edits (Lua/XML under
`cloud/` and `data/gamedata`) are used by your node; remote clients get server
behaviour only. Client asset/model work is separate (TPAK, see
[tpak-format.md](../08-reverse-engineering/tpak-format.md)); meshes were
reported workable in Blender ⚠ (not verified).

**Caveat (batch 004, ⚠ Q36):** the answer above is a simplification. Files in
`data/gamedata/shared` (quests, battle pass, bot presets, ship defs) are also
part of the *client* install; community members report that custom content
the client reads from its own files needs the same files on every player's
machine (or a launcher/patcher), while `cloud/data` is server-only. Test
before promising remote players custom ships or quests.

**Q: How do I change quest rewards?** Reported: edit `quests.lua` *and*
`quests.xml` (order: Lua, prepare scripts with Mongo running, then XML; repeat
after every change). Only one reward is displayed in the quest UI. Unverified
([tuning-recipes](../05-configuration/tuning-recipes.md)).

**Q: I edited the DB but the client shows old data.** Log in again; no way to
force a refresh is known (Q32).

**Q: Players hit an iridium limit. How do I raise it?** Daily cap:
`cvars.sv_tokenCreditsDailyLimit` (shipped 1000) in
`cloud/data/default_platform_config.lua`; one operator reports 100 000 works.
Absolute caps (credits 400 000 000, iridium/tokens 10 000, xenochips 300,
ship XP pool 5 000 000) are Lua globals in `data/gamedata/shared/reputation.lua`;
`cloud/data/aux_limits.xml` is generated from them by `prepare_shared`
(editing the XML alone is overwritten). A stock client keeps showing its own
copy of the cap ([pipeline](../08-reverse-engineering/config-pipeline-and-limiters.md)).

**Q: I get disconnected when I click too fast.** The Shard has a per-channel
request limiter (`sm_overloadCounterLimit`, `sm_reqFreqOverloadLine`,
`sm_reqFreqCalculationSamples`); raise the first two in
`cloud/data/shard_local.cfg`. Log text: `Disconnecting … due to request spam`.
The shipped `cloud/data/shard.cfg` line 6 sets `sm_overloadCounterLimit 20`
*(file)*; hosts report raising it (e.g. to 900) in that file (b006 I7).

**Q: Is there a mod manager?** *(S18)* Yes, a community tool ("Star Conflict
Mod Manager"/SCPatcher v0.1 by Furebel) applies a set of Lua/XML patches to a
local install with backups and the correct `prepare_shared` order. It does not
patch executables. Its mods are Python code: run only mods you trust. Review
and checks: [community-mod-manager](community-mod-manager.md).

**Q: The post-battle "search" gives nothing.** *(file-verified cause)* The
shipped loot rules reference `CommonRanks_<band>` tables, but only
`CommonRanks_<band>_v3` exist; `NeodiumDrop`/`LezortiumDrop` are missing too.
Alias the tables or rename the references:
[community-mod-manager §4.2](community-mod-manager.md). Runtime effect: Q45.

**Q: How do I credit DLC content to a player?** Not solved. DLC ownership is
normally checked through Steam's publisher API (no key on a community node);
the DLC bundles are `Bundle_DLC_*` in
`data/gamedata/def/objects/bundles_dlc.lua`. For now only manual DB grants of
the bundle contents work. Static research: Q44.

**Q: Where are custom seed chips (autogen modules) defined?** *(file, b006
I10)* `cloud/data/autogen.xml` and `autogen_special_values.xml`; the admin task
`giveAutogenModule` grants one ([shard-admin-tasks](../08-reverse-engineering/shard-admin-tasks.md)).
The field semantics are not documented yet.

**Q: Can bots be stronger for high-rank players?** Name a preset per rank band
in the queue template (`special.botPresetNames`); example in
[bot-presets](../05-configuration/bot-presets.md) section 5. A broken block is
ignored silently - test with one queue first, or run
[`tools/queue_lint.py`](config-validation-tools.md). If both `botPresetByTier`
and `botPresetNames` are set, the tier table wins; a list is a random pick.

**Q: How do I get the event ship parts (Helicon, Salyut)?** Static analysis ([details](../05-configuration/event-ships-mail-and-clan-ship.md)): Salyut parts came from event bundles, a blueprint and event quests; Helicon parts have no producer in the shipped data. Reported: the parts
have no store UI and no prices; add the defs to the account in the DB, or
change the craft recipe (`def/ex/craft.lua`). See
[tuning-recipes](../05-configuration/tuning-recipes.md) (batch 005) and Q34.

**Q: Where are the craft recipes?** *(file-verified, b010 N3)* Blueprints:
`BP_*` definitions in `data/gamedata/def/ex/craft.lua` (`craft_result`,
`craft_ingredients` with `def` and `count`); ships built from parts:
`craftable_reagents` in `def/ex/ship.lua`. `store.xml` only holds the
compiled copy - edit the Lua, then run `prepare_shared`. `Iridium_plate` is
the "Metal blank" resource, not iridium.

**Q: My new item/ship shows a blank or raw-text name.** *(file, B-8)* Definitions have no automatic naming: set the def's `uiName` (and `uiDesc`) to string keys and add those keys to the client string table `strings/<language>/string.txt` on **every** player's install. Most definitions in the game carry no name on purpose (they are internal parts); only player-visible items do. See [data-files](../05-configuration/data-files.md) "Definition display names".

**Q: I put another model on a ship and it has no weapons or modules.**
*(file-verified fields, b010 N6)* Each hull class binds every module slot to a
named bone of its model (`slot_bones` in `data/gamedata/def/objects/ships.lua`,
for example `gun`, `gun_1`), next to `weapon_slots` and `fire_sectors`. If the
new model lacks those bones, the slots have nowhere to mount *(inferred)*.
Boss and alien hulls added as player ships may not move at all (Q49).

**Q: I changed the store and the server no longer starts.** An invalid or
mistyped def name is the usual cause (check names with
[`tools/defname_check.py`](config-validation-tools.md)); restore the file (keep a copy, or use
Steam "verify files", which also drops all your other edits).

**Q: Why can't players send mail / ships by mail?** Sending needs an anti-bot counter of at least 50 (`shard_minAntibotCounterForMailSending`) and 2-step authorisation; ships are not mailable, parts/resources are ([details](../05-configuration/event-ships-mail-and-clan-ship.md)).

**Q: How do I change the clan-ship (dreadnought) requirement?** `cvars.clan_shipBuildHighRanks` (shipped 3 rank-9 members), `clan_shipPartsCanBuild`, `clan_shipUpgradeCanBuild` in `ConfigureClanServer()`; prices/durations in `data/gamedata/shared/clan_ship.lua` (`ClanShipKF`).

**Q: How do I run GM actions (give module, ban, reset)?** Shard admin tasks are jobs in the Mongo collection `adminTasks`; see [shard-admin-tasks](../08-reverse-engineering/shard-admin-tasks.md) and the operator how-to [admin-tasks-howto](admin-tasks-howto.md) (verified examples).

**Q: Where do I find more community guides?** The fan site "The Outpost" keeps
a *Server Guide Modules* snippet collection, including an English translation
of the comments of `default_platform_config.lua` (S17 in the
[source register](../sources/source-register.md); link only).

**Q: Can a squad enter PvP / random missions?** Reported failing for some
operators. Static analysis ([matchmaking guide §8](../05-configuration/matchmaking-guide.md)): arcade queues need squad rank 1-15, coop queues rank 1-15 and `mmValue` 0-99; accounts edited to own rank 16/17 hulls fall outside. Runtime test pending (Q35).

**Q: GM / chat commands?** No chat-command interface exists, but the binaries contain an admin/GM toolbox: 58 Shard admin tasks (`ban`, `mute`, `assignRole`, `giveSpecModule`, `unlockAllVesselNodes`, `copyAccount`, ...) and `cheat_*` console commands in the QuestServer, AchievementServer, ClanServer, Universe and the battle server (`cheat_giveQuest`, `cheat_setOwner`, `cheat_equipWeapon`, ...). Full list with arguments: [console-commands.md](console-commands.md) *(static, not yet executed; how to invoke the Shard tasks is Q37)*. Admin roles also exist in the DB (`admRole`). Our SSH engine console is documented in verification-log V-7.

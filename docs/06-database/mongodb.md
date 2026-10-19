# MongoDB and persistent state

> Status: **Stage 1 draft.** Database *names* are from the data directory and
> logs; *field* names come from the official page and the community wiki.
> Schema discovery (collections, document structure) is a Stage 2 task.

## 1. Engine and location

| Item | Value |
|------|-------|
| Server | MongoDB **2.6.12** (Windows x64, bundled in `cloud/mongodb/`) — MMAPv1 storage, no auth by default |
| Bind | `127.0.0.1:27017` (`cloud/mongodb/config.cfg`) |
| Data dir | `%LOCALAPPDATA%\Targem\StarConflict\cloud\mongodb\data` (set by `launch.bat` / `local_server.xml`) |
| Shell | `cloud/mongodb/mongo.exe`; `admin.bat` opens `127.0.0.1/cosmosim` |
| Tools | `mongodump`, `mongorestore`, `mongoexport`, `mongoimport` … in the same folder — use these for backups |

> Modern MongoDB drivers/GUIs cannot talk to 2.6. Use NoSQLBooster 4.7.5
> (Windows reports) or 5.2.12 (Linux AppImage report, S11 update), MongoBooster
> 3.5.x, or the bundled `mongo.exe`. Newer versions may refuse the server.

## 2. Databases (observed on disk)

For a local build the Shard rewrites the default DB names by appending
`_<WindowsUserName>`:

| DB | Purpose (inferred from name; verify) |
|----|--------------------------------------|
| `cosmosim_<user>` | Main game DB — `accounts` and other game state |
| `stats_cosmosim_<user>` | Statistics — `accountsStats` etc. |
| `achievements_<user>` | Achievement progress |
| `games_<user>` | Battle/session records |
| `delivered_<user>` | Delivered rewards/mail items |
| `logs_<user>` | Action/audit logs |
| `local` | MongoDB internal |

Each DB occupies 64 MB + 16 MB `.ns` file at creation (MMAPv1 preallocation).

> The Shard also rewrites `db_dedicatedDbCollectionSuffix` (default empty) to `_<WindowsUserName>` — collections used by dedicated servers carry that suffix.
>
> **Changing the machine name or Windows user changes the DB names** and
> hides existing data. To move a save between PCs, rename the databases
> (`mongodump` → `mongorestore --db`) or set `db_name`/`db_stats_name`
> explicitly in `common_local.cfg` *(unverified)*.

## 3. Accounts (`cosmosim_<user>.accounts`)

One document per account (UID). Passwords are stored hashed.
Fields confirmed by the community/official page:

| Field | Meaning |
|-------|---------|
| `goldCredits` | Galactic Standards (GS) |
| `credits` | Credits |
| `tokenCredits` | Iridium |
| `accountExpPool` | Clearance (account) experience *(also called synergy by some)* |
| `accountRank` | Clearance level |
| `vesselExpPool` | Free ship experience / free synergy |
| `premiumTill` | Premium expiry time: Unix epoch **milliseconds** (int64; 0 / past = no premium) |
| `bannedTill` | Ban expiry (the community wiki says `banTill`; **verified name is `bannedTill`**, int64) |
| `craftRessources.pve_ressource` | PvE "insignias" |
| `unlimPvE_player1Level1`, `…Level2` | PvE attack/defence levels |
| `unlimPve_missionLevels` | PvE mission levels (needs testing) |
| `lootCounters.rareAttemptsCount` | Loot attempt counter (needs testing) |

IDs of ships, modules etc. live in `data/gamedata/**.lua` (e.g.
`gamedata/shared/def_ids.lua`).

`stats_cosmosim_<user>.accountsStats` also contains per-account data. The
community suspects (unconfirmed) that editing it is why some accounts got
"bricked" — edit `accounts` first and leave `accountsStats` alone unless needed.

## 3a. Id counters (`cosmosim_<user>.counters`) *(static + observed, 2026-10-14)*

New ids are not computed from existing documents. The Shard takes them from
the `counters` collection: `findAndModify({_id: <name>}, {$inc: {c: 1}})`
(`m3d::persistence::AcquireCounter`; a batched variant reserves several ids
for a new account's starting kit). The stored `c` is the **next free id**
(lab node: `uid` 5 with four accounts, `vid` 12 with highest vessel id 11).

| Counter | Used for |
|---|---|
| `uid` | accounts |
| `vid` | `accounts.vessels[].vid` - unique per database, not per account |
| `iid` | `accounts.items[].iid`, `autogenItems[].iid` (ids of consumed items are not reused) |
| `mailId`, `sqid`, `leagueTmId`, `advertId`, `steamOID` | mail, squads, league teams, adverts, Steam orders |

**Hand-made grants** (server stopped): give the new vessel or item the
current counter value, then increment the counter by one. Copying "highest id
+ 1" without updating the counter makes the next purchase reuse the id
(details and open runtime part: Q57/Q54 in
[open-questions](../08-reverse-engineering/open-questions.md)).

**Balances** are int64 in the database, but the game treats them as signed
32-bit values: currency caps above 2 147 483 647 are refused when data is
prepared. Keep hand-set balances below that value (Q52).

## 3b. Where owned items are stored *(observed, V-14; ship and module rows from the schema)*

| Owned thing | Account field | Value |
|---|---|---|
| ship | `vessels[]` | `{vid, defName, equipped, munition, ...}` |
| module, weapon, munition in storage | `items[]` | `{iid, defName, amount, ench, timeEnd}`; fitted items are referenced from `vessels[].equipped[]` by `iid` |
| loaded munition | `vessels[].munition[]` | `{def, amount, res}` (field `def`, not `defName`) |
| craft resource, part, blueprint | `craftResources.<defName>` | amount |
| seed chip (autogen) | `autogenItems[]` | `{iid, upgradeLevel, rollData, exp}` |
| title | `acquiredTitles[]`; active `title` | `{id: <id from titles.xml>}`; active id, 0 = none |
| avatar / motto | `acquiredAvatars` / `acquiredMottos`; active `avatar` / `motto` | objects `{<defName>: 1}`; active = `defName` string |
| custom element, not fitted | `freeVesselCustomElements` | `{<element name>: <count>}` |

New `iid`s come from the `iid` counter (§3a). Not yet observed: where junk
items are kept.

## 4. Safe editing procedure

1. Start the server **at least once**, log in, then log out and close both the
   game and the server (MongoDB may remain running).
2. `launch_mongodb.bat` (if it is not running) and connect with the tool.
3. Edit with the tool (Run/Save). Keep numeric types (int32 vs int64 vs double)
   — do not type values larger than the type allows; use sane values.
4. Start the server and log in again to see the changes.
5. Back up first: `mongodump --out backup-<date>`.

## 5. Related

* Official: "Removing the players' data" — delete the data directory.
* Account migration idea from the community: a tool that imports the client's
  ship-preset file into the DB (not for all items: skins/stickers/seed chips
  are not included).
* Gaijin: *In-game items cannot be transferred to unofficial servers* — any
  restoration is the server owner's decision.
* Personal-data caution: the `accounts` collection may contain e-mail/login
  data and device fingerprints — see
  [administration → privacy](../07-administration/administration.md#privacy).

## 5a. Verified schema (Stage 2)

The full list of **7 databases, 40+ collections, indexes and ~700 field paths**
is in [schema.md](schema.md) (generated from a live node, types only); which executables reference each collection name is in [service-data-map](../08-reverse-engineering/service-data-map.md). Key
facts:

* `cosmosim_<user>`: 32 collections — `accounts` (≈ 220 field paths; unique
  indexes on `username`, `uid`; lookups by `puid`, `steamID`, `nickName`),
  `auth`, `puids`, `mailbox`, `clans`, `squads`, `lobbies`, `mmQueue`
  (matchmaker queue entries), `leagueTeams`, `tournament*`, `universes`,
  `warMap`, `conflicts`, `leaderboards`, `scripts` (ScriptsServer state),
  `globals`, `counters`, `vlocks`, `steamOrders`, `adminTasks`/`adminMail`,
  `surveys*`, `teaching`, `thumbsUp`, `reports`, `social`, `welcomeMsg`.
* `stats_cosmosim_<user>`: `accountsStats` (≈ 90 paths, 12 indexes),
  `fingerprints` / `suspiciousFingerprints` (PC fingerprint data used for
  `isSingleUidOnPC`), `botPresets*`, `onlineCounter` (online player samples —
  the value matchmaker uses for low-online mode), `earlyActionsLogs`,
  `playerActionsLogs`.
* `games_<user>.games`: one document per battle (≈ 230 paths: players,
  vessels, rewards, leaver data) — also the **GameSessionParameters** the
  DedicatedServer reads.
* `achievements_<user>.achievements`, `delivered_<user>.delivered`,
  `logs_<user>.logs`.
* Field names confirmed for editing: `credits` (int64), `goldCredits` (int64),
  `tokenCredits`, `vesselExpPool`, `accountExpPool`, `accountRank`,
  `premiumTill` (int64), `bannedTill` (int64), `craftResources.<resource>`,
  `unlimPve_missionLevels`, `lootCounters.{rare,epic}{Attempts,Picks}Count`,
  `lootCounters.resetTime`.

## 6. TODO (Stage 2)

* Dump collection list + sample documents (anonymised) for every DB.
* Document indexes (created by `Persistence::_CreateTables`).
* Confirm the effect of editing `accountsStats`.
* Test `db_*` cvars for custom DB names/remote Mongo.

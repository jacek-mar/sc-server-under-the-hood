# Admin tasks: operator how-to (mute, give, player info, ...)

> For hosts of a community node. Built on the lab results of **V-10**
> ([verification-log](../04-installation/verification-log.md), V-10/V-11)
> and the static analysis in [shard-admin-tasks](../08-reverse-engineering/shard-admin-tasks.md),
> [shard-admin-tasks-table](../08-reverse-engineering/shard-admin-tasks-table.md)
> and [shard-task-privileges](../08-reverse-engineering/shard-task-privileges.md).
> Evidence tags: *(observed)* = tested on a lab node, *(static)* = read from the
> binary, not yet tested.

## 1. How it works

The Shard polls the MongoDB collection **`adminTasks`** in the game database
and executes every new document addressed to it. There is no admin command in
the game client or on the Shard console for this - you **insert a document**
(by hand in the mongo shell, from a script, or from a web panel you build).
The result is written back into the same document a few seconds later.
*(observed)*

Requirements *(observed)*:

1. The node is running (the Shard picks tasks up only while it runs).
2. The **requesting account** has `accounts.admRole = "root"` (or a role whose
   privileges allow the task; role table in DB `web_adm`, collection
   `admRoles`, layout in §4a - static, not yet tested). A `player` requester gets
   `Not enough privilege`.
3. The task document contains:

| Field | Value | Note |
|---|---|---|
| `cmd` | task name, e.g. `"mute"` | 58 names in the [table](../08-reverse-engineering/shard-admin-tasks-table.md) |
| task parameters | e.g. `uid`, `reason`, `amount` | at the top level of the document; uids as `NumberLong` |
| `requestedByUid` | uid of the root account (`NumberLong`) | authorisation is checked at execution time |
| `serviceType` | `2` (Shard) | |
| **`pickedBy`** | **`0`** | **mandatory**: the Shard's selector is `{serviceType: 2, pickedBy: 0}`; without this field the task waits forever and nothing is logged |

After execution the Shard adds `pickedBy` (its service id), `pickedAt`,
`finishedAt` (milliseconds since 1970), `success` (1/0), `errMsg` and, for
read-only tasks, `result`. Shard log lines: `Sys_PickupAdminTasks: picked
admin task '<cmd>'`, `Sys_AdminTask: performing '<cmd>'`. With the Shard
cvars `ctm_debugTaskPickup 1` / `dbg_logAdminTask 1` (settable live on the
SSH console) the selector and task documents are logged. *(observed)*

## 2. Step by step (mongo shell)

Open the bundled shell on the node machine (`cloud\mongodb\mongo.exe`,
loopback only) and select the game database. The name depends on the build
(`cosmosim_<suffix>` on a local build); list it with `show dbs`.

```js
use cosmosim_<suffix>
// 1. make your admin account root (once) - uid of YOUR account
db.accounts.update({uid: NumberLong(1)}, {$set: {admRole: "root"}})

// 2. queue a task (example: read account data of uid 2)
db.adminTasks.insert({cmd: "playerInfo", uid: NumberLong(2),
    requestedByUid: NumberLong(1), serviceType: 2, pickedBy: 0})

// 3. a few seconds later: read the result
db.adminTasks.find().sort({_id: -1}).limit(1).pretty()
```

Set the admin account back to `player` when you do not need it
(`$set: {admRole: "player"}`); see section 5.

## 3. Verified tasks *(observed, V-10 and V-11)*

| Task | Parameters | Effect / result | Errors seen |
|---|---|---|---|
| `playerInfo` | `uid` | `result` = `admRole`, `username`, `nickName`, `uid`, `bannedTill` | - |
| `mute` | `uid`, `durationInHours`, `category`, `rules` (string), `reason` | `accounts.chatMutedTill` = now + duration (ms); stored `muteCategory` is a translated value (category 1 -> 5); **effective immediately**: the player gets a chat notice with the remaining time and cannot send | - |
| `cancelMute` | `uid`, **`reason`** | `chatMutedTill` = 0, chat works at once | `Specify the reason please` without `reason` |
| `give` (currency) | `uid`, `reason`, `value` = `"credits"` or `"goldCredits"`, `amount` | **adds** `amount` to the balance; visible at the player's next login | - |
| `give` (free synergy) | `uid`, `reason`, `value: "vesselExpPool"`, `amount` | adds to `accounts.vesselExpPool` (V-11) | - |
| `give` (ship) | `uid`, `reason`, **`vid`**, `value` = `"level"` / `"hullCondition"` / `"munition"` (+ `index`), `amount` | `level`: **adds** levels to that ship (1 -> 4 with `amount: 3`), logged as `ACCOUNT_EXP_GOT`; refused for upgradeable ships (`Can't set level for upgradeable ships`) (V-11) | `Incorrect value name` for anything else - **there is no per-ship `exp` value**; use `vesselExpPool` |
| `unlockAllVesselNodes` | `uid` + **either** `vid` **or** `vesselDefName` (optional `specModuleDefName`) | sets `vessels[].unlockedMask` = `NumberLong(-1)` (all research nodes) on that one ship; level/exp unchanged (V-11) | `Both 'vid' and 'vesselDefName' are not specified` / `... are specified`, `Vessel not found` |
| `assignRole` | `uid`, `role` (+ `reason`) | sets `accounts.admRole` (V-11); no audit-log entry | - |
| `ban` / `cancelBan` | `ban`: `uid`, `category`, `durationInHours`, `rules` (string), `reason`; `cancelBan`: `uid`, `reason` | `bannedTill` = now + duration (ms), `banCategory` stored as given (1 -> 1, unlike mute) and kept after `cancelBan`, which sets `bannedTill` 0 (V-11); no audit-log entry | - |
| `changeNickName` | `uid`, `nickname` (+ `reason`) | updates `accounts.nickName` **and** `stats_<db>.accountsStats.nickName`, audit `NICK_CHG {oldNickName, nickName}` (V-11) | `Invalid nickname` - the check is stricter than account auto-creation: a name that login accepted was refused here |

Examples:

```js
db.adminTasks.insert({cmd: "mute", uid: NumberLong(4), durationInHours: 1, category: 1,
    rules: "1", reason: "spam", requestedByUid: NumberLong(1), serviceType: 2, pickedBy: 0})
db.adminTasks.insert({cmd: "cancelMute", uid: NumberLong(4), reason: "appeal accepted",
    requestedByUid: NumberLong(1), serviceType: 2, pickedBy: 0})
db.adminTasks.insert({cmd: "give", uid: NumberLong(3), value: "credits", amount: 1000000,
    reason: "event prize", requestedByUid: NumberLong(1), serviceType: 2, pickedBy: 0})
db.adminTasks.insert({cmd: "unlockAllVesselNodes", uid: NumberLong(2), vid: NumberLong(4),
    reason: "restore", requestedByUid: NumberLong(1), serviceType: 2, pickedBy: 0})
```

Which changes are audited: the game database's audit collection
`logs_<db>.logs` records `give` of a ship level (`ACCOUNT_EXP_GOT`), gold
(`ADMIN_GOLD`) and nickname changes (`NICK_CHG`); bans and role changes were
**not** recorded there (V-11) - keep your own log if you need one (the task
documents in `adminTasks` remain and carry `requestedByUid`).

### 3a. More verified tasks and queue behaviour *(observed, V-13)*

| Task | Parameters | Effect |
|---|---|---|
| `give` (premium) | `uid`, `reason`, `value: "premiumTill"`, `amount` = **hours** | `premiumTill` (epoch ms) = max(`premiumTill`, now) + `amount` x 3 600 000; negative `amount` shortens it (static: `premium already expired`, `premiumTime underflow`) |
| `give` (iridium) | `value: "tokenCredits"`, `amount` | adds |
| `set` | `uid`, `reason`, `value` (e.g. `"credits"`), `amount` | **sets** the exact value |
| `giveTitle` | `uid`, `title` (id from `cloud/data/titles.xml`) | appends `{id: <title>}` to `acquiredTitles`; the active title (`title`, a number, 0 = none) is not changed (V-14) |
| `giveVesselCustomElement` | `uid`, `item` (custom element name from `vessel_custom_elements.xml`) | `freeVesselCustomElements.<name>` = count (NumberLong) (V-14) |
| `giveAutogenModule` | `uid`, `classId` (from `autogen.xml`), `rank` | rolls a seed chip into `autogenItems[]`: `{iid, upgradeLevel, rollData, exp}` (V-14) |
| `give` (store item) | `uid`, `reason`, **`item` = numeric store id** (`store.xml`), `amount`; no `value` | munitions -> `items[]` (stacks onto an existing entry); craft resources, parts, blueprints -> `craftResources.<defName>`; avatars / mottos -> `acquiredAvatars` / `acquiredMottos` and become active. Junk: `Unsupported item type` (V-14) |
| `mutePermanent` / `banPermanent` | as `mute` / `ban` | `chatMutedTill` / `bannedTill` = 2^63 - 1 (int64 maximum - tools must not convert it to a floating-point number); lifted by `cancelMute` / `cancelBan` |
| `enterMMode` / `leaveMMode` | `minutesLeft` / none | maintenance mode without a console: countdown in the Hub log, at zero the Shard disconnects all clients; tasks keep working; `leaveMMode` ends it |
| `createAccount` | `username`, `nickName`, `password`, `role`, `allowLogin` | new account (uid from `counters`, `accountsStats` created; starter kit at first login). **`password` is stored as given** - pass a value in the stored format or the account cannot log in |
| `assignRolePrivileges` | `role`, `privileges` | merges the role into `web_adm.admRoles`; effective after a Shard restart (§4a) |

Queue behaviour: **one task every ~5 s** (about 12 per minute); identical
documents with different `_id`s are both executed; a task left "picked"
without `finishedAt` (Shard stopped mid-task) is never re-picked; extra
top-level fields are ignored.

## 4. Other tasks *(static - parameters from the binary, untested)*

| Task | Parameters found in the handler | Privilege | Notes |
|---|---|---|---|
| `give` (other) | `achievement`, `factionRep`, `eventCredits`, `accountRank` (refused on a `live` server) | propertyEdit | ship values: see §3; message: "Specify the vid = <vid> (if changing vessel attr) value = <name>, index = <index> (if value is array), amount" |
| `resetAccount` | `uid` | (see table) | destructive |

Full list with all 58 tasks and their privilege ids:
[shard-task-privileges](../08-reverse-engineering/shard-task-privileges.md).
Some tasks refuse to run while `cl_versionType` is `live` (the default), e.g.
`set rank`, `giveTestAutogenModule` *(static)*.

## 4a. Custom roles: `web_adm.admRoles` *(static 2026-10-13; read timing and a grant/deny case observed, V-13)*

> **Observed (V-13):** the Shard reads `admRoles` **only at start-up**. A role
> written directly or with `assignRolePrivileges` while the node runs grants
> nothing until the next restart; afterwards a role `{gmView: 1}` may run
> `playerInfo` and is refused `give` (`Not enough privilege`).

Read from `Shard.exe` (`AcquireAdminRoles`, `AssignRolePrivileges`, the
privilege check next to `AccessPrivileges.cpp`):

* Database = cvar `db_adm_name` (default `web_adm`), collection `admRoles`.
  The Shard reads the documents and takes the field **`roles`**, an object
  whose keys are role names and whose values are objects of
  **privilege name -> number**. A privilege counts as granted when its value
  is a non-zero number (read as an integer, missing = 0):

  ```js
  // web_adm.admRoles - one document (inferred layout)
  { roles: {
      gm:        { gmView: 1, mute: 1, cancelMute: 1, ban: 1 },
      support:   { gmView: 1, mute: 1 }
  } }
  ```

  Privilege names (the 17 ids of
  [shard-task-privileges.md](../08-reverse-engineering/shard-task-privileges.md)):
  `play`, `playInMaintenance`, `mute`, `mutePermanent`, `ban`,
  `banPermanent`, `gmView`, `propertyEdit`, `adminView`, `adminEdit`,
  `privilegesControl`, `promoControl`, `observeGames`, `playFreeSpace`,
  `giveFreeSpace`, `playClosedPTR`, `roleAssignment`. Note: `cancelMute`,
  `cancelBan` etc. are *task* names - the role needs the privilege the task
  is registered with (`cancelMute` -> `mute`, `cancelBan` -> `ban`), so the
  example above is equivalent to `{ gmView: 1, mute: 1, ban: 1 }`.
  Use the **names**: the client's `MasterServer.Privilege` enum
  ([masterserver-enums](../08-reverse-engineering/masterserver-enums.md)) is
  an older 15-entry list whose id 14 is the closed-PTR privilege, while the
  Shard's table has `giveFreeSpace` = 14, `playClosedPTR` = 15,
  `roleAssignment` = 16.
* `root` is special: the check returns "allowed" for `root` before looking at
  the table, and if the stored table has no `root` entry the Shard creates
  one **in memory** with all 17 privileges. A fresh node therefore works
  with `admRole: "root"` and an empty `web_adm` (as observed in V-10).
* Writing roles without the mongo shell: admin task
  **`assignRolePrivileges`** (`role` = name, `privileges` = the object
  above; requester needs `privilegesControl`). The Shard replaces that role's
  entry and writes the whole `roles` object back with `$set` (upsert).
* Give an account the role with the task `assignRole` (privilege
  `roleAssignment`) or by setting `accounts.admRole` directly; the role name
  is also what `auth_infinitePremiumForRoles` (shipped `gm;support`) matches.
* Re-read *(observed, V-13)*: at Shard start-up only; no reload while the
  node runs, also not after `assignRolePrivileges`.
* **What a role shows in the game client** *(static, client UI scripts,
  2026-10-13)*: the only account-privilege checks in the shipped client are
  in the chat moderation UI (`data/ui/scripts/work/uigamefuncs.lua`,
  `data/ui/scripts/windows/complaintwnd.lua`, via
  `MasterServer_CheckAccessPrivilege`). An account with `mute`, `ban`,
  `mutePermanent` or `banPermanent` gets an extra **punishment** entry in a
  player's chat context menu; it opens the complaint window in punishment
  mode with a duration list and **Mute**/**Ban** buttons (a permanent
  duration needs the `*Permanent` privilege). No client script checks
  `gmView`, `observeGames` or the other privileges, and there is no GM
  panel. Consequence: on a stock node (`web_adm.admRoles` empty) an account
  with `admRole: "gm"` or `"support"` has **no privileges** and sees nothing
  new except infinite premium; give the role privileges first (above), or
  use `root` *(inferred: `root` gets all privileges in the Shard, so it
  should see the punishment entry too - not observed)*.

## 4b. Broadcast mail: the `adminMail` collection *(static, 2026-10-13; delivery not yet tested)*

* `Task_SendAdminMail` runs per account: it reads `accounts.lastAdminMailId`,
  queries `adminMail` (game database) with
  `{ amid: { $gt: lastAdminMailId }, expTime: { $gt: <now> } }`, sends the
  matching letters to that account and stores the highest `amid` back
  (`SetFieldsIfVer`). Each letter is delivered **once per account**; a letter
  whose `expTime` has passed is no longer delivered to accounts that did not
  get it yet. The unique index on `amid` (schema.md) means every letter needs
  a new, larger `amid`.
* A letter document uses the same reader as the personal mailbox
  (`MailShared.cpp`). Fields: `amid`, `sender`, `receiver`, `sentAt`,
  `expTime`, `important`, `source`, `state`, `mailId`, `goldCost`, and
  **`attachments`** = array (max 64) of `{ type: <number>, content: {...} }`.
* Attachment types (`MasterServer.AttachmentType`, values decoded from the
  client's `masterserver.lua` bytecode) and the `content` fields the client
  UI reads (`data/ui/scripts/work/uigamefuncs.lua`, `windows/mailwnd.lua`):

  | type | Name | `content` fields |
  |---:|---|---|
  | 0 | `LAT_INVALID` | - |
  | 1 | `LAT_GAME_MESSAGE` | `stringId` (localised key `<stringId>_msg`), optional `zoneId` |
  | 2 | `LAT_MESSAGE` | `subject`, `body` (plain text; without a user `sender` the client treats it as a server string) |
  | 3 | `LAT_CREDITS` | one of `credits`, `goldCredits`, `tokenCredits`, `eventCredits` |
  | 4 | `LAT_LOYALTY_LEGACY` | `race`, `loyalty` / `reputation` |
  | 5 | `LAT_ITEM` | `defName`, `amount`, optional `enchantments` |
  | 6 | `LAT_TOKENS` | (tokens; may also travel as `tokenCredits` in type 3) |
  | 7 | `LAT_VESSEL_EXP_POOL` | `vesselExpPool` |
  | 8 | `LAT_PREMIUM` | `premiumTime` (unit not confirmed; hours *inferred* from the DLC window, which divides `premiumTime` by 24 for days) |
  | 9 | `LAT_CUSTOM_NOTIFY` | - |
  | 10 | `LAT_VESSEL_EXP` | `exp` |
  | 11 | `LAT_TITLE` | `tid` |
  | 12 | `LAT_TALENT_SET` | `talentSet` |
  | 13 | `LAT_CLAN_RESOURCE` | - |
  | 14 | `LAT_ACCOUNT_AURA` | `defName` |
  | 15 | `LAT_AUTOGEN` | `autogenItem` |
  | 16 | `LAT_CUSTOM_ELEMENT` | `customElement` |
  | 17 | `LAT_AVATAR` | `avatar` |
  | 18 | `LAT_MOTTO` | `motto` |

* Candidate document *(inferred, not yet tested;
  timestamps in milliseconds like `chatMutedTill`)*:

  ```js
  db.adminMail.insert({
    amid: NumberLong(1),
    sentAt: NumberLong(Date.now()),
    expTime: NumberLong(Date.now() + 7*24*3600*1000),
    attachments: [
      { type: 2, content: { subject: "Welcome", body: "Server notice text" } },
      { type: 3, content: { credits: 100000 } }
    ]
  })
  ```

  Open in the lab: which event triggers `Task_SendAdminMail` (login is the
  likely one), whether `sender`/`receiver`/`state` must be present, and
  whether item attachments are delivered by `Task_MailDeliver` as for
  normal letters.

## 5. Safety notes

* Anyone who can write to MongoDB can run these tasks (the database has no
  authentication by default - [security S-01, S-23](security.md)). Keep
  MongoDB on loopback.
* Keep `root` accounts to a minimum and do not play on them; a `root`
  account's uid is all a task document needs.
* Tasks are logged in the Shard log and stay in `adminTasks` - a useful audit
  trail; do not delete them routinely.
* A web panel that inserts task documents must authenticate its users itself
  and must never pass raw user input as `cmd`.
* Password resets: there is no task for it; copying a known
  `accounts.password` value works (test V-10) but see [S-07](security.md).

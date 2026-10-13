# Shard admin tasks: how they are queued, authorised and what they need (static)

> Analysis of 2026-10-11. Static analysis of `Shard.exe` (build 1.99.0.167293)
> (strings and machine code). **Nothing was executed**; every behavioural
> statement is *(inferred)* from machine code and strings unless it is tagged
> *(file)*. The per-task listing is generated:
> [shard-admin-tasks-table.md](shard-admin-tasks-table.md). Answers the
> mechanism part of Q37 and part of Q40. Companion: the name list in
> [console-commands.md](../07-administration/console-commands.md) section 2.

## 1. The big picture

The 58 admin tasks are **not** chat or console commands. They are *jobs in a
MongoDB queue* that the Shard picks up and executes:

```
 operator / web admin / support tool / GDPR service
        │  insert a document {cmd, <params>, requestedByUid | requestedByService, serviceType}
        ▼
 <db_name>.adminTasks            (collection exists, empty on a fresh node; schema.md)
        │  Sys_PickupAdminTasks polls; FindAndModify selector {serviceType: 2, pickedBy: 0}  (observed, V-10)
        │  sets pickedBy / pickedAt
        ▼
 Sys_AdminTask in the Shard      (Tasks\Sys_AdminTask.cpp)
        │  1. privilege check   2. look up `cmd` in the task table   3. run handler
        ▼
 FinalizeAdminTask               writes finishedAt, success, err / errMsg back into the document
```

Evidence *(disasm + strings)*: `CreateAdminTask(): failed to Insert`,
`PickupAdminTask(): failed to FindAndModify`, `FinalizeAdminTask(): failed to
FindAndModify`, `Selector for admint task: `, `Admint task pickup result: `,
`Sys_PickupAdminTasks: picked admin task '%s'`, `Sys_AdminTask: performing
'%s'`, `Sys_AdminTask: empty 'cmd'`; collection name `adminTasks`; field names
`serviceType`, `pickedBy`, `pickedAt`, `finishedAt`, `errMsg`, `success`,
`err`, `_id`, `cmd`, `requestedByUid`, `requestedByService`. The collection
and its indexes (`{serviceType,pickedBy}`, `{cmd}`, `{uid}`) exist in a live
node *(observed, [schema.md](../06-database/schema.md))*, which also tells
that task parameters sit **at the top level of the document** (index on
`uid`), next to `cmd`.

Two producers exist:

1. **In-game RPC `Task_AdminCmd`** *(disasm)*: a logged-in client with an
   `admRole` calls the Shard; the handler loads the caller's `admRole`
   (`Task_AdminCmd: Failed to GetFields() for user %s`) and creates the queue
   document (`Failed to CreateAdminTask() for user %s`). The RPC is therefore
   a *submission* path, authorisation happens again at execution time.
2. **External tools** that write into the database directly (the community
   mentions an "admin panel in Mongo" and `admRole` edits; this matches the
   design: the queue is plain Mongo documents, `requestedByService` carries a
   service name such as `gaijin_gdpr` for the data-protection tooling).

Cvars of the machinery *(binary, [cvar-defaults.md](../05-configuration/cvar-defaults.md))*:
`ctm_taskRecoveryInterval` (2 s, "controls task restoration interval"; the
shipped config also sets it), `ctm_debugTaskPickup` (0), `ctm_taskDebugDelay`
(0, "artificial delay to test slow tasks"), `dbg_logAdminTask` (0).

## 2. Authorisation

*(disasm of `Sys_AdminTask`, function around `0x4d9780`; role check `0x4d76c0`)*

1. If the document's `requestedByService` equals **`gaijin_gdpr`** the task
   runs without a user check (the GDPR service identity; relevant for
   `forgetAccount`, whose handler reads `requestData`, `type`, `request_id`,
   `fetch_id`, `service_id`).
2. Otherwise the Shard loads the account named by `requestedByUid`, reads its
   `admRole` and asks the role table whether it may run admin tasks. Failure
   logs `Not enough privilege` and the task is finalised as failed.
3. The role check treats an **empty role as denied** and the role name
   **`root` as always allowed**; any other role is resolved in the role table.
4. The role table lives in a separate database named by the cvar
   **`db_adm_name`** (default **`web_adm`**: "database which includes a
   `admRoles` collection and some other options"), collection `admRoles`,
   field `roles` (functions `AcquireAdminRoles`, `AssignRolePrivileges`;
   tasks `assignRole` and `assignRolePrivileges` write it/`accounts.admRole`).
5. Privilege names compiled in (`AccessPrivileges.cpp`, `PRIVILEGE_NUM = 17`):
   `play`, `playInMaintenance`, `mute`, `mutePermanent`, `ban`, `banPermanent`,
   `gmView`, `propertyEdit`, `adminView`, `adminEdit`, `privilegesControl`,
   `promoControl`, `observeGames`, `playFreeSpace`, `giveFreeSpace`,
   `playClosedPTR`, `roleAssignment`. Four privilege names double as the name
   of one specific task (`mute`, `mutePermanent`, `ban`, `banPermanent`,
   `giveFreeSpace`): those get their own dedicated gate; the other 53 tasks
   share one of the twelve general privileges. **Which privilege each of the
   58 tasks needs is now resolved for all of them**, each read from the
   store into the task's registration record (two tasks, `changeNickName`
   and `copyAccount`, store it before the name push, i.e. at a different
   stack offset) - see
   [shard-task-privileges.md](shard-task-privileges.md) (generated). `root` still bypasses the whole table
   (point 3). The cvar `auth_infinitePremiumForRoles` (shipped `gm;support`)
   is a separate, role-name based feature, unrelated to this privilege table.

**Consequence for a community node** *(confirmed in test V-10 - see below)*:
to run a task you need (a) an account whose `accounts.admRole` is `root` (or a
role defined in `web_adm.admRoles`) and (b) a document in `adminTasks` with
`cmd`, the task's parameters, `requestedByUid` = that account's uid and
`serviceType` = the Shard's service type (`ST_SHARD = 2`, from `cloud.xml`).
The Shard has to be running; results appear in the same document.

**Test result (V-10, observed):** the document must also carry
**`pickedBy: 0`** - without it the task is never picked up and no error is
logged (`ctm_debugTaskPickup 1` prints the selector `{ "serviceType": 2,
"pickedBy": 0 }`). Pick-up takes a few seconds; the Shard writes `pickedBy`
(its service id), `pickedAt`, `finishedAt` (ms epoch), `success`, `errMsg` and,
for read-only tasks, `result`. Verified: `playerInfo` (`result` = `admRole`,
`username`, `nickName`, `uid`, `bannedTill`); `mute` (`durationInHours`,
`category`, `rules`, `reason` -> `chatMutedTill`, stored `muteCategory` 5 for
category 1, effective immediately in chat); `cancelMute` (refused without
`reason`); `give` with `value` = `credits` or `goldCredits` and `amount`
(additive). A requester whose `admRole` is `player` gets `Not enough
privilege`.

## 3. Parameters and preconditions (condensed)

The generated table lists, per task, the field names and error messages found
in the handler (and the shared implementation behind thin thunks such as
`ban`/`banPermanent`/`cancelBan`, `mute`/`mutePermanent`/`cancelMute`). Reading
them as a signature is a lead, not a specification. Highlights *(disasm)*:

| Task | Parameters (field names) | Preconditions / notes |
|------|--------------------------|-----------------------|
| `ban`, `banPermanent`, `cancelBan` | `uid`, `requestedByUid`, `category`, `durationInHours`, `rules`, `reason` | "Specify the points of rules please"; "Incorrect category"; stores `bans[]` with `bannedBy/bannedAt/banDuration/removedBy/removeTime/removeReason` and `bannedTill` (the live DB field, see schema) |
| `mute`, `mutePermanent`, `cancelMute` | same, plus `isTrade` | chat vs trade-chat mute (`chatMutedTill`, `tradeChatMutedTill`); "This mute is shorter than already applied one" |
| `set` / `give` | `uid`, `reason`, `value`, `amount`, `index`, `vid`, `item`, `achievement`, `credits`, `goldCredits`, `premiumTill`, `factionRep`, `vesselExpPool`, `tokenCredits`, `eventCredits`, `rank` | "Specify the reason please" (a reason is mandatory); overflow guards for premium time, vessel exp pool, event credits, token credits, gold, credits, faction rep; **"Cannot set rank on 'live' server"** - refused while `cl_versionType` is `live` (the default) |
| `giveSpecModule` | `uid`, `vid` **xor** `vesselDefName`, `specModuleDefName` | exactly one of vid / vesselDefName; checks `specialModulesVariants`, `budget`, `budgetAccountAura` |
| `giveAutogenModule` | `uid`, `classId`, `rank`, `amount` | capped by the account's autogen item maximum |
| `giveTestAutogenModule` | `uid`, `rollData` | **refused on a `live` server** |
| `giveTitle`, `giveVesselCustomElement`, `giveFreeSpace` | `uid`, `title` / `item` / - | `giveFreeSpace` requires the account to be a `player`; sets the `alpha-tester-dlc` flag |
| `unlockAllVesselNodes` | `uid`, `vid` | all research nodes of one ship |
| `delete` | `uid`, `iid` **or** `vid` **or** `craftResource`+`craftResourceAmount`, `moneyback`/`refund` | inventory removal with optional refund |
| `copyAccount` | `srcUid`, `destUid`, `fields` | copies credits, gold, tokens, event credits, vessel exp pool, rank, exp, station, faction rep, vessels, items, autogen items |
| `copyNewAccount` | `nickname`, `password`, `srcUid` | creates a new account from a source one; uses a platform authorisation call and renames on nickname clash (`(Renamed_%u)`) |
| `createAccount` | `username`, `password`, `role`, `nickName`, `allowLogin`, `autoGenerated` | "Player with this username already exists" |
| `createAccountFromPattern` | `src`, `username`, `yuplayID`, `recreateStats` | clones a template account (`items`, `vessels`, `equipped`, `bSlots`) |
| `resetAccount`, `resetStats`, `resetAchievements` | `uid` | **`resetStats` requires the cloud to be in maintenance mode and the target offline** |
| `enterMMode` / `leaveMMode` | `minutesLeft` | maintenance mode via the Hub endpoint |
| `playerInfo`, `gamesInfo` | `uid` / `username` / `nickname`; `queryParams` | read-only; result written into the `result` field |
| `setUnlimPveMissionLevel` | `uid`, `value`, `amount`, mission name | level >= 1 |
| `questServerExecConsoleCmd` | `uid`, `console_command` | max 1024 characters; executed on the QuestServer |
| `sendCheatToUniverse` | `cheatCommand`, `zoneId`, `cid` | sub-commands `setOwner`, `addPressure`, `startConflict`, `endConflict` |
| clan tasks | `cid`, `name`/`tag`/`role`/`resource`, `amount` | all go through the ClanServer ("ClanServer didn't respond") |
| league tasks | `ltid`, `name`, `major`, `numAcceptedMembers`, `rating`, `banTill` | |
| `changeServiceId`, `linkServices`, `unlinkService`, `togglePromo` | `uid`, `service` (`steam`/`arc`/`yuplay`), ids | account <-> store identity mapping |

## 4. What this means

* **The "unlock everything" wishes have an intended path**: `giveSpecModule`,
  `giveVesselCustomElement`, `giveTitle`, `unlockAllVesselNodes`,
  `giveFreeSpace`, `set`/`give` (credits, gold, premium) and `copyAccount`
  are exactly what the live operation used; they validate their input
  (defName lookups, overflow guards) where a hand-edited Mongo document does
  not - which is the likely reason hand edits with a mistyped def name make the
  server refuse to start (see
  [config-validation-tools](../07-administration/config-validation-tools.md)).
* **Moderation is data**: `ban`/`mute` write histories (`bans[]`,
  `chatMutes[]`) plus the `bannedTill`/`chatMutedTill` fields the Shard checks
  at login.
* **Security note**: any process that can write to the MongoDB (no
  authentication in the stock setup, security S-02) can enqueue tasks; the
  only gate is a `root` role or a `requestedByUid` account with privileges,
  and the Shard does not authenticate the *producer*. Keep Mongo on
  127.0.0.1 (as shipped).
* **For a re-implementation** (language-neutral): the queue is a clean
  boundary - a replacement admin plane only has to produce the documents
  described above and honour the result fields; a replacement Shard has to
  implement the 58 handlers and the role check; the `web_adm` database is a
  separate trust domain by design.

## 5. Open points

* ~~The exact set of privileges per task~~ **resolved:**
  [shard-task-privileges.md](shard-task-privileges.md) maps all 58 tasks to
  one of the 17 privilege ids. ~~Data model of `admRoles`~~ **resolved
  statically (2026-10-13):** `roles` = object role name -> object of
  privilege *name* -> number (non-zero = granted); `root` is implicit -
  [admin-tasks-howto.md](../07-administration/admin-tasks-howto.md) §4a
  (not yet confirmed by a test).
* ~~Whether a community node is a "live" server~~ **resolved:** the check is
  `strcmp(cl_versionType, "live")` (cvar object `0xad6c04`, registered as
  `cl_versionType`, default **`live`**, "Type of deployed version"). The
  shipped `common.cfg` only has the line as a comment, so a stock node **is
  "live"** and `set rank` / `giveTestAutogenModule` are refused until the
  cvar is set to another value (for example in `common_local.cfg`; side
  effects on the client version handshake are unknown, Q3).
* Whether the in-game `Task_AdminCmd` RPC is reachable from a stock client
  (it needs the UI; the client has no admin console in the shipped scripts).

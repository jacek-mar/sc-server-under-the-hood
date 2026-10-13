# Event-ship parts, mail rules and the clan ship (static answers to Q34, Q42, Q43, Q44)

> Analysis of 2026-10-11. Everything below is **file-verified** unless tagged
> *(disasm)* (Shard.exe strings/code, see
> [shard-admin-tasks.md](../08-reverse-engineering/shard-admin-tasks.md) for
> the method) or *(community)*. These are the operator topics that the Discord
> batch 005 asked about most ("no way to get Helicon/Salyut parts", "ships
> cannot be mailed", "10 rank-9 players for the dreadnought"). Nothing was run.

## 1. Where event-ship parts come from (Q34)

Both ships are built from two **craft resources**: `Ship_<Name>_Rank5` has the
recipe `<Name>Corpse` x1 + `<Name>Module` x10 (`<Ingr resource= amount=>` in
`cloud/data/store.xml`, `Vessel` rows `Ship_Salyut_S_ECM_Rank5` at line 133677
and `Ship_Helicon_L_SNIPER_Rank5` at line 16397). The resources themselves are
defined in `data/gamedata/def/ex/craft.lua` (`Def.SalyutCorpse` ...
`price 100000`, `cant_be_bought`, `is_rare`, `mark 3`, inherit
`CraftResource_Base`) and appear as type-5 items in `store.xml`
(`SalyutCorpse` id 2259, `SalyutModule` id 9271, `HeliconCorpse` id 3151,
`HeliconModule` id 3152; all `cantBeBought="1"`).

| Ship | How the parts were obtainable in the shipped data |
|------|---------------------------------------------------|
| **Salyut-ST** | (1) Event shop bundles `Bundle_SalyutEvent_Parts_1` (1 x `SalyutCorpse`, `eventPrice` 400) and `_2` (1 x `SalyutModule`, `eventPrice` 200; ten are needed), `_3` (2 x `SalyutWing`, 100), `_4` (blueprint `BP_SalyutWing`, 300); all flagged `cantBeBought` outside the event. (2) Crafting `BP_SalyutCorpse` (`isDefault`): 60 x `SalyutCorpse_part` + 15 `Iridium_monocrystall` + 10 `AlienCompositeAlloy` + 15 `Computing_chip` + 15 `Pure_silicon`. (3) `SalyutCorpse_part` is a quest reward: four event quests (`quests.lua` lines 9032, 9056, 9080, 9105; the first is `QuestId.SpaceDay_1`, `event_day_min 9 .. event_day_max 21`) give 6 each. (4) `SalyutWing` also drops from zone rewards (`zones.xml` lines ~275, 2000/2500 units) and is the research currency of `SalyutNodesPrice`. |
| **Helicon** | **No producer exists in the shipped data**: `HeliconCorpse` / `HeliconModule` occur only as the two item rows and the recipe ingredients; there is no bundle, blueprint, quest reward, loot-table or zone reward for them (grep over `cloud/data`, `data/gamedata/shared`, `def/objects`). Helicon *modules/weapons* (`Module_HeliconModule_T*`, `Weapon_HeliconGun_T*`) do have blueprints (`BP_Module_HeliconModule_T3_Mk1`, token price 400-800, `BP_Weapon_HeliconGun_T*`). |
| **Tester's Agony** (and similar) | Recipe contains `NeverMind` x99 and `unreachable_activator` x99 (`Def.unreachable_activator` in `craft.lua`, price 1 000 000 000, `cant_be_bought`): an *intentional blocker* - the ship is not obtainable by crafting. |

**Consequences for an operator** *(derived)*:

* The "no UI / no price" reports are correct: the parts were handed out by
  *time-limited event bundles* and *quests*, so outside the event window the
  store flag `cantBeBought="1"` hides them. Helicon parts were evidently
  delivered by a mechanism outside the shipped data (retail/promo grant).
* Ways to obtain a ship on a private node, from least to most invasive:
  grant the two craft resources to the account (DB item rows or the
  admin task `give` with `item`), change the **recipe** of the ship in
  `craft.lua`/`store.xml` source (lower the module count or replace the
  ingredients), or run the event's quest group while the event day range
  matches (`event_day_min/max` are relative event days, see
  [zone-events](zone-events.md)). Hand-written def names must exist
  ([config-validation-tools](../07-administration/config-validation-tools.md)).
* Defs written with a typo stop the server from starting (community, batch
  005); the admin tasks validate def names, a raw DB insert does not.

## 2. Mail rules (Q43) *(disasm + cvars)*

* **Who may send:** `shard_minAntibotCounterForMailSending` (default **50**):
  the sender's `antibotCounter` must reach it; if the machine counter
  (`machineAntibotCounter`) is not enough and
  `shard_is2StepAuthForMailSendingNeeded` (default **1**) is on, 2-step
  authorisation is required. A fresh account therefore cannot send mail until
  it has accumulated anti-bot counter (how the counter is raised was not
  analysed; the admin task `set` can write `antibotCounter` /
  `machineAntibotCounter`, error text "Incorrect counter value").
  `chat_minAntibotCounterForSendMsg` (default 0) is the chat equivalent.
  *Operator lever:* lower the two `shard_*` cvars (Shard) to allow mail on a
  small trusted node.
* **What may be attached:** letters need at least one attachment
  (`MailSendLetter: no attachments, cannot send letter`; obligatory
  attachment rule for system letters). Bundles are sent only if flagged
  `can_be_sent_by_mail` (`def/objects/bundles.lua`, `store.xml
  canBeSentByMail`, 4 bundles carry it; `ComposeBundleLetter: bundle has to be
  marked as 'can_be_sent_by_mail'`), and only some content types are
  supported (`AddEntryToBundleLetter: content type %d is not supported for
  sending by mail`). Craft resources and parts are plain inventory items and
  can be sent; **ships (vessels) are not a mailable content type** - this is
  the technical reason behind "ships cannot be mailed, parts can".
* **Trade by mail:** letters can be `isTrade` (payment on delivery;
  `DeliverPaymentToSender`), counted in `mailTradeCounter`; auto-trade without
  a trade flag is rejected (`isAutoTrade && !isTrade`).
* **Delivery:** `Task_MailDeliver` moves attachments into inventory (items,
  autogen items with `rollData`, custom elements, avatar/motto/title
  items, talent sets); unknown item types and amount overflow abort the
  delivery; `Task_MailRemove` / `Task_MailAcknowledgeExpiration` return
  attachments to the sender or archive the letter (collections `mailbox`,
  archive).
* **Broadcast mail:** the collection **`adminMail`** (index in schema.md,
  empty on a fresh node) is read by `Task_SendAdminMail` with the per-account
  pointer `lastAdminMailId`: documents inserted there are delivered once to
  every account (a ready-made announcement/gift channel for operators).
  Layout decoded statically on 2026-10-13 (query `amid > lastAdminMailId`
  and `expTime > now`, `attachments[{type, content}]`, 19 attachment types)
  - [admin-tasks-howto.md](../07-administration/admin-tasks-howto.md) §4b;
  delivery not yet confirmed by a test.

## 3. Clan ship / "dreadnought" requirement (Q42)

* The community statement "10 players of rank 9 are required" is **a host
  setting, not the stock value**. The shipped `ConfigureClanServer()`
  (`default_platform_config.lua` lines 2129-2142) sets:

  | Cvar | Shipped | Meaning (original comment, translated) |
  |------|---------|----------------------------------------|
  | `clan_shipBuildHighRanks` | **3** | number of clan members of the "high rank" (rank 9) required to build the clan ship |
  | `clan_shipPartsCanBuild` | **4** | main parts available for building: 0..4 are the build stages of the dreadnought |
  | `clan_shipUpgradeCanBuild` | **3** | module upgrade stages available (T3, T4, T5) |

  Engine defaults (binary): 0 / 100 / 100. The "high rank" is
  `ClanHighRank = 9` (`data/gamedata/shared/clan_upgrades.lua`, generated into
  `aux_limits.xml` `<ClanHighRank value="9"/>`). A server that quotes "10" has
  edited `clan_shipBuildHighRanks`.
* Build economy is in `data/gamedata/shared/clan_ship.lua`: the function
  `ClanShipKF(x) = max(1, ceil(x * 0.1))` scales every price and duration to
  **10 %** (the Russian comment is garbled by its encoding; it mentions
  version 1.4.4 and 10 days, ticket #67206); the constants (`mine_T3..T5_price/duration`, `turret_*`,
  `additional_*`, `part_duration` 604 800 s before scaling; main parts
  `Shipyard`, `Carcas`, `Engine`, `Weapon` at 5 000-25 000 clan tokens
  before scaling) all go through it. Set `ClanShipKF` to return `x` to get
  the unscaled values, or to `1` for instant builds (the commented
  `return 10 --- test only` line in the file is the original test hook).
* Admin and cheat paths: tasks `giveClanShipModule` (`cid`, `clanShip`,
  `slotName` - decoration slots only, `module`), `setClanResource`, and the
  ClanServer console commands `cheat_clanShipBuildMain` /
  `cheat_clanShipBuildCurrent` (see [console-commands](../07-administration/console-commands.md)).
* The clan-ship *battle* is game mode 14 (`dreadnoughtbattle_map_01..06`;
  queue block at `default_platform_config.lua` line ~827).

## 4. Persistent event ships in the open world (Q42, second half)

Not answered statically: the event ships (Nagelfar-like) in the open world are
Universe/zone events (`ow-events-catalog.md`, `zone-events.md`); whether they
can be pinned permanently depends on `forceEvents` (Q10, runtime).

## 5. Crediting DLC content (Q44) *(disasm + strings, 2026-10-13)*

How the Shard grants the contents of a bought DLC, and what a community node
can use instead of Steam's publisher API. All from `Shard.exe` (build
1.99.0.167293); nothing here has been run yet (proposed test below).

**The task.** `Task_UpdateDLCOwnership` (client request `AC_UPDATE_DLC_OWNERSHIP`)
loads the account (`credits`, `goldCredits`, `premiumTill`, `bSlots`,
`invExtLevel`, `auras`, `vessels`, `title`, `acquiredTitles`,
`freeVesselCustomElements`, `steamID`, `steamDLC`, `premiumAccess`,
`admRole`, `craftResources`, `promo`, `puid`, `yupPurchases`,
`steamYupPurchases`, `boughtArcDLC`) and asks the owner source which DLC app
ids the account owns:

* **Steam account** (`steamID` set): `SteamWebAPI_GetPublisherAppOwnership`
  - needs the publisher key, which is empty in the shipped build
  ([external-services-and-login-modes.md](../08-reverse-engineering/external-services-and-login-modes.md)),
  so this path fails on a community node.
* **Simulation cvar `dbg_simulatedSteamDlcOwnership`** (Shard, string). Its
  built-in description gives the format:

  ```
  uid1[,uid2...];appid1[,appid2...][|uid1[,uid2...];appid1[,appid2...]]
  example: 10,11;appid1,appid2|10;appid3
  ```

  For a listed uid every app id is appended to the ownership list as
  `{ appid: <id>, ownsapp: 1 }` - the same shape as Steam's answer. An
  account **without** a `steamID` is processed only when this list is
  non-empty, so the cvar also covers own-login accounts. Whether a
  Steam-linked account still receives the simulated ids when the publisher
  API call fails was not traced - test with an own-login account first.
  The Yuplay twin `dbg_simulatedYupDlcOwnership` uses
  `uid...;guid...` with Yuplay GUIDs.
* **Gate:** the cvar's change handler parses the value only when
  `cl_versionType` is **not** `live`. With the default (`live`, also the
  shipped commented line in `cloud/data/common.cfg`) the value is accepted
  and silently ignored. A host would have to set `cl_versionType` to another
  value on the Shard *before* the DLC cvar (order in the cfg matters, the
  parse happens when the DLC cvar changes) *(inferred from the code order)*.
  Side effect: the same switch unlocks the `set rank` /
  `giveTestAutogenModule` admin tasks
  ([shard-admin-tasks.md](../08-reverse-engineering/shard-admin-tasks.md));
  effects on other services were not checked.

**What gets credited per owned app id.** The task looks the app id up in an
in-memory table of DLC records (fixed array of 0x760-byte records, key =
app id; fields for credits, gold, premium time, account aura, vessels,
title, vessel custom elements, battle-pass unlock and bundle contents). The
contents are applied directly or sent as a letter (`SendBundleByLetter`,
string id `DLCReward`), and the app id is recorded on the account
(`steamDLC` with `appIds` / `guids` lists; `dlcName` + `appId` per entry) so
it is not credited twice (`dlc is not saved to account` otherwise). Arc
purchases are tracked separately in `boughtArcDLC` (`Task_BuyArcDLC`).

**What is *not* the mapping:**

* `steamDlcPrices` / `yupDlcPrices` / `arcDlcPrices` (`LoadDlcPrices`) hold
  `{ time, dlc: [ { appId, price } ] }` - store prices for display, not
  contents.
* `DLCList` in `data/gamedata/ui_properties.lua` (client UI: `name`,
  `steam_url`, `steam_appId`, `yuplay_guid`, `arc_bundle`, `hidden`) - the
  Shard binary contains none of these key names.
* `store.xml` has the DLC bundles (`Bundle_DLC_*`, `Bundle_Arc_DLC_*`) but
  no app-id attribute.

**Where the DLC record table does *not* come from** *(static, 2026-10-13)*.
The keys a record needs - the 303 Steam app ids and the Gaijin-store GUIDs of
`DLCList` (for example 222280 and its GUID pair for the first DLC) - occur in
**no** server-side file: not in `cloud/data` (XML, cfg, Lua), not in the
server pak scripts, and not as integer constants in `Shard.exe` (a byte
search finds 4 of 303 values, at unrelated code offsets - chance matches).
They appear only in client files (`ui_properties.lua`, `vessel_stickers.lua`).
The table is therefore filled at run time from a source that was not
released (a vendor service or a database collection that a fresh database
does not have) *(inferred)*. Consequence for a community node: with an empty
table, `Task_UpdateDLCOwnership` has nothing to credit even when ownership is
simulated *(inferred; the lab test below would confirm it)*. The practical
route for former DLC owners is granting the contents directly - the bundle
definitions with their `fixed_contents` (`Bundle_DLC_*`, `Bundle_Arc_DLC_*` in
`def/objects/bundles_dlc.lua` / `bundles.lua`) list what each DLC gave, and
the `give` admin task or an `adminMail` attachment (`LAT_ITEM`, `LAT_PREMIUM`,
`LAT_CREDITS`, ...) can deliver those items
([admin-tasks-howto](../07-administration/admin-tasks-howto.md)).

**Open (Q44):** confirm the empty table on a running node (the record array
lives in the same shared-data object that loads `store.xml`,
`special_values.xml` and the other `cloud/data` XML files). Proposed test
(on a server copy):
set `cl_versionType` to a non-`live` value and
`dbg_simulatedSteamDlcOwnership` to `<test uid>;<app id from DLCList>` in
the node copy's `shard_local.cfg`, log in with the test account and watch
the Shard log and `accounts.steamDLC` / inventory. Needs one client login.

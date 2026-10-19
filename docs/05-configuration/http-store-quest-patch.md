# Live store and quest patches over HTTP

> Answers the static part of open question **Q72**. Lead: a public host's
> configuration overlay (source S20, CO1) sets these cvars with a 60 s
> interval *(community)*. Everything below was read from the release
> binaries (Hub 1.99.0.167293) *(static, 2026-10-19)* unless marked
> otherwise. Lab test V-15 (2026-10-19, server only) *(observed)*: the quest
> patch works; **the store items patch crashes the stock Shard every time**
> (§2a).

> ⚠ **Operators: do not set `store_patchItemsUrl` on the stock Shard.** The
> first patch that arrives kills the Shard with a stack overflow, whatever
> its content (§2a).

## 1. Summary

Two services can poll a URL and apply what they receive **while running**:

| Service | Cvars | Default | Patch content | Effect |
|---|---|---|---|---|
| Shard (and GameRewardDispencer, same code) | `store_patchItemsUrl`, `store_patchItemsInterval` | empty, `0` (off) | XML `<Store><Items><Item id=… price=…/>` designed to change **prices and availability flags** of existing store items and push them to online clients - **crashes the Shard in this build** *(observed, V-15)* |
| Shard (and GameRewardDispencer) | `store_patchSpecialValuesUrl` (same interval) | empty | XML | **parsed and then discarded** - no effect in this build |
| QuestServer | `quests_patchUrl`, `quests_patchInterval` | empty, (interval default not decoded) | XML `<QuestGroups><QuestGroup id=…><quest id=…/>` (same layout as `cloud/data/quests.xml`) replaces the quest-group membership; players' offered/active quests that are no longer available are removed - **works** *(observed, V-15)* |

The three `store_patch*` cvars are also registered by AchievementServer,
AdventureServer, ClanServer, LobbyServer and MatchMaker (shared code), but
only Shard and GameRewardDispencer contain the request code *(static: the
request and `ApplyItemsPatch` strings occur only in those two binaries)*.

## 2. Store items patch (Shard)

**Timer** (`GameStore.cpp`, Shard `0x4cb390`): on every store tick, if
`store_patchItemsInterval` is non-zero and at least *interval x 1000 ms*
have passed since the last request, the Shard sends one asynchronous request
per non-empty URL through its HTTP client (bundled `libcurl.dll` 7.62.0 with
OpenSSL 1.1, so `https://` URLs are possible). Interval unit: **seconds**.
A failed request logs `GameStore: Failed to g_httpClient->Request(
store_patchItemsUrl )`; a failed transfer logs `ReceiveItemsPatch() failed,
err: %d`.

**Reply handling** (`ApplyItemsPatch`, `0x4cb140`):

1. A hash of the reply body is compared with the hash of the last applied
   body. **Same content = nothing happens** (polling an unchanged file is
   cheap). New content logs `GameStore::ApplyItemsPatch: new patch content
   arrived: hash %u vs %u`, the size and the whole XML (log level 1).
2. The body is parsed as XML (`ApplyItemsPatch: !doc.ReadBuffer` on a parse
   error). The reader descends `Store` -> `Items` and reads every `Item`
   element with the normal store-item reader (`StoreItem.cpp`).
3. The previous patch list is **cleared** first: each patch is a complete
   set, not an increment.
4. `ApplyItemsPatchReal` builds a new store from the **base store**
   (`store.xml` as loaded at start) plus the patch, matched by `id` (the
   `<Item id>` of `store.xml`, the same "store id" the admin task `give`
   takes as `item`, see [admin-tasks-howto §3a](../07-administration/admin-tasks-howto.md)).
   Because every patch starts from the base, removing an item from the patch
   file restores its original values at the next change.
5. **All or nothing:** if any `id` is not in the base store the Shard logs
   `Item with id = %u is not in store, can't patch` and keeps the current
   store unchanged. The hash is already stored, so the same file is **not
   retried** - change the file (fix the id) to make it apply. A patch cannot
   add new store items.
6. On success the new store replaces the old one and a "store changed" flag
   is set; the session manager (`SessionManager.cpp`, `0x40a0a8`) clears the
   flag and sends a store message to **every logged-in client**: no relog
   is needed. How battle servers get it is not traced *(inferred: they
   share the receiver below)*. The receiving side is
   `StoreSvc::ApplyStorePatch` in `MasterServerStore.cpp` of both
   `DedicatedServer.exe` and the client `game.exe` (`Store patch size :
   %3.5f Kb`; an id it does not know logs `StoreSvc::ApplyStorePatch:
   !patchee for id %u`).

**Which attributes a patch changes.** The reader parses the usual item
attributes (`id`, `price`, `premiumPrice`, `tokenPrice`, `eventPrice`,
`tradePremiumPrice`, `basePrice`, `basePremiumPrice`, `baseTokenPrice`,
`baseEventPrice`, `race`, `requiredRank`, `stacks`, `cantBeBought`,
`requiredAccountAura`, `type`, `defName`, `flags`, `deleteFromInventory`),
but the merge onto the base item (`0x4f91e0`) copies only:

| Copied from the patch | Kept from the base store |
|---|---|
| `price`, `premiumPrice`, `tokenPrice`, `eventPrice`, `tradePremiumPrice`, `cantBeBought`, `flags` (and the derived effective price) | `base*Price`, `requiredRank`, `stacks`, `race`, `requiredAccountAura`, `type`, `defName`, `deleteFromInventory` |

So the patch is a **price and availability** lever (for example a sale, or
`cantBeBought="1"` to withdraw an item), not a way to change ranks, stacks
or what an item is. Omitted price attributes are read as 0 *(inferred from
the reader's defaults)* - give every price field you want to keep.

Candidate patch file *(inferred from the reader; untested)*:

```xml
<?xml version="1.0"?>
<Store>
  <Items>
    <Item id="855" price="5000" premiumPrice="0" tokenPrice="0" eventPrice="0"
          tradePremiumPrice="0" cantBeBought="0" />
  </Items>
</Store>
```

Copy the attribute values of the same `<Item id>` from `cloud/data/store.xml`
and change only what you need. ⚠ unverified: whether the root must be
`Store` or whether the reader also accepts `<Items>` at the top, and whether
`flags` uses the same notation as in `store.xml`.

## 2a. Lab result: the items patch crashes the Shard *(observed, V-15)*

Three runs on a node copy (own database, loopback HTTP server, interval
15 s): a minimal one-item patch arriving during start-up, the same patch
arriving after the Shard was fully ready, and a patch with the complete
original `<Item>` line and only `price` changed. Every time the Shard logged
`GameStore::ApplyItemsPatch: new patch content arrived`, the XML, and died
0.15-0.25 s later (Hub: `OnDisconnect … reason 5`; the node stays without a
Shard until restarted). The three crash dumps carry exception **0xC00000FD
(stack overflow)** at the same address, inside the stack-probe helper
`_chkstk` *(observed)*.

Cause *(static, matches the dumps)*: `ApplyItemsPatchReal` builds the new
store as a local array and requests a **0x130174-byte (≈1.19 MiB) stack
frame**, while the PE header of `Shard.exe` reserves only **1 MiB** of stack
(`SizeOfStackReserve` 0x100000). The probe runs past the end of the stack
before any item is examined, so the content of the patch does not matter -
an unknown id would crash the same way *(inferred)*. `GameRewardDispencer.exe`
has the identical function (same 0x130174 frame, 1 MiB stack) and is
expected to crash too *(static; not run)*. A host that reports using this
feature (S20) may run a modified binary or a different stack setting
⚠ unverified. Changing the binary's stack reserve is a binary patch and is
out of scope here.

Side observations: a missing file is handled cleanly (`ReceiveItemsPatch()
failed, err: 404` - `err` is the HTTP status); the special-values patch is
fetched and ignored without harm.

## 3. Special values patch (Shard): no effect

`store_patchSpecialValuesUrl` is requested on the same timer
(`ReceiveSpecialValuesPatch() failed, err: %d` on a failed transfer).
`ApplySpecialValuesPatch` (`0x4befb0`) checks the hash, logs the content and
parses the XML (`ApplySpecialValuesPatch: !doc.ReadBuffer` on error) - and
then frees the document and returns success **without applying anything**.
In this build the cvar only costs a request per interval. The shipped
special values come from `cloud/data/atlas_special_values.xml` and
`autogen_special_values.xml` at start-up.

## 4. Quest patch (QuestServer)

Same pattern in `QuestServer.cpp`: `quests_patchUrl` ("url for requesting
patch info") and `quests_patchInterval` ("interval for requesting patch
info, in seconds"); `QuestServer: Failed to g_httpClient->Request(
quests_patchUrl )`, `ReceivePatch() failed, err: %d`. The reply
(`ApplyPatch`, `0x412bd0`) is hash-checked, parsed as
`QuestGroups` -> `QuestGroup` -> `quest` - the layout of
`cloud/data/quests.xml` (`<QuestGroup id="0" cooldownInHoursOffer="24"
unchangeable="1"><quest id="519"/>`) - validated (`InitQuestGroups:
invalid quest group %d`, `invalid quest %d in group %d`) and logged as
`Quest groups patched`. The following code removes quests players can no
longer have (`Remove unavailable active quest %d, user %s`, `Remove
unavailable offered quest %d, user %s`, `Remove expired active interval
quest %d, user %s`) and logs `UpdateQuestsNewPatch: took %…`.

*(observed, V-15)*: with an unchanged copy of `quests.xml` as the patch,
the QuestServer polled every 15 s, applied it once per start (`ApplyPatch:
new patch content arrived`, `Quest groups patched`, `UpdateQuestsNewPatch:
took 0.0001 ms, 0 users`) and ignored the unchanged file afterwards; no
errors. The effect on online players' quests was not tested (no client).
⚠ unverified: which `QuestGroup` attributes the patch reads besides the
ids, and whether a patch must list every group.

## 5. Operator notes

* **Store items patch: do not enable** on the stock Shard (§2a). The rest
  of this list applies to the quest patch, and to the store patch only if a
  future binary fixes the crash.
* **Off by default.** With interval `0` nothing is requested. Enable in the
  service's `*_local.cfg` (or `cloud.xml` service cvars), for example
  `set store_patchItemsUrl "http://127.0.0.1:8080/store_patch.xml"` and
  `set store_patchItemsInterval 60`; the platform Lua does not assign these
  cvars, so `_local.cfg` is enough ([config-system](config-system.md))
  *(observed, V-15: `shard_local.cfg` and `quest_server_local.cfg` took
  effect)*. GameRewardDispencer reads its own
  `game_reward_dispencer_local.cfg`.
* **What it is for:** timed sales and withdrawing items without a restart.
  Base store edits (new items, ranks, stacks) still need `store.xml` and a
  restart ([settings-reload-map](settings-reload-map.md)).
* **Keep the file and the store in step:** one stale `id` blocks the whole
  patch; watch the Shard log for `can't patch`.
* **Security:** the patch URL is an outbound dependency. Whoever controls
  that URL (or can intercept plain HTTP) controls prices and item
  availability on the server and in every connected client. Prefer a
  loopback or LAN address you control; `https://` needs a valid certificate
  chain for libcurl ⚠ (whether certificate checks are enabled is not
  decoded). libcurl 7.62.0 (2018) has known vulnerabilities; do not point
  it at untrusted servers. See [security](../07-administration/security.md).

## 6. Still open

* Quest patch with a changed group membership and a logged-in client: are
  removed quests visible to players at once?
* Whether the S20 host's Shard differs (stack reserve) or crashes as well.

# Troubleshooting

> Status: **Stage 1 draft.** Collected symptoms from the community and from the
> analyst's own logs. Add new items with the template at the bottom.

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Cannot log in right after starting | Services still starting (~40–90 s; Universe/Adventure ~15 s each) | Wait; watch `Hub/logs/hub_*.log` |
| Matchmaking fails ("MM fail") | A service crashed or Mongo not ready | Restart the server (community report); check `matchmaker_*.log` |
| MongoDB won't start / window closes | Stale `mongod.lock` or a leftover `mongod.exe` process | Kill stray `mongod.exe`; run the commands of `launch.bat` from `cmd` to see the error; if the DB was not shut down cleanly, repair/remove lock |
| Mongo GUI cannot connect | Modern GUI/driver does not speak MongoDB 2.6 | Use an old tool (NoSQLBooster ≤ 4.7.5 / MongoBooster 3.5.x) |
| Edited DB values revert | Server/game was running and overwrote them | Stop client **and** server (Mongo may stay up), edit, restart |
| Changes to Lua data have no effect on services | Services read generated XML | Run `cloud/prepare_shared.bat` (Mongo must be running), restart cloud |
| `NetSocket::Send … error 10053` / `reason 5` disconnects in Hub log | Appears for every service right after it registers during startup *(observed)*; meaning not yet analysed (probably handshake/reconnect behaviour) | Not a failure by itself; only investigate if a service never stays registered |
| `Hub has already exited; leaving MongoDB and Redis running` | Client exited after Hub; informational | None |
| Loot "not found" at end of match | `sv_lootFailChance` | Set to `0` in `ConfigureDediServer()` (it is `0` in the shipped file — check your copy) |
| No leaderboards | Redis not configured | See [quick start §6](quick-start.md#6-optional-leaderboards-redis) |
| Start-up stalls / some services never register, a Windows Firewall dialog may be hidden behind other windows | Windows Defender Firewall prompt per new executable path (observed, V-8) | Answer the prompts (Private network) or pre-create rules; then restart the node |
| Only some services stay up after start, others "start" then vanish | CPU starved (client loading, other apps): Hub stalled ≈ 60 s and services timed out registering *(observed)* | Start the server alone first; wait until `/status` reports 17 services; then start the client; avoid heavy background load |
| Hub log `Caught application terminal signal 21`, `Failed to TerminateProcess … error 5` | A console window of the Hub/services was closed | Never close service windows; stop via the Hub window (WM_CLOSE) or `/quit` |
| Client log `No more loadbalancers available` / `10061` | Server not up yet (or died) | Check ports 3801/3802 and `Hub/logs` |
| Hub, services and Mongo still running after closing the client | Client does not stop a local server it started *(observed)* | Stop manually (see [verification log](verification-log.md#clean-shutdown-verified)) |
| Players from LAN cannot connect | `cloud.xml` still points to `127.0.0.1` | Set the LAN/public address; open ports |
| Squad/wing stuck loading in PvP arena, or bots missing after queue edits | Open — reported without a solution | See [open questions](../08-reverse-engineering/open-questions.md) |

## "Cannot enter the battle" - matchmaker refusal messages

When the MatchMaker refuses a queue request it returns a join-result code
(`MasterServer.MMJoinResult`, see
[masterserver-enums](../08-reverse-engineering/masterserver-enums.md)); the
client shows the English text from its string table (`mmError_<code>`).
The table maps the message a player sees to the code and to the causes that
fit **hand-edited accounts and configs** *(message ↔ code: static, client
string table; causes: inferred unless marked)*:

| Message shown (English client) | Code | Likely cause after edits |
|---|---|---|
| "you can't enter a battle. Your account has a negative galactic standards balance…" | `MMJR_IN_DEBT` | `goldCredits` set above 2 147 483 647 is read as negative (signed 32-bit, Q52) - set a smaller value with the Hub stopped |
| "ships of all pilots in the battle have to match the location's tech level." | `MMJR_VESSEL_TIER_INAPPROPRIATE` | a ship's tier outside the location's tier band (open world / Conquest); the "tech level" in community reports |
| "ships in your combat slots do not meet rank requirements." / "…don't fit mission conditions." | `MMJR_VESSEL_RANK_INAPPROPRIATE(_PVE)` | combat-slot ship ranks outside the queue's ranks (for example rank 16-17 vs co-op queues 1-15, *file*) |
| "all ships have to be ranks $min_rank$-$max_rank$." / "no ships of ranks …" | `MMJR_VESSEL_RANK_ALL` / `_ANY` | same, for modes with an explicit rank band |
| "the highest ship rank in combat slots should be in the range …" | `MMJR_SQUAD_RANK_DIFF` | squad rank filter (`mmSquadRank`, Q35) |
| "the player and all pilots in the squad need clearance level $rank$ or higher." | `MMJR_INVALID_ACCOUNT_RANK` | `accountRank` below the mode's requirement |
| "unable to join the queue with damaged ships." | `MMJR_SHIPS_BROKEN` | a ship marked as destroyed/damaged; hand-inserted vessel records with odd condition fields ⚠ |
| "ship equipment failure." | `MMJR_WRONG_EQUIPMENT` | a module or munition that does not fit the hull (slot, size, tier) - typical after hand-editing `vessels[].modules` ⚠ |
| "this ship is not allowed to take part in battles." | `MMJR_FORBIDDEN_SHIP` | the hull is in `mm_forbiddenShips` / `lobby_forbiddenShips`, or an AI-only hull ⚠ |
| "no ships selected for battle." | `MMJR_NO_SHIPS_IN_BSLOTS` | battle slots (`bSlot`) empty after a vessel edit |
| "you need a license." | `MMJR_PREMIUM_REQUIRED` | premium expired or overflowed (Q63) |
| "the queue is not available." | `MMJR_QUEUE_DISABLED` | queue disabled or outside its schedule |
| "internal matchmaking error." | `MMJR_ERROR` | look in the MatchMaker log at that time |

Karma does not appear among these codes: no karma-based entry check was
found in Shard, MatchMaker, ZoneCoordinator or LobbyServer (only the karma
reset task, `KarmaResetCost`). For the full list of 53 codes see the
masterserver enums; the decision log (`mm_decisionLog`) shows the
MatchMaker's side.

## Where to look

1. `Hub/logs/hub_<date>.log` — spawn/registration/errors for every service.
2. `Hub/logs/<serviceId>_<service>_<date>.log` — per-service log.
3. `Hub/cloud_exceptions/`, `Hub/dediserver_exceptions/` — crash dumps.
4. Enable `hub_detachChildProcesses 0` to see service consoles.
5. For matchmaking: `cvars.mm_decisionLog` (bitmask, see
   [matchmaking guide](../05-configuration/matchmaking-guide.md)).

## Report template

```
Environment: OS / Proton version / depot build
Start method: Steam | manual | client button
Steps:
Expected / actual:
Relevant log excerpt (service id + timestamp):
```

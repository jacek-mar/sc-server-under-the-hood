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

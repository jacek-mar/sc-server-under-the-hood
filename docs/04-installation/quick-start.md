# Installation & quick start

> Status: **Stage 1 draft** — synthesised from the official page and from files
> shipped in the depot. Steps marked ⚠ have not yet been independently
> re-verified by this project.

## 1. Requirements

| Item | Requirement |
|------|-------------|
| OS | Windows 10/11 x64 (Linux via Proton — see [linux-proton.md](linux-proton.md)) |
| Game | Star Conflict client from **Steam** (the server files are part of the depot) |
| Disk | ≈ 12 GB for the depot, + MongoDB data (≈ 0.5 GB preallocated per set of DBs) |
| RAM | Whole node is ~17 processes of 30–80 MB each plus MongoDB; a few GB is enough |
| CPU | Game logic is mostly **single-threaded** (per-process) — clock speed matters more than cores |
| Optional | Redis (or compatible) for leaderboards; a MongoDB GUI compatible with MongoDB 2.6 (e.g. NoSQLBooster ≤ v4.7.5) |

## 2. Quick start (everything on one PC)

1. Install **Star Conflict** from Steam.
2. Start it from Steam. The client launches MongoDB and the Hub
   (`win64/local_server.xml`), which launches the other server applications.
3. On the login screen keep **`localhost`** selected (default).
4. Enter a user name and password and press *Login*. A new account is created
   automatically if the name does not exist.
5. First start (or after config changes) takes a while — wait until all server
   applications are up before logging in.

Closing the client (when started via Steam) shuts the server down gracefully.

## 3. Three ways to start the server

| Method | How | Notes |
|--------|-----|-------|
| Automatic | Launch via Steam | Client starts Mongo + Hub, stops them on exit |
| Manual | `launch_mongodb.bat`, wait, (start Redis), then `launch_server.bat` | Recommended for headless/dedicated hosting |
| Client button | "Launch server" on the login screen → `win64/launch_server_and_db.bat` | Starts Mongo, waits 3 s, starts Hub — no guarantee Mongo is ready |

Equivalent scripts (as shipped):

```bat
:: launch_mongodb.bat  (depot root)
start "" /D "%~dp0cloud\mongodb" launch.bat

:: launch_server.bat   (depot root)
start "" /D "%~dp0cloud" "Hub.exe"

:: win64\launch_server_and_db.bat
start "" /D "%~dp0..\cloud\mongodb" launch.bat
timeout /t 3
start "" /D "%~dp0..\cloud" Hub.exe
```

`cloud/mongodb/launch.bat` runs `mongod.exe -f ./config.cfg --dbpath
"%LOCALAPPDATA%\Targem\StarConflict\cloud\mongodb\data"`.

### Visible service windows

By default the Hub starts services *detached* (no windows). To see each
service's console set in `cloud/data/hub.cfg`:

```
set hub_detachChildProcesses 0
```

> **Unattended start (verified).** Start `mongod.exe` directly (not via `launch.bat` under a hidden window), wait for port 27017, then start `Hub.exe` with `cloud\` as working directory. A full node is up in < 90 s and uses ≈ 1.2 GB RAM. Details: [verification log](verification-log.md).

## 4. Stopping the server cleanly

> Verified (see [verification log](verification-log.md#clean-shutdown-verified)): closing the Hub window (WM_CLOSE) stops Hub and all 17 services within ~8 s; then shut MongoDB down with `mongo.exe 127.0.0.1/admin --eval "db.shutdownServer()"`. The client does **not** stop a server it started, on this build.

Manual sequence:

1. In the **Hub console** run `/enterMaintenanceMode <minutes>`.
2. Wait until all clients have disconnected.
3. `/quit` in the Hub console.
4. Close MongoDB (Ctrl+C in its window and confirm).
5. Close Redis, if used.

## 5. Playing with friends / hosting for others

1. Edit `cloud/data/cloud.xml` and replace `127.0.0.1:3850` in
   `<Node address="…">` with the **address clients should use** (LAN or public
   IP/DNS name).
2. Forward/allow the ports in [architecture §4](../03-architecture/architecture.md#4-ports)
   (at minimum 3850, 3801, 3802, plus chat 3815; battle ports TBD ⚠).
3. In the client login screen choose **`server`** and type address and port.
4. Read the [security notes](../07-administration/administration.md#5-security)
   before exposing anything to the internet — the stock configuration is
   **not hardened**.

> Remember the licence terms: no monetisation; label the server
> "Unofficial Server".

## 6. Optional: leaderboards (Redis)

1. Install and start Redis 5.x (or a compatible server, e.g. Memurai on Windows).
2. In `cloud/data/common.cfg` uncomment
   `set db_redisHost "127.0.0.1:6379|connpool=5"`.
3. Add the Redis start command to `launch_server_and_db.bat` if you want it
   auto-started. Shut down with `redis-cli SHUTDOWN SAVE`.

## 7. Changing language

Add `-lang ENGLISH` (also `RUSSIAN, FRENCH, GERMAN, SPANISH, POLISH,
PORTUGUESE, HUNGARIAN, CZECH, UKRAINIAN, CHINESE`) to the Steam launch options,
or set `cl_language` in `%LOCALAPPDATA%\Targem\StarConflict\user_config.xml`.

## 8. Resetting all data

Stop everything and delete
`%LOCALAPPDATA%\Targem\StarConflict\cloud\mongodb\data` (and Redis data, if
used). Next start creates a fresh database. To start over with one account only,
log in with a new user name.

## 9. Where things are

| What | Path |
|------|------|
| Server logs | `%LOCALAPPDATA%\Targem\StarConflict\cloud\Hub\logs\` |
| Client logs | `%LOCALAPPDATA%\Targem\StarConflict\logs\<timestamp>\` |
| MongoDB data | `%LOCALAPPDATA%\Targem\StarConflict\cloud\mongodb\data\` |
| Client config | `%LOCALAPPDATA%\Targem\StarConflict\user_config.xml` |
| Server config | `<depot>\cloud\data\` |

See also: [troubleshooting](troubleshooting.md).

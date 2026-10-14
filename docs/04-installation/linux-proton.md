# Linux (Proton / Wine) and containers

> Status: **community-reported, not verified by this project.** Collected from
> the community wiki and Discord export. Verification is a Stage 3 task.

## Summary

The depot ships **Windows binaries only**: the client (`win64/game.exe`) and MongoDB are x64, but the 22 server executables in `cloud/` are **32-bit x86** (checked with `pefile`, 2026-10-11) - a 32-bit-capable Wine is needed. Native/portable alternatives are analysed in [linux-native-and-portable-server.md](../09-community-edition/linux-native-and-portable-server.md). Steam on Linux installs only an
`EmptySteamDepot` directory natively (the old native Linux client is gone), so
Proton is required.

## Reported working recipe

1. In Steam: *Properties → Compatibility → force Proton* (reports mention
   **Proton 11.0-2** and **9.0-4**, the latter tested on Debian 13 with an
   integrated Intel GPU; any recent version may work).
2. Run *Validate files* — this then downloads the real depot.
3. Start the game normally; the client spawns Mongo + Hub under Proton.
   Running the game fullscreen avoids accidentally clicking the console windows.
4. To run only the server without the game UI: either minimise the game after
   pressing *Launch server*, or use `winetricks`/Wine to run
   `launch_mongodb.bat` and `launch_server.bat` (or `win64/launch_server_and_db.bat`)
   yourself from a Wine prefix pointing at the Steam install.
5. To edit `default_platform_config.lua` and regenerate XML with
   `prepare_shared.bat`, use Wine (via winetricks) to execute the batch file.

**Editing the database on Linux** *(community, S11 update)*: NoSQLBooster
**5.2.12** as an AppImage (make it executable; it needs the FUSE 2 library,
for example `libfuse2`/`libfuse2t64` on Debian, `fuse` on Fedora). Start the
game, then close the game and the Hub window but leave `mongod` running, and
connect to `localhost:27017`. Edit only while the Hub is stopped
([mongodb.md](../06-database/mongodb.md)).

Reports also say the whole thing "works fine with Proton" for a LAN server on a
spare Linux box; ARM hosts would need x86 emulation (FEX) — untested.

## Containers (update 2026-10-11)

A headless Wine-in-Docker image **now exists** (community project, announced
on release day). It runs the 17 services under Wine, MongoDB 2.6 and Redis as
native containers, and patches the executables. Our evaluation, the check of
its patches against the shipped build and a hardened blueprint are in
[docker.md](docker.md). Use that document rather than the Proton recipe for
24/7 Linux hosting.

## Ideas / open items

* Steam on Linux (S19, 2026-10-14): without a Proton version selected, Steam
  shows a 0-byte install or "game.exe not found" - there is no native Linux
  build; choose a Proton version in the game's compatibility settings (or
  download the Windows depot with SteamCMD). *(community)*

* Headless Wine-in-Docker image — see above. Still open: Wine without the
  patches (DK-2), battle with a non-loopback node address (DK-3/DK-4).
  Requirements: Wine prefix, no X11 for services (they are
  console processes), Mongo 2.6 on Linux natively (replaces the Windows
  `mongod.exe`; protocol-compatible) — see [open questions](../08-reverse-engineering/open-questions.md).
* Native Linux `mongod` 2.6 + Wine only for the cloud executables is a plausible
  split deployment.
* Exposing ports from a container: see [ports](../03-architecture/architecture.md#4-ports).

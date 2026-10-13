# When does a setting take effect? (reload map)

> Lab S11-R2, 2026-10-13, on the lab node copy (build 1.99.0.167293, agent
> alone, no game client). *(observed)* unless marked otherwise. Answers the
> operator question behind b008 K13 ("hosts restart every few minutes while
> tuning"). Related: [config-system.md](config-system.md) (layer order),
> [config-pipeline-and-limiters.md](../08-reverse-engineering/config-pipeline-and-limiters.md)
> (`prepare_shared`), [verification-log.md](../04-installation/verification-log.md) V-7/V-11
> (SSH console).

## 1. Summary

| How you change it | Takes effect | Survives a restart | Caveat |
|---|---|---|---|
| **SSH console**, Lua assignment `cvars.<name> = <value>` | **immediately** in that one service process (read back with `/cvarList <name>`) | no - lost when the service or node restarts | only services with a console (`ssh_passwd` etc. in `*_local.cfg`); a cvar read only at start-up changes its value but not the behaviour already set up |
| **`<service>_local.cfg`** (`set <name> <value>`) | at the next service / node start | yes | **loses** against any value the platform Lua (`default_platform_config.lua`) assigns, because the Lua runs after the cfg layer |
| **`default_platform_config.lua`** | at the next service / node start | yes | the authoritative place for every cvar it assigns (257 cvars, [cvar-binary-catalogue](cvar-binary-catalogue.md)) |
| **Lua game data** (`data/gamedata/**`) | services that use `cloud/data` XML: only after **`prepare_shared` + restart**; client and battle server read the Lua directly ([gamedata-readers](gamedata-readers.md)) | yes | `prepare_shared` needs MongoDB; check with `tools/data_drift_check.py` |
| **`cloud/data/*.xml` edited by hand** | next start of the services that load it | until the next `prepare_shared`, which rewrites 29 of these files (V-11) | prefer editing the Lua source |
| **Database values** (accounts, roles, admin tasks) | admin tasks: within ~5 s (pick-up poll); direct edits of account documents: the client sees them after re-login (Q32) | yes | see [admin-tasks-howto](../07-administration/admin-tasks-howto.md) |

## 2. Test results

Live = console assignment then `/cvarList`; cfg = `set` lines appended to the
node copy's `*_local.cfg`, Hub restarted (MongoDB kept running), value read
back with `/cvarList`. Files restored afterwards (hash-checked).

| Service | Cvar | Shipped value | Live change | `_local.cfg` + restart | Assigned in platform Lua? |
|---|---|---|---|---|---|
| Shard | `sm_overloadCounterLimit` | 20 (`shard.cfg`) | 20 -> 25, read back 25 | 30 -> **30** (cfg wins) | no |
| Shard | `ctm_debugTaskPickup` | 0 | 0 -> 1: **behaviour changed at once** (`Pick up admin task...` every 5 s) | 1 -> **1** (cfg wins, log lines from start-up) | no |
| Shard | `store_maxUniqueModules` | 3 | 3 -> 4, read back 4 | 5 -> **3** (Lua wins) | yes (lines 222, 1837) |
| Shard | `sv_tokenCreditsDailyLimit` | 1000 | 1000 -> 1500, read back 1500 | 2000 -> **1000** (Lua wins) | yes (lines 269, 1622) |
| MatchMaker | `mm_botsCount` | 6 | 6 -> 4, read back 4 | 4 -> **6** (Lua wins) | yes (line 889) |
| MatchMaker | `mm_lowOnlineLo` | 250 | - | 100 -> **250** (Lua wins) | yes |

Not tested here: battle-server cvars (the battle server has a console only
while a battle runs - needs a client or the vendor's autotest mode), and
whether each live-changed gameplay cvar is re-read by the code (only
`ctm_debugTaskPickup` was observed changing behaviour; for the others only
the stored value was confirmed).

## 3. Practical rules for operators

1. Look up the cvar in the platform Lua first. If the Lua assigns it, change
   it **there** (or the dispatcher function for that service type), not in
   `*_local.cfg` - a `_local.cfg` line is silently overridden.
2. To try a value without a restart, use the SSH console
   (`cvars.<name> = <value>`), confirm with `/cvarList <name>`, then make it
   permanent in the platform Lua. The console change is lost on restart and
   applies to one service instance only (several Shards = several consoles).
3. The service log, not the SSH session, receives the console output of the
   cloud services (`/cvarList`, errors); Lua `print()` output did not appear
   in the log at all - use `/cvarList` to read values.
4. Restarting only the Hub (MongoDB left running) brought the node back to
   READY in about 27 s on the 2-core lab machine.
5. Game-data edits: Lua -> `prepare_shared` -> restart; then run
   `tools/data_drift_check.py` against an untouched depot copy.

## 4. Console gotchas seen in this lab

* The Shard and MatchMaker consoles often drop a new connection right after
  the TCP accept (`SSHServer: disconnected SSH client` within 0.2 s, before
  authentication); retrying after a few seconds works (2-4 attempts).
* Every typed character is echoed back, so the SSH session text is noisy;
  read results from the service log (`CONSOLE` lines).

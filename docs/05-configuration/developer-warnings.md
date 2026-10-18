# Developer warnings in the shipped files (translated)

> Warnings and constraints that the developers left as **Russian comments**
> in the shipped Lua files. Translated into English: an offline machine
> draft, then checked by hand against the original comment (playground
> task 012, reviewed 2026-10-18). Each row is a *(file)* statement *of the
> comment*. It says what the developers wrote, not what was tested. Paths
> are relative to `star conflict/`; line numbers are for the reference
> build.

This is a curated shortlist of 30 out of 16,333 Cyrillic comments in 300
files. It is not exhaustive. Comments on cvars in
`default_platform_config.lua` also appear in the
[cvar reference](cvar-reference.md).

## Do not change or delete

| File : line | Warning (translation) |
|---|---|
| `data/gamedata/def/effects.lua:615` | There used to be a different effect here; do not delete it, it is still used. |
| `data/gamedata/def/effects.lua:953` | There used to be a different effect here, smoke_fire_big_v2; do not delete it, it is still used. |
| `data/gamedata/def/objects/bundles_dlc.lua:10` | USED IN DLC! DO NOT CHANGE! |
| `data/gamedata/def/objects/ships.lua:176` | For an April Fools joke. After April 1 it is probably better to comment this out, but never delete it. #50964 |
| `data/gamedata/shared/login_rewards.lua:22` | offerId must not be changed after deployment to live. |
| `data/gamedata/shared/titles.lua:4` | WARNING! Do not change title numbers or order, or comment out/delete titles. New titles may only be appended at the end. |

## Stored in the database

| File : line | Warning (translation) |
|---|---|
| `cloud/data/default_platform_config.lua:16` | Warning: player progress is stored for only one event. Changing the event start time discards it because this counts as a different event. This excludes premium purchased through dlc, which is retained across events. |
| `cloud/data/default_platform_config.lua:287` | Number of adaptive presets stored in the database. 0 clears the data. (Type: integer; range: 0..1000.) |
| `cloud/data/default_platform_config.lua:1012` | Disables validation of the format of Lua data (for example, zone playerLuaData) during conversion and saving to the database. |
| `cloud/data/default_platform_config.lua:1351` | Limit on adaptive-preset database records per mode, rank and role; 0 clears the database. |
| `cloud/data/default_platform_config.lua:1438` | Disables format checks on Lua data during conversion and saving to the database. 1 writes data without checking the schema; only for builds that are not live. |
| `data/gamedata/shared/adventures.lua:11` | Adventures are stored in the database with references to definitions by indices. Simply deleting adventure N and replacing it with another is risky if a player still has it in the database. |
| `data/gamedata/shared/sc_achievements.lua:3831` | The database value is 100; tests use 1. |
| `data/gamedata/shared/sc_achievements.lua:3864` | Number of times the condition in numerical_conditions[1] must be met; the database value is 50, while tests use 1. |
| `data/gamedata/shared/sc_achievements.lua:3888` | The database value is 10; tests use 1. |
| `data/gamedata/shared/sc_achievements.lua:3914` | The database value is 20; tests use 1. |

## Needs a restart

| File : line | Warning (translation) |
|---|---|
| `data/gamedata/shared/referrals.lua:72` | WARNING! Changes to these parameters take effect only after a server restart. |

## Which program reads the file

| File : line | Warning (translation) |
|---|---|
| `data/gamedata/music_states.lua:27` | The dedicated server has no music assets and currently does not read "sound/playlist.lua"; this file must not reference it directly. |
| `data/gamedata/shared/adventure_stages.lua:1` | This file is not read by the service, only by the dedicated server and the client. |
| `data/gamedata/shared/adventures.lua:1` | This file is read by the service. |

## Units, ranges and limits

| File : line | Warning (translation) |
|---|---|
| `cloud/data/default_platform_config.lua:7` | Change the start and end times in whole-hour increments; otherwise the imaginary quest may behave unpredictably. |
| `cloud/data/default_platform_config.lua:18` | Ensure that the end dates/times of stages 1 and 2 of the same battle pass match! Stage 3 was added in summer 2023. |
| `cloud/data/default_platform_config.lua:72` | Minimum anti-bot counter value required to send mail. (Type: integer; range: 0..100.) |
| `cloud/data/default_platform_config.lua:110` | Store ship-price multiplier. Applies to all ship price types: credits, premium, tokens and event price. (Type: float; range: 0.001f..100.0f.) |
| `cloud/data/default_platform_config.lua:165` | Specified in seconds; allowed range: 0.01..5. |
| `cloud/data/default_platform_config.lua:185` | Group-composition filter for raid queues: determines whether solo players, ordinary squads and/or wing groups may enter a raid. |
| `cloud/data/default_platform_config.lua:264` | Premium time (in seconds; default: one day). |
| `cloud/data/default_platform_config.lua:1228` | Minimum interval for sending player progress to the achievement server, in seconds. (Type: float.) |
| `cloud/data/default_platform_config.lua:1262` | Time budget for incremental Lua GC work, in microseconds. (Type: integer.) |
| `cloud/data/default_platform_config.lua:1345` | Number of top players whose ships are saved for adaptive presets; -1 means all players and all ships. (type: integer; range: -1..MAX_PLAYERS) |

## What this means for operators *(inferred)*

* Do not renumber or delete titles or adventures. The comments say that the
  database refers to them by number or index, so add new ones at the end.
  Keep the effects, the DLC bundle and the April ship entry that the comments
  mark as still in use.
* Changing an event or battle-pass **start time** creates a new event, and
  stored player progress is lost (`default_platform_config.lua:16`).
* Four achievement thresholds note a "database value" next to a test value.
  The shipped code uses the database value. The comment does not show what a
  live database held.

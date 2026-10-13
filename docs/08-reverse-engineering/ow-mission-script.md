# Open-world server script (`scripts/general/missions.lua`)

> Status: **observed** from the lifted bytecode (
> names only). This script defines the global `Mission` object that runs
> inside every ZoneInstance (open world) and, in part, in battles. ~5 400
> lifted pseudo-Lua lines, 60 `Mission.*` functions.

## Entry points the engine calls (`SV_*` / `On*`)

| Group | Functions |
|-------|-----------|
| Frame / lifecycle | `SV_OnUpdate`, `InitMap`, `InitPlayers`, `NewShip`, `UpdatePlayers`, `CheckPlayers`, `OnNewPlayer`, `OnRemovePlayer`, `OnEntityRemoved`, `AddPlayer`, `GetLivePlayers` |
| Combat hooks | `SV_OnSpaceShipKill`, `SV_OnEntityKill`, `SV_OnSpaceShipDamage`, `SV_OnEntityDamage`, `EventOnKillBotCheck`, `GetWinnersByDeathIds` |
| Interaction | `SV_OnRecieveQuestItem`, `SV_OnQuestObjectInteracted`, `SV_OnQuestTriggerInteracted`, `SV_OnQuestTriggerInRange` |
| Universe / zone sync | `OnZoneOwnerChanged`, `OnZoneRaceChanged`, `OnZoneHasConflictChanged`, `OnZoneIsCivilianChanged`, `OnZoneLuaEvent`, `OnOutsideZoneLuaEvent`, `SV_ZoneInstance_SendLuaEvents` |
| Player relations | `UpdateCriminalPlayers`, `UpdatePlayersRelationships`, `LoadPlayerRelationships` |
| Events manager | `EventsManager`, `TryStartEvent`, `CreateEvent`, `RegistrateEvent`, `EventUpdate`, `EventReward`, `EventCanStart`, `DailyEventCanStart`, `EventEndByFail`, `EventEndByComplete`, `EventEndCommon`, `HasActiveEvent`, `HasActiveEventByClass`, `RemoveGate` |
| Daily quests | `QuestsDaylyUpdate`, `QuestsDaylyOnNewPlayer`, `QuestsDaylyOnCompletePersonalQuest` |
| Tags / entities | `InsertTags`, `AddDefaultTags`, `AddTags`, `KeepAnyTag`, `KeepAllTags`, `EntityKeepTags`, `RemoveTags`, `GetEntitiesWithTag`, `GetEventTarget`, `GetPlace2Spawn`, `ParseMobConfig`, `GetPoint` |

State kept on `Mission`: `ZiEvents`, `Tags`, `Turrets`, `ActiveEvents`,
`map` (`size`), `big_space_size = 70`, `eventsManager_lastTime`,
`StartLocalTimeOfDay`, `levelName`.

## How the pieces fit (inferred)

1. ScriptsServer (global) owns *event state* per zone and pushes it to zone
   instances (`OnZoneLuaEvent`, `ZiEvents`).
2. The events manager in `Mission` creates entity-level event objects of the
   classes defined in `events_global.lua` (`AttackerStation`, `OwnerStation`,
   `ChinaCyberBoss`, …) and spawns child encounters (`childEvents`).
3. Personal quests (`QuestPersonal` in `quests.lua`, see
   [open-world-quests.md](../05-configuration/open-world-quests.md)) are
   enabled while particular events are active and hook the kill/interaction
   callbacks above.
4. Rewards go through `EventReward` and the `reward` tables (credits and
   faction *loyalty* deltas).

Companion data: [zone-events.md](../05-configuration/zone-events.md),
[open-world-and-services.md](../05-configuration/open-world-and-services.md).
## Companion scripts (2026-10-11; names from the lifted bytecode, *(observed)*)

| Script | What it defines |
|---|---|
| `scripts/general/event_manager.lua` | `EventManager` object: `Init`, `EventStart`, `OnUpdate`, `OnNewPlayer`, `OnRemovePlayer`, `OnSpaceShipKill/Damage`, `OnEntityKill/Damage`, `OnInteractiveObjectInteracted/Detached`, def lookup (`GetDef`, `GetPrototype`, `GetInstancesWithDef`), pre-caching (`PrecacheDefs`, `PrecacheDefsInTable`) and an `EventManager.EventPrototype` base (`Start`, `OnStart`, `OnUpdate`, ... ) that event classes (`Common`, `Boss`, `PathPatrol`, `DefendEntPatrol`, `HuntPlayer`, `MiningVein`, ...) specialise. The definitions it runs are catalogued in [ow-events-catalog.md](ow-events-catalog.md) |
| `scripts/general/special_ow_features.lua` | Helpers mixed into `Mission`: **difficulty buffs by number of players** (`buffByNumPlayers`, `buffByNumPlayers2`, `buffTableByNumPlayers`, `buffByNumPlayersPeriod`, `buffByNumPlayersOnMapMinCoef`, applied to bots that carry an `agroTable`, i.e. bosses scale with players in aggro), map helper tables (`Mission.map.*`: `bigSpace`, `platformSpace`, `gate2Random...`), `Mission.level.OwnerStationPos/AttackerStationPos`, `SavePlayer/SavePlayerUID`, notifications (`ShowNotify`, `ShowWowMsg`, `ShowDialogs2players`) |
| `scripts/general/missions2.lua` | Small secondary mission script: scanner mechanic (`Scan`, `ScanInit`, `scan_max_dist`, `scanMatrix`, spawn tries) and **fast-fly** (`InitFastFly`, `SV_UpdateFastFly`, `FastFlyArray`, `GatheringDist`) plus `SV_OnStart/SV_OnUpdate` and client counterparts `CL_OnStart/CL_OnUpdate` |

Practical consequence: tuning a boss fight means editing the `Events.*`
rows (HP/damage come from the boss ship defs referenced there, see
[ship-defs](../05-configuration/ship-defs.md)), not these engine scripts; the
scripts themselves are LuaJIT bytecode in `misc.pak` and are not editable
without repacking (a clean-room server would reimplement them).

# Server → client Lua RPC allow-list

> Status: **observed** (plain-text file `data/gamedata/client_lua_rpc_allowlist.lua`,
> 34 names). The client executes only these function names when a server
> script calls a function on a client (`ClientLuaRpcAllowlist = { … }`).
> It is the safety boundary between a (possibly untrusted) community server
> and the client's Lua state — relevant for the official warning that
> "the game client may contain vulnerabilities".

| Group | Names |
|-------|-------|
| PvE events (HUD) | `CL_ActivatePVEEvent`, `CL_UpdatePVEEvent`, `CL_CompletePVEEvent`, `CL_FailPVEEvent`, `CL_PveEventsReset` |
| Tasks / log | `CL_AddTask`, `CL_UpdateTask`, `CL_RemoveTask`, `CL_AddLogMessage`, `CL_WOW_MSG`, `ShowWow`, `CL_ShowDialogScript` |
| Progress UI | `CL_ShowProgressPhase`, `CL_HideProgressPhase`, `CL_SetBossId` |
| Entities / marks | `CL_SpawnPersonalEntity`, `CL_RemovePersonalEntity`, `ADD_MARK_BY_DEF_NAME`, `ADD_ACTIVITY_BY_DEF_NAME`, `CL_FocusPointsAdd`, `CL_FocusPointsClear`, `CL_FindEffects` |
| Effects / visuals | `CL_EffectStart`, `CL_EffectStop`, `CL_LightSpawn`, `CL_SetColorRemap`, `CL_ResetColorRemap` |
| Audio | `PlaySoundOnClient`, `CL_SetPlaylist`, `CL_ResetPlaylist`, `CL_StopPlaylist` |
| Misc gameplay | `CL_BALL_SYNC` (football), `CL_FastFlyUpdateStatus`, `CL_Get_Mining` |

Use: a community battle server written from scratch must restrict itself to
these calls when talking to stock clients.
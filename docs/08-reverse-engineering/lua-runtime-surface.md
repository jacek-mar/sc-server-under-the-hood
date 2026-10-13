# Lua runtime surface: which libraries game scripts can reach (static)

> Analysis of 2026-10-13. Static analysis of build 1.99.0.167293 (strings
> and machine code of the executables). **Nothing was executed.** Answers open question **Q47** (static part) and backs
> security finding **S-29**. Trigger: community claim that the game's Lua is
> not sandboxed (source register, batch 008 K3).

## 1. Result

| Executable | Libraries opened into each Lua state | Registered in `package.preload` | Absent standard libraries |
|---|---|---|---|
| `win64/game.exe` (client, x64) | base, package, table, string, math, debug, bit, jit | **ffi** | io, os |
| `cloud/DedicatedServer.exe` and 20 other service executables | same | **ffi** | io, os |
| `cloud/StatServer.exe` (older build, not in `cloud.xml`) | no LuaJIT library table found | - | - |

*(static, high confidence)* Every executable that embeds LuaJIT opens its
libraries through LuaJIT's standard opener (`luaL_openlibs`): a static table of
`{name, luaopen_*}` pairs (`lj_lib_load`) followed by a second table
(`lj_lib_preload`) whose only entry is `ffi`. The vendor removed `io` and `os`
from the first table, but **kept `package` (with `require` and
`package.loadlib`), `debug` and the preloaded `ffi`**. The preload table is
referenced from live code (1-3 places per executable).

No code path removes them again:

* no shipped Lua script (plain-text Lua under `data/gamedata` and
  `cloud/data`, and the 87 bytecode scripts from `misc.pak`) mentions
  `require`, `package`, `preload`, `loadlib`, `ffi` or `debug`;
* in `DedicatedServer.exe` the name strings `require` and `loadlib` have no
  code references outside LuaJIT's own registration tables, so the engine does
  not overwrite these globals by name. (The only non-LuaJIT reference to the
  string `"ffi"` is a typographic-ligature table next to `"ffl"`.)

## 2. What this means

* **Any Lua chunk that the game executes can run native code**:
  `local ffi = require("ffi")` gives `ffi.cdef` / `ffi.C` / `ffi.load` (call any
  Windows API or DLL), and `package.loadlib` loads a DLL directly. Removing
  `io`/`os` therefore does **not** sandbox the runtime. *(inferred from the
  library set; a runtime confirmation is the optional VM probe below)*
* This applies to the **client** (scripts and data shipped by a launcher or a
  community file server) and to **every service** (the platform config
  `default_platform_config.lua`, mission/zone scripts, defs, and the SSH
  console, which is a Lua prompt - security S-03).
* The community statement about "shell execute and arbitrary file write" was
  not checked for game-specific bindings; FFI alone is sufficient for the
  conclusion.

## 3. Consequences for operators, players and downstream designs

* **Players:** treat Lua and data files from servers, launchers or mod packs
  as programs ([security S-29](../07-administration/security.md)).
* **Hosts:** review third-party Lua for the server like code; protect the
  depot and `cloud/data` with file permissions; never expose the SSH console.
* **Downstream runtimes** (a future server or launcher): if scripts must be
  loadable from untrusted sources, build LuaJIT without FFI
  (`LUAJIT_DISABLE_FFI`), do not open `package`/`debug`, or remove
  `require`, `package.loadlib` and `package.preload.ffi` before running any
  script; additionally isolate the process (restricted token, AppContainer).

## 4. Open (optional) runtime confirmation

In a throw-away VM only: a test script that logs
`pcall(require, "ffi")` and `type(package.loadlib)` from a client-side and a
server-side script context. Not needed for the design conclusion.

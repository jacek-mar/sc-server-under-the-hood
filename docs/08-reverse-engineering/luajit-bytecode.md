# LuaJIT bytecode in the shipped scripts — reader and disassembler

> Status: **verified.** A disassembler written from the LuaJIT 2.1 format
> description parses **87 / 87** bytecode scripts of `misc.pak` without
> error and produces a coherent disassembly.

## 1. What the scripts are

* Magic `1B 4C 4A`, bytecode version byte `02` (LuaJIT 2.1 dump), flags
  `0x02` = **stripped** (no chunk name, no line numbers, no local/upvalue
  names). Function prototypes are therefore anonymous (`proto#N`) and locals
  are `rN` registers.
* Global names, field names (`TGETS`/`TSETS` constants) and string literals
  are fully preserved — enough to recover logic, events, enums and the Lua API
  surface.
* Only one script in `misc.pak` is plain text; everything under `scripts/` is
  bytecode.

## 2. Dump layout (as implemented)

```
ESC 'L' 'J' <version u8> <flags uleb> [<chunkname len uleb, bytes> unless stripped]
repeat { <proto length uleb> proto }   # 0 terminates; children precede parents, main chunk last
proto: flags u8 | numparams u8 | framesize u8 | sizeuv u8 | sizekgc uleb | sizekn uleb | sizebc uleb
       [| sizedbg uleb [firstline uleb, numline uleb] unless stripped]
       bytecode: sizebc x u32 | upvalue refs: sizeuv x u16
       kgc: per entry uleb tag: 0 child proto (popped from stack), 1 table, 2 int64, 3 uint64,
            4 complex, >=5 string of length tag-5
       knum: per entry "uleb128_33": low bit = is-double (then a second uleb33 gives the high word)
       [debug info unless stripped]
```

Instruction word: `op` = bits 0–7, `A` = 8–15, `C` = 16–23, `B` = 24–31 (ABC form)
or `D` = bits 16–31 (AD form). Jump targets are `pc + 1 + D − 0x8000`.
String constants are indexed **from the end** of the kgc array. The opcode
table is the LuaJIT 2.1 `BCDEF` order (`ISLT … FUNCCW`, including `ISTYPE`,
`ISNUM`, `TGETR`, `TSETR`).

## 3. Example

Sample (anonymised excerpt shape — ScriptsServer main loop): `GGET pairs` →
`TGETS ScriptsServer.zones` → `CALL` → `ISNEXT/ITERN/ITERL` loops, then
`TGETV Events[id]`, `TGETS …disableOriginalQuests`, `TSETS … disableQuests`
— i.e. per zone, per active event: remove events without a definition, and
mirror `enable/disableOriginalQuests` into zone flags.

## 4. Outputs

* [lua-api-surface.md](lua-api-surface.md) (generated): 327 global names read
  by the scripts (304 beyond the Lua standard library), 192 defined by scripts.
  Engine-provided examples: `UI`, `Def`, `designers`, `Vec3`, `Quat`,
  `ScriptWriteFile`, `Game_IsServer`, `TraceLine`, `CL_GetPlayerShip`,
  `TimerGetGameTime`, `GetEntitiesByClass`, `PrecacheDef`, `ItemSubtype`.
* Disassembly listings are not published (they are derived from proprietary
  scripts).

## 5. Limits / next steps

* No structured decompilation (loops/ifs are shown as jumps); names of locals
  are lost by stripping. Control-flow reconstruction for the important
  scripts (ScriptsServer events, masterserver RPC definitions) can be done by
  hand with the disassembly.
* Table constructors (`TDUP`) carry constant table templates; the numeric
  values of the master-server enums were read from them
  ([masterserver-enums](masterserver-enums.md)).
* Next: use `TGETS`/`TSETS` field names to document the `ai.*` and
  `ScriptsServer.*` namespaces, and the event definition tables
  (`DIRECTOR_BOSS_EVENTS`, `*_OWNERSHIP`, `*_EXPANSION`).
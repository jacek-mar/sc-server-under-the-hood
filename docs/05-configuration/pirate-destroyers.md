# Pirate destroyers - definitions, names and modules (static analysis)

> Analysis of 2026-10-14, reference build 1.99.0.167293. Everything below is
> **file-verified** unless tagged otherwise. Sources:
> `data/gamedata/def/ex/ow_bot_preset.lua` (open-world boss definitions),
> `def/ex/pvebot_preset.lua` (parent and PvE copies),
> `def/objects/pve_entities.lua` (AI module variants), `def/ex/ship.lua` and
> `def/ex/active.lua` (player hulls and modules), the English client string
> table `strings/english/string.txt` (inside `data/strings.pak`, see
> [tpak-format](../08-reverse-engineering/tpak-format.md)) and the lifted
> open-world script `scripts/general/events_piratsboss.lua`
> ([ow-events-catalog](../08-reverse-engineering/ow-events-catalog.md)).
> Nothing was run. Display names are the English strings; other languages
> use the same keys.

The "pirate destroyers" are the open-world boss ships of the pirate events.
**Whether a player can fly one is open** ([Q49](../08-reverse-engineering/open-questions.md));
§4 collects the facts that bear on it.

## 1. Definitions and display names

Each boss is a ship definition with `uiName` pointing to a string key.

| Definition | String key | English name | Parent (`inherit`) | Hull / model |
|---|---|---|---|---|
| `Ship_OW_Boss_Empire_Destroyer` | `ow_Boss_02` | Pirate destroyer "Adventure" | `Ship_Gen_Boss_Empire_Destroyer` -> `Ship_Race1_H_T4` | Empire destroyer hull (`models/ships/race_1/h/r1_h_t2`) |
| `Ship_OW_Boss_Federation_Destroyer` | `ow_Boss_03` | Pirate destroyer "Revenge" | `Ship_Gen_Boss_Federation_Destroyer` -> `Ship_Race3_H_T4` | Federation destroyer hull (`models/ships/race_3/h/r3_h_altair`) |
| `Ship_OW_Boss_Jericho_Destroyer` | `ow_Boss_04` | Pirate destroyer "Fortune" | `Ship_Gen_Boss_Jericho_Destroyer` -> `Ship_Race2_H_T4` | Jericho destroyer hull (`models/ships/race_2/h/r2_h_t2`) |
| `Ship_OW_Boss_Empire_Destroyer2` | `ow_Boss_05` | Enclave destroyer "Golden Hind" | `Ship_OW_Boss_Empire_Destroyer` | as "Adventure" |
| `Ship_OW_Boss_Federation_Destroyer2` | `ow_Boss_06` | Corsair destroyer "Pearl" | `Ship_OW_Boss_Federation_Destroyer` | as "Revenge" |
| `Ship_OW_Boss_Jericho_Destroyer2` | `ow_Boss_07` | Cartel destroyer "Happy" | `Ship_OW_Boss_Jericho_Destroyer` | as "Fortune" |
| `Ship_OW_Boss_PirateEvent` | `ow_PirateEvent_Boss` | Experimental destroyer | `Ship_Gen_Boss_Empire_Destroyer` | own model `models/ships/race_4/h/race4_h_t1_craftuniq_boss` |
| `Ship_OW_Elite_PirateEvent_Guard` | `ow_PirateEvent_Guard` | Enclave Destroyer (the event boss's escort) | `Ship_Gen_Elite_Pirate_Guard_Hook_L` | frigate model `models/ships/race_2/l/race2_l_t5_craftuniq` |

Notes:

* The first six bosses set no `model` of their own; they inherit the hull of
  the rank-11 player destroyers `Ship_Race1_H_T4`, `Ship_Race3_H_T4` and
  `Ship_Race2_H_T4` (`storeItemId` 73, 147, 221 in `def/ex/ship.lua`).
* Despite its name, the "Enclave Destroyer" guard inherits a large-ship
  (frigate) preset and model, not a destroyer.
* The "rescue pirates" PvE mission has three copies,
  `Ship_rescue_Boss_{Empire,Federation,Jericho}_Destroyer`
  (`pvebot_preset.lua`), with the same names (`ow_Boss_02`..`04`) and the same
  modules as the first three bosses.
* `shared/adventures.lua` uses `Ship_OW_Boss_*_Destroyer[2]` as kill targets
  of open-world missions (`ai.AdventureFilter.ENTITY_DEF`).

Common fields of all seven bosses: `ship4bot=true`, `AiSettings="Harder_AID"`,
`avtomat="BossEasyPatrol"`, `hud_ico="supressor_ico"`,
`hudType="major"`, tags `piratElite`, `pirat` (not on the event boss). The
`Ship_Gen_Boss_*` parents add `bot_rank=17`, `storeItemId=0` and
`pve_ship_level=ai.PveShipLevel.NORMAL`.

## 2. Which event spawns which boss

From [ow-events-catalog](../08-reverse-engineering/ow-events-catalog.md)
(`events_piratsboss.lua`, boss class, spawn at `designers.EventsConst.Gate`,
relationship group Enclave). The event-to-definition pairing for the
`*Corsar` events follows the order of constants in the bytecode *(inferred)*:

| Event | Boss definition | Timeout s | Credits |
|---|---|---:|---:|
| `EmpirePirat` / `FederationPirat` / `JerichoPirat` | `Ship_OW_Boss_<Race>_Destroyer` | 14 400 | 600 000 |
| `EmpireCorsar` / `FederationCorsar` / `JerichoCorsar` | `Ship_OW_Boss_<Race>_Destroyer2` *(inferred)* | 14 400 | 600 000 |
| `EventCorsar` | `Ship_OW_Boss_PirateEvent` | 3 600 | 2 000 000 |
| `PirateInvasion_Boss_01` (`events_pirate_invasion.lua`) | `Ship_OW_Boss_PirateEvent` | 360 | 500 000 |

## 3. Modules

Slots come from `default_modules`; the missile is `default_rocket_munition`.
Most entries are AI copies (`*_Mob`, `*_PvE`) of player items in
`def/objects/pve_entities.lua`. Such a copy usually has no `uiName` and
takes its name from the `item_subtype` of the player item it inherits from
(string key `ItemSubtype_<subtype>`). The OW definitions replace the
`default_modules` of their `Ship_Gen_Boss_*` parents.

### 3.1 The six basic bosses

| Boss | Primary weapon | Active 1 | Active 2 | Active 3 | Active 4 | Missile |
|---|---|---|---|---|---|---|
| "Adventure" | `Weapon_Destroyer_Rocket_Heavy_T3` - Coil Mortar | `Module_TachRay_Mob_T4` - Pyro Emitter | `Module_PushRay_Mob` - Repelling Beam | `Module_TeleportToKill_Mob` - "Unidentified Weapon" | `Module_Empty_PvE` | `DestrMunition_HealBot_Boss` - Heavy Repair Drone |
| "Revenge" | `Weapon_RailgunDestr_Mob_T3` - Coilgun | `Module_AdaptiveBigShieldBoost_Mob` - Multiphase shield | `Module_TurretThermo_Mob` - Blaster Turret | `Module_MassRemotePulsar_Mob` - "Unidentified Weapon" | `Module_Empty_PvE` | `DestrMunition_SectorShield_T3_Mk3` - Static Shield |
| "Fortune" | `Weapon_PlasmaVolley_Mob_Round_Slow` - Fuse Blaster | `Module_GravityAnomaly_Mob` - Gravitational Lens | `Module_DestrBeamDrone_Mob` - Hybrid missile | `Module_TurretPlasma_Mob` - Plasma Turret | `Module_Empty_PvE` | Static Shield |
| "Golden Hind" | `Weapon_OrbGunUnique_II_Round_Slow` - 'Torch' Launcher Mk II | Multiphase shield | `Module_TractorBeam_Mob_T3` - Tractor Beam | `Module_IsotopeHarvester_Mob` - Isotope Harvester | `Module_TeleportToKill_Mob` | Heavy Repair Drone |
| "Pearl" | Coil Mortar | Blaster Turret | Repelling Beam | `Module_Javelin_Mob` - Photon Emitter | `Module_MassRemotePulsar_Mob` | Static Shield |
| "Happy" | `Weapon_GreenGravityAnomaly_Mob_Slow` - G'Thar'Du Cannon | `Module_DestrMovementRestrictor_Mob` - Destabilizing Field | `Module_RocketSilo_Mob` - 'Tempest' Launcher | `Module_PredatorTrap_Mob_T3` - Remote minelayer | `Module_MassRemotePulsar_Mob` | Static Shield |

### 3.2 Experimental destroyer and its escort

| Slot | Experimental destroyer (`Ship_OW_Boss_PirateEvent`) | Enclave Destroyer (`Ship_OW_Elite_PirateEvent_Guard`) |
|---|---|---|
| Primary weapon | `Weapon_Destroyer_BossPlasmaHeavy` - Boson Cannon (subtype `ElectricPotentialInductor`) | `Weapon_PirateEvent_ChargedBlast` |
| Active 1 | `Module_PirateBoss_EntityRay` - Enclave Emitter / "Laser" (see below) | `Module_PirateEvent_shield` |
| Active 2 | `Module_PirateBoss_ReverseDash` - Jump drive | `Module_PirateEvent_Dash` |
| Active 3 | `Module_PirateBoss_RocketSilo` - 'Tempest' Launcher | `Module_RepairDrones_Mob_l` |
| Active 4 | `Module_TurretPlasma_Mob` - Plasma Turret | `Module_Pulsar_PirateEvent` |
| Secondary weapon | `Module_SectorShield_PVE` | - |
| Missile | `DestrMunition_HealBot_Boss` - Heavy Repair Drone | - |

The escort's modules were not resolved to display names.

### 3.3 Uncertain names

* `Module_TeleportToKill_Mob` and `Module_MassRemotePulsar_Mob` set
  `uiName = "AlienGun"` ("Unidentified Weapon"; source comment
  "Неопознанное орудие", translated: "unidentified weapon") and
  `item_subtype = ai.DONT_INHERIT`. They inherit `Module_CoverShieldProto_Mob`;
  what they actually do is not resolved (the IDs suggest a teleport-to-target
  ability and a mass pulsar) ⚠ unverified.
* `Module_PirateBoss_EntityRay` assigns `uiName` twice in one table
  constructor: `PirateBoss_EntityRay_name` ("Laser") and later
  `EntityRayHolder_name` ("Enclave Emitter", commented as being for the
  death log). In a Lua table constructor the later assignment wins, so
  "Enclave Emitter" is the effective name *(inferred)*.
* `Module_SectorShield_PVE` resolves through `Module_SectorShield` ->
  `Module_SectorShield_Base` to the subtype string
  `itemSubType_OverseerEntitySpawner` = "Destroyer", which is not a module
  name ⚠ unverified.
* The `Ship_Gen_Boss_*` parents have their own `uiName` keys
  (`Ship_Gen_Boss_<Race>_Destroyer`), which have no English string.

## 4. Facts that bear on flying a boss (Q49, open)

Collected for [Q49](../08-reverse-engineering/open-questions.md). None of
these settles the question; it needs a runtime test.

* **Store:** no `Ship_OW_Boss_*` or `Ship_Gen_Boss_*` entry exists in
  `cloud/data/store.xml`; the parents set `storeItemId=0`. Normal progression
  therefore offers none of them.
* **Customisation rules:** all seven bosses have `<Vessel>` entries in
  `cloud/data/vessel_custom_elements_rules.xml`. That file lists all 2 398
  ship definitions including bots, so an entry says nothing about whether a
  hull can be flown.
* **Shared hull with player destroyers:** the six basic bosses inherit model,
  `slot_bones` and the other hull fields of the player destroyers
  `Ship_Race{1,3,2}_H_T4` and override only stats, modules and AI fields.
  Q49's known failure case (`Ship_OW_Boss_Manta`, does not move) has its own
  model, so these six differ from it in that respect.
* **The Experimental destroyer** has its own model, its own
  `capacitor_grades` / `engine_grades` tables
  (`designers.capacitor_huge_craftuniq_boss`,
  `designers.engine_huge_craftuniq_boss`), resistances of 400 on every
  damage type, and engine effects under a `craftuniq.boss` entry in
  `def/def_extension.lua`. Its icon fields (`default_icon`, `hangarIco`,
  `hangarIcoSmall`) are `icon_error`.
* **AI-only fields** (`ship4bot`, `avtomat`, `AiSettings`): per Q49 they are
  read only by AI and designer scripts, not by `DedicatedServer.exe`.
* **Modules:** most fitted items are `*_Mob` / `*_PvE` AI variants; some
  call boss-only spells (for example `Spell_PirateBossEntityRayPrepare`,
  `BossEvent_OnDeathEnemy` on the Enclave Emitter). Whether these work on a
  player-controlled ship is not known.
* **Community grant recipe (S17, ⚠):** a vessel record inserted into
  `accounts.vessels` with `defName: Ship_OW_Boss_PirateEvent1` and special
  module `Module_PhaseBuff_Prec`. That `defName` does not occur in the shipped
  data (only `Ship_OW_Boss_PirateEvent`); the hull has no store entry, so the
  admin task `give` (`item`) cannot grant it. Test proposal
  [Q53](../08-reverse-engineering/open-questions.md).

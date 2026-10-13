r"""Find references to definitions that do not exist (dangling references).

A reference to a name nobody defines - a loot table in the loot rules, a
module in a ship's `default_modules`, a spell, a bundle in an account aura -
fails silently at run time: an empty arena search, a ship without a weapon, a
quest reward that never arrives. This read-only checker indexes every name the
game data defines and reports references that resolve to nothing.

    .venv\Scripts\python.exe -X utf8 -I tools\ref_lint.py [--depot DIR]
    .venv\Scripts\python.exe -X utf8 -I tools\ref_lint.py --depot "<edited copy>" --reference "<untouched copy>"
    .venv\Scripts\python.exe -X utf8 -I tools\ref_lint.py --depot DIR --key inherit --key spell --limit 0

The default depot is `sc-server-files/star conflict`; pass the `star
conflict` folder of your install. With `--reference`, only findings that the
untouched copy does not have are printed - the ones your edits introduced.

Defined names are collected from:
  * data/gamedata/**/*.lua and sys_data/gamedata/**/*.lua: `<Registry>.<name> =` and `<Registry>["<name>"] =`
    for every capitalised registry table (Def, Spell, LootTable, AccountAura,
    DefItemPrice, ModulePresets, VesselTree, Materials, AiPreset, ...)
  * cloud/data/store.xml `<Item defName=...>` (generated from the Lua,
    including names that Lua builds in loops)
  * identifiers compiled into DedicatedServer.exe and win64/game.exe (engine
    built-ins such as `TriggerHurt` or `AuraHolderEntity`); `--no-exe` skips
    this step
References checked:
  * the same Lua files: `<key> = "Name"` for the reference keys listed in
    REF_KEYS (keys whose values resolve to a definition in the shipped data
    almost always); comments are ignored
  * cloud/data/default_platform_config.lua: loot-rule tables (`lt = "Name"`
    -> LootTable) and the same reference keys
  * cloud/data/*.xml: `defName=` and `resource=` attributes

Limits: names created at run time (loops that build names from counters,
string concatenation) are not seen, so a reference to such a name is
reported; check those by hand. Disabled entries (`disabled = true`) are still
reported - their impact is lower. Exit status 1 when findings are printed.
Output contains no secrets.
"""
import argparse
import collections
import os
import re
import sys

REGISTRY_ASSIGN = re.compile(
    r'^\s*([A-Z][A-Za-z]+)\s*(?:\.\s*([A-Za-z_]\w*)|\[\s*["\']([^"\']+)["\']\s*\])\s*=')
KEY_VALUE = re.compile(
    r'(?:\b|\.)([A-Za-z_]\w*)\s*(?:\[[^\]]*\])?\s*=\s*"([A-Za-z_][A-Za-z0-9_]*)"')
XML_ATTR = re.compile(r'\b(defName|resource)="([A-Za-z_][A-Za-z0-9_]*)"')
STORE_DEFNAME = re.compile(r'<Item\b[^>]*?\bdefName="([^"]+)"')
EXE_IDENT = re.compile(rb'[A-Za-z_][A-Za-z0-9_]{3,63}')

# Keys whose string values name a definition (>= 85 % resolve in the shipped
# build 1.99.0.167293). Keys holding texture, model, engine-class or UI string
# names (class, tex, hangarIco, uiName, decal, ...) are deliberately absent.
REF_KEYS = {
    "inherit", "default_modules", "modules", "spell", "required_ship", "item",
    "def", "material", "projectile", "upgrade_cost_negator", "craft_result",
    "ship_def", "additional_spell", "death_blast_wave", "explosion_blast_wave",
    "munition", "spell_on_equip", "default_rocket_munition", "source_zone",
    "resource", "death_wreck", "parent_prototype", "base_preset", "avtomat",
    "children", "AiSettings", "required_account_aura", "target_spell",
    "spell_on_hit", "spell_on_cancel", "child", "aura_holder_def",
    "deactivate_spell", "situation_def", "required_item", "bundle", "effect",
    "discounted_def", "spell_on_max_speed_plus", "spell_on_launch",
    "loot_table", "reward_account_aura", "depends_on", "behavior",
    "spell_on_special_activate", "spawnpoint", "spell_on_death_someone",
    "activate_entity", "shield_disabled_spell", "emergency_barrier_spell",
    "drop_item", "testdrive_preset", "spell_on_crit", "spell_on_no_firing",
    "scrap_def", "moduleBaseDefName", "blueprint", "loot_item", "focus_spell",
    "cargoship", "spell_approach", "start_sentence", "spell_on_max_speed_minus",
    "death_entity", "spell_on_max_health_minus", "entityDef", "reward_def",
    "nebula", "sTargetDef", "defName", "explosion", "spell_on_death_active",
    "suicide_blastwave_def", "aura", "spell0", "spell1", "pointDef", "lootDef",
    "account_aura", "drone_def", "big_shield_def", "shell_def",
}
PLATFORM_KEYS = {"lt": "loot table"}


def lua_files(base):
    for root, _dirs, files in os.walk(base):
        for fn in sorted(files):
            if fn.endswith(".lua"):
                yield os.path.join(root, fn)


def gamedata_files(depot):
    # the client and battle server search data/ and sys_data/ (datasources.txt);
    # sys_data/gamedata holds base definitions (logic, base_defs, properties)
    for sub in (("data", "gamedata"), ("sys_data", "gamedata")):
        yield from lua_files(os.path.join(depot, *sub))


def strip_comment(line):
    # good enough for data files: no "--" inside the string values we read
    return line.split("--", 1)[0]


def index_names(depot, use_exe):
    names = {}
    for p in gamedata_files(depot):
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = REGISTRY_ASSIGN.match(line)
                if m:
                    names.setdefault(m.group(2) or m.group(3), set()).add(m.group(1))
    # store.xml is generated from the Lua definitions, including names that
    # Lua builds in loops (Avatar_<n>, Motto_<n>, bundles): count its items
    store = os.path.join(depot, "cloud", "data", "store.xml")
    if os.path.exists(store):
        with open(store, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                for n in STORE_DEFNAME.findall(line):
                    names.setdefault(n, set()).add("store.xml")
    if use_exe:
        for rel in ("cloud/DedicatedServer.exe", "win64/game.exe"):
            p = os.path.join(depot, *rel.split("/"))
            if os.path.exists(p):
                with open(p, "rb") as fh:
                    for b in set(EXE_IDENT.findall(fh.read())):
                        names.setdefault(b.decode("ascii"), set()).add("exe")
    return names


def scan(depot, names, keys):
    """Return list of (key, name, where) for unresolved references."""
    out = []
    for p in gamedata_files(depot):
        rel = os.path.relpath(p, depot).replace(os.sep, "/")
        with open(p, encoding="utf-8", errors="replace") as fh:
            for ln, line in enumerate(fh, 1):
                for k, v in KEY_VALUE.findall(strip_comment(line)):
                    # "_first_1"-style values are beacon ids inside level
                    # scripts (shared/adventures.lua), not definition names
                    if k in keys and v not in names and not v.startswith("_"):
                        out.append((k, v, f"{rel}:{ln}"))
    plat = os.path.join(depot, "cloud", "data", "default_platform_config.lua")
    if os.path.exists(plat):
        with open(plat, encoding="utf-8", errors="replace") as fh:
            for ln, line in enumerate(fh, 1):
                for k, v in KEY_VALUE.findall(strip_comment(line)):
                    if (k in PLATFORM_KEYS or k in keys) and v not in names:
                        out.append((k, v, f"cloud/data/default_platform_config.lua:{ln}"))
    xml_dir = os.path.join(depot, "cloud", "data")
    if os.path.isdir(xml_dir):
        for fn in sorted(os.listdir(xml_dir)):
            if not fn.endswith(".xml"):
                continue
            with open(os.path.join(xml_dir, fn), encoding="utf-8", errors="replace") as fh:
                for ln, line in enumerate(fh, 1):
                    for k, v in XML_ATTR.findall(line):
                        if v not in names:
                            out.append((f"xml:{k}", v, f"cloud/data/{fn}:{ln}"))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--depot", default=os.path.join("sc-server-files", "star conflict"))
    ap.add_argument("--reference", help="untouched copy: print only findings it does not have")
    ap.add_argument("--key", action="append", help="check only these keys (repeatable)")
    ap.add_argument("--no-exe", action="store_true", help="do not read engine names from the executables")
    ap.add_argument("--limit", type=int, default=8, help="lines shown per name (0 = all)")
    a = ap.parse_args()
    if not os.path.isdir(os.path.join(a.depot, "data", "gamedata")):
        sys.exit(f"not a game folder (no data/gamedata): {a.depot}")
    keys = set(a.key) if a.key else REF_KEYS

    names = index_names(a.depot, not a.no_exe)
    found = scan(a.depot, names, keys)
    if a.reference:
        ref_names = index_names(a.reference, not a.no_exe)
        known = {(k, v) for k, v, _ in scan(a.reference, ref_names, keys)}
        found = [f for f in found if (f[0], f[1]) not in known]

    by_name = collections.OrderedDict()
    for k, v, where in sorted(found, key=lambda f: (f[0], f[1], f[2])):
        by_name.setdefault((k, v), []).append(where)
    print(f"defined names: {len(names)}; unresolved references: {len(found)} "
          f"({len(by_name)} distinct key/name pairs)"
          + (" not present in the reference copy" if a.reference else ""))
    last = None
    for (k, v), wheres in by_name.items():
        if k != last:
            print(f"\n[{k}]")
            last = k
        shown = wheres if a.limit == 0 else wheres[:a.limit]
        more = "" if len(shown) == len(wheres) else f" (+{len(wheres) - len(shown)} more)"
        print(f"  {v}  x{len(wheres)}: {', '.join(shown)}{more}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())

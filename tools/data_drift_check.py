r"""Compare a node's data files with a reference depot and flag drift (read-only).

    .venv\Scripts\python.exe -X utf8 -I tools\data_drift_check.py <reference-root> <node-root> [--out report.md] [--scope DIR ...]

Both roots are "star conflict" folders (depot layout: `cloud/data`,
`data/gamedata`). Default scope: `cloud/data` and `data/gamedata`; add more
with `--scope data/ui` etc. Nothing is modified; the report contains paths,
sizes and hash prefixes only, never file contents.

Checks:

1. **File diff**: changed / added / missing files (SHA-256).
2. **Generated XML vs Lua sources**: `DedicatedServer -prepareSharedData`
   writes `cloud/data` XML from the Lua game data (config-pipeline-and-
   limiters.md). The generated set is the 29 files a stock run rewrote in lab
   verification (2026-10-13, all byte-identical to the shipped files). Findings:
   - Lua changed but no generated XML changed -> **stale**: run
     `prepare_shared` (needs MongoDB) or the server keeps the old values;
   - a generated XML changed while its paired Lua source did not ->
     **hand-edited generated file**: the next `prepare_shared` overwrites it;
   - pair present in both but the XML is older than its Lua (mtime) -> stale.
   Pairs are by base name (`battle_pass.lua` -> `battle_pass.xml`) plus the
   verified pairs `reputation.lua` -> `aux_limits.xml`, `quests_base.lua` ->
   `quests.xml` and `data/gamedata/def/**` -> `store.xml`.
3. **Positional store ids**: definitions that take their store id from a
   load-order counter (`<Family>_GetNextStoreItemId()`, e.g. `Bundles_`,
   `Avatars_`, `Mottos_`, `Drugs_`) must keep their order; inserting or
   removing one shifts the ids of every later definition. The ordered list of such definitions is compared per file and per
   family (files in sorted path order - the engine's real load order may
   differ, so family-level results are indicative).

Exit code 0 = no differences, 1 = differences found, 2 = usage error.
"""
import argparse
import hashlib
import os
import re
import sys

DEFAULT_SCOPE = ["cloud/data", "data/gamedata"]

# cloud/data XML files written by -prepareSharedData (observed 2026-10-13,
# build 1.99.0.167293). special_values.xml and regions.xml are named in
# DedicatedServer.exe but were not rewritten.
GENERATED_XML = {
    "account_auras", "achievements", "atlas_special_values", "autogen",
    "autogen_special_values", "aux_limits", "battle_pass",
    "bot_preset_exclusion_lists", "clan_emblems", "clan_quests", "clan_ship",
    "faction_rep", "karma", "league_equipment_lists", "medals", "offers",
    "quests", "ship_quests", "skills",
    "starter_pack", "store", "titles", "tournaments", "universe",
    "vessel_custom_elements", "vessel_custom_elements_rules",
    "vessel_presets", "war", "zones",
}
# Verified pairs beyond the same-base-name rule (Lua path prefix -> xml base).
EXTRA_PAIRS = [
    ("data/gamedata/shared/reputation.lua", "aux_limits"),
    ("data/gamedata/shared/quests_base.lua", "quests"),
    ("data/gamedata/def/", "store"),
]

DEF_RE = re.compile(r"^\s*Def\.([A-Za-z0-9_]+)\s*=")
DEFIDX_RE = re.compile(r"^\s*Def\s*\[\s*\"([A-Za-z0-9_]*)\"\s*\.\.\s*([A-Za-z_]\w*)\s*\]\s*=")
FOR_RE = re.compile(r"^\s*for\s+([A-Za-z_]\w*)\s*=\s*(-?\d+)\s*,\s*(-?\d+)\s*do(?![A-Za-z0-9_])")
ALIAS_RE = re.compile(r"^\s*(?:local\s+)?([A-Za-z_]\w*)\s*=\s*(?:(-?\d+)\s*\+\s*([A-Za-z_]\w*)|([A-Za-z_]\w*)\s*\+\s*(-?\d+))\s*;?\s*$")
CTR_RE = re.compile(r"\b([A-Za-z0-9]+)_GetNextStoreItemId\s*\(\s*\)")


def walk(root, scope):
    out = {}
    for sub in scope:
        base = os.path.join(root, sub)
        if not os.path.isdir(base):
            continue
        for dp, _, files in os.walk(base):
            for f in files:
                full = os.path.join(dp, f)
                rel = os.path.relpath(full, root).replace(os.sep, "/")
                out[rel] = full
    return out


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_lua_comments(text):
    """Remove --[[ ]] / --[==[ ]==] blocks and -- line comments (string literals are not parsed)."""
    text = re.sub(r"--\[(=*)\[.*?\]\1\]", "", text, flags=re.S)
    return re.sub(r"--[^\n]*", "", text)


def counter_defs(path):
    """Ordered [(family, def name)] for defs whose block calls <Family>_GetNextStoreItemId().

    Handles `Def.Name = {...}` and numeric loops of the form
    `for i = a, b do Def[ "Prefix" .. i ] = { ... _GetNextStoreItemId() ... }`
    (expanded to Prefix<a> .. Prefix<b>), also with an offset variable
    (`nn = 39 + i`). Other generated defs are not seen.
    """
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    out, cur, loop, alias = [], None, None, {}
    for line in strip_lua_comments(text).splitlines():
        f = FOR_RE.match(line)
        if f:
            loop = (f.group(1), int(f.group(2)), int(f.group(3)))
            alias = {loop[0]: 0}
        if loop:
            al = ALIAS_RE.match(line)
            if al:
                var, k1, v1, v2, k2 = al.groups()
                src, k = (v1, int(k1)) if v1 else (v2, int(k2))
                if src in alias:
                    alias[var] = alias[src] + k
        m = DEF_RE.match(line)
        if m:
            cur = [m.group(1)]
        mi = DEFIDX_RE.match(line)
        if mi:
            if loop and mi.group(2) in alias:
                off = alias[mi.group(2)]
                cur = [f"{mi.group(1)}{i + off}" for i in range(loop[1], loop[2] + 1)]
            else:
                cur = [f"{mi.group(1)}<{mi.group(2)}>"]
        c = CTR_RE.search(line)
        if c and cur:
            out.extend((c.group(1), n) for n in cur)
            cur = None
    return out


def first_divergence(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return min(len(a), len(b)) if len(a) != len(b) else None


def xml_base_for(rel):
    """Generated XML base names that depend on a Lua file (pairing rules)."""
    bases = set()
    if rel.endswith(".lua"):
        b = os.path.splitext(os.path.basename(rel))[0]
        if b in GENERATED_XML:
            bases.add(b)
        for prefix, xml in EXTRA_PAIRS:
            if rel == prefix or (prefix.endswith("/") and rel.startswith(prefix)):
                bases.add(xml)
    return bases


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("reference")
    ap.add_argument("node")
    ap.add_argument("--out")
    ap.add_argument("--scope", nargs="*", default=None)
    a = ap.parse_args(argv)
    scope = DEFAULT_SCOPE + (a.scope or [])
    for r in (a.reference, a.node):
        if not os.path.isdir(os.path.join(r, "cloud", "data")):
            print(f"not a depot root (no cloud/data): {r}", file=sys.stderr)
            return 2

    ref, node = walk(a.reference, scope), walk(a.node, scope)
    changed, added, missing = [], sorted(set(node) - set(ref)), sorted(set(ref) - set(node))
    for rel in sorted(set(ref) & set(node)):
        if os.path.getsize(ref[rel]) != os.path.getsize(node[rel]) or sha(ref[rel]) != sha(node[rel]):
            changed.append(rel)
    touched = set(changed) | set(added) | set(missing)

    # 2. generated XML vs Lua
    findings = []
    gen_touched = {os.path.splitext(os.path.basename(r))[0] for r in touched
                   if r.startswith("cloud/data/") and r.endswith(".xml")}
    lua_touched = sorted(r for r in touched if r.endswith(".lua") and r.startswith("data/"))
    dep = {}
    for r in lua_touched:
        for x in xml_base_for(r):
            dep.setdefault(x, []).append(r)
    for x, srcs in sorted(dep.items()):
        if x not in gen_touched:
            findings.append(("stale", f"`cloud/data/{x}.xml` unchanged although its source(s) changed: "
                             + ", ".join(f"`{s}`" for s in srcs)
                             + " -> run `prepare_shared` (needs MongoDB) and restart"))
    if lua_touched and not dep:
        findings.append(("info", "changed Lua files have no known generated-XML pair; if they are server-side "
                         "game data, check whether `prepare_shared` is needed: "
                         + ", ".join(f"`{s}`" for s in lua_touched)))
    for x in sorted(gen_touched):
        if x in GENERATED_XML and x not in dep:
            findings.append(("hand-edit", f"`cloud/data/{x}.xml` differs from the reference but none of its "
                             "paired Lua sources changed - a direct edit of a generated file is overwritten "
                             "by the next `prepare_shared`"))
    for rel in sorted(node):
        if rel.endswith(".lua"):
            for x in xml_base_for(rel):
                xr = f"cloud/data/{x}.xml"
                if xr in node and os.path.getmtime(node[xr]) + 1 < os.path.getmtime(node[rel]) and rel in touched:
                    findings.append(("stale", f"`{xr}` is older than `{rel}` on the node (mtime)"))

    # 3. positional store ids
    pos = []
    fam_ref, fam_node = {}, {}
    for rel in sorted(set(ref) | set(node)):
        if not rel.endswith(".lua"):
            continue
        r = counter_defs(ref[rel]) if rel in ref else []
        n = counter_defs(node[rel]) if rel in node else []
        for fam, name in r:
            fam_ref.setdefault(fam, []).append(name)
        for fam, name in n:
            fam_node.setdefault(fam, []).append(name)
        if (r or n) and r != n:
            i = first_divergence(r, n)
            rn, nn = {x[1] for x in r}, {x[1] for x in n}
            pos.append(f"`{rel}`: {len(r)} -> {len(n)} counter-based defs; first difference at position {i}"
                       f" (ref `{r[i][1] if i is not None and i < len(r) else '-'}`, node "
                       f"`{n[i][1] if i is not None and i < len(n) else '-'}`); "
                       f"inserted {len(nn - rn)}, removed {len(rn - nn)}")
    fam_lines = []
    for fam in sorted(set(fam_ref) | set(fam_node)):
        r, n = fam_ref.get(fam, []), fam_node.get(fam, [])
        i = first_divergence(r, n)
        state = "same order" if i is None else f"**differs from position {i}** - every later id shifts"
        fam_lines.append(f"| `{fam}_` | {len(r)} | {len(n)} | {state} |")

    lines = ["# Data drift report", "",
             f"Reference: `{os.path.basename(os.path.abspath(a.reference))}` - node: "
             f"`{os.path.basename(os.path.abspath(a.node))}` - scope: " + ", ".join(f"`{s}`" for s in scope), "",
             f"Files: reference {len(ref)}, node {len(node)}; changed **{len(changed)}**, added **{len(added)}**, "
             f"missing **{len(missing)}**.", ""]
    for title, items in (("Changed", changed), ("Added on the node", added), ("Missing on the node", missing)):
        if items:
            lines.append(f"## {title}\n")
            for rel in items:
                p = node.get(rel) or ref.get(rel)
                lines.append(f"* `{rel}` ({os.path.getsize(p)} bytes)")
            lines.append("")
    lines.append("## Generated XML vs Lua sources\n")
    lines += [f"* **{k}**: {t}" for k, t in findings] or ["* no findings"]
    lines += ["", "## Positional store ids\n", "| Counter family | Reference defs | Node defs | Order |",
              "|---|---:|---:|---|"] + fam_lines + [""]
    lines += [f"* {p}" for p in pos] or ["* no per-file differences"]
    report = "\n".join(lines) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(report)
        print(f"report -> {a.out}")
    else:
        sys.stdout.write(report)
    return 1 if touched else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

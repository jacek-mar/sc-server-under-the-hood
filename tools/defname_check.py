r"""Check definition names (defNames) against the shipped depot.

Mistyped def names are the most common reason a community node refuses to
start after a store / quest / loot edit (community reports, see
docs/05-configuration/tuning-recipes.md). This read-only checker builds an index of every
name the depot defines and tells you whether yours exists, where it is
defined and what the closest known names are.

    .venv\Scripts\python.exe -X utf8 -I tools\defname_check.py [--depot DIR] NAME [NAME ...]
    .venv\Scripts\python.exe -X utf8 -I tools\defname_check.py [--depot DIR] --names-file names.txt
    .venv\Scripts\python.exe -X utf8 -I tools\defname_check.py [--depot DIR] --xml edited_store.xml
    .venv\Scripts\python.exe -X utf8 -I tools\defname_check.py [--depot DIR] --lua edited_quests.lua

The default depot is `sc-server-files/star conflict`; pass
`--depot <game>/star conflict` for your own install. Sources
indexed (name -> where):
  * cloud/data/store.xml: `defName="..."` attributes (type from the Item row)
    and the element names used inside `<Resources>` / `<Ingr resource=...>`
  * data/gamedata/def/**/*.lua and data/gamedata/shared/*.lua: `Def.<name> =`,
    `Def["<name>"] =`, `DefItemPrice.<name>`, `AiPreset.<name>`

`--xml` extracts candidate names from the attributes defName / def /
resource / preset / nextShip / discounted_def / requiredShip and from
`<Ingr resource=>`; `--lua` looks at `key = "Name"` pairs for the keys def,
defName, resource, item, reward, preset and at `Def.Name` references.
Anything unknown is printed with up to three near matches.
Exit status 1 when unknown names were found. Output contains no secrets.
"""
import argparse
import difflib
import os
import re
import sys

DEF_ASSIGN = re.compile(r'^\s*(?:Def|DefItemPrice|AiPreset)\s*(?:\.\s*([A-Za-z_][A-Za-z0-9_]*)|\[\s*["\']([^"\']+)["\']\s*\])\s*=')
DEF_REF = re.compile(r'\b(?:Def|DefItemPrice)\.([A-Za-z_][A-Za-z0-9_]*)')
XML_NAME_ATTRS = ("defName", "def", "resource", "preset", "nextShip",
                  "discounted_def", "requiredShip", "storeDefName")
XML_ATTR = re.compile(r'\b(' + "|".join(XML_NAME_ATTRS) + r')="([^"]*)"')
LUA_KV = re.compile(r'\b(def|defName|resource|item|reward|preset)\s*=\s*"([A-Za-z_][A-Za-z0-9_]*)"')
STORE_ITEM = re.compile(r'<Item\b[^>]*?\bid="(\d+)"[^>]*?\btype="(\d+)"[^>]*?\bdefName="([^"]+)"')
STORE_DEFNAME = re.compile(r'\bdefName="([^"]+)"')
ELEM_IN_RESOURCES = re.compile(r'<([A-Za-z_][A-Za-z0-9_]*)\s+amount="')


def build_index(depot):
    idx = {}  # name -> list of "where"
    store = os.path.join(depot, "cloud", "data", "store.xml")
    if os.path.exists(store):
        with open(store, encoding="utf-8", errors="replace") as fh:
            for ln, line in enumerate(fh, 1):
                m = STORE_ITEM.search(line)
                if m:
                    idx.setdefault(m.group(3), []).append(
                        f"store.xml:{ln} Item id={m.group(1)} type={m.group(2)}")
                    continue
                m = STORE_DEFNAME.search(line)
                if m:
                    idx.setdefault(m.group(1), []).append(f"store.xml:{ln} defName")
                m = ELEM_IN_RESOURCES.search(line)
                if m:
                    idx.setdefault(m.group(1), []).append(f"store.xml:{ln} resource element")
    for sub in ("data/gamedata/def", "data/gamedata/shared"):
        base = os.path.join(depot, *sub.split("/"))
        for root, _dirs, files in os.walk(base):
            for fn in files:
                if not fn.endswith(".lua"):
                    continue
                p = os.path.join(root, fn)
                rel = os.path.relpath(p, depot).replace(os.sep, "/")
                with open(p, encoding="utf-8", errors="replace") as fh:
                    for ln, line in enumerate(fh, 1):
                        m = DEF_ASSIGN.match(line)
                        if m:
                            name = m.group(1) or m.group(2)
                            lst = idx.setdefault(name, [])
                            if len(lst) < 6:
                                lst.append(f"{rel}:{ln}")
    return idx


def report(names, idx, source):
    known = list(idx)
    unknown = []
    for n in names:
        if n in idx:
            print(f"  ok       {n}  <- {idx[n][0]}" + (f" (+{len(idx[n]) - 1})" if len(idx[n]) > 1 else ""))
        else:
            near = difflib.get_close_matches(n, known, n=3, cutoff=0.78)
            unknown.append(n)
            print(f"  UNKNOWN  {n}" + (f"   did you mean: {', '.join(near)}" if near else ""))
    print(f"{source}: {len(names)} name(s), {len(unknown)} unknown")
    return unknown


def extract_xml(path):
    out = []
    seen = set()
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            for m in XML_ATTR.finditer(line):
                v = m.group(2).strip()
                for part in re.split(r"[;,\s]+", v):
                    if part and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", part) and part not in seen:
                        seen.add(part)
                        out.append(part)
            for m in ELEM_IN_RESOURCES.finditer(line):
                if m.group(1) not in seen:
                    seen.add(m.group(1))
                    out.append(m.group(1))
    return out


def extract_lua(path):
    out, seen = [], set()
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.lstrip().startswith("--"):
                continue
            for m in LUA_KV.finditer(line):
                if m.group(2) not in seen:
                    seen.add(m.group(2))
                    out.append(m.group(2))
            for m in DEF_REF.finditer(line):
                if m.group(1) not in seen:
                    seen.add(m.group(1))
                    out.append(m.group(1))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("names", nargs="*")
    ap.add_argument("--depot", default=os.path.join("sc-server-files", "star conflict"))
    ap.add_argument("--names-file")
    ap.add_argument("--xml")
    ap.add_argument("--lua")
    a = ap.parse_args()
    idx = build_index(a.depot)
    print(f"index: {len(idx)} defined names from {a.depot}")
    bad = []
    if a.names:
        bad += report(a.names, idx, "command line")
    if a.names_file:
        with open(a.names_file, encoding="utf-8") as fh:
            names = [l.strip() for l in fh if l.strip() and not l.startswith("#")]
        bad += report(names, idx, a.names_file)
    if a.xml:
        bad += report(extract_xml(a.xml), idx, a.xml)
    if a.lua:
        bad += report(extract_lua(a.lua), idx, a.lua)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

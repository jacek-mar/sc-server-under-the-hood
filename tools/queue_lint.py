r"""Static linter for the matchmaker queue block of default_platform_config.lua.

Community reports (docs/05-configuration/tuning-recipes.md) say a
mistyped queue block makes matches "never start" or the config is silently
ignored. This tool parses the Lua text (no Lua interpreter needed) and checks
the parts that operators edit most often.

    .venv\Scripts\python.exe -X utf8 -I tools\queue_lint.py [config.lua] [--depot DIR] [--no-coverage]

Default config: <depot>/cloud/data/default_platform_config.lua; default
depot: `sc-server-files/star conflict` (pass `--depot <game>/star conflict`
for your own install; the shipped files are
only read). Checks:

  E1 unbalanced braces / parentheses / unterminated string or long comment
  E2 `InstantiateQueueTemplate(...)` argument count (7 or 8) and non-numeric
     rank / value arguments
  E3 min > max for rank, squad rank or value; ranks outside 1..17; values
     outside 0..100
  E4 unknown queue-template variable in a call
  E5 unknown bot preset name in botPresetNames / botPresetByTier
     (source: data/gamedata/shared/ai_settings.lua incl. the generated
     Bots<T>_<sym> families)
  W1 level in a template's `levelsDesc` that is not in data/levels/active_maps.list
  W2 (level, mode) pair of `levelsDesc` that has no `Setting` row in
     cloud/data/aux_limits.xml LobbySettings
  W3 missing comma between two entries of a `levelsDesc` / `special` block
  I1 coverage: per (queue list, template) the mmRank x mmValue grid that no
     queue accepts (rank 1..17 x value 0..99) - explains "no match" for
     accounts whose rank/value falls into a gap
  I2 queues whose mmSquadRank range differs from their mmRank range (squad
     filter; shown with the coverage block)
  I3 a co-op (vs AI) template whose levelsDesc includes mode 11 (bomb the
     base) - bots are reported not to carry the bomb (shown with coverage)
  L1 loot rules (DedicatedServcerServices_SetLootRules): a ship rank 1..17
     without a row - ships of that rank silently get no loot search after
     battles
  L2 loot rules row syntax: each row needs common / rare / epic, each with
     lt = "<table>" and a numeric iter = {...} list; rank outside 1..17,
     duplicate rank, missing comma between rows (counts as an error)
  L3 loot rules summary: which ranks share which tables (shown with the
     coverage block). Whether the table names exist is checked by
     tools/ref_lint.py.

Exit status 1 when an E-class or L2 finding exists. The tool never executes the
config and never prints secrets.
"""
import argparse
import os
import re
import sys

RANK_MIN, RANK_MAX = 1, 17
VAL_MIN, VAL_MAX = 0, 99


def strip_lua(text, findings):
    """Return text with comments and string contents blanked, same length/lines."""
    out = []
    i, n, line = 0, len(text), 1
    while i < n:
        c = text[i]
        if text.startswith("--[[", i) or re.match(r"--\[=*\[", text[i:i + 8] or ""):
            m = re.match(r"--\[(=*)\[", text[i:i + 12])
            close = "]" + m.group(1) + "]"
            j = text.find(close, i)
            if j < 0:
                findings.append(("E1", line, "unterminated long comment"))
                j = n - len(close)
            seg = text[i:j + len(close)]
            out.append(re.sub(r"[^\n]", " ", seg))
            line += seg.count("\n")
            i = j + len(close)
        elif text.startswith("--", i):
            j = text.find("\n", i)
            j = n if j < 0 else j
            out.append(" " * (j - i))
            i = j
        elif c in "\"'":
            j = i + 1
            while j < n and text[j] != c and text[j] != "\n":
                j += 2 if text[j] == "\\" else 1
            if j >= n or text[j] != c:
                findings.append(("E1", line, f"unterminated string starting with {c}"))
                out.append(text[i:j])
                i = j
                continue
            out.append(c + text[i + 1:j] + c)  # keep content, handled by callers
            i = j + 1
        else:
            if c == "\n":
                line += 1
            out.append(c)
            i += 1
    return "".join(out)


def mask_strings(text):
    """Blank string contents (for bracket matching) but keep delimiters."""
    return re.sub(r'"[^"\n]*"|\'[^\'\n]*\'', lambda m: m.group(0)[0] + " " * (len(m.group(0)) - 2) + m.group(0)[-1], text)


def check_balance(masked, findings):
    stack = []
    pairs = {")": "(", "}": "{", "]": "["}
    line = 1
    for ch in masked:
        if ch == "\n":
            line += 1
        elif ch in "({[":
            stack.append((ch, line))
        elif ch in ")}]":
            if not stack or stack[-1][0] != pairs[ch]:
                findings.append(("E1", line, f"unmatched {ch!r}"))
                return
            stack.pop()
    for ch, ln in stack[-3:]:
        findings.append(("E1", ln, f"unclosed {ch!r}"))


def match_close(text, open_pos, o, c):
    depth = 0
    for i in range(open_pos, len(text)):
        if text[i] == o:
            depth += 1
        elif text[i] == c:
            depth -= 1
            if depth == 0:
                return i
    return -1


def split_args(s):
    args, depth, cur = [], 0, []
    for ch in s:
        if ch in "({[":
            depth += 1
        elif ch in ")}]":
            depth -= 1
        if ch == "," and depth == 0:
            args.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    tail = "".join(cur).strip()
    if tail:
        args.append(tail)
    return args


def lineno(text, pos):
    return text.count("\n", 0, pos) + 1


def parse_num(s):
    s = s.strip()
    try:
        return int(s, 0)
    except ValueError:
        return None


def preset_names(depot):
    names = set()
    p = os.path.join(depot, "data", "gamedata", "shared", "ai_settings.lua")
    if os.path.exists(p):
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = re.match(r'\s*AiPreset\s*(?:\.\s*([A-Za-z_][A-Za-z0-9_]*)|\[\s*"([^"]+)"\s*\])\s*=', line)
                if m:
                    names.add(m.group(1) or m.group(2))
    # generated families (see the loops at the end of ai_settings.lua)
    for t in range(2, 6):
        for sym in "EFJSMLHPR":
            names.add(f"BotsT{t}_{sym}")
    for sym in "EFJSML":
        names.add(f"BotsT1_{sym}")
    names.add("BotsT35_R")
    return names


def active_levels(depot):
    p = os.path.join(depot, "data", "levels", "active_maps.list")
    out = set()
    if os.path.exists(p):
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip().replace("\\", "/")
                if line:
                    out.add(line.split("/")[-1])
    return out


def lobby_modes(depot):
    p = os.path.join(depot, "cloud", "data", "aux_limits.xml")
    out = set()
    if os.path.exists(p):
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = re.search(r'<Setting\s+levelName="([^"]+)"\s+gameMode="(\d+)"', line)
                if m:
                    out.add((m.group(1), int(m.group(2))))
    return out


LOOT_TIERS = ("common", "rare", "epic")


def check_loot_rules(clean, findings):
    """L1/L2 on the DedicatedServcerServices_SetLootRules table; return L3 summary rows.

    Each row `[rank] = { common = { lt = "Name", iter = { n, ... } }, rare = ..., epic = ... }`
    picks the after-battle loot tables for one ship rank. A rank without a row
    silently gets no loot search. Table names themselves are checked by ref_lint.py.
    """
    summary = []
    for m in re.finditer(r"DedicatedServcerServices_SetLootRules\s*\(", clean):
        if re.search(r"function\s*$", clean[max(0, m.start() - 20):m.start()]):
            continue  # a definition, not a call
        o = clean.find("{", m.end())
        if o < 0:
            continue
        c = match_close(clean, o, "{", "}")
        if c < 0:
            continue  # E1 already reports the imbalance
        body = clean[o + 1:c]
        base = o + 1
        rows = {}
        pos = 0
        for rm in re.finditer(r"\[\s*(\d+)\s*\]\s*=\s*\{", body):
            if rm.start() < pos:
                continue  # inside an earlier row
            rank = int(rm.group(1))
            ro = rm.end() - 1
            rc = match_close(body, ro, "{", "}")
            ln = lineno(clean, base + rm.start())
            if rc < 0:
                findings.append(("L2", ln, f"loot rules: row [{rank}] is not closed"))
                break
            pos = rc + 1
            row = body[ro + 1:rc]
            if not RANK_MIN <= rank <= RANK_MAX:
                findings.append(("L2", ln, f"loot rules: row [{rank}] outside ranks {RANK_MIN}..{RANK_MAX}"))
            if rank in rows:
                findings.append(("L2", ln, f"loot rules: rank {rank} defined twice (the later row wins)"))
            names = []
            for tier in LOOT_TIERS:
                tm = re.search(tier + r"\s*=\s*\{", row)
                if not tm:
                    findings.append(("L2", ln, f"loot rules: row [{rank}] has no '{tier}' entry"))
                    names.append("-")
                    continue
                to = tm.end() - 1
                tc = match_close(row, to, "{", "}")
                entry = row[to + 1:tc] if tc > 0 else ""
                lt = re.search(r'\blt\s*=\s*"([^"]*)"', entry)
                it = re.search(r"\biter\s*=\s*\{([^{}]*)\}", entry)
                if not lt or not lt.group(1):
                    findings.append(("L2", ln, f"loot rules: row [{rank}] '{tier}' has no lt = \"<table>\""))
                if not it:
                    findings.append(("L2", ln, f"loot rules: row [{rank}] '{tier}' has no iter = {{...}} list"))
                elif not all(re.fullmatch(r"\s*\d+\s*", x) for x in it.group(1).split(",") if x.strip()):
                    findings.append(("L2", ln, f"loot rules: row [{rank}] '{tier}' iter holds a non-number"))
                names.append(lt.group(1) if lt else "-")
            rows[rank] = tuple(names)
            # a row must be followed by ',' or the end of the table
            nxt = body[rc + 1:].lstrip()
            if nxt and not nxt.startswith(","):
                findings.append(("L2", ln, f"loot rules: missing comma after row [{rank}]"))
        missing = [r for r in range(RANK_MIN, RANK_MAX + 1) if r not in rows]
        ln = lineno(clean, m.start())
        if missing:
            spans, s = [], None
            for r in missing:
                if s is None:
                    s = p = r
                elif r == p + 1:
                    p = r
                else:
                    spans.append(f"{s}-{p}" if s != p else str(s)); s = p = r
            spans.append(f"{s}-{p}" if s != p else str(s))
            findings.append(("L1", ln, f"loot rules: no row for rank(s) {','.join(spans)} - ships of "
                                       "these ranks get no loot search after battles"))
        # L3: consecutive ranks sharing the same (common, rare, epic) tables
        cur = None
        for r in sorted(rows):
            if cur and rows[r] == cur[2] and r == cur[1] + 1:
                cur = (cur[0], r, cur[2])
            else:
                if cur:
                    summary.append(cur)
                cur = (r, r, rows[r])
        if cur:
            summary.append(cur)
    return summary


TEMPLATE_DEF = re.compile(r"(?:local\s+)?([A-Za-z_][A-Za-z0-9_]*QueueTemplate)\s*=\s*\{")


def parse_templates(clean, findings, levels, modes):
    """Return list of (name, start_pos, info)."""
    templates = []
    for m in TEMPLATE_DEF.finditer(clean):
        o = m.end() - 1
        c = match_close(clean, o, "{", "}")
        if c < 0:
            continue
        body = clean[o:c + 1]
        info = {"line": lineno(clean, m.start())}
        ld = re.search(r"levelsDesc\s*=\s*\{", body)
        info["levels"] = {}
        if ld:
            lo = ld.end() - 1
            lc = match_close(body, lo, "{", "}")
            block = body[lo:lc + 1]
            for e in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{([^{}]*)\}", block):
                ms = [int(x) for x in re.findall(r"\d+", e.group(2))]
                info["levels"][e.group(1)] = ms
            # W3: an entry that closes with '}' and is followed by an identifier on the next non-blank text without ','
            for e in re.finditer(r"\}\s*\n\s*(?=[A-Za-z_][A-Za-z0-9_]*\s*=)", block):
                findings.append(("W3", lineno(clean, m.start()) + body[:lo + e.start()].count("\n"),
                                 f"{m.group(1)}: missing comma between levelsDesc entries"))
        q = re.search(r"mmRank\s*=\s*\{[^}]*\}", body)
        templates.append((m.group(1), m.start(), info))
        for lvl, ms in info["levels"].items():
            if levels and lvl not in levels:
                findings.append(("W1", info["line"], f"{m.group(1)}: level '{lvl}' is not in active_maps.list"))
            elif modes:
                for mode in ms:
                    if (lvl, mode) not in modes:
                        findings.append(("W2", info["line"],
                                         f"{m.group(1)}: ({lvl}, mode {mode}) has no LobbySettings row in aux_limits.xml"))
    return templates


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("config", nargs="?")
    ap.add_argument("--depot", default=os.path.join("sc-server-files", "star conflict"))
    ap.add_argument("--no-coverage", action="store_true")
    a = ap.parse_args()
    cfg = a.config or os.path.join(a.depot, "cloud", "data", "default_platform_config.lua")
    with open(cfg, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    findings = []
    clean = strip_lua(text, findings)
    check_balance(mask_strings(clean), findings)
    presets = preset_names(a.depot)
    levels = active_levels(a.depot)
    modes = lobby_modes(a.depot)
    templates = parse_templates(clean, findings, levels, modes)
    tnames = {t[0] for t in templates}
    loot_summary = check_loot_rules(clean, findings)

    calls = []
    for m in re.finditer(r"InstantiateQueueTemplate\s*\(", clean):
        o = m.end() - 1
        c = match_close(clean, o, "(", ")")
        if c < 0:
            continue
        before = clean[max(0, m.start() - 80):m.start()]
        lm = re.search(r"table\.insert\s*\(\s*([A-Za-z_][A-Za-z0-9_.]*)\s*,\s*$", before)
        if not lm:
            continue  # the function definition itself or another use
        args = split_args(clean[o + 1:c])
        ln = lineno(clean, m.start())
        if len(args) not in (7, 8):
            findings.append(("E2", ln, f"InstantiateQueueTemplate has {len(args)} argument(s), expected 7 or 8"))
            continue
        tpl = args[0]
        nums = [parse_num(x) for x in args[1:7]]
        if any(v is None for v in nums):
            bad = [args[1 + i] for i, v in enumerate(nums) if v is None]
            findings.append(("E2", ln, f"non-numeric rank/value argument(s): {bad}"))
            continue
        if tpl not in tnames:
            findings.append(("E4", ln, f"unknown queue template variable '{tpl}'"))
        rmin, rmax, smin, smax, vmin, vmax = nums
        if rmin > rmax:
            findings.append(("E3", ln, f"mmRank min {rmin} > max {rmax}"))
        if smin > smax:
            findings.append(("E3", ln, f"mmSquadRank min {smin} > max {smax}"))
        if vmin >= vmax:
            findings.append(("E3", ln, f"mmValue min {vmin} >= max {vmax} (max is exclusive)"))
        for nm, v in (("mmRank min", rmin), ("mmRank max", rmax), ("mmSquadRank min", smin), ("mmSquadRank max", smax)):
            if not RANK_MIN <= v <= RANK_MAX:
                findings.append(("E3", ln, f"{nm} {v} outside {RANK_MIN}..{RANK_MAX}"))
        if vmin < VAL_MIN or vmax > VAL_MAX + 1:
            findings.append(("E3", ln, f"mmValue {vmin}..{vmax} outside {VAL_MIN}..{VAL_MAX + 1}"))
        if len(args) == 8:
            for key in ("botPresetNames", "botPresetByTier"):
                km = re.search(key + r"\s*=\s*\{([^}]*)\}", args[7])
                if km:
                    for nm in re.findall(r'"([^"]+)"', km.group(1)):
                        if presets and nm not in presets:
                            findings.append(("E5", ln, f"unknown bot preset '{nm}' in {key}"))
        calls.append((lm.group(1), tpl, m.start(), rmin, rmax, vmin, vmax, ln, smin, smax))

    for sev, ln, msg in sorted(findings, key=lambda f: (f[1], f[0])):
        print(f"{sev} line {ln}: {msg}")

    if not a.no_coverage and calls:
        groups = {}
        squad_diff = {}
        for lst, tpl, pos, rmin, rmax, vmin, vmax, ln, smin, smax in calls:
            defpos = max([p for (n, p, _i) in templates if n == tpl and p < pos], default=-1)
            groups.setdefault((lst, tpl, defpos), []).append((rmin, rmax, vmin, vmax))
            if (smin, smax) != (rmin, rmax):
                squad_diff.setdefault((lst, tpl), []).append((ln, rmin, rmax, smin, smax))
        print()
        for (lst, tpl, defpos), rects in groups.items():
            grid = [[False] * (VAL_MAX + 1) for _ in range(RANK_MAX + 1)]
            for rmin, rmax, vmin, vmax in rects:
                for r in range(max(rmin, 1), min(rmax, RANK_MAX) + 1):
                    for v in range(max(vmin, 0), min(vmax, VAL_MAX + 1)):
                        grid[r][v] = True
            norank = [r for r in range(1, RANK_MAX + 1) if not any(grid[r])]
            allgaps = [v for v in range(VAL_MAX + 1) if not any(grid[r][v] for r in range(1, RANK_MAX + 1))]
            partial = {}
            for r in range(1, RANK_MAX + 1):
                if r in norank:
                    continue
                miss = [v for v in range(VAL_MAX + 1) if not grid[r][v] and v not in allgaps]
                if miss:
                    partial[r] = miss
            def rng(vs):
                out, s = [], None
                for i, v in enumerate(vs):
                    if s is None:
                        s = p = v
                    elif v == p + 1:
                        p = v
                    else:
                        out.append(f"{s}-{p}" if s != p else str(s)); s = p = v
                if s is not None:
                    out.append(f"{s}-{p}" if s != p else str(s))
                return ",".join(out)
            print(f"I1 {lst} / {tpl} (defined line {lineno(clean, defpos) if defpos >= 0 else '?'}): "
                  f"{len(rects)} queue(s)")
            if norank:
                print(f"   ranks with no queue: {rng(norank)}")
            if allgaps:
                print(f"   mmValue not served for any rank: {rng(allgaps)}")
            for r, miss in list(partial.items())[:6]:
                print(f"   rank {r}: uncovered mmValue {rng(miss)}")
    if not a.no_coverage and calls:
        if squad_diff:
            print()
        for (lst, tpl), rows in squad_diff.items():
            sample = ", ".join(f"line {ln}: rank {r0}-{r1} / squad {s0}-{s1}" for ln, r0, r1, s0, s1 in rows[:3])
            print(f"I2 {lst} / {tpl}: {len(rows)} queue(s) with mmSquadRank range != mmRank range ({sample}"
                  f"{', ...' if len(rows) > 3 else ''}) - squads are filtered by the squad range; players report "
                  "squads with bots only matched when both ranges are equal")
        for name, _pos, info in templates:
            if "coop" not in name.lower():
                continue
            bomb = sorted(lvl for lvl, ms in info["levels"].items() if 11 in ms)
            if bomb:
                print(f"I3 {name} (line {info['line']}): mode 11 (bomb the base / Detonation) on "
                      f"{len(bomb)} map(s) of a vs-AI template - bots are reported not to carry the bomb")
    if not a.no_coverage and loot_summary:
        print("\nL3 loot rules by rank (common / rare / epic table):")
        for r0, r1, names in loot_summary:
            print(f"   {f'{r0}-{r1}' if r0 != r1 else r0:>6}: {' / '.join(names)}")
    errs = [f for f in findings if f[0].startswith("E") or f[0] == "L2"]
    print(f"\n{len(errs)} error(s), {len(findings) - len(errs)} warning(s) in {cfg}")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()

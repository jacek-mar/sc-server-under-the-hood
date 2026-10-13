#!/usr/bin/env python3
r"""Generate the cvar reference (Markdown) from default_platform_config.lua.

Usage (inside the project venv only):
    .venv\Scripts\python.exe -X utf8 tools\extract_cvars.py <path/to/default_platform_config.lua> \
        docs/05-configuration/cvar-reference.md

It scans for `cvars.<name> = <value>` assignments, remembers which
`function ConfigureXxx()` they live in, and attaches the comment lines
immediately above the assignment (the original comments are Russian).
Only names, shipped defaults and the original comments are emitted - no other
content of the source file is reproduced.
"""
import json
import os
import re
import sys
from collections import OrderedDict, Counter

SERVICE = {
    "ConfigureShard": ("Shard", "ST_SHARD"),
    "ConfigureMatchmaker": ("MatchMaker", "ST_MATCHMAKER"),
    "ConfigureScriptsServer": ("ScriptsServer", "ST_SCRIPTS_SERVER"),
    "ConfigureDediServer": ("DedicatedServer", "ST_DEDICATED_SERVER"),
    "ConfigureDediServerFlags": ("DedicatedServer (per-queue flags)", "helper"),
    "ConfigureZoneInstance": ("ZoneInstance (open world)", "ST_ZONE_INSTANCE"),
    "ConfigureGRD": ("GameRewardDispencer", "ST_GAME_REWARD_DISPENCER"),
    "ConfigureLoadBalancer": ("LoadBalancer", "ST_LOAD_BALANCER"),
    "ConfigureChatServer": ("ChatServer", "ST_CHAT_SERVER"),
    "ConfigureUniverse": ("Universe", "ST_UNIVERSE"),
    "ConfigureQuestServer": ("QuestServer", "ST_QUEST_SERVER"),
    "ConfigureAchievementServer": ("AchievementServer", "ST_ACHIEVEMENT_SERVER"),
    "ConfigureLobbyServer": ("LobbyServer", "ST_LOBBY_SERVER"),
    "ConfigureLeaderboardServer": ("LeaderboardServer", "ST_LEADERBOARD_SERVER"),
    "ConfigureZoneCoordinator": ("ZoneCoordinator", "ST_ZONE_COORDINATOR"),
    "ConfigureTournament": ("Tournament", "ST_TOURNAMENT"),
    "ConfigureClanServer": ("ClanServer", "ST_CLAN_SERVER"),
    "ConfigureAdventureServer": ("AdventureServer", "ST_ADVENTURE_SERVER"),
    "ConfigureHub": ("Hub", "ST_HUB"),
}


def parse(path):
    func = None
    pending = []
    out = []
    for no, raw in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
        s = raw.strip()
        m = re.match(r"function\s+(\w+)", s)
        if m:
            func, pending = m.group(1), []
            continue
        if s.startswith("--") and not s.startswith("--[["):
            pending.append(s.lstrip("-").strip())
            continue
        m = re.match(r"cvars\.(\w+)\s*=\s*(.+?)\s*(--(.*))?$", s)
        if m:
            comment = " ".join(p for p in pending if p) or (m.group(4) or "").strip()
            out.append(dict(line=no, func=func, name=m.group(1),
                            value=m.group(2), comment=comment))
            pending = []
            continue
        if s:
            pending = []
    return out


def esc(t):
    return t.replace("|", "\\|").replace("`", "'")


def main(src, dst):
    rows = parse(src)
    tpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cvar_translations.json")
    tr = json.load(open(tpath, encoding="utf-8")) if os.path.exists(tpath) else {}
    names = {r["name"] for r in rows}
    missing = sorted(n for n in names if n not in tr)
    if missing:
        print("untranslated:", len(missing), ", ".join(missing))
    print("translated: %d / %d unique cvars" % (len(names) - len(missing), len(names)))
    groups = OrderedDict()
    for r in rows:
        groups.setdefault(r["func"], []).append(r)
    with open(dst, "w", encoding="utf-8", newline="\n") as o:
        o.write("# CVar reference (generated)\n\n")
        o.write("> **Generated** by `tools/extract_cvars.py` from the shipped "
                "`cloud/data/default_platform_config.lua`. Do not edit by hand; "
                "put corrections in `cvar-notes.md`.\n\n")
        o.write("* `Line` = line number in the shipped file (build 1.99.0.167293).\n")
        o.write("* *Default* = value assigned in the shipped file (may be a Lua local, see source).\n")
        o.write("* *Original comment* is Gaijin/Targem's own (Russian). "
                "English translations come from `tools/cvar_translations.json`.\n")
        o.write(f"* Total cvar assignments: **{len(rows)}** "
                f"(unique names: {len({r['name'] for r in rows})}).\n\n")
        c = Counter(r["func"] for r in rows)
        o.write("| Service | Function | cvars |\n|---|---|---:|\n")
        for f, n in c.most_common():
            svc = SERVICE.get(f, (f, ""))[0]
            o.write(f"| {svc} | `{f}` | {n} |\n")
        o.write("\n")
        for f, items in groups.items():
            svc, st = SERVICE.get(f, (f, ""))
            o.write(f"## {svc}\n\n")
            o.write(f"Function `{f}()`" + (f", dispatched when `service_type == \"{st}\"`." if st and st != "helper" else ".") + "\n\n")
            o.write("| Line | CVar | Default | English | Original comment (RU) |\n|---:|---|---|---|---|\n")
            for r in items:
                o.write(f"| {r['line']} | `{r['name']}` | `{esc(r['value'])}` | {esc(tr.get(r['name'], ''))} | {esc(r['comment'])} |\n")
            o.write("\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

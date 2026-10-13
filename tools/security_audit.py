"""Read-only security audit of a Star Conflict server node (depot copy).

Usage:
  python -X utf8 -I tools/security_audit.py <depot_root> [--listening] [--out report.md]

<depot_root> is the directory that contains `cloud/` (e.g. ".../star conflict").
Nothing is modified. With --listening the script also parses `netstat -ano`
(Windows) and reports which node ports are bound to all interfaces.

Secrets are never printed: password-like values are reported as
"set (N chars)" only. Exit code = number of HIGH findings (max 255).
"""
import argparse
import glob
import os
import re
import subprocess
import sys

HIGH, MED, LOW, INFO = "HIGH", "MED", "LOW", "INFO"
findings = []


def add(level, area, msg, fix=""):
    findings.append((level, area, msg, fix))


def read(path):
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None


def cfg_values(text, key):
    """Return values of `set <key> <value>` lines (cfg syntax), ignoring // comments."""
    out = []
    for ln in text.splitlines():
        ln = ln.split("//", 1)[0].strip()
        m = re.match(r'set\s+%s\s+(?:"([^"]*)"|(\S+))' % re.escape(key), ln)
        if m:
            out.append(m.group(1) if m.group(1) is not None else m.group(2))
    return out


def lua_cvar(text, name):
    vals = []
    for ln in text.splitlines():
        ln = ln.split("--", 1)[0]
        m = re.search(r'cvars\.%s\s*=\s*(.+?)\s*$' % re.escape(name), ln)
        if m:
            vals.append(m.group(1).strip())
    return vals


def audit_mongo(cloud):
    cfg = read(os.path.join(cloud, "mongodb", "config.cfg"))
    if cfg is None:
        add(INFO, "mongo", "mongodb/config.cfg not found - skipped")
        return
    live = [l.split("#")[0].strip() for l in cfg.splitlines()]
    bind = [l for l in live if l.startswith("bind_ip")]
    if not bind:
        add(HIGH, "mongo", "no bind_ip: MongoDB listens on all interfaces",
            "set `bind_ip = 127.0.0.1`")
    elif "127.0.0.1" not in bind[0]:
        add(HIGH, "mongo", f"bind_ip is not loopback ({bind[0]})",
            "bind to 127.0.0.1 or a private VLAN only")
    else:
        add(INFO, "mongo", "bind_ip is loopback")
    if not any(l.replace(" ", "").startswith("auth=true") or l.startswith("keyFile")
               for l in live):
        add(MED, "mongo", "authentication not enabled (MongoDB 2.6.12, services connect without credentials)",
            "keep loopback-only; if remote DB is needed use a private network/VPN")
    if not any(l.replace(" ", "").startswith("noscripting=true") for l in live):
        add(LOW, "mongo", "server-side JavaScript enabled (`noscripting` not set)",
            "test whether `noscripting = true` is compatible with the services")
    ver = re.search(r"mongo-r(\d+\.\d+\.\d+)", " ".join(os.listdir(os.path.join(cloud, "mongodb"))))
    if ver:
        add(MED, "mongo", f"bundled MongoDB {ver.group(1)} is end-of-life (2.6 branch, 2016)",
            "never expose; isolate; restrict file access to the data directory")


def audit_cfgs(cloud, profile):
    files = glob.glob(os.path.join(cloud, "data", "*.cfg"))
    if profile:
        files += glob.glob(os.path.join(profile, "**", "*_local.cfg"), recursive=True)
    for f in files:
        t = read(f) or ""
        for pw in cfg_values(t, "ssh_passwd"):
            if pw:
                level = HIGH if len(pw) < 12 else MED
                add(level, "ssh", f"{os.path.basename(f)}: ssh_passwd set ({len(pw)} chars) - "
                    "full Lua prompt inside the service, binds all interfaces",
                    "use >= 16 random chars, firewall the ssh_port, disable when not needed")
        for ak in cfg_values(t, "ssh_port"):
            add(INFO, "ssh", f"{os.path.basename(f)}: ssh_port {ak}")
    if not any(f for f in files if cfg_values(read(f) or "", "ssh_passwd")):
        add(INFO, "ssh", "no ssh_passwd configured: SSH console disabled (default)")


def audit_platform_lua(cloud):
    t = read(os.path.join(cloud, "data", "default_platform_config.lua"))
    if t is None:
        add(INFO, "lua", "default_platform_config.lua not found")
        return
    v = lua_cvar(t, "auth_allowInternalAutoCreate")
    if v and v[0] == "1":
        add(MED, "accounts", "auth_allowInternalAutoCreate = 1: any login string creates an account "
            "(account flooding, nickname squatting)",
            "set 0 on public servers and create accounts out-of-band, or front with a registration gate")
    v = lua_cvar(t, "store_allowAllItemsForBying")
    if v and v[0] != "0":
        add(LOW, "economy", "store_allowAllItemsForBying enabled (every item purchasable)")
    v = lua_cvar(t, "auth_infinitePremiumForRoles")
    if v:
        add(INFO, "accounts", f"admin roles with infinite premium: {v[0]} "
            "(admRole is a plain DB field: anyone with DB write access is admin)")


def audit_cloud_xml(cloud):
    t = read(os.path.join(cloud, "data", "cloud.xml"))
    if t is None:
        return
    for m in re.finditer(r'<Node\b[^>]*address="([^"]+)"', t):
        addr = m.group(1)
        if addr.startswith("127.") or addr.startswith("localhost"):
            add(INFO, "network", f"cloud.xml Node address {addr} (advertised address is loopback: "
                "remote clients cannot use it as-is)")
        else:
            add(INFO, "network", f"cloud.xml Node address {addr} (advertised to clients)")
    if re.search(r'dbg_disableLuaDataFormatChecking"\s+value="1"', t):
        add(LOW, "hardening", "CommonCVars: dbg_disableLuaDataFormatChecking = 1 "
            "(data-format validation of Lua data is off)")


def audit_libs(cloud):
    for name in ("libcrypto-1_1_tg.dll", "libssl-1_1_tg.dll", "libcurl.dll"):
        p = os.path.join(cloud, name)
        if not os.path.exists(p):
            continue
        b = open(p, "rb").read()
        m = re.search(rb"OpenSSL \d\.\d\.\d[a-z]?|libcurl/\d+\.\d+\.\d+", b)
        ver = m.group(0).decode() if m else "unknown"
        level = MED if ("1.1.0" in ver or "7.62" in ver) else INFO
        add(level, "deps", f"{name}: {ver} (outdated; bundled by the vendor, cannot be patched safely)",
            "treat service-to-internet paths (HTTP/TLS to third parties) as untrusted; no outbound access needed for a private node")


NODE_PORTS = {3850: "Hub", 9001: "Hub HTTP status", 3801: "LoadBalancer", 3802: "Shard",
              3815: "ChatServer", 27017: "MongoDB", 2222: "SSH console", 35000: "DedicatedServer (UDP)"}


def audit_listening():
    try:
        out = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=30).stdout
    except Exception as e:  # noqa: BLE001
        add(INFO, "listening", f"netstat unavailable: {e}")
        return
    seen = {}
    for ln in out.splitlines():
        p = ln.split()
        if len(p) >= 4 and p[0] in ("TCP", "UDP") and (p[0] == "UDP" or p[3] == "LISTENING"):
            m = re.match(r"(.+):(\d+)$", p[1])
            if m:
                seen.setdefault((int(m.group(2)), p[0]), set()).add(m.group(1))
    hit = False
    for (port, proto), addrs in sorted(seen.items()):
        if port in NODE_PORTS or 2300 <= port <= 2330:
            hit = True
            wide = any(a in ("0.0.0.0", "[::]", "*") for a in addrs)
            name = NODE_PORTS.get(port, "service SSH console range")
            if port == 27017 and wide:
                add(HIGH, "listening", f"{proto}/{port} {name} bound to all interfaces", "bind 127.0.0.1")
            elif port in (9001, 2222) or 2300 <= port <= 2330:
                add(MED if wide else INFO, "listening",
                    f"{proto}/{port} {name} bound to {','.join(sorted(addrs))}",
                    "block from outside" if wide else "")
            else:
                add(INFO, "listening", f"{proto}/{port} {name} on {','.join(sorted(addrs))}")
    if not hit:
        add(INFO, "listening", "no node ports are listening (node not running)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("depot_root")
    ap.add_argument("--profile", help="runtime profile dir to scan for *_local.cfg")
    ap.add_argument("--listening", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    cloud = os.path.join(a.depot_root, "cloud")
    if not os.path.isdir(cloud):
        sys.exit(f"no cloud/ under {a.depot_root}")
    audit_mongo(cloud)
    audit_cfgs(cloud, a.profile)
    audit_platform_lua(cloud)
    audit_cloud_xml(cloud)
    audit_libs(cloud)
    if a.listening:
        audit_listening()
    order = {HIGH: 0, MED: 1, LOW: 2, INFO: 3}
    findings.sort(key=lambda f: order[f[0]])
    lines = ["| Level | Area | Finding | Suggested fix |", "|---|---|---|---|"]
    for lv, ar, msg, fix in findings:
        lines.append(f"| {lv} | {ar} | {msg} | {fix} |")
    text = "\n".join(lines) + "\n"
    if a.out:
        open(a.out, "w", encoding="utf-8", newline="\n").write(text)
    print(text)
    sys.exit(min(255, sum(1 for f in findings if f[0] == HIGH)))


if __name__ == "__main__":
    main()

# Administration, operations and security

> Status: **Stage 1 draft.** Commands are taken from strings in `Hub.exe` and
> the official page; arguments marked ⚠ are unverified.

## 1. Hub console

The Hub (and every service) has a console with a Quake-style command/cvar
system. Typed commands start with `/`.

| Command | Purpose |
|---------|---------|
| `/enterMaintenanceMode <minutes>` | Announce and enter maintenance mode after N minutes (also a seconds variant exists in the binary) |
| `/leaveMaintenanceMode` | Leave maintenance mode |
| `/quit` | Shut the Hub down |
| `/status` | Cloud/hub status (⚠) |
| `/cron_addCmd <dow> <hours> <minutes> <cmd>` | Schedule a console command |
| `/cron_addCvarToggler <dow> <hours> <minutes> <duration> <cvar> <toggle_to> <toggle_back_to>` | Temporarily set a cvar on a schedule |
| `/cron_remove <idx>` | Remove a cron entry (0-based) |
| `http_get "<url>"`, `http_upload "<url>" "<file>" <field>` | HTTP helpers |
| `help <cmd/cvar>` | "Show description for commands and cvars" |

Cvars: `cloud_maintenanceMode`, `cloud_status`, `hub_status`, `hub_state`,
`hub_overrideStatus`, `hub_updating_stage`.
Note `cron_enabled = 1` is set in `ConfigureGRD()` (GameRewardDispencer owns the
cron scheduler).

`hub_maintainanceStateURL`, `hub_cloudXmlURL`, `hub_statusReportFile` show the
original deployment published state/config over HTTP/files — usable for
status pages.

## 1a. Status endpoint (port 9001)

`GET http://<host>:9001/status?key=<built-in key>` returns a JSON health
document (version, CPU, battles `gs`, zones `zi`, per-service ports/load).
The key is hard-coded in `Hub.exe`, so it offers no protection — see
[verification log §V-3](../04-installation/verification-log.md#v-3--hub-status-endpoint-port-9001).
Block port 9001 from outside; reverse-proxy it with real auth if you need it.

The full static command list (usage strings of every service, the Shard admin tasks and the `cheat_*` family) is in [console-commands.md](console-commands.md).

## 2. SSH debug console

> **Verified (2026-10-11):** works when `ssh_passwd`, `ssh_port`, `ssh_privateKeyFile`
> (PEM RSA) and `ssh_publicKeyFile` are set; legacy algorithms only
> (group1-sha1 / ssh-rsa / aes128-cbc / hmac-sha1), shell only, **Lua prompt**
> with `/cvarList`, `/cmdList`, `= expr`. Recipe and findings:
> [verification log V-7](../04-installation/verification-log.md#v-7--built-in-ssh-console-works-engine-cvar-defaults-read-2026-10-11).
> Security: it is a full Lua prompt inside the service — an authenticated
> user can change cvars and run script code. Bind-all by default; firewall it.

`ssh_port` (2222 in `dediserver.cfg`), `ssh_passwd`, `ssh_privateKeyFile`,
`ssh_publicKeyFile`, `ssh_MOTD`. The logs print
`SSH server is disabled: ssh_passwd is empty`, so it is off by default. If you
enable it, use a strong password and **never** expose the port publicly.

## 3. Logs

| Log | Location |
|-----|----------|
| Hub | `%LOCALAPPDATA%\Targem\StarConflict\cloud\Hub\logs\hub_<date>.log` |
| Service | `…\Hub\logs\<serviceId>_<service>_<date>.log` (+`.conlog` for console) |
| Crash dumps | `…\Hub\cloud_exceptions\`, `…\Hub\dediserver_exceptions\` |
| Client | `%LOCALAPPDATA%\Targem\StarConflict\logs\<timestamp>\{game,game.net,chat,combat}.log` |

Each start prints a memory-statistics block and a banner with version/build
time. Typical volume: 60–350 KB per service per session (QuestServer largest).

## 4. Backups & maintenance

* Back up MongoDB with `mongodump` (server may stay running) or copy the data
  directory with Mongo **stopped**.
* Rotate/clean `Hub\logs` periodically (no automatic cleanup observed).
* Schedule restarts with `cron_*` + maintenance mode.
* Set `lb_disallowAccess 1` to refuse new logins during maintenance.

## 5. Security

> **Full chapter:** [security.md](security.md) (threat model, findings S-01..S-18, hardening profiles, incident response). The table below is the short summary; audit a node with `tools/security_audit.py`.

> The stock node is designed for **localhost use**. The official page warns
> that exposure needs additional measures by the operator.

| Risk | Detail | Mitigation |
|------|--------|-----------|
| Hub status endpoint (9001) uses a key that is the same in every build | Anyone reaching 9001 can read node status (observed) | Firewall; do not publish |
| Hub accepts any source address | `address` in `cloud.xml` only changes what is *advertised* to clients (official) | Firewall: allow only the client-facing ports to the world, keep Hub-internal traffic on loopback/VLAN |
| Modified clients | Anyone who knows the IP can connect with a patched client | Network-level allow-lists / VPN for private servers |
| MongoDB 2.6 | No authentication configured, old release | Keep `bind_ip=127.0.0.1`; never publish 27017 |
| Redis | No auth in the sample line | Loopback only |
| SSH console | Disabled by default | Keep disabled or use strong password + private network |
| Client vulnerabilities | Official: game client may contain vulnerabilities that let a malicious server compromise your PC | Only connect to servers you trust; run the client in a VM/sandbox if unsure |
| Credentials | Never use a Gaijin account password on an unofficial server | Use throw-away credentials |
| Account auto-creation | `auth_allowInternalAutoCreate = 1` | Set `0` once your accounts exist (private servers) |

### Privacy

A public server operator becomes a data controller for whatever the server
stores (accounts, IPs in logs, hardware fingerprints used for MMV
`isSingleUidOnPC`, chat logs). Minimise retention, and see Gaijin's notice:
operators process personal data independently.

## 6. Operating checklist

- [ ] `cloud.xml` address correct for your audience
- [ ] Firewall rules reviewed
- [ ] `*_local.cfg` used for all overrides; stock files untouched
- [ ] Event dates in `default_platform_config.lua` updated (or events off)
- [ ] Mongo backup schedule
- [ ] Server labelled "Unofficial Server", no monetisation

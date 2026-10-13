# External services, login modes and crash upload (static)

> Analysis of 2026-10-11. Derived from the generated
> [binary-endpoints-and-options.md](binary-endpoints-and-options.md)
>, the cvar table
> [cvar-defaults.md](../05-configuration/cvar-defaults.md) and the
> registration strings of `Shard.exe`. Static only; a string in a binary does
> not prove the path is taken at run time. Offline/privacy relevant for anyone
> hosting a node.

## 1. What a node may contact

| Endpoint (string) | Component | Gate / purpose |
|-------------------|-----------|----------------|
| `api.steampowered.com`, `partner.steam-api.com` (`ISteamUserAuth/AuthenticateUserTicket`, `ISteamUser/GetPublisherAppOwnership`, `GetUserGroupList`, `GetUserInfo`, micro-transactions `InitTxn`/`FinalizeTxn`) | Shard | Steam ticket authentication and purchases. Needs a **publisher key**: `steam_publisherKeyGaijin` / `steam_publisherKeyTargem` are **empty** in the shipped config; `steam_usePartnerWebAPI` 1; `steam_useMicroTxnSandbox` is set to 1 in `shard.cfg`. Without a key the Steam path cannot succeed |
| `api.vk.com`, `oauth.vk.com` (friends, group membership, wall photo upload) | Shard (membership/rewards), DS and client (social posting) | `vk_groupRewardGroupId` 30227294 (reward for a VK group, `vk_groupRewardSpamPeriod` 1440 min); empty `vk_appId` disables the client part |
| `graph.facebook.com`, `www.facebook.com/dialog/oauth` | Shard, DS, client | `fb_appId` empty = unused |
| yuplay (`yuplay_authUrl`, `yuplay_checkPurchaseUrl`, `yuplay_itemInfoUrl`, ... all **empty** by default) | Shard | Gaijin/Yuplay account and shop; disabled while `auth_useYuplay` = 0 |
| Arc (`arc_apiUrlBase` ... empty, `arc_appId` 0) | Shard | Arc store integration, unused |
| `crashdumps.targem.ru:55080/submit`, `/submit_script_errors` | **CrashReporter.exe** | crash dump upload, see section 3 |
| `cqc.ping.eu/ru`, `cqc.loss.eu/ru` | Hub | connection-quality probe host names (`cqc_*` cvars); only meaningful with the vendor measurement service |
| `office.targem.ru:996` | StatServer.exe (not started by the shipped `cloud.xml`) | vendor stat reporting host, dead code on a community node |
| `127.0.0.1:8125` (statsd), `127.0.0.1:37331` (gonalytics), `127.0.0.1:10000` (net log), Redis | all | **telemetry sinks, all disabled by default** (`statsd_enabled` 0, `gonalytics_enabled` 0, `cl_netLogEnabled` 0, `redis_logger_enabled` 0, `hub_cloudXmlURL` empty) |

Everything else in the generated list is certificate-chain material of the
code-signed binaries (DigiCert/GlobalSign CRL/OCSP URLs) or library comments.

## 2. Login modes of a community node *(cvars, Shard registration strings)*

| Cvar | Default | Effect |
|------|---------|--------|
| `auth_useYuplay` | 0 | "use yuplay accounts or autoregister ours": **0 = own accounts** (the stock node) |
| `auth_allowInternalAutoCreate` | 1 | account is created on first login with a new name/password (the community's "register by logging in") |
| `auth_allowSteamCreation` | 0 | no account creation through a Steam login |
| `auth_useYuplayIdVerification` | 1 | verification of linked Yuplay ids (only with the Yuplay path) |
| `auth_closedPTRMode` | 0 | 1 = only specific roles may log in (maintenance/test servers) |
| `auth_goldDebtToDisallow` | 10000 | accounts in gold debt beyond this cannot log in |
| `auth_allowStressBots` | 0 | stress-test bots may log in |
| `auth_logIncomingMessages` | 1 | **logs incoming Authenticator messages** (debug; see S-19/S-24) |

So with the shipped defaults a node is a **closed own-account system**: the
Shard does not need or reach Steam or Yuplay, and a player's registration is
local to the node (matches the community statement "you have to register on
every server"). The admin role of an account is the string field `admRole`
(S-02, [shard-admin-tasks](shard-admin-tasks.md)).

## 3. Crash reporting (privacy) *(strings + cvars)*

* `CrashReporter.exe` is a separate executable; its `crash_url` cvar defaults
  to `http://crashdumps.targem.ru:55080/submit` (plain HTTP). A second path,
  `/submit_script_errors`, sends Lua script errors.
* The dump type is `crash_dumpType = 0x41` = `MiniDumpWithDataSegs |
  MiniDumpWithIndirectlyReferencedMemory`: dumps contain **data segments and
  referenced heap memory**, i.e. potentially keys, passwords, tokens and
  player data of the crashing service.
* The Hub's coordinator creates dumps itself for hung services
  (`coordinator_procdumpTimeout`) and the engine installs crash handlers in
  every executable; whether the reporter is launched automatically on a
  community node (and whether the vendor host still answers) was not tested.
* **Mitigation** (candidate, untested): set `crash_url` to an empty string or an
  own collector in `*_local.cfg`, and/or block outbound traffic of
  `CrashReporter.exe` in the firewall; keep dump directories private (they
  would otherwise reveal the contents above). Recorded as security finding
  S-25.

## 4. Command-line switches worth knowing

From the generated catalogue (names only; semantics from context, not tested):

| Switch | Executables | Meaning *(inferred)* |
|--------|-------------|----------------------|
| `-cloudAddr`, `-hub`, `-hostInstanceId`, `-instId`, `-gsid`, `-regionId`, `-outputDir` | all services | set by the Hub when it spawns a service/DS (see [protocol-observed](protocol-observed.md) §4) |
| `-nohub` | services | do not connect to a Hub (debug aid; not tested here - V-6 only established that a service started outside `cloud.xml` is removed by a running Hub) |
| `-datasource`, `-logFileName`, `-nullCon` | services | data source path, log file, no console |
| `-install`/`-uninstall`/`-start`/`-stop` | all | Windows service control (`WinService.cpp`) |
| `-prepareSharedData` | DedicatedServer, game | build the generated XML from Lua (needs MongoDB, [pipeline](config-pipeline-and-limiters.md)) |
| `-launchLocalServer`, `-autoLogin`, `-noMenu`, `-skiplogos` | game | local server/automation switches of the client |
| `-navmapRebuild`, `-navmapRebuildForce` | DedicatedServer | navigation map rebuild for AI |
| `-multiCopies` | Hub, game | allow several instances (the "multi-instance" switch of Q31) |
| `-accepteula` | Hub | purpose unclear (name suggests a licence-prompt suppression of an embedded tool) |
| `-resetcfg`, `-resetprlf`, `-safe`, `-nompcheck` | game | reset client config/profile, safe mode, skip multi-player checks |

`-multiCopies` answers the static part of **Q31**.

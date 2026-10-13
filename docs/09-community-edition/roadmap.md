# Community Edition — roadmap & design space

> **Design analysis - not verified, not a plan.** This page compares options for a
> possible future server built by a *separate* project. Nothing here was built
> or tested, and nothing here is a recommendation of this repository.
>
> The tracks below are the design space a separate project may choose from,
> derived from the documented findings and from wishes expressed by the
> community.

## 1. Directions

| Track | Description | Prereqs | Effort |
|-------|-------------|---------|--------|
| A. **Operate the stock server** | Reliable hosting recipes: Windows service wrapper, Wine/Docker, firewall, backups, status page | Q1–Q3, Q19 | Low |
| B. **Config/content mods** | Rebalanced queues, bots, economy, custom events by editing Lua/XML | config docs | Low |
| C. **Tooling** | Save editor (Mongo), account import from presets, cvar/queue editor, log viewer, `prepare_shared` helper, backup scripts | DB schema (Q17) | Medium |
| D. **Protocol documentation** | Wire format, message ids, auth flow | Q14 | High |
| E. **Clean-room server** | Open-source re-implementation of LoadBalancer/Shard/MatchMaker speaking the same protocol, reusing stock `DedicatedServer.exe` | D | Very high |
| F. **Client patches / launcher** | Server browser, auto-update of server list, localisation | Q2, Q3 | Medium |

> Detailed comparison of architectures, languages, formats and work
> packages: [implementation-options.md](implementation-options.md); Linux-native
> and portable variants: [linux-native-and-portable-server.md](linux-native-and-portable-server.md).

## 2. Community wishes seen in discussion

* A shared community-run public server list / browser; "download a zip and
  host" simplicity.
* Docker image (24/7 base server), Linux hosting.
* Save editor and migration of progress from the retired official service
  (only owners of a server can restore items).
* Rebalancing "in ways Gaijin never let us"; more bots in lobbies.
* Keeping the project "about making SC operational, not a new game".

## 3. Possible layout of a separate server repository

```
/docs          design notes (linking to this documentation)
/tools         scripts (DB helpers, log parsers)
/config        sample *_local.cfg and Lua overlay files (no game files)
/docker        Wine/Mongo container recipes
/server        clean-room implementation
```

## 4. Milestones

| M | Deliverable |
|---|-------------|
| M0 | Docs v0.1: inventory, architecture, install, config (done) |
| M1 | Verified install/ops guide (Windows + Linux/Proton), ports known, troubleshooting |
| M2 | Complete cvar & data-file reference in English; DB schema |
| M3 | Tooling: backup, save editor prototype, config overlay mechanism |
| M4 | Protocol notes, packet dissector |
| M5 | Decision point: clean-room server feasibility |

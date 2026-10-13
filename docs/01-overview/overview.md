# Overview

> Status: **Stage 1 draft** — based on the released server files, the official
> "Local Game Launch" page and community notes. See [source register](../sources/source-register.md).

## 1. What this project documents

*Star Conflict* is a free-to-play online space-combat game developed by Targem
Games (StarGem Inc.) and published by Gaijin Entertainment. On **9 October 2026,
13:00 UTC+3** Gaijin permanently shut down the official servers.
As a final step Gaijin released:

* the game client (Steam only), and
* the **complete server software for Windows** (the same set of services that
  ran the live "cloud"), bundled with the client in the Steam depot.

The server is a *distributed* system: a "node" (one machine) runs a **Hub** that
spawns ~17 service executables, backed by a **MongoDB 2.6** database
(and optionally Redis for leaderboards). The game client can start and stop a
complete local node by itself.

This repository documents that software: how it is built, how to run it, what it
can do, how to configure it and what is known (or still unknown) about its
internals.

## 2. Goals

| # | Goal | Where |
|---|------|-------|
| 1 | Inventory of everything that was released | [02-inventory](../02-inventory/inventory.md) |
| 2 | Architecture & capability analysis | [03-architecture](../03-architecture/architecture.md) |
| 3 | Install / configure / operate guide | [04-installation](../04-installation/quick-start.md), [05-configuration](../05-configuration/config-system.md), [07-administration](../07-administration/administration.md) |
| 4 | Data model & account editing | [06-database](../06-database/mongodb.md) |
| 5 | Groundwork for reverse engineering / open-source community edition | [08-reverse-engineering](../08-reverse-engineering/re-notes.md), [09-community-edition](../09-community-edition/roadmap.md) |

## 3. Key facts at a glance

* **Platform:** Windows (client and MongoDB x64; the 22 `cloud/` service executables are 32-bit x86). Linux works through Steam Proton (reported by the
  community; see [Linux notes](../04-installation/linux-proton.md)).
* **Server version string:** `Hub 1.99.0.167293 (Oct 9 2026 14:07:47)` (from Hub log).
* **Scripting:** LuaJIT 2.1.0-alpha embedded in the engine (Lua 5.1 API); server
  game data and configuration are Lua + XML.
* **Database:** MongoDB 2.6.12 (bundled), `127.0.0.1:27017`, DB names
  `cosmosim_<user>`, `stats_cosmosim_<user>` etc.
* **Default endpoint:** `127.0.0.1:3850` (Hub); client talks to LoadBalancer
  `3801` and Shard `3802` (see [ports](../03-architecture/architecture.md#ports)).
* **Single node, no clustering by default:** `cloud.xml` defines one node with
  17 services.
* **Out of the box:** a client login screen has a `localhost` option; unknown
  usernames are auto-created (`auth_allowInternalAutoCreate = 1`).

## 4. Legal context (summary — not legal advice)

The official end-of-service notice (page last updated 9 Oct 2026) states, in
short:

* Gaijin permits use of the **server files**, **modification** of the game, and
  **connection to unofficial servers**.
* Unofficial servers **must not be monetised** and must be clearly identified as
  **"Unofficial Server"** wherever the game's name is used.
* In-game items cannot be transferred to unofficial servers; purchases ended
  1 June 2026.
* IP in the game remains with Gaijin or its licensors; the game client is
  distributed only through Steam, "AS IS".
* Never enter Gaijin account credentials on unofficial servers.

Consequences for this repository are discussed in
[09-community-edition/legal-and-licensing.md](../09-community-edition/legal-and-licensing.md).
**This repo must not redistribute game binaries or assets.**

## 5. Reading order

1. [Architecture](../03-architecture/architecture.md)
2. [Quick start](../04-installation/quick-start.md)
3. [Configuration system](../05-configuration/config-system.md)
4. [Matchmaking guide](../05-configuration/matchmaking-guide.md)
5. [MongoDB & accounts](../06-database/mongodb.md)
6. [Administration](../07-administration/administration.md)

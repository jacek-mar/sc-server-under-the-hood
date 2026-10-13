# CLAUDE.md - instructions for AI agents and contributors

Rules for anyone (human or AI agent) who edits this repository. Read this
first, then [`docs/00-index.md`](docs/00-index.md) and
[`CONTRIBUTING.md`](CONTRIBUTING.md).

> Maintainers keep a private, git-ignored working log
> (`_user_notes/handoff.md`). If that file exists in your checkout, read it
> after this one; it never goes into the public repository.

## 1. Project

Documentation and analysis of the Star Conflict (Gaijin/Targem) server
software released at the end of the official service (9 October 2026):
architecture, capabilities, installation, configuration, operation and
security, plus an information base for separate projects (for example a
community-edition server).

* **Scope:** analysis of the existing software and how it behaves. The
  repository contains **no game code or assets**, only our own analyses.
  Any new server software belongs in a separate repository.
* **Role:** a *decision-support information base*. It does not choose a
  solution type, language, framework or architecture. It collects
  language-neutral facts - constraints, interfaces, data formats,
  invariants, failure modes, what operators look for and where they get
  stuck. The option analyses in `docs/09-community-edition/` compare
  trade-offs; they are **not recommendations**.
* **Tools:** only small read-only helpers for server operators are
  published in `tools/` (see [`tools/README.md`](tools/README.md)).

## 2. Rules

1. **No game files in the repository.** Never commit executables, `.pak`
   archives, extracted assets or full Lua/XML data files. Short excerpts that
   explain a setting are fine; otherwise cite the path inside the game
   install.
2. **English.** All documentation is in English. Translations of
   foreign-language sources (for example Russian comments in the shipped
   config) are welcome - mark them as translations and name the source.
3. **Evidence tags.** Mark statements *(official)*, *(observed)*,
   *(community)*, *(inferred)* or ⚠ unverified, and register sources in
   [`docs/sources/source-register.md`](docs/sources/source-register.md).
   Keep verified findings and hypotheses clearly apart.
4. **Community statements are leads, not facts.** Chat and forum reports
   usually describe one host's setup. Verify against files, logs or a test
   before promoting a claim. Community material appears only as anonymised
   summaries (no names, ids, IP addresses or quotes of private chats).
5. **No personal or local data.** No real IP or MAC addresses, host names,
   Windows user names or profile paths, account names, e-mail addresses,
   Discord/Steam ids, keys or passwords. Use placeholders (`<HOST_IP>`,
   `<WinUser>`, documentation addresses `192.0.2.x` / `198.51.100.x`).
   Values copied from live dumps must be sanitised before they reach a doc.
6. **Python only in a virtual environment** at the repository root
   (`.venv/`): `.venv\Scripts\python.exe -X utf8 -I tools\<script>.py ...`.
   Never install packages globally. Treat game data as untrusted input:
   pass paths as arguments, do not run interpreters from inside data folders.
7. **Generated documents** (headed "generated") are not edited by hand;
   `docs/05-configuration/cvar-reference.md` comes from
   `tools/extract_cvars.py`.
8. **Keep the index current.** When adding, moving or renaming a document,
   update [`docs/00-index.md`](docs/00-index.md) and
   [`CHANGELOG.md`](CHANGELOG.md).
9. **Licence and legal terms.** Everything authored here is CC0-1.0
   ([`LICENSE`](LICENSE)). Servers built from this material must not be
   monetised and must be labelled "Unofficial Server"
   ([legal notes](docs/09-community-edition/legal-and-licensing.md)).

## 3. Useful facts

* Game install (Steam): the server lives in `star conflict/cloud/` (about 20
  32-bit x86 console services started by `Hub.exe` from `cloud/data/cloud.xml`),
  shared game data in `star conflict/data/`, the client in `win64/game.exe`
  (x64). MongoDB 2.6.12 is bundled (`cloud/mongodb/`, loopback only).
* Configuration layers: `cloud.xml` -> per-service `.cfg` (+ optional
  `*_local.cfg`) -> `cloud/data/default_platform_config.lua` (runs last and
  wins for every cvar it assigns) -> generated `cloud/data/*.xml`
  (`prepare_shared.bat`). See
  [config-system](docs/05-configuration/config-system.md) and
  [settings-reload-map](docs/05-configuration/settings-reload-map.md).
* Runtime profile and logs: `%LOCALAPPDATA%\Targem\StarConflict\`.
* Reference build: Hub 1.99.0.167293 (9 October 2026).
* Open questions for contributors:
  [`docs/08-reverse-engineering/open-questions.md`](docs/08-reverse-engineering/open-questions.md).

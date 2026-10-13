# Contributing

Thanks for helping to document the Star Conflict server.

## Ground rules

1. **No game assets or binaries** in pull requests (executables, `.pak`, level
   data, textures, full Lua/XML data files). Short excerpts needed to explain a
   setting are fine; link to the file path instead of pasting it.
2. **No personal data** (user names, IPs, Discord IDs, tokens, Windows user
   names in paths). Use placeholders such as `%LOCALAPPDATA%`, `<WinUser>`,
   `<HOST_IP>` and documentation addresses `192.0.2.x` / `198.51.100.x`.
3. By contributing you dedicate your work to the public domain (CC0 1.0). **No monetisation** material; follow the
   [legal notes](docs/09-community-edition/legal-and-licensing.md).
4. **Tag your evidence:** *(official)*, *(observed)*, *(community)*,
   *(inferred)*; mark untested steps with ⚠ unverified. Community reports
   are leads until checked against files, logs or a test.
5. **Say how to reproduce**: build id (`Hub 1.99.0.167293`), OS, exact steps.

## How to help

* Pick an item in
  [`open-questions.md`](docs/08-reverse-engineering/open-questions.md).
* Verify a ⚠ step and update the doc (change the tag to *(observed)* with the date
  and build).
* Translate/explain cvar comments in
  [`cvar-notes.md`](docs/05-configuration/cvar-notes.md).
* Add troubleshooting entries using the template in
  [`troubleshooting.md`](docs/04-installation/troubleshooting.md).

## Style

* Markdown, English, GitHub-flavoured; one theme per file; tables for
  reference data, short paragraphs for explanation.
* Relative links only. Keep headings stable (other docs link to anchors).
* Documents headed "generated" are not edited by hand; `cvar-reference.md`
  comes from `tools/extract_cvars.py`.
* Update `docs/00-index.md` and `CHANGELOG.md` when adding or moving files.

## Agents

AI agents: read [`CLAUDE.md`](CLAUDE.md) first (rules, evidence tags,
privacy, virtual-environment requirement).

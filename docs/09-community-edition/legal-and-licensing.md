# Legal & licensing notes

> **Not legal advice.** A reading of the official notice (page "Local Game
> Launch", *Last updated: October 9, 2026*) for the purpose of keeping this
> project within the stated permissions. Re-check the original page before
> publishing anything.

## 1. What Gaijin states

| Topic | Statement (paraphrased) |
|-------|-------------------------|
| End of service | Official servers closed 9 Oct 2026, 13:00 (UTC+3). No updates/support. In-game purchases ended 1 Jun 2026 |
| Unofficial servers | Only independent third-party operators; not affiliated or endorsed |
| Permission | Despite EULA 1.2, 3.2.2, 3.2.8 and ToS 4.3.2, Gaijin **permits use of the Game's server files, modification of the Game and connections to unofficial servers** |
| Conditions | Unofficial servers **must not be monetised** and must be **clearly identified as "Unofficial Server"** wherever the Game's name is used |
| Items | In-game items are licensed, not sold; cannot be transferred to unofficial servers |
| Personal data | Operators are independently responsible; Gaijin does not transfer user data; never enter Gaijin credentials on unofficial servers |
| IP | All rights remain with Gaijin or licensors |
| Distribution | The client is available exclusively through Steam, "AS IS" |

## 2. Implications for this repository

| Item | Guidance |
|------|----------|
| Game binaries / assets | **Do not commit or redistribute** (`sc-server-files/` is git-ignored). Users obtain them from Steam |
| Large verbatim extracts of Gaijin files | Avoid. Short excerpts needed for documentation (cvar names, defaults, brief comments) are used. The generated cvar reference carries the original (Russian) comments; English translations are being added in `cvar-notes.md` |
| `docs/05-configuration/matchmaking-guide.md` | Documented English adaptation of Gaijin's official `matchmaking.md` (maintainer decision 2026-10-10: adaptations/translations are allowed); the source is credited in the file |
| Naming | Use "Unofficial Server" wording; don't imply endorsement; don't use Gaijin logos |
| Monetisation | No donation-gated gameplay, no paid items on servers described by this project |
| Community material | Discord export contains personal data of members — **never publish** it, quote only anonymised technical facts |
| Our own docs/tools | **CC0 1.0** (maintainer decision 2026-10-10: as open as possible) — see `LICENSE`. The repo contains analysis only; any future server code goes to a separate repository |
| Third-party components | MongoDB 2.6.12 is **AGPL-3.0** (licence text in `cloud/mongodb/GNU-AGPL-3.0`); OpenSSL, libcurl, FMOD have their own terms. A community edition that redistributes MongoDB must comply with AGPL; the project should instruct users to use the copy from the depot |

## 3. Open legal questions

* Does the permission cover **re-implementing** the server (clean-room open
  source) and redistribution of reverse-engineered protocol documentation? The
  notice speaks of *using server files* and *modification of the Game*; a clean
  re-implementation is likely safer but unaddressed.
* Can data tables (Lua defs, store XML) be redistributed in a community
  repository, or must they be taken from the user's installation? **Assume
  "from the installation"** until clarified.
* Trademark: "Star Conflict" naming in the project title — keep "unofficial /
  community" qualifiers.
* Forum practice (2026-10-12, S19): the game's Steam forum pins a list for
  unofficial-server announcements with three removal grounds - missing
  "Unofficial Server" label, monetisation, and use of software
  vulnerabilities with malicious intent. Players also warn that adding ship
  designs from films or TV series is a separate copyright risk, unrelated to
  the publisher's permission.

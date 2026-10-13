# Reading the MatchMaker decision log (static catalogue)

> Analysis of 2026-10-11. The MatchMaker writes a **decision log** when
> `mm_decisionLog` is set (it is assigned twice in the shipped config, see
> [cvar-defaults](cvar-defaults.md)). The messages below were extracted from
> the format strings of `MatchMaker.exe` (`MMQueue.cpp`, `PveMatcher`-like
> code, `mmTest`) - **static**: the meaning is read from the text, not from a
> run. Use it to diagnose "no match", "match never starts" and squad failures
> ([matchmaking-guide](matchmaking-guide.md), Q35, Q39). The log is bracketed
> by `-- new decision log here --` ... `-- end of decision log --`, a full
> buffer prints `Decision log is full!`, and the final summary line is
> `<result>. Decisions leading to this:` followed by the decisions.

## 1. PvP / arcade team forming

> Numbers quoted in the right-hand column are **engine defaults** from
> [cvar-defaults](cvar-defaults.md); the shipped config may override them
> (check [cvar-reference](cvar-reference.md)).

The matchmaker builds two **teams out of "hands"** (groups of players: squads
and singles), balances them by `mmValue` and by the number of *destroyers*
(destroyer-class ships), then opens a game.

| Message (shortened) | Meaning |
|---------------------|---------|
| `Create game with %d players, qid %d` / `Creating game for uids: ...` | a game was formed from queue `qid` (the queue index in `queuesConfig*`) |
| `Each team has %u players (%u groups), mmValue0/1 = ...` | resulting team sizes and total MMV per team |
| `Hand %u goes to team 0`, `Hand %u: uids ... mmValue ...`, `Hands composition:` | how hands were assigned |
| `Using num destroyers balancing because hand 0 has %d destrs ...` | destroyer counts differ, balancing by destroyer count was applied |
| `Adding 1 man (mmValue, enqTime) to hand N, %u singles left` / `Adding %u-group ...` | filling a hand from singles / groups; `skilled` marks skilled players (`mm_skilledPlayer/Squad`) |
| `No more people in singles queue`, `Group is too big, skipping current hand`, `Hands are empty`, `Hands size mismatch (...) dropping hands` | the hand could not be completed: not enough singles/groups of the right size |
| `Ignore candidate %u-group (leader ..), bmmv %2.0f` | rejected: base MMV too far (`mm_bmmvSquadDiff`) |
| `... squad size` | rejected: squad size not allowed for this slot (`mm_arcadeMaxSquadSize` 2 for arcade, `mm_universeArenaMaxSquadSize` 8) |
| `... same clan` | rejected: only one squad of a clan per game (`mm_oneClanSquad` 1) |
| `... destr rank %d`, `num destr diff`, `too many destroyers` | rejected by the destroyer rules (`mm_unpairedDestroyers` 0: players with destroyers must be paired) |
| `Ignore candidate daddy ...`, `Ignore candidate reserved ...`, `in pair` | player is reserved for a bigger squad (`mm_reservingForSquadMinSize` 3) or already paired |
| `Ignore candidate %s, less time in queue` / `out of range %d` | older queuer preferred; MMV range of the candidate does not fit the current expansion range |
| `Use %s, new range %d` / `Use: uid = %s, uidOpponent = %s` | candidate accepted (range widened) / explicit opponent pairing |
| `Squad filter %d, %d groups, %d singles` | per-queue summary of waiting groups and singles (what Q35 needs) |
| `Somebody was already in game, skipping this tick` | a candidate was matched by another queue in the same tick; harmless |
| `Queues are empty, breaking`, `There are %d people in teams[0], breaking`, `There isn't skilled in queues, breaking` | exit reasons of the loop: nothing to do or not enough people |
| `Expand game %d|%s by %d players`, `Couldn't expand game %d`, `Ignoring full/expired/region-/qid- game` | filling bots-less running games with late joiners; reasons a running game is not expandable |
| `Have %d basic games` | number of open games that could still be expanded |
| `Popping %d queuers with result = %s reason = %d` | queuers leave the queue (matched or timed out); `reason` is the numeric code |

## 2. PvE / coop matching

PvE queues try two strategies in turn (cvars `mm_timePveMatchByPlayerLevel` 30 s and
`mm_timePveMatchByMissionLevel` 30 s):

1. **By buffs** (player level; fields `unlimPve_playerLevel1/2`): `PVE: Probe
   team by buffs (...): mission=, waitTime, minBuff, maxBuff, numGroups,
   numPlayers, numRandomGroups, numGroupsWithMission, numGroupsWithMissionLevel`;
   rejection messages `probe team doesn't accumulate enough players (%d<%d)`,
   `group doesn't fit by buffs`, `group doesn't fit by size into probe team
   (%d+%d>%d)`; success `Final team by buffs: mission=...`.
2. **By mission level** (`unlimPve_minMissionLevel`, `rankMin/rankMax`,
   `accountRank`, `difficulty`): `Probe team by mission level`, `Final team by
   mission level: mission=, missionLevel=...`; failure `No team matched by
   mission level`.

Other PvE lines: `%d groups have proper min waiting time`, `%d groups are
waiting, region %d`, `Found a random group that doesn't fit any mission`,
`Kick out %u people because of pve schedule change` (the PvE schedule window
closed while waiting), `CreateRaidGame: team size %d > max %d`, `Creating
SINGLE game for uids`, `Team sizes are %u and %u. Bots count are %u and %u,
bot tier %u` (the line to read for the bot tier of Q28), `Paired zone %d cids
%s-%s` (open-world arena pairing).

## 3. How to use it

1. Set `mm_decisionLog` on the node (Shard/MatchMaker config; effect is on the
   MatchMaker log).
2. Queue one account and read the log of the MatchMaker for `Squad filter`,
   `Ignore candidate ...` and `Final team ... / No team matched ...` lines.
3. If the log shows the queue as empty although a client is searching, the
   account does not satisfy any queue `query` (see the coverage output of
   [queue_lint](../07-administration/config-validation-tools.md), Q35).
4. Typo'd or invalid queue blocks are visible as a missing `qid` in the
   `Create game ... qid N` lines (Q39).

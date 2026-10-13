# CVar reference (generated)

> **Generated** by `tools/extract_cvars.py` from the shipped `cloud/data/default_platform_config.lua`. Do not edit by hand; put corrections in `cvar-notes.md`.

* `Line` = line number in the shipped file (build 1.99.0.167293).
* *Default* = value assigned in the shipped file (may be a Lua local, see source).
* *Original comment* is Gaijin/Targem's own (Russian). English translations come from `tools/cvar_translations.json`.
* Total cvar assignments: **271** (unique names: 243).

| Service | Function | cvars |
|---|---|---:|
| DedicatedServer | `ConfigureDediServer` | 64 |
| Shard | `ConfigureShard` | 61 |
| ZoneInstance (open world) | `ConfigureZoneInstance` | 47 |
| Universe | `ConfigureUniverse` | 22 |
| ChatServer | `ConfigureChatServer` | 16 |
| QuestServer | `ConfigureQuestServer` | 12 |
| MatchMaker | `ConfigureMatchmaker` | 9 |
| GameRewardDispencer | `ConfigureGRD` | 9 |
| LoadBalancer | `ConfigureLoadBalancer` | 6 |
| LobbyServer | `ConfigureLobbyServer` | 6 |
| Tournament | `ConfigureTournament` | 6 |
| ClanServer | `ConfigureClanServer` | 5 |
| AchievementServer | `ConfigureAchievementServer` | 3 |
| DedicatedServer (per-queue flags) | `ConfigureDediServerFlags` | 2 |
| AdventureServer | `ConfigureAdventureServer` | 1 |
| ScriptsServer | `ConfigureScriptsServer` | 1 |
| ZoneCoordinator | `ConfigureZoneCoordinator` | 1 |

## Shard

Function `ConfigureShard()`, dispatched when `service_type == "ST_SHARD"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 67 | `auth_allowInternalAutoCreate` | `1` | Allow automatic creation of an internal account on first login (bool). Set 0 to forbid new accounts. | Разрешает автоматическое создание внутреннего аккаунта при первом входе. (тип: логический) |
| 70 | `sm_sandboxAccess` | `4` | Access level to sandbox functions (int). | Уровень доступа к sandbox-функциям. (тип: целое число) |
| 73 | `shard_minAntibotCounterForMailSending` | `50` | Minimum anti-bot counter value required to send mail (int, 0..100). | Минимальное значение антибот-счётчика для отправки почты. (тип: целое число; диапазон: 0..100) |
| 76 | `auth_infinitePremiumForRoles` | `"gm;support"` | Semicolon-separated list of admin roles (admRole) that have infinite premium (string). | Список admRole через ;, для которых действует бесконечный premium. (тип: строка) |
| 79 | `squad_maxNonPremiumSize` | `12` | Squad size that can queue without premium (int). | Размер отряда, которому не требуется premium для постановки в очередь. (тип: целое число) |
| 83 | `store_allowAllItemsForBying` | `0` | Allow buying store items even if flagged cant_be_bought (bool). | Разрешает покупать предметы магазина, даже если у них стоит флаг cant_be_bought. (тип: логический) |
| 86 | `shipQuests_dbgLog` | `0` | Enable ship-quest debug logging (bool). | Включает логирование корабельных квестов. (тип: логический) |
| 89 | `gold_on_start` | `300` | Starting Galactic Standards (gold) of a new account (int). | Стартовое количество gold для нового аккаунта. (тип: целое число) |
| 91 | `premium_on_start` | `0` | Starting premium time/value of a new account (int). | Стартовое premium-время/значение для нового аккаунта. (тип: целое число) |
| 93 | `credits_on_start` | `0` | Starting credits of a new account (int). | Стартовое количество credits для нового аккаунта. (тип: целое число) |
| 96 | `store_prestigePerVssl` | `0.01` | Prestige contribution of one regular ship. Prestige = regular*this + premium*store_prestigePerPremVssl (float). | Коэффициент вклада одного обычного корабля в prestige аккаунта. Итоговый prestige считается как: обычные корабли * store_prestigePerVssl + premium-корабли * store_prestigePerPremVssl. (тип: дробное число) |
| 98 | `store_prestigePerPremVssl` | `0.01` | Prestige contribution of one premium ship; higher = premium ships raise prestige more (float). | Коэффициент вклада одного premium-корабля в prestige аккаунта. Чем выше значение, тем сильнее premium-корабли повышают prestige. (тип: дробное число) |
| 101 | `store_vesselExpExtractionCost` | `store_vesselExpExtractionCost` | Cost factor of extracting ship experience (float). | Стоимость извлечения опыта корабля. (тип: дробное число) |
| 104 | `store_vesselExpExtractionCostVisualBonus` | `0` | Visual bonus/indicator of the XP-extraction cost (float); set in a Lua if-branch depending on the cost value. | Визуальный бонус/индикатор стоимости извлечения опыта корабля. (тип: дробное число) |
| 107 | `store_vesselExpExtractionCostVisualBonus` | `1` | Visual bonus/indicator of the XP-extraction cost (float); set in a Lua if-branch depending on the cost value. | Визуальный бонус/индикатор стоимости извлечения опыта корабля. (тип: дробное число) |
| 111 | `store_vesselPriceMod` | `1` | Multiplier for ship prices (credits, premium, tokens, event price), 0.001..100 (float). | Множитель цен кораблей в магазине. Умножает все типы цены корабля: credits, premium, tokens и event-цену. (тип: дробное число; диапазон: 0.001f..100.0f) |
| 113 | `store_modulePriceMod` | `1` | Multiplier for module prices (credits, premium, tokens, event price), 0.001..100 (float). | Множитель цен модулей в магазине. Умножает credits, premium, tokens и event-цену для предметов типа module. (тип: дробное число; диапазон: 0.001f..100.0f) |
| 115 | `store_munitionPriceMod` | `1` | Multiplier for munition prices, 0.001..100 (float). | Множитель цен боеприпасов в магазине. Умножает credits, premium, tokens и event-цену для предметов типа munition. (тип: дробное число; диапазон: 0.001f..100.0f) |
| 118 | `mm_squad1AsSquad` | `0` | Treat a single player as a squad of one in matchmaking (bool). | Считать одиночного игрока отрядом из одного человека при подборе боя. |
| 121 | `mm_totalMMVMdCap` | `2` | Cap on the total MMV modification from efficiency, KPM, wins and other factors. | Общий лимит суммарной поправки MMV от эффективности, KPM, побед и других факторов. |
| 124 | `mm_effRatingMMVMdBase` | `0` | MMV-from-efficiency: base threshold (Base/Step/Cap). | Параметр формулы MMV по рейтингу эффективности: Base - порог, Step - шаг, Cap - максимум. |
| 126 | `mm_effRatingMMVMdStep` | `25` | MMV-from-efficiency: step; smaller step = efficiency raises MMV faster. | Параметр формулы MMV по рейтингу эффективности: Base - порог, Step - шаг, Cap - максимум. |
| 128 | `mm_effRatingMMVMdCap` | `50` | MMV-from-efficiency: maximum contribution. | Параметр формулы MMV по рейтингу эффективности: Base - порог, Step - шаг, Cap - максимум. |
| 131 | `mm_kpmMMVBase` | `0` | MMV-from-KPM: base threshold. | Параметр формулы MMV по KPM: Base - порог, Step - шаг, Cap - максимум. |
| 133 | `mm_kpmMMVStep` | `0.0325` | MMV-from-KPM: step; smaller = KPM raises MMV faster. | Параметр формулы MMV по KPM: Base - порог, Step - шаг, Cap - максимум. |
| 135 | `mm_kpmMMVCap` | `50` | MMV-from-KPM: maximum contribution. | Параметр формулы MMV по KPM: Base - порог, Step - шаг, Cap - максимум. |
| 139 | `mm_winLoseMMVMinBattles` | `2000` | Win/lose term only applies after this many battles. | Параметр формулы MMV по соотношению побед и поражений; MinBattles включает поправку только после нужного числа боёв. Clamp (winLose - mm_winLoseMMVBase)/mm_winLoseMMVStep ; 0 ; mm_winLoseMMVCap ) |
| 141 | `mm_winLoseMMVBase` | `0.75` | Win/lose term: base ratio. Value = clamp((winLose - Base)/Step, 0, Cap). | Параметр формулы MMV по соотношению побед и поражений. |
| 143 | `mm_winLoseMMVStep` | `0.012` | Win/lose term: step. | Параметр формулы MMV по соотношению побед и поражений. |
| 145 | `mm_winLoseMMVCap` | `50` | Win/lose term: cap. | Параметр формулы MMV по соотношению побед и поражений. |
| 148 | `mm_mmvMdBattles` | `"200,200,200,200,200,200,200,100,0,0,0,0,0,0,0,0,0,0"` | Per-rank battle thresholds (18 values) after which the MMV modifiers/floors apply (newbie protection). | Таблица MMV-значений по рангам/группам матчмейкинга. |
| 150 | `mm_mmvMdPenalty` | `"30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30"` | Per-rank MMV modifier (18 values). | Таблица MMV-значений по рангам/группам матчмейкинга. |
| 154 | `mm_mmvMin` | `"30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30"` | Per-rank lower bound of final MMV, active after the battle threshold; list length must equal mm_mmvMdBattles. | Нижняя граница итогового MMV по рангам корабля, которая начинает действовать после порога боёв из mm_mmvMdBattles. Не даёт штрафам и другим отрицательным поправкам опустить MMV ниже указанного значения. Задаётся списком чисел: первое число для 1-го ранга, второе для 2-го и т. д.; количество значений должно совпадать с mm_mmvMdBattles. |
| 158 | `mm_mmvMdUniqFingerprintClamp` | `"30,30,30,30,30,30,30,80,80,80,80,80,80,80,80,80,80,80"` | Per-rank upper bound of MMV for players with a unique PC fingerprint while they have fewer battles than the threshold. | Верхняя граница итогового MMV для игроков с уникальным fingerprint ПК, пока у них меньше боёв, чем порог из mm_mmvMdBattles. Ограничивает, насколько высоко матчмейкинг может оценить нового игрока по его статистике. Задаётся списком чисел по рангам; если список заполнен, его длина должна совпадать с mm_mmvMdBattles. |
| 161 | `sm_initialKeepAliveTime` | `120` | Seconds to wait for the client's first keep-alive after connect; no answer = disconnect. | Время ожидания keep-alive от клиента после подключения; если ответа нет, клиента отключают. |
| 166 | `ctm_taskRecoveryInterval` | `5` | Interval (s, 0.01..5) at which the shard polls storage for deferred admin tasks. | Интервал, с которым shard-сервер проверяет в хранилище отложенные административные задачи и берёт их в работу. Чем меньше значение, тем быстрее задачи начнут выполняться, но тем чаще будут опросы хранилища. Указывается в секундах; допустимый диапазон: 0.01..5. |
| 171 | `squad_maxNonWingSize` | `4` | Max size of a regular squad that is not yet a wing; exceeding it requires a wing group. | WINGS Максимальный размер обычного отряда, который ещё не считается wing-группой. Если при приглашении игроков этот лимит будет превышен, нужно создавать wing-группу. |
| 174 | `squad_maxWingSize` | `12` | Max size of a wing group. | Максимальный размер wing-группы при приглашении игроков в отряд. После достижения этого лимита новых участников добавить в wing нельзя. |
| 177 | `mm_sectorMinWingSize` | `5` | Min wing size to enter sector (universe) queues. | Минимальный размер wing-группы для входа в sector-очерь матчмейкера. Отряды меньше этого размера не будут приняты в режимы, где требуется sector-wing. |
| 180 | `mm_sectorMaxWingSize` | `8` | Max wing size for sector queues. | Максимальный размер wing-группы для sector-очерей матчмейкера. Отряды больше этого размера не будут приняты в режимы, где требуется sector-wing. |
| 183 | `mm_raidMinWingSize` | `10` | Min wing size to enter a raid queue. | Минимальный размер wing-группы для входа в raid-очерь матчмейкера. Отряды меньше этого размера не смогут встать в raid-очерь. |
| 192 | `mm_raidSquadFilter` | `0` | Who may queue for raids: 0 any, 1 solo only, 2 solo+squads, 3 squads+wings, 4 wings only. | Фильтр состава групп для raid-очерей: задаёт, кто может вставать в рейд — одиночные игроки, обычные отряды и/или wing-группы. 0 - все типы составов: solo, обычные отряды и wing. 1 - только solo; любые отряды и wing в raid-очерь не пускаются. 2 - solo и обычные отряды; wing-группы не пускаются. 3 - обычные отряды и wing; solo-игроки не пускаются. 4 - только wing; solo и обычные отряды не пускаются. Для режимов с wing дополнительно действует минимальный размер из mm_raidMinWingSize. |
| 195 | `mm_enablePveRaids` | `1` | Enable PvE raids in matchmaking (bool). | Включает PvE-рейды в матчмейкере. |
| 198 | `mm_notArcadeSquadRankDiff` | `17` | Allowed ship-rank spread inside a squad for non-arcade modes. | Допустимая разница рангов в отряде для не-arcade режимов. |
| 203 | `raid_lootAuraInterval` | `1` | Days between re-granting raid loot auras (checked at the player's first login of the day). | Интервал в днях, через который игроку снова выдаются loot-ауры для raid-миссий. Проверка и выдача происходят при первом входе игрока в эти сутки. Значение 1 означает ежедневную выдачу; 3 — раз в три дня. |
| 206 | `store_creditsEventStart` | `creditsEventStart` | Start time of the credits event (ISO-8601 string). | Время начала события с кредитами. (тип: строка) |
| 208 | `store_creditsEventEnd` | `creditsEventEnd` | End time of the credits event (ISO-8601 string). | Время окончания события с кредитами. (тип: строка) |
| 212 | `store_maxTransactionSum` | `20000` | Maximum sum of one transaction/mail (int). | Trade Максимальная сумма одной транзакции/письма. (тип: целое число) |
| 214 | `shard_minAntibotCounterForMailSending` | `50` | Minimum anti-bot counter value required to send mail (int, 0..100). | Минимальное значение антибот-счётчика для отправки почты. (тип: целое число; диапазон: 0..100) |
| 218 | `mm_decisionLog` | `0` | Matchmaker decision-log bitmask: 1 PvP, 2 PvP join-in-progress, 4 PvP candidates, 8 coop, 16 coop JIP, 32 PvE, 64 universe, 128 brawl, 256 brawl candidates, 512 hunger games, 1024 one against all, 2048 zombie, 4096 three teams, 8192 close distance, 16384 general (32767 = all). | Включает детальный лог решения при попытке игрока или отряда встать в очередь матчмейкера. 0 - лог выключен, любое число больше 0 - лог включён. |
| 222 | `store_maxUniqueModules` | `3` | Max number of identical unique modules per regular ship. | Лимит одинаковых unique-модулей на один корабль; отдельно задаётся для обычных и premium-кораблей. Balanse rule |
| 225 | `store_maxUniqueModulesOnPremium` | `2` | Max identical unique (experimental) modules on premium/DLC ships. | Лимит одинаковых unique-модулей на один корабль; отдельно задаётся для обычных и premium-кораблей. #0098493: Сделать возможнсть установки экспериментальных модулей на прем. и ДЛЦ корабли в кол-ве 1 шт |
| 230 | `sv_offerEnable` | `"6,7,17,18,19"` | Comma/space/tab separated offerIds from offers.xml to enable on the shard; empty string disables all offers. | Список offerId офферов, которые нужно включить на shard-сервере. Идентификаторы берутся из файла offers.xml в этой же папке: ищите атрибут offerId у нужного оффера. Формат: числа через запятую, пробел или табуляцию; пустая строка отключает все офферы. |
| 233 | `store_maxTransactionSum` | `20000` | Maximum sum of one transaction/mail (int). | Максимальная сумма одной транзакции/письма. (тип: целое число) |
| 261 | `store_bonusBundleChancePercentageMax` | `0.2` | Max chance of a bonus bundle when buying a bundle; scaled by prestige/maxPrestige (0..1). | Максимальный шанс получить бонусный набор при покупке набора; шанс умножается на коэффициент (prestige / maxPrestige). (тип: дробное число; диапазон: 0.0f..1.0f) |
| 265 | `premiumTimeForAccountRank` | `1 * 24 * 60 * 60` | Premium time (seconds) granted per account rank (default one day). | Premium-время, выдаваемое за ранг аккаунта. (тип: целое число) премиум (в секундах, по умолчанию - день) |
| 269 | `sv_tokenCreditsDailyLimit` | `1000` | Daily limit of token credits (Iridium) a player can earn. | Дневной лимит token credits, которые игрок может заработать за день. #106983 |
| 277 | `store_battlePassUnlockLvlBtnStart` | `"2023-07-14T00:00:00Z"` | Time from which the battle-pass 'unlock level' button appears (ISO-8601). | Время, с которого появляется кнопка разблокировки уровня battle pass. (тип: строка) |
| 283 | `sm_bflRoleInc` | `0.5` | Adaptive bot presets: factor increasing a BFL role (battle time for life time) statistic. | Адаптивные пресеты ботов. Коэффициент увеличения BFL-роли. (тип: дробное число) bfl - battle time for life time цвар на увеличение статистики пресетов SC-115316 |
| 286 | `sm_bflRoleDec` | `0.05` | Adaptive bot presets: factor decreasing a BFL role statistic. | Коэффициент уменьшения BFL-роли. (тип: дробное число) цвар на уменьшение статистики пресетов |
| 288 | `sm_numAdaptivePresetsToSaveDB` | `numAdaptivePresets` | Number of adaptive presets stored in the DB; 0 clears the data (0..1000). | Количество адаптивных пресетов, сохраняемых в БД. 0 - очищает данные. (тип: целое число; диапазон: 0..1000) |

## MatchMaker

Function `ConfigureMatchmaker()`, dispatched when `service_type == "ST_MATCHMAKER"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 883 | `mm_lowOnlineLo` | `250` | Enter low-online mode when online is below this value. | Переход в режим низкого онлайна, если онлайн меньше этого значения. (тип: целое число) |
| 885 | `mm_lowOnlineHi` | `300` | Leave low-online mode when online is at or above this value. | Выход из режима низкого онлайна, если онлайн не меньше этого значения. (тип: целое число) |
| 889 | `mm_botsCount` | `6` | Default number of bots (0..31); can be overridden per queue. | Количество ботов. (тип: целое число; диапазон: 0..31) Базовое количество ботов; в конкретной очереди может быть переопределено. |
| 925 | `mm_defaultGameplay` | `3` | Default gameplay id for a new session (see game-modes.md); can be overridden per queue. | Базовый игровой режим для новой игровой сессии; в конкретной очереди может быть переопределён. Возможные значения (не все работают): 0 - none 1 - space battle 2 - capture the flag 3 - capture the base 4 - control 5 - practice 6 - tutorial 7 - PvE mission 8 - free space 9 - sentinel 10 - king of the hill 11 - bomb the base 12 - TDM 13 - GTDM 14 - clanship 15 - capture the frag 16 - last man standing 17 - transport escort 18 - open space 19 - mission script 20 - PvP mission 21 - football 22 - battle royale 23 - capture the base 2 24 - hunger games 25 - one against all 26 - ATDM 27 - zombie 28 - close distance 29 - autogen DM 30 - three teams DM 31 - april control |
| 929 | `mm_timeInQueueAveragingCf` | `200` | Smoothing of the average time in queue (2..10000); ~10 dev/test, >100 live. | Чем больше значение, тем плавнее и медленнее меняется среднее время в очереди. (тип: целое число; диапазон: 2..10000) 10 for dev/test, >100 for live |
| 933 | `rate_exp` | `"1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"` | XP multipliers per rank, comma list (18 values). | Множители выдаваемого опыта по рангам, список через запятую. (тип: строка) reward multiplication rates |
| 935 | `rate_cred` | `"1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"` | Credit multipliers per rank, comma list (18 values). | Множители выдаваемых кредитов по рангам, список через запятую. (тип: строка) |
| 942 | `mm_decisionLog` | `0` | Matchmaker decision-log bitmask: 1 PvP, 2 PvP join-in-progress, 4 PvP candidates, 8 coop, 16 coop JIP, 32 PvE, 64 universe, 128 brawl, 256 brawl candidates, 512 hunger games, 1024 one against all, 2048 zombie, 4096 three teams, 8192 close distance, 16384 general (32767 = all). | Детальность decision-log внутри матчмейкера. Это битовая маска: чтобы включить несколько категорий, сложите их числа. 0 - выключено; 1 - базовые PvP-решения; 2 - PvP join-in-progress; 4 - PvP-кандидаты. 8 - coop; 16 - coop join-in-progress; 32 - PvE; 64 - universe; 128 - brawl; 256 - brawl-кандидаты. 512 - hunger games; 1024 - one against all; 2048 - zombie; 4096 - three teams; 8192 - close distance; 16384 - общие решения. Пример: 33 включит базовый PvP-лог и PvE-лог (1 + 32). Все категории: 32767. |
| 946 | `mm_decisionDbg` | `0` | Decision-log output: 0 buffer and dump as one block to the info log; 1 write each message immediately to the debug log. | Способ вывода decision-log матчмейкера. 0 - накапливать строки лога и выводить их одним блоком в info-лог после окончания разбора записей. 1 - писать каждое сообщение сразу в debug-лог; удобно для онлайн-отладки, но может давать много записей. |

## AdventureServer

Function `ConfigureAdventureServer()`, dispatched when `service_type == "ST_ADVENTURE_SERVER"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 1002 | `adventure_saveGiverOffers` | `0` | Persist adventure-giver offers in the DB (bool). | Включает/выключает сохранение предложений adventure-giver в базу данных. (тип: логический) при 1 - сохраняются предложения, при 0 - не сохраняются |

## ScriptsServer

Function `ConfigureScriptsServer()`, dispatched when `service_type == "ST_SCRIPTS_SERVER"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 1010 | `sv_enableCommunticationWithSS` | `1` | Whether the zone instance talks to the scripts server (bool). | Должен ли экземпляр зоны обмениваться данными с сервером скриптов. (тип: логический) |

## DedicatedServer

Function `ConfigureDediServer()`, dispatched when `service_type == "ST_DEDICATED_SERVER"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 1181 | `cl_maxFps` | `18` | Frame-rate cap of the process; 0 = unlimited. Server simulation rate is derived from it. | Ограничивает FPS этим значением; 0 — ограничение выключено. (тип: дробное число) |
| 1184 | `sv_dbgJoinInProgress` | `0` | Debug join-in-progress behaviour (bool). | Отладка подключения к уже идущему бою. (тип: логический) |
| 1188 | `cl_combatLog` | `0` | Combat-log verbosity written to the log: 0 off, 1 kills/deaths/rewards, 2 + module/missile/aura use, 3 + all damage, 4 + gameplay-aura parameter coefficients. | Логирование combat-событий в файл лога; каждый уровень включает все предыдущие. 0 - отключено; 1 - убийства/смерти/награды; 2 - +использование модулей, ракет и аур. 3 - +весь урон; 4 - +коэффициенты параметров геймплейных аур. |
| 1191 | `db_logMessages` | `0` | Database protocol logging: 0 off, 1 brief, 2 full. | Логирование протокола базы данных: 1 — краткое, 2 — полное. (тип: целое число) to catch some nasty stuff |
| 1194 | `sv_respawnTimePenalty` | `-1` | Override of the respawn-time penalty for deaths; -1 = use gameplay settings (newbie queues force 0). | Переопределяет игровую настройку штрафа времени возрождения за смерть. (тип: дробное число) to use gameplaysettings values |
| 1197 | `sv_afkCheckDuration` | `120` | Seconds without control input before an AFK kick; a huge value (e.g. 3600) effectively disables it. | Время в секундах, через которое игрок кикается за AFK, если он не присылал управляющие ввод или они не менялись. Большое значение (напр. 3600) фактически отключает AFK-кик. (тип: дробное число) |
| 1200 | `sv_lootEnabled` | `1` | Enable post-battle loot (bool). | Включает/выключает послебоевой loot. (тип: логический) |
| 1202 | `sv_lootFailChance` | `0` | Probability (0..1) of finding nothing in post-battle loot. | Шанс ничего не найти. (тип: дробное число; диапазон: 0.0f..1.0f) |
| 1204 | `sv_lootScanTime` | `1` | Loot scan time in seconds. | Время сканирования в секундах. (тип: дробное число) |
| 1206 | `sv_lootDuration` | `120` | Duration of the loot-collection stage in seconds. | Длительность стадии сбора loot. (тип: дробное число) |
| 1210 | `sv_salvageTokenConversion` | `0.2` | Regular salvage: tokens refunded = item tokenPrice * this. | Коэффициент обычной salvage-конвертации найденного loot-предмета в токены. Возврат считается от tokenPrice предмета: tokensRefund = tokenPrice * sv_salvageTokenConversion. (тип: дробное число) |
| 1213 | `sv_salvagePremiumTokenConversion` | `0.6` | Premium salvage: tokens refunded = tokenPrice * this. | Коэффициент premium salvage-конвертации найденного loot-предмета в токены. Premium-вариант требует оплату premium-валютой и возвращает токены по формуле: tokensRefund = tokenPrice * sv_salvagePremiumTokenConversion. (тип: дробное число) |
| 1216 | `sv_salvagePremiumPriceConversion` | `0.0008` | Premium salvage price = item price * this. | Коэффициент стоимости premium salvage для найденного loot-предмета. Цена premium-варианта считается от обычной цены предмета: premiumPrice = price * sv_salvagePremiumPriceConversion. (тип: дробное число) |
| 1219 | `sv_universeWingVsWingRewardCf` | `2.0` | Reward multiplier for wing-vs-wing BFS (universe) battles, 1..10. | Коэффициент награды для BFS-боя wing vs wing. (тип: дробное число; диапазон: 1.0f..10.0f) |
| 1222 | `ship_controlForceMode` | `-1` | Force a ship control mode: -1 none, 0 FOLLOWING, 1 COMBINED, 2 LOCAL_TURRET, 3 REMOTE_TURRET, 4 LANDED, 5 WOW. | Принудительный режим управления кораблём. (тип: целое число; диапазон: -1..5) Значения: -1 — не форсировать; 0 — FOLLOWING; 1 — COMBINED; 2 — LOCAL_TURRET; 3 — REMOTE_TURRET; 4 — LANDED; 5 — WOW. |
| 1225 | `ship_ufoRotateX` | `1` | Special X-axis rotation mode for UFO ships. | Особый режим поворота UFO-корабля по оси X. UFO ship controls |
| 1227 | `sv_achievementEnabled` | `1` | Enable in-game achievements (bool). | Включает/выключает игровые достижения. (тип: логический) |
| 1229 | `sv_achievProgressTimer` | `3` | Minimum interval (s) for sending player progress to the achievement server. | Минимальный интервал отправки прогресса игрока на сервер достижений, в секундах. (тип: дробное число) |
| 1233 | `event_cosmonauticsDay` | `0` | Enable the 'Cosmonautics Day' event (bool). | Включает событие «День космонавтики». (тип: логический) EVENTS |
| 1235 | `event_gameAnniversary` | `0` | Enable the game-anniversary event (bool). | Включает событие «Годовщина игры». (тип: логический) |
| 1237 | `event_february23` | `0` | Enable the 23 February event (bool). | Включает событие «23 февраля». (тип: логический) |
| 1239 | `event_march8` | `0` | Enable the 8 March event (bool). | Включает событие «8 марта». (тип: логический) |
| 1241 | `event_botPrefix` | `0` | Enable the bot-prefix event (bool). | Включает событие с префиксом ботов. (тип: логический) |
| 1243 | `event_claws` | `0` | Enable the 'Claws' event (April 1 event) (bool). | Включает событие Claws. (тип: логический) |
| 1245 | `event_knowledgeDay` | `0` | Enable the Knowledge Day event (bool). | Включает событие «День знаний». (тип: логический) |
| 1247 | `event_halloween` | `0` | Enable the Halloween event (int). | Включает событие Halloween. (тип: целое число) |
| 1249 | `event_invasionPVP` | `0` | Enable the PvP invasion event (bool). | Включает событие вторжения в PvP. (тип: логический) |
| 1251 | `event_valentinesDay` | `0` | Enable the Valentine's Day event (bool). | Включает событие «День святого Валентина». (тип: логический) |
| 1254 | `ship_aiThink` | `1` | Enable ship AI logic (bool). | Включает AI-логику кораблей. (тип: логический) DEBUG |
| 1256 | `sv_freeSynergyRewardCf` | `0.05` | Free-synergy reward coefficient. | Коэффициент награды свободной синергии. (тип: дробное число) |
| 1258 | `sv_freeSynergyRewardCfPremiumVessel` | `0.2` | Free-synergy reward coefficient for premium ships. | Коэффициент награды свободной синергии для premium-корабля. (тип: дробное число) |
| 1260 | `sv_goldMunitionExpRewardCf` | `1.0` | Extra synergy-XP coefficient for kills/assists with gold munitions. | Дополнительный коэффициент опыта синергии за убийство/помощь с gold munition. (тип: дробное число) |
| 1263 | `script_gcWorkBudget` | `1` | Incremental Lua GC time budget per frame in microseconds. | Бюджет времени для инкрементальной работы Lua GC, в микросекундах. (тип: целое число) |
| 1267 | `sv_dailyWinPveExpRewardCf` | `x3fw` | XP multiplier for the first PvE win of the day. | Множитель опыта за первую PvE-победу дня. (тип: дробное число) x3 FIRST WIN |
| 1269 | `sv_dailyWinPvpExpRewardCf` | `x3fw` | XP multiplier for the first PvP win of the day. | Множитель опыта за первую PvP-победу дня. (тип: дробное число) |
| 1271 | `sv_dailyWinCoopExpRewardCf` | `x3fw` | XP multiplier for the first coop win of the day. | Множитель опыта за первую coop-победу дня. (тип: дробное число) |
| 1273 | `sv_dailyWinBrawlExpRewardCf` | `x3fw` | XP multiplier for the first brawl win of the day. | Множитель опыта за первую brawl-победу дня. (тип: дробное число) |
| 1277 | `sv_pvpLabelChances` | `"0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"` | Per-rank (18 values, 0..1) chance of granting an event label (marks a ship as an event agent) in PvP. | Шанс выдачи event-label (пометки корабля как агента события для игрока) для PvP-боёв. Задаётся по рангам как список из 18 дробных чисел от 0 до 1; первое число для 1-го ранга, второе для 2-го и т. д. (тип: строка) |
| 1279 | `sv_pveLabelChances` | `"0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"` | Same as sv_pvpLabelChances, for PvE missions and raids. | То же, что и sv_pvpLabelChances, но для PvE-миссий и рейдов. (тип: строка) |
| 1283 | `sv_rarePicksNumberWithFloatingChances` | `100` | Number of attempts for choosing a rare loot table with floating chances (rare_limit). | Количество попыток выбора rare-таблицы loot с плавающими шансами. (тип: целое число) rare_limit |
| 1286 | `sv_epicPicksNumberWithFloatingChances` | `150` | Number of attempts for choosing an epic loot table with floating chances (epic_limit). | Количество попыток выбора epic-таблицы loot с плавающими шансами. (тип: целое число) epic_limit |
| 1288 | `sv_overlootedRarePickChance` | `0.004` | Base chance of picking the rare loot table. | Базовый шанс выбрать rare-таблицу loot. (тип: дробное число) |
| 1290 | `sv_overlootedEpicPickChance` | `0` | Base chance of picking the epic loot table. | Базовый шанс выбрать epic-таблицу loot. (тип: дробное число) |
| 1293 | `sv_lootCommonPickChance` | `0.2` | Base chance of picking the common loot table. | Базовый шанс выбрать common-таблицу loot. (тип: дробное число) common_default_weight |
| 1296 | `sv_lootMaxLevelRestriction` | `0` | Restrict rare/epic loot tables to max-level ships only (bool). | Ограничивает rare- и epic-таблицы loot только кораблями максимального уровня. (тип: логический) max rank ships for loot |
| 1299 | `sv_lootRuleCfA` | `0.25` | Factor A of the rare/epic table weight: weight = max(0, A*(attempts-(it+Offset)) + B). | Множитель A в формуле веса выбора rare/epic loot-таблицы. (тип: дробное число) |
| 1301 | `sv_lootRuleCfB` | `0.25` | Constant B of the same weight formula. | Базовый вес B (свободный член) в формуле веса rare/epic loot-таблицы. (тип: дробное число) |
| 1305 | `sv_lootRuleCfOffset` | `-1` | Offset shifting the attempts threshold at which the floating rare/epic chance starts to grow. | Сдвиг offset: корректирует порог attempts, с которого начинает расти плавающий шанс rare/epic. (тип: дробное число) Формула: weight = max(0, sv_lootRuleCfA * (attempts - (it + sv_lootRuleCfOffset)) + sv_lootRuleCfB). attempts - число попыток без rare/epic; it - порог из iter в loot-правиле для текущей по счёту выдачи. |
| 1308 | `sv_autorecordReplaysTo` | `""` | Directory for dedicated-server replays; empty = disabled. | Путь для сохранения replay dedicated-сервера. (тип: строка) |
| 1312 | `event_custom` | `event_custom` | Start time of the custom event (ISO-8601); start and end must be whole hours or the 'imaginary' quest may misbehave. | Время начала кастомного события. (тип: строка) "Необходимо изменять время начала и конца кратно часу, иначе квест imaginary может вести себя |
| 1343 | `sv_kickExcessiveBotsEnabled` | `1` | Kick players from a battle when bots outnumber players (bool). | Кикать ли игроков из боя, если ботов стало больше, чем игроков. |
| 1347 | `sv_numBestPlayerToSave` | `2` | How many best players' ships are saved for adaptive presets; -1 = all. | Количество лучших игроков, чьи корабли сохраняются для адаптивных пресетов; -1 — все игроки и все корабли. (тип: целое число; диапазон: -1..MAX_PLAYERS) количество сохранения лучших игроков SC-115316 |
| 1350 | `sv_minEfficiencyVesselToSave` | `1500` | Minimum ship efficiency (points) to be saved into adaptive presets. | Минимальная эффективность корабля для сохранения в базу адаптивных пресетов. (тип: целое число) минимальное количество очков для сохранения пресета корабля лучшего игрока |
| 1352 | `sv_numAdaptivePresetsInDB` | `numAdaptivePresets` | Limit of adaptive-preset records in DB per mode, rank and role; 0 clears. | Лимит записей адаптивных пресетов в БД для режима, ранга и роли; 0 очищает базу. |
| 1355 | `sv_numUniqueAdaptivePresets` | `20` | How many unique presets a dedicated server requests from the DB (0..100). | Лимит от 0 до 100 на чтение из базы адаптивных пресетов для ранга и роли игрового режима. (тип: целое число; диапазон: 0..100) сколько уникальных пресетов запрашивает дедик с базы |
| 1358 | `sv_rangeRankAdaptivePresets` | `3` | Rank window for presets read from the DB, counted down from the queue's max rank (12 with value 3 -> ranks 9..12). | Диапазон рангов от 0 до MAX_SHIP_RANK для чтения из базы адаптивных пресетов. (тип: целое число; диапазон: 0..MAX_SHIP_RANK) разница запрашиваемых рангов пресетов с базы от максимального ранга очереди ( если максимальный ранг 12, то при цваре 3, минимальный ранг будет 9 ) |
| 1362 | `sv_leaveFineRewardCoef` | `0.8` | Reward multiplier for players who left previous battles (0..1; 1 = no penalty). | Множитель награды для случая, когда игрок покидал предыдущие игры. (тип: дробное число; диапазон: 0.0f..1.0f) коэффициент награды. По умолчанию 1(нет штрафа). |
| 1365 | `sv_leaveCounterMaxDecay` | `4` | Max amount by which the leave counter can decrease when the player gets a penalty. | Максимальное снижение счётчика выходов из боя. (тип: целое число; диапазон: 0..INT_MAX) максимальное значение, на которое может уменьшиться счетчик ливов, когда игрок получает штраф(счетчик ливов больше единицы. По умолчанию равен 3. Целое. |
| 1368 | `sv_leaveCounterDecayWithoutFine` | `0.9` | Amount the leave counter decreases when the player is not penalised (counter < 1). | Снижение leaveCounter, если игрок не получил штраф. (тип: дробное число; диапазон: 0.0f..FLT_MAX) значение, на которое уменьшается счетчик, когда игрок не получает штраф(счетчик меньше единицы). По умолчанию 0.1 . |
| 1371 | `sv_normalLeaveCounterAdd` | `0` | Added to the leave counter on a normal exit ('Leave battle' button). | Добавляет это значение к leaveCounter, если игрок вышел из игры штатно. (тип: дробное число) значение, на которое увеличивается счетчик при нормальном выходе из боя(нажал на кнопку "Покинул бой"). По умолчанию 0.5. |
| 1374 | `sv_abnormalLeaveCounterAdd` | `0` | Added to the leave counter on an abnormal exit (crash, network loss). | Добавляет это значение к leaveCounter, если игрок вышел из игры нештатно. (тип: дробное число) значение, на которое увеличивается счетчик при ненормальном выходе(упал клиент, пропала сеть). По умолчанию 0. |
| 1378 | `sv_leaverReputationAdd` | `1` | Added to leaver reputation when a leaver ban is issued (0..100). | Добавляет это значение к leaverReputation, если игрок получил leaver-ban. (тип: дробное число; диапазон: 0.0f..100.0f) [0, 100], по умолчанию 1. Это значение добавляется к leaverReputation, когда игрок получает бан. |
| 1381 | `sv_leaverBanTime` | `0` | Minimum battle-ban time (s, 0..1800) for leaving; engine default 300. | Минимальное время battle-ban при штрафе за выход, в секундах. (тип: дробное число; диапазон: 0.0f..1800.0f) [0, 1800], по умолчанию 300. Время, на которое игрок получает бан на вход в бой, в секундах. |
| 1384 | `sv_leaverReputationDecay` | `0.9` | Leaver reputation decrease per battle without leaving. | Снижение leaverReputation, если игрок не покидает игру. (тип: дробное число; диапазон: 0.0f..FLT_MAX) по умолчанию 0.01. На эту величину уменьшается leaverReputation, когда игрок не ливает. |

## DedicatedServer (per-queue flags)

Function `ConfigureDediServerFlags()`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 1392 | `sv_respawnTimePenalty` | `0` | Override of the respawn-time penalty for deaths; -1 = use gameplay settings (newbie queues force 0). | Переопределяет игровую настройку штрафа времени возрождения за смерть. (тип: дробное число) |
| 1397 | `sv_mmBattleRank` | `queueFlags.rank` | Battle rank of the match; passed to battle parameters and affects rank restrictions. | Боевой ранг матча; передаётся в параметры боя и влияет на ранговые ограничения. |

## ZoneInstance (open world)

Function `ConfigureZoneInstance()`, dispatched when `service_type == "ST_ZONE_INSTANCE"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 1407 | `cl_maxFps` | `18` | Frame-rate cap of the process; 0 = unlimited. Server simulation rate is derived from it. | restart cloud after changing these cvars Ограничивает FPS этим значением; 0 — ограничение выключено. (тип: дробное число) |
| 1410 | `ship_aiThink` | `1` | Enable ship AI logic (bool). | Включает AI-логику кораблей. (тип: логический) |
| 1414 | `cl_combatLog` | `0` | Combat-log verbosity written to the log: 0 off, 1 kills/deaths/rewards, 2 + module/missile/aura use, 3 + all damage, 4 + gameplay-aura parameter coefficients. | Логирование combat-событий в файл лога; каждый уровень включает все предыдущие. 0 - отключено; 1 - убийства/смерти/награды; 2 - +использование модулей, ракет и аур. 3 - +весь урон; 4 - +коэффициенты параметров геймплейных аур. |
| 1416 | `sv_shipWeaponDamageCoef` | `1` | Global weapon damage coefficient (0..FLT_MAX). | Коэффициент урона оружия. (тип: дробное число; диапазон: 0.0f..FLT_MAX) |
| 1419 | `sv_eventObjectRespawnTimeMin` | `60` | Minimum respawn time of an event object (s). | Минимальное время respawn event-объекта. (тип: дробное число) |
| 1422 | `sv_eventObjectRespawnTimeMax` | `420` | Maximum respawn time of an event object (s); min/max give the random delay range for the first and subsequent spawns. | Максимальное время respawn event-объекта. (тип: дробное число) задают диапазон для выбора случайно задержки первого и последующих созданий объекта. |
| 1425 | `sv_eventObjectEndTime` | `"2026-04-10T05:00:00Z"` | Time after which the event object is no longer created (ISO-8601). | Время отключения event-объекта. (тип: строка) время, после которого ивентовый объект больше не создается. |
| 1429 | `event_claws` | `0` | Enable the 'Claws' event (April 1 event) (bool). | Включает событие Claws. (тип: логический) April 1 |
| 1433 | `sv_pickedLootRateToClanResource` | `0.1` | Conversion rate of picked-up loot to clan resource (clan iridium). | Коэффициент конвертации подобранного loot в ресурс клана. (тип: дробное число) 0.1 курс перевода числа подъемов лута в корпоративный иридиум |
| 1436 | `sv_pickedLootUpdateTime` | `6 * 3600` | Interval (s) at which picked-loot iridium is sent to the clan. | Время обновления подобранного loot. (тип: дробное число) интервал отправки иридиума в корпу в секундах. |
| 1442 | `sv_spaceStationPortalTimer` | `3` | Timer of the portal to a station in open space (s). | Отключает проверку формата Lua-данных при конвертации и сохранении в базу. 1 - данные записываются без сверки со схемой; только для не-live сборок. cvars.dbg_disableLuaDataFormatChecking = 1 Таймер портала к станции в открытом космосе. |
| 1445 | `sv_autogenModulesEnabled` | `0` | Enable auto-generated modules (seed chips, SC-112454). | SC-112454 сид-чипы |
| 1448 | `sv_dbgAutogenDefs` | `0` | Where to show seed chips: 1 in game only, 2 in game and hangar. | Где показывать сид-чипы: 1 - только в игре, 2 - в игре и в ангаре. 1 — в игре, 2 — в игре и в ангаре. (тип: целое число) |
| 1451 | `sv_enableCommunticationWithSS` | `1` | Whether the zone instance talks to the scripts server (bool). | Должен ли экземпляр зоны обмениваться данными с сервером скриптов. (тип: логический) |
| 1455 | `sv_ranksDiff` | `"-5, -2, 0, 2, 5, 10"` | Rank-difference intervals (player rank - mob rank) for open-world damage scaling. | Интервалы разницы рангов для масштабирования урона, список через запятую. (тип: строка) сколько Rplayer - Rmob |
| 1458 | `sv_ranksDiffCoeff` | `"-0.5, 0.2, 0.5, 0.6, 0.7, 0.8, 1"` | Damage scaling coefficients for the intervals of sv_ranksDiff. | Коэффициенты масштабирования урона в OW по разнице рангов, список через запятую. (тип: строка) цифры "в диапозонах" предыдущей таблицы |
| 1461 | `dbg_logRankDiffScaling` | `0` | Log damage-scaling parameters (bool). | Показывать ли параметры масштабирования. (тип: логический) |
| 1464 | `ai_logSquads` | `5` | AI squad logging: 1 spawn, 2 movement, 3 combat, 5 everything. | Логировать информацию squad: 1 — spawn, 2 — движение, 3 — бой, 5 — всё. (тип: целое число) |
| 1467 | `ai_convoyDefendRadius` | `300` | Distance between the player and the despawn point for convoys. | Расстояние между игроком и точкой despawn. (тип: дробное число) |
| 1469 | `sv_lootCrateScanTime` | `1` | Scan time of loot crates in open space (s). | Время сканирования loot crate в открытом космосе. |
| 1471 | `ai_kiteDistance` | `5000` | Max distance an AI squad may drift from its start point while chasing an enemy. | Максимальная дистанция, на которую AI-отряд может отходить от точки старта при преследовании врага. (тип: дробное число) |
| 1475 | `sv_dailyWinPveExpRewardCf` | `x3fw` | XP multiplier for the first PvE win of the day. | Множитель опыта за первую PvE-победу дня. (тип: дробное число) x3 FIRST WIN |
| 1477 | `sv_dailyWinPvpExpRewardCf` | `x3fw` | XP multiplier for the first PvP win of the day. | Множитель опыта за первую PvP-победу дня. (тип: дробное число) |
| 1479 | `sv_dailyWinCoopExpRewardCf` | `x3fw` | XP multiplier for the first coop win of the day. | Множитель опыта за первую coop-победу дня. (тип: дробное число) |
| 1481 | `sv_dailyWinBrawlExpRewardCf` | `x3fw` | XP multiplier for the first brawl win of the day. | Множитель опыта за первую brawl-победу дня. (тип: дробное число) |
| 1484 | `sv_aggressorMinNPCDamage` | `3000` | Damage dealt to a non-player target after which the player gets the aggressor flag. | Игрок получает статус агрессора после такого объёма урона по неигровой цели. (тип: дробное число) |
| 1486 | `sv_aggressorTimer` | `30` | Maximum value of the aggressor-flag timer (s). | Максимальное значение таймера флага агрессора. (тип: дробное число) |
| 1489 | `sv_resurrectionCreditsPrice` | `100000` | Credits price of resurrecting a player. | Цена воскрешения игрока в credits. |
| 1492 | `sv_instanceLifeTime` | `720` | Seconds after which an empty zone instance is closed. | Через это время экземпляр зоны будет закрыт, если в нём нет клиентов, в секундах. (тип: дробное число) |
| 1496 | `sv_freeSynergyRewardCf` | `0.05` | Free-synergy reward coefficient. | Коэффициент награды свободной синергии. (тип: дробное число) OW synergy |
| 1498 | `sv_freeSynergyRewardCfPremiumVessel` | `0.20` | Free-synergy reward coefficient for premium ships. | Коэффициент награды свободной синергии для premium-корабля. (тип: дробное число) |
| 1501 | `sv_freeSpaceExpMastery` | `"1.95,1.95,1.95,1.95,1.95,1.95,1.95,2.35,2.575,3.04,3.4,3.64,3.915,4.045,4.1,4.1,4.1,4.1"` | Replacement ship mastery values for free space, per rank (18 values). | Замена mastery корабля для free space, список по рангам через запятую. (тип: строка) |
| 1503 | `sv_expRate` | `"1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"` | XP multipliers per rank (18 values). | Множитель выдаваемого опыта по рангам, список через запятую. (тип: строка) |
| 1506 | `sv_freeSpaceExpRewards` | `2` | Ship XP for combat in Free Space: 0 nobody, 1 premium only, 2 everyone; also limited by zone rank and sv_freeSpaceExpCap. | Разрешает выдачу опыта кораблю за боевые действия в открытом космосе (Free Space). 0 - никому, 1 - только premium-игрокам, 2 - всем игрокам. Дополнительно опыт ограничен рангом зоны и sv_freeSpaceExpCap. (тип: целое число) |
| 1510 | `sv_expForDamageFreeSpace` | `0` | Grant XP for damage in Free Space (bool, 'fast synergy gain'). | Выдавать опыт за урон во Free Space. (тип: логический) Fast Synergy Gain |
| 1514 | `sv_randomLootDef` | `"LootCrate_Craft_paradise_Weapon20"` | Def name of the loot crate used by the random-loot system in Free Space; must be a LootCrate with isRare, otherwise random loot is disabled with a log error. | Def-имя loot crate, который используется системой случайного лута в Free Space. Указанный def должен быть сущностью типа LootCrate и иметь признак isRare; иначе случайный лут в зоне отключится с ошибкой в логах. (тип: строка) |
| 1518 | `sv_afkCheckDuration` | `3600` | Seconds without control input before an AFK kick; a huge value (e.g. 3600) effectively disables it. | Время в секундах, через которое игрок кикается за AFK, если он не присылал управляющие ввод или они не менялись. Большое значение (напр. 3600) фактически отключает AFK-кик. (тип: дробное число) |
| 1522 | `event_invasionWithBeacons` | `0` | Enable the 'Invasion with beacons' event (bool). | Включает событие «Invasion with beacons». (тип: логический) #57052 |
| 1525 | `sv_owLabelChances` | `"0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"` | Per-rank (18 values) chances of granting label marks to ships in the open world. | Шансы выдачи label-меток кораблям по рангам; строка содержит 18 значений. |
| 1529 | `ship_ufoRotateX` | `1` | Special X-axis rotation mode for UFO ships. | Особый режим поворота UFO-корабля по оси X. UFO ship controls |
| 1576 | `sv_frendlyFactionDamageCoef` | `0.25` | Damage coefficient against friendly-faction entities (0..1); affects damage only, other cvars affect relations. | Коэффициент урона по дружественным фракционным сущностям. (тип: дробное число; диапазон: 0.0f..1.0f) SC-113076 пиратский евент коэффициент урона дружественным фракциям в ОМ, данный параметр влияет на урон, остальные только на отношение |
| 1580 | `sv_enemyMinFactionNPCDamage` | `6` | Damage to non-player faction targets after which the faction becomes the player's enemy. | Игрок становится врагом фракции после такого объёма урона по неигровой фракционной цели. (тип: дробное число) значение счётчика урона, после которого фракция становится врагом игроку |
| 1583 | `sv_factionBadRelationshipTime` | `45` | Seconds during which the faction stays hostile after the player hit its NPCs. | Время, на которое у игрока портятся отношения с фракцией после урона по её NPC. время в секундах, в течение которого фракция будет врагом игроку |
| 1587 | `sv_enemyMaxFactionNPCDamage` | `100` | Max accumulated damage value for a faction-relation group (does not change real damage). | Максимальная сумма урона для группы отношений с фракцией; не влияет на фактический урон по сущностям. (тип: дробное число) максимальное значение счётчика урона от игрока |
| 1590 | `sv_enemyMaxFactionNPCDamagePerSec` | `1` | Max damage per second counted for a faction-relation group. | Максимальный урон в секунду для группы отношений с фракцией; не влияет на фактический урон по сущностям. (тип: дробное число) ограничение счётчика урона, накапливаемого за одну секунду |
| 1593 | `sv_factionNPCDamageDecay` | `0.2` | Decay rate of accumulated faction-NPC damage per second. | Скорость снижения накопленного урона по фракционным NPC для расчёта враждебности. уменьшение счётчика урона за секунду |
| 1596 | `sv_autorecordReplaysTo` | `""` | Directory for dedicated-server replays; empty = disabled. | Путь для сохранения replay dedicated-сервера. (тип: строка) |

## GameRewardDispencer

Function `ConfigureGRD()`, dispatched when `service_type == "ST_GAME_REWARD_DISPENCER"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 1603 | `reward_bonusGoldForWinner` | `0` | Bonus gold given to battle winners. | Если задано, добавляет bonus gold победителям боя. (тип: целое число) |
| 1605 | `reward_bonusGoldForLooser` | `0` | Bonus gold given to battle losers. | Если задано, добавляет bonus gold проигравшим боя. (тип: целое число) |
| 1609 | `reward_eventGoldTimePeriod` | `"2025-09-02T12:00:00Z;2025-09-11T06:00:00Z"` | Period of the 'gold for first and fifth win' event: 'start;end' ISO-8601. | Период события «gold за первую и пятую победу» в формате 2013-04-12T12:00:00Z;2013-04-13T12:00:00Z. (тип: строка) event 'gold for first and fifth win' |
| 1611 | `reward_eventGoldTimeValue` | `"0;0;0;0;50;0;0;0;0;100;0;0;0;0;150;0;0;0;0;200"` | Event gold amounts per win slot, ';'-separated. | Размер награды события «gold за первую и пятую победу» в формате 500;0;0;0;5000. (тип: строка) |
| 1614 | `cron_enabled` | `1` | Enable the scheduler (cron) service. | Включает планировщик. (тип: целое число) |
| 1617 | `store_creditsEventStart` | `creditsEventStart` | Start time of the credits event (ISO-8601 string). | Время начала события с кредитами. (тип: строка) |
| 1619 | `store_creditsEventEnd` | `creditsEventEnd` | End time of the credits event (ISO-8601 string). | Время окончания события с кредитами. (тип: строка) |
| 1622 | `sv_tokenCreditsDailyLimit` | `1000` | Daily limit of token credits (Iridium) a player can earn. | Дневной лимит token credits, которые игрок может заработать за день. |
| 1626 | `reward_leaveCounterMax` | `12` | Maximum value of the leave counter. | Максимальное значение leaveCounter. (тип: дробное число; диапазон: 0.0f..FLT_MAX) SC-113769 |

## LoadBalancer

Function `ConfigureLoadBalancer()`, dispatched when `service_type == "ST_LOAD_BALANCER"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 1633 | `lb_disallowAccess` | `0` | 1 = refuse access to the server (maintenance). | Включение запрещает доступ к серверу. (тип: целое число) |
| 1636 | `lb_limitPlayersOnShardTo` | `800` | Max players per shard. | Максимальное количество игроков на каждый shard. (тип: целое число) |
| 1639 | `lb_avgTimeMinClamp` | `10` | Average queue time never goes below this. | Среднее время постановки в очередь не опускается ниже этого значения. (тип: дробное число) |
| 1641 | `lb_avgTimeAveragingCf` | `10` | Number of last queued players used for the average time. | При расчёте среднего времени учитывается столько последних игроков в очереди. (тип: целое число) |
| 1644 | `lb_minNextPlayerDelay` | `0.05` | Load-balancer throttle: minimum delay between admitting players. | Параметр балансировщика нагрузки: ограничивает задержки и длину очерей на shard. |
| 1646 | `lb_maxTaskQLenOnShard` | `500` | Load-balancer throttle: max task-queue length on a shard. | Параметр балансировщика нагрузки: ограничивает задержки и длину очерей на shard. |

## ChatServer

Function `ConfigureChatServer()`, dispatched when `service_type == "ST_CHAT_SERVER"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 1659 | `antispam_autobanSec` | `60` | Chat ban duration for spammers (s). | Длительность бана нарушителя. (тип: целое число) |
| 1663 | `antispam_autobanAwareness` | `500` | Awareness threshold above which a player is auto-banned in chat. Awareness grows with frequent/repeated messages and decays over time. | Порог показателя awareness, при превышении которого игрок автоматически банится в чате. Awareness - накопительный показатель уровня спама: растёт, если игрок пишет часто и повторяется, и постепенно снижается со временем при перерывах. (тип: целое число) |
| 1666 | `antispam_notifyAwareness` | `450` | Awareness threshold at which the user is warned to stop spamming. | Порог awareness для уведомления пользователя о прекращении спама. (тип: целое число) |
| 1669 | `antispam_notifyExtended` | `0` | Send the extended notification (bool). | Включает отправку расширенного уведомления. (тип: целое число) |
| 1672 | `antispam_awarenessDecay` | `10` | Awareness decrease per second. | Уменьшается на это значение в секунду. (тип: дробное число) |
| 1676 | `antispam_awarenessIntervalNumerator` | `40` | Numerator A of the frequency term: gain = A/dt (dt = seconds since last message, min 0.5). | Числитель A в формуле прироста awareness по частоте сообщений: прирост = A / dt. dt - время в секундах с прошлого сообщения (минимум 0.5 сек); большее A - быстрее растёт awareness при частых сообщениях. (тип: дробное число) |
| 1682 | `antispam_awarenessSimilarityMul` | `1` | Factor K of the similarity term: gain = K*similarity^P (similarity = share of the message matching previous ones). | Коэффициент K в формуле прироста awareness по похожести сообщений: прирост = K * similarity ^ P. (тип: дробное число) Прирост начисляется при каждом новом сообщении. similarity - доля текста текущего сообщения, совпадающая с предыдущими: сумма длин совпадающих подстрок (длиннее 2 символов) из предыдущих сообщений, делённая на длину текущего сообщения. |
| 1684 | `antispam_awarenessSimilarityPow` | `1` | Exponent P of the similarity term. | Степень P в формуле прироста awareness по похожести сообщений: прирост = K * similarity ^ P. (тип: дробное число) |
| 1688 | `antispam_trade_autobanSec` | `60` | Trade chat: ban duration (s). | Длительность бана нарушителя. (тип: целое число) Trade Chat |
| 1691 | `antispam_trade_autobanAwareness` | `200` | Trade chat: auto-ban threshold. | Awareness - накопительный показатель уровня спама: растёт, если игрок пишет часто и повторяется, и постепенно снижается со временем при перерывах. Тот же порог автобана, но для trade-канала. (тип: целое число) |
| 1693 | `antispam_trade_notifyAwareness` | `150` | Trade chat: warning threshold. | Порог awareness для уведомления пользователя о прекращении спама. (тип: целое число) |
| 1695 | `antispam_trade_notifyExtended` | `0` | Trade chat: extended notification. | Включает отправку расширенного уведомления. (тип: целое число) |
| 1697 | `antispam_trade_awarenessDecay` | `10` | Trade chat: awareness decay per second. | Уменьшается на это значение в секунду. (тип: дробное число) |
| 1700 | `antispam_trade_awarenessIntervalNumerator` | `100` | Trade chat: numerator A of the frequency term. | Числитель A в формуле прироста awareness: прирост = A / dt (dt в секундах, мин 0.5). Большее A - быстрее растёт awareness при частых сообщениях; тот же параметр, что и antispam_awarenessIntervalNumerator. (тип: дробное число) |
| 1703 | `antispam_trade_awarenessSimilarityMul` | `1` | Trade chat: factor K of the similarity term. | Коэффициент K в формуле прироста awareness по похожести сообщений: прирост = K * similarity ^ P. Тот же параметр, что и antispam_awarenessSimilarityMul, но для trade chat. (тип: дробное число) |
| 1706 | `antispam_trade_awarenessSimilarityPow` | `1` | Trade chat: exponent P of the similarity term. | Степень P в формуле прироста awareness по похожести сообщений: прирост = K * similarity ^ P. Тот же параметр, что и antispam_awarenessSimilarityPow, но для trade chat. (тип: дробное число) |

## Universe

Function `ConfigureUniverse()`, dispatched when `service_type == "ST_UNIVERSE"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 1714 | `universe_unid` | `2` | Id of the Universe in use (1..65535). | Идентификатор используемой Universe. (тип: целое число; диапазон: 1..65535) |
| 1717 | `universe_newYearStartTime` | `"2018-12-17T00:00:00Z"` | Start time of the New Year event (ISO-8601, 'NY2016 params'). | Время начала новогоднего события. (тип: строка) NY2016 params |
| 1719 | `universe_empireKillsCF` | `0` | Growth rate of the Empire kills counter. | Скорость роста счётчика убийств Empire. (тип: дробное число) |
| 1721 | `universe_federationKillsCF` | `0` | Growth rate of the Federation kills counter. | Скорость роста счётчика убийств Federation. (тип: дробное число) |
| 1723 | `universe_jerichoKillsCF` | `0` | Growth rate of the Jericho kills counter. | Скорость роста счётчика убийств Jericho. (тип: дробное число) |
| 1725 | `universe_factorOwnerInReward` | `0.4` | Share of a zone's reward given to the current owner; the rest is split among rivals (0..1). | Доля награды зоны, которая достаётся текущему владельцу; оставшаяся доля распределяется между соперниками. (тип: дробное число 0..1) |
| 1727 | `universe_decayOwner` | `0.25` | Share of the owner's accumulated influence removed at conflict start (0..1). | Доля накопленного влияния владельца зоны, которая списывается в начале конфликта. (тип: дробное число 0..1) |
| 1729 | `universe_decayRival` | `0.1` | Share of rivals' accumulated influence removed at conflict start (0..1). | Доля накопленного влияния соперников, которая списывается в начале конфликта. (тип: дробное число 0..1) |
| 1732 | `universe_takeOwnerCoeffA` | `2` | Coefficient A of the owner-penalty formula: rival contribution = influence/(A*place+B), place counted from 0. | Коэффициент A в формуле штрафа владельца по итогам конфликта: вклад соперника = влияние / (A * место + B), место считается с 0. (тип: дробное число) 1/3, 1/5, 1/7... |
| 1734 | `universe_takeOwnerCoeffB` | `3` | Coefficient B of the same formula. | Коэффициент B в формуле штрафа владельца по итогам конфликта: вклад соперника = влияние / (A * место + B), место считается с 0. (тип: дробное число) |
| 1737 | `universe_decayIdle` | `0.5` | Share of accumulated influence removed after a conflict in which no new influence was added (0..1). | Доля накопленного влияния, которая списывается после конфликта без нового влияния за время конфликта. (тип: дробное число 0..1) SC-111290 |
| 1742 | `war_coeffAssist` | `0.2` | Global war: multiplier for assisting participants (final killer gets 1). | Параметры глобальной войны: настраивают формулы начисления военного опыта и урона корпорации. Базовая формула события: raw = множитель_убийства * множитель_цели; затем raw переводится в опыт и урон отдельными коэффициентами. Множитель для участников, которые помогли убить цель, но не нанесли финальный удар. Финальный убийца получает множитель 1. (тип: дробное число 0..1) |
| 1744 | `war_coeffRivalA` | `1` | Global war: A in target multiplier = A*victimRank + B for a rival-corporation target. | Коэффициент A для цели-врага в формуле множителя цели: множитель = A * ранг_жертвы + B. (тип: дробное число) |
| 1746 | `war_coeffRivalB` | `2` | Global war: B of the same formula. | Коэффициент B для цели-врага в формуле множителя цели: множитель = A * ранг_жертвы + B. (тип: дробное число) |
| 1748 | `war_coeffNeutral` | `0.1` | Global war: target multiplier when the victim is not at war with the attacker's corporation. | Множитель цели, если жертва не состоит в войне с корпорацией атакующего. (тип: дробное число) |
| 1750 | `war_coeffBot` | `0.05` | Global war: target multiplier for a bot replacing a real player. | Множитель цели для bot-заменителя вместо реального игрока. (тип: дробное число) |
| 1752 | `war_damageRawRateToMilitaryExp` | `10` | Conversion of raw event points to military-rank progress. | Коэффициент пересчёта raw-очков события в прогресс военного звания игрока. (тип: дробное число) |
| 1754 | `war_damageRawRateToDamage` | `100` | Conversion of raw event points to corporation damage on the global map. | Коэффициент пересчёта raw-очков события в урон корпорации на глобальной карте. (тип: дробное число) |
| 1756 | `war_decayCostBase` | `0.1` | Periodic decrease of the base war cost, applied as multiplier 1 - value (0..1). | Доля периодического уменьшения базовой стоимости войны; применяется как множитель 1 - значение. (тип: дробное число 0..1) |
| 1760 | `universe_allowExternalControl` | `1` | Allow an external service to control zone logic; when disabled the server neither starts/ends conflicts nor accepts contributions (bool). | Разрешает внешнему сервису управлять логикой зон: при отключённой логике зоны сервер сам не запускает/завершает конфликты и не принимает вклад. (тип: булево значение) SC-112644 |
| 1763 | `universe_raceFactorStellar` | `0.1` | Clan influence bonus when its race matches the dominant race of the stellar system; multiplier = 1 + value. | Доля бонуса к влиянию клана в зоне, если раса клана совпадает с доминирующей расой звёздной системы; множитель = 1 + значение. (тип: дробное число 0..1) |
| 1765 | `universe_raceFactorZone` | `0.1` | Clan influence bonus when its race matches the zone's race; multiplier = 1 + value. | Доля бонуса к влиянию клана в зоне, если раса клана совпадает с расой самой зоны; множитель = 1 + значение. (тип: дробное число 0..1) |

## QuestServer

Function `ConfigureQuestServer()`, dispatched when `service_type == "ST_QUEST_SERVER"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 1774 | `quests_enable` | `1` | Enable quests (bool). | Включает/выключает квесты. (тип: логический) |
| 1776 | `event_newYear` | `"2030-12-17T00:00:00Z"` | Start time of the New Year event (ISO-8601). | Время начала новогоднего события. (тип: строка) |
| 1778 | `quests_readWaveMaxUids` | `100` | Max number of UIDs loaded per DB read operation (1..1024). | Максимальное число UID для загрузки в операции чтения БД. (тип: целое число; диапазон: 1..1024) |
| 1781 | `quests_dbgLog` | `31` | Quest debug-log bitmask: 1 caching, 2 availability, 4 user state, 8 quest selection, 16 progress; 31 = all. | Битовая маска логирования debug-сообщений квестов: сложением значений включаются нужные категории. 1 - кэширование; 2 - доступность квестов; 4 - состояние пользователя; 8 - выбор квестов; 16 - прогресс квестов. 31 - все категории. (тип: целое число) |
| 1783 | `event_summer` | `0` | Enable the summer event (int). | Включает летнее событие. (тип: целое число) |
| 1785 | `event_summerShip` | `0` | Enable the summer ship event (int). | Включает летнее событие с кораблём. (тип: целое число) |
| 1787 | `event_halloween` | `0` | Enable the Halloween event (int). | Включает событие Halloween. (тип: целое число) |
| 1791 | `event_custom` | `event_custom` | Start time of the custom event (ISO-8601); start and end must be whole hours or the 'imaginary' quest may misbehave. | Время начала кастомного события. (тип: строка) Необходимо изменять время начала и конца кратно часу, иначе квест imaginary может вести себя непредсказуемо. |
| 1796 | `quests_imaginaryRewardCoeffA` | `25` | Imaginary-quest diminishing reward: amount = floor((A-1)*(1-tanh(B*(completions-1)))+1); A = initial reward. | Коэффициенты формулы убывающего вознаграждения за imaginary-квесты: количество = floor((A - 1) * (1 - tanh(B * (прохождений - 1))) + 1), где «прохождения» - сколько раз игрок уже выполнил этот квест. Коэффициент A: начальная величина награды при первом прохождении; с ростом числа прохождений награда убывает до 1. (SC-109926; тип: дробное число) |
| 1798 | `quests_imaginaryRewardCoeffB` | `0.17` | Speed of reward decay with completions; larger = faster. | Коэффициент B: скорость убывания награды с ростом числа прохождений; большее B - быстрее падает награда. (SC-109926; тип: дробное число) |
| 1801 | `store_creditsEventStart` | `creditsEventStart` | Start time of the credits event (ISO-8601 string). | Время начала события с кредитами. (тип: строка) |
| 1803 | `store_creditsEventEnd` | `creditsEventEnd` | End time of the credits event (ISO-8601 string). | Время окончания события с кредитами. (тип: строка) |

## AchievementServer

Function `ConfigureAchievementServer()`, dispatched when `service_type == "ST_ACHIEVEMENT_SERVER"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 1814 | `achievements_enable` | `1` | Enable server-side achievement processing. | Включает серверную обработку достижений. |
| 1816 | `achievements_readWaveMaxUids` | `100` | Max number of UIDs loaded per DB read (1..256). | Максимальное число UID для загрузки в операции чтения БД. (тип: целое число; диапазон: 1..256) |
| 1819 | `achievements_dbgLogEnable` | `0` | Extra achievement debug logging (bool). | Уровень/флаг отладочного логирования. (тип: логический) дополнительное логирование |

## LobbyServer

Function `ConfigureLobbyServer()`, dispatched when `service_type == "ST_LOBBY_SERVER"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 1828 | `lobby_enabled` | `1` | Enable the custom-games (lobby) server. | Включает сервер пользовательских игр. |
| 1830 | `lobby_rewardRates` | `1` | Multiplier applied to rewards of custom games. | Награды за пользовательские игры умножаются на это значение. (тип: дробное число) |
| 1832 | `lobby_reqPlayersPvEMin` | `3` | Minimum players to start a PvE lobby. | Минимум/максимум игроков для запуска PvE-lobby. |
| 1834 | `lobby_reqPlayersPvEMax` | `4` | Maximum players of a PvE lobby. | Минимум/максимум игроков для запуска PvE-lobby. |
| 1837 | `store_maxUniqueModules` | `3` | Max number of identical unique modules per regular ship. | Лимит одинаковых unique-модулей на один корабль; отдельно задаётся для обычных и premium-кораблей. #85547 |
| 1840 | `store_maxUniqueModulesOnPremium` | `2` | Max identical unique (experimental) modules on premium/DLC ships. | Лимит одинаковых unique-модулей на один корабль; отдельно задаётся для обычных и premium-кораблей. #0098493: Сделать возможнсть установки экспериментальных модулей на прем. и ДЛЦ корабли в кол-ве 1 шт |

## ZoneCoordinator

Function `ConfigureZoneCoordinator()`, dispatched when `service_type == "ST_ZONE_COORDINATOR"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 2104 | `zc_enableZoneBlocks` | `0` | Block zones on the raid schedule: ZoneCoordinator passes the flag to zone instances; in FreeSpace a raid zone is picked by schedule and jumps into it are forbidden. | Включает блокировку зон по расписанию raid: ZoneCoordinator передаёт флаг в запускаемые ZoneInstance и в уже работающие инстансы. Внутри FreeSpace по текущему расписанию выбирается raid-зона, и переходы/джампы в эту зону запрещаются. (тип: целое число) |

## Tournament

Function `ConfigureTournament()`, dispatched when `service_type == "ST_TOURNAMENT"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 2113 | `tournament_idOffset` | `0` | Offset of tournament team-name numbers in the UI (client uses string single_tournament_name_N). | Смещение номеров имён турнирных команд в UI: клиент прибавляет это значение к номеру имени и берёт строку single_tournament_name_N. Позволяет сдвинуть набор отображаемых имён команд без изменения их реальных teamId. (тип: целое число) |
| 2116 | `tournament_levels` | `"s1338_devilsjaw;s1338_pandora_dreadnwreck;s1340_thar_aliendebris13;s1420_ceres3_asteroidcity;s1420_ceres3_northmsite;s8256_thar_barrierdebris;s8256_thar_lavastone;s8256_thar_threshold;desttown"` | Semicolon-separated list of tournament maps. | Уровни/карты турнира. (тип: строка) ;s1338_pandora_anomaly глючит |
| 2118 | `tournament_battleRank` | `17` | Tournament battle rank (copied to sv_mmBattleRank). | Боевой ранг турнира; копируется в sv_mmBattleRank. (тип: целое число; диапазон: 0..ai::MAX_SHIP_RANK) |
| 2120 | `tournament_gamemode` | `12` | Tournament gameplay id (12 = TDM). | Игровой режим турнира. (тип: целое число; диапазон: ai::GT_SPACE_BATTLE..ai::GT_MISSION_SCRIPT - 1) |
| 2122 | `tournament_teamSize` | `8` | Max team size in tournaments. | Максимальный размер команды в турнире. (тип: целое число; диапазон: 1..MAX_TOURNAMENT_TEAM_SIZE) |
| 2124 | `tournament_gameInterval` | `2000` | Interval between game creations in ms (50..10000). | Интервал между созданием игр в миллисекундах. (тип: целое число; диапазон: 50..10000) |

## ClanServer

Function `ConfigureClanServer()`, dispatched when `service_type == "ST_CLAN_SERVER"`.

| Line | CVar | Default | English | Original comment (RU) |
|---:|---|---|---|---|
| 2133 | `clan_shipPartsCanBuild` | `4` | Number of main clan-ship (dreadnought) parts that can be built (0..4 stages). | Количество основных частей кланового корабля, доступных для строительства. (тип: целое число) (0,1,2,3,4) этапы строительства дредноута |
| 2136 | `clan_shipUpgradeCanBuild` | `3` | Number of clan-ship module-upgrade stages available (0..3 = T3, T4, T5). | Максимальное количество апгрейдов модулей кланового корабля, доступных для строительства. (тип: целое число) (0,1,2,3) этапы апгрейдов дредноута (Т3,Т4,Т5) |
| 2139 | `clan_shipBuildHighRanks` | `3` | Number of high-rank (rank 9) members a clan needs to build the clan ship. | Количество высокоранговых участников клана, необходимое для строительства кланового корабля. (тип: целое число) кол-во человек в клане 9 ранга |
| 2142 | `clans_historyMinResourceAddByZone` | `10` | Minimum zone resource amount that is written to clan history (avoid log spam). | Минимальное количество ресурса из зоны для записи в историю клана. (тип: целое число) Если с зоны пришло меньше иррисок - не спамить в лог корпы. |
| 2144 | `clan_warWinRewardAura` | `'Bundle_ClanWar_Win'` | Reward aura/bundle for winning a clan war. | Награда за победу в войне. (тип: строка) |


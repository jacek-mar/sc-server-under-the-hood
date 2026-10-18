> Перевод с английского. Источник: 04-installation/troubleshooting.md @ 92208619bfea79166f541d909f34c1ec89dc8688, 2026-10-18.
>
> При расхождении верен английский текст.

Легенда: *(official)* — официально; *(observed)* — наблюдалось; *(community)* — сообщество; *(inferred)* — вывод; *(file)* / *file-verified* — по файлам; *static* — статический анализ; ⚠ — не проверено. Исходные метки достоверности сохранены.

# Устранение неполадок

> Статус: **черновик этапа 1.** Симптомы собраны по сообщениям сообщества и
> собственным журналам аналитика. Добавляйте новые пункты по шаблону внизу.

| Симптом | Вероятная причина | Решение |
|---------|--------------|-----|
| Не удаётся войти сразу после запуска | Службы ещё запускаются (~40–90 с; Universe/Adventure — по ~15 с) | Подождите; следите за `Hub/logs/hub_*.log` |
| Ошибка подбора боя («MM fail») | Служба завершилась аварийно или Mongo не готова | Перезапустите сервер (сообщение сообщества); проверьте `matchmaker_*.log` |
| MongoDB не запускается / окно закрывается | Нет каталога данных, второй `mongod` использует тот же каталог или порт, мало места для журнала либо некорректное завершение | Выполните `mongod.exe --dbpath "<folder>"` в консоли и найдите сообщение в таблице ниже |
| Графический клиент Mongo не подключается | Современный клиент/драйвер не поддерживает протокол MongoDB 2.6 | Используйте старую программу (NoSQLBooster ≤ 4.7.5 / MongoBooster 3.5.x) |
| Изменённые значения в БД возвращаются обратно | Сервер/игра работали и перезаписали их | Остановите клиент **и** сервер (Mongo может работать), внесите изменения, перезапустите |
| Изменения данных Lua не влияют на службы | Службы читают сгенерированный XML | Выполните `cloud/prepare_shared.bat` (Mongo должна работать), перезапустите cloud |
| `NetSocket::Send … error 10053` / отключения `reason 5` в журнале Hub | Возникает у каждой службы сразу после регистрации при запуске *(observed)*; смысл ещё не разобран (вероятно, согласование соединения/переподключение) | Само по себе не является сбоем; исследуйте, только если служба так и не остаётся зарегистрированной |
| `Hub has already exited; leaving MongoDB and Redis running` | Клиент завершился после Hub; информационное сообщение | Ничего делать не нужно |
| После боя добыча «не найдена» | `sv_lootFailChance` | Задайте `0` в `ConfigureDediServer()` (в поставляемом файле уже `0` — проверьте свою копию) |
| Нет рейтингов | Redis не настроен | См. [быстрый запуск, §6](quick-start.md#6-optional-leaderboards-redis) |
| Запуск зависает / некоторые службы не регистрируются; за другими окнами может скрываться запрос брандмауэра Windows | Запрос Windows Defender Firewall для каждого нового пути к исполняемому файлу (observed, V-8) | Ответьте на запросы (частная сеть) или заранее создайте правила; затем перезапустите узел |
| После запуска остаются лишь некоторые службы, остальные «запускаются» и исчезают | Нехватка процессорного времени (загрузка клиента, другие приложения): Hub простаивал ≈ 60 с, и у служб истекло время регистрации *(observed)* | Сначала запустите только сервер; дождитесь, пока `/status` покажет 17 служб; затем запускайте клиент; избегайте большой фоновой нагрузки |
| В журнале Hub `Caught application terminal signal 21`, `Failed to TerminateProcess … error 5` | Закрыли консольное окно Hub/службы | Не закрывайте окна служб; останавливайте через окно Hub (WM_CLOSE) или `/quit` |
| В журнале клиента `No more loadbalancers available` / `10061` | Сервер ещё не запущен (или завершился) | Проверьте порты 3801/3802 и `Hub/logs` |
| Hub, службы и Mongo работают после закрытия клиента | Клиент не останавливает запущенный им локальный сервер *(observed)* | Остановите вручную (см. [журнал проверок](https://github.com/jacek-mar/sc-server-under-the-hood/blob/92208619bfea79166f541d909f34c1ec89dc8688/docs/04-installation/verification-log.md#clean-shutdown-verified)) |
| Игроки из локальной сети не могут подключиться | `cloud.xml` всё ещё указывает на `127.0.0.1` | Задайте локальный/публичный адрес; откройте порты |
| Диалог ошибки «<Service>: Memory leak detected. Amount: N, size: M byte», после которого Hub или служба перестаёт отвечать | Процедура статистики памяти движка сообщает об оставшихся выделениях через **модальное** окно `MessageBoxA` (`MB_ICONERROR` + `MB_SERVICE_NOTIFICATION`), только без подключённого отладчика; служба ждёт закрытия диалога *(static; trigger - shutdown or a statistics dump - not pinned down)*. Текст есть во всех 21 исполняемом файле служб | Закройте диалог (OK) — он может находиться за другими окнами или на рабочем столе скрытого окна службы; затем корректно перезапустите узел. Сообщите имя службы и время; это симптом, а не причина |
| Критическая ошибка «can't initialize file server. Two or more files within packages are the same.» | Два архива `.pak` содержат один путь (оставшиеся или добавленные пакеты) *(static)* | Удалите лишний пакет или проверьте файлы игры в Steam; обычный файл с тем же путём, что у упакованного, **не** вызывает эту ошибку ([data-files](https://github.com/jacek-mar/sc-server-under-the-hood/blob/92208619bfea79166f541d909f34c1ec89dc8688/docs/05-configuration/data-files.md), «Какая копия имеет приоритет») |
| «Server under heavy load» на экране входа | Текст клиента для входа, ожидающего в очереди (`login_connecting_desc`), — вход не завершается *(static)* | Службы (ещё) не запущены, остался запущенный клиентом сервер от предыдущего сеанса или неудачная правка конфигурации — проверьте журналы служб |
| Отряд/крыло застревает на загрузке арены PvP или после изменения очередей нет ботов | Открытый вопрос — сообщалось без решения | См. [открытые вопросы](https://github.com/jacek-mar/sc-server-under-the-hood/blob/92208619bfea79166f541d909f34c1ec89dc8688/docs/08-reverse-engineering/open-questions.md) |

## MongoDB не запускается — сообщения поставляемой MongoDB 2.6.12

Запустите `mongod.exe` вручную в консоли (`mongod.exe --dbpath "<folder>"`
из `cloud/mongodb`), чтобы окно не закрывалось, затем найдите сообщение.
Тексты взяты из поставляемого `mongod.exe` *(static, 2026-10-14)*;
точные строки журнала для каждой причины ещё предстоит проверить в лаборатории (MS-1).

| Сообщение (фрагмент) | Причина | Решение |
|---|---|---|
| `ERROR: dbpath (<folder>) does not exist` … `give existing directory in --dbpath` | Каталог данных отсутствует — `launch.bat` использует `%LOCALAPPDATA%\Targem\StarConflict\cloud\mongodb\data`, в старой установке данные могут лежать в другом месте | Создайте каталог или передайте правильный `--dbpath` |
| `Unable to create/open lock file: …mongod.lock` … `Is a mongod instance already running?` | Другой `mongod` использует тот же каталог — часто тот, что запустился вместе со Steam (`local_server.xml`) | Закройте другой экземпляр (`Ctrl+C` в его окне) или отключите автозапуск из клиента |
| `addr already in use` | Другая программа (часто другой `mongod`) слушает порт 27017 | То же, либо другой `--port` (тогда службам нужен `db_mongoHosts`) |
| `Insufficient free space for journal files` … `or use --smallfiles` | 64-разрядная сборка заранее выделяет файлы журнала (около 3 × 1 ГБ), и ей нужно свободное место | Освободите место или добавьте `--smallfiles` (меньшие файлы журнала и данных) — по сообщениям игроков это помогает |
| `Unclean shutdown detected.` … `Please visit http://dochub.mongodb.org/core/repair` | Предыдущее завершение было некорректным, и восстановление по журналу не удалось | Восстановите резервную копию или выполните `--repair` на **копии** каталога |
| `exception in initAndListen …, terminating` / `dbexit` | Общая последняя строка после любой ошибки выше | Прочитайте предшествующую строку |

## «Невозможно вступить в бой» — сообщения отказа MatchMaker

Когда MatchMaker отклоняет запрос на очередь, он возвращает код результата
вступления (`MasterServer.MMJoinResult`, см.
[masterserver-enums](https://github.com/jacek-mar/sc-server-under-the-hood/blob/92208619bfea79166f541d909f34c1ec89dc8688/docs/08-reverse-engineering/masterserver-enums.md)); клиент
показывает английский текст из своей таблицы строк (`mmError_<code>`).
Таблица сопоставляет видимое игроку сообщение, код и причины, подходящие
для **вручную изменённых учётных записей и конфигураций** *(message ↔ code: static, client
string table; causes: inferred unless marked)*:

| Сообщение (английский клиент) | Код | Вероятная причина после правок |
|---|---|---|
| «you can't enter a battle. Your account has a negative galactic standards balance…» | `MMJR_IN_DEBT` | `goldCredits` выше 2 147 483 647 читается как отрицательное число (знаковое 32-разрядное, Q52) — задайте меньшее значение при остановленном Hub |
| «ships of all pilots in the battle have to match the location's tech level.» | `MMJR_VESSEL_TIER_INAPPROPRIATE` | Технологический уровень корабля вне диапазона локации (открытый мир / Завоевание секторов); это «tech level» из сообщений сообщества |
| «ships in your combat slots do not meet rank requirements.» / «…don't fit mission conditions.» | `MMJR_VESSEL_RANK_INAPPROPRIATE(_PVE)` | Ранги кораблей в боевых слотах вне диапазона очереди (например, ранг 16–17 против кооперативных очередей 1–15, *file*) |
| «all ships have to be ranks $min_rank$-$max_rank$.» / «no ships of ranks …» | `MMJR_VESSEL_RANK_ALL` / `_ANY` | То же для режимов с явным диапазоном рангов |
| «the highest ship rank in combat slots should be in the range …» | `MMJR_SQUAD_RANK_DIFF` | Фильтр ранга отряда (`mmSquadRank`, Q35) |
| «the player and all pilots in the squad need clearance level $rank$ or higher.» | `MMJR_INVALID_ACCOUNT_RANK` | `accountRank` ниже требования режима |
| «unable to join the queue with damaged ships.» | `MMJR_SHIPS_BROKEN` | Корабль помечен как уничтоженный/повреждённый; вручную добавленные записи кораблей с необычными полями состояния ⚠ |
| «ship equipment failure.» | `MMJR_WRONG_EQUIPMENT` | Модуль или боеприпас не подходит корпусу (слот, размер, технологический уровень) — типично после ручных правок `vessels[].modules` ⚠ |
| «this ship is not allowed to take part in battles.» | `MMJR_FORBIDDEN_SHIP` | Корпус в `mm_forbiddenShips` / `lobby_forbiddenShips` либо предназначен только для ИИ ⚠ |
| «no ships selected for battle.» | `MMJR_NO_SHIPS_IN_BSLOTS` | Боевые слоты (`bSlot`) пусты после правки корабля |
| «you need a license.» | `MMJR_PREMIUM_REQUIRED` | Премиум истёк или произошло переполнение (Q63) |
| «the queue is not available.» | `MMJR_QUEUE_DISABLED` | Очередь отключена или недоступна по расписанию |
| «internal matchmaking error.» | `MMJR_ERROR` | Посмотрите журнал MatchMaker за это время |

Кармы среди этих кодов нет: проверок допуска по карме в Shard, MatchMaker,
ZoneCoordinator и LobbyServer не найдено (только задача сброса кармы,
`KarmaResetCost`). Полный список из 53 кодов см. в перечислениях masterserver;
журнал решений (`mm_decisionLog`) показывает сторону MatchMaker.

## Где искать

1. `Hub/logs/hub_<date>.log` — запуск/регистрация/ошибки всех служб.
2. `Hub/logs/<serviceId>_<service>_<date>.log` — журнал отдельной службы.
3. `Hub/cloud_exceptions/`, `Hub/dediserver_exceptions/` — аварийные дампы.
4. Включите `hub_detachChildProcesses 0`, чтобы видеть консоли служб.
5. Для подбора боя: `cvars.mm_decisionLog` (битовая маска, см.
   [руководство по подбору боя](https://github.com/jacek-mar/sc-server-under-the-hood/blob/92208619bfea79166f541d909f34c1ec89dc8688/docs/05-configuration/matchmaking-guide.md)).

## Шаблон сообщения

```
Environment: OS / Proton version / depot build
Start method: Steam | manual | client button
Steps:
Expected / actual:
Relevant log excerpt (service id + timestamp):
```

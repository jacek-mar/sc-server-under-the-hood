> Перевод с английского. Источник: 04-installation/quick-start.md @ 92208619bfea79166f541d909f34c1ec89dc8688, 2026-10-18.
>
> При расхождении верен английский текст.

Легенда: *(official)* — официально; *(observed)* — наблюдалось; *(community)* — сообщество; *(inferred)* — вывод; *(file)* / *file-verified* — по файлам; *static* — статический анализ; ⚠ — не проверено. Исходные метки достоверности сохранены.

# Установка и быстрый запуск

> Статус: **черновик этапа 1** — составлен по официальной странице и файлам,
> поставляемым в депо. Шаги с меткой ⚠ пока не прошли независимую
> повторную проверку в этом проекте.

## 1. Требования

| Компонент | Требование |
|------|-------------|
| ОС | Windows 10/11 x64 (Linux через Proton — см. [linux-proton.md](https://github.com/jacek-mar/sc-server-under-the-hood/blob/92208619bfea79166f541d909f34c1ec89dc8688/docs/04-installation/linux-proton.md)) |
| Игра | Клиент Star Conflict из **Steam** (серверные файлы входят в депо) |
| Диск | ≈ 12 ГБ для депо плюс данные MongoDB (≈ 0,5 ГБ заранее выделяется на набор БД) |
| ОЗУ | Весь узел — около 17 процессов по 30–80 МБ плюс MongoDB; достаточно нескольких ГБ |
| ЦП | Игровая логика в основном **однопоточная** (в каждом процессе) — частота важнее числа ядер |
| Необязательно | Redis (или совместимый сервер) для рейтингов; графический клиент MongoDB, совместимый с MongoDB 2.6 (например, NoSQLBooster ≤ v4.7.5) |

## 2. Быстрый запуск (всё на одном ПК)

1. Установите **Star Conflict** из Steam.
2. Запустите игру из Steam. Клиент запускает MongoDB и Hub
   (`win64/local_server.xml`), а Hub запускает остальные серверные приложения.
3. На экране входа оставьте выбранным **`localhost`** (по умолчанию).
4. Введите имя пользователя и пароль и нажмите *Войти*. Если такого имени
   нет, новая учётная запись создаётся автоматически.
5. Первый запуск (или запуск после изменения конфигурации) занимает время —
   дождитесь запуска всех серверных приложений, прежде чем входить.

В этой сборке закрытие клиента **не** останавливает запущенный им сервер
*(observed)*; останавливайте его, как описано в [§4](quick-start.md#4-stopping-the-server-cleanly).

## 3. Три способа запуска сервера

| Способ | Действие | Примечания |
|--------|-----|-------|
| Автоматический | Запуск через Steam | Клиент запускает Mongo и Hub и останавливает их при выходе |
| Ручной | `launch_mongodb.bat`, подождать, (запустить Redis), затем `launch_server.bat` | Рекомендуется для выделенного сервера без графического интерфейса |
| Кнопка в клиенте | «Запустить сервер» на экране входа → `win64/launch_server_and_db.bat` | Запускает Mongo, ждёт 3 с, запускает Hub — готовность Mongo не гарантируется |

Эквивалентные скрипты (как в поставке):

```bat
:: launch_mongodb.bat  (depot root)
start "" /D "%~dp0cloud\mongodb" launch.bat

:: launch_server.bat   (depot root)
start "" /D "%~dp0cloud" "Hub.exe"

:: win64\launch_server_and_db.bat
start "" /D "%~dp0..\cloud\mongodb" launch.bat
timeout /t 3
start "" /D "%~dp0..\cloud" Hub.exe
```

`cloud/mongodb/launch.bat` выполняет `mongod.exe -f ./config.cfg --dbpath
"%LOCALAPPDATA%\Targem\StarConflict\cloud\mongodb\data"`.

### Видимые окна служб

По умолчанию Hub запускает службы *отсоединёнными* (без окон). Чтобы видеть
консоль каждой службы, задайте в `cloud/data/hub.cfg`:

```
set hub_detachChildProcesses 0
```

> **Запуск без участия пользователя (проверено).** Запустите `mongod.exe` напрямую (не через `launch.bat` в скрытом окне), дождитесь открытия порта 27017, затем запустите `Hub.exe` с рабочим каталогом `cloud\`. Весь узел запускается менее чем за 90 с и использует ≈ 1,2 ГБ ОЗУ. Подробности: [журнал проверок](https://github.com/jacek-mar/sc-server-under-the-hood/blob/92208619bfea79166f541d909f34c1ec89dc8688/docs/04-installation/verification-log.md).

## 4. Корректная остановка сервера

> Проверено (см. [журнал проверок](https://github.com/jacek-mar/sc-server-under-the-hood/blob/92208619bfea79166f541d909f34c1ec89dc8688/docs/04-installation/verification-log.md#clean-shutdown-verified)): закрытие окна Hub (WM_CLOSE) останавливает Hub и все 17 служб примерно за 8 с; затем завершите MongoDB командой `mongo.exe 127.0.0.1/admin --eval "db.shutdownServer()"`. В этой сборке клиент **не** останавливает запущенный им сервер.

Ручная последовательность:

1. В **консоли Hub** выполните `/enterMaintenanceMode <minutes>`.
2. Дождитесь отключения всех клиентов.
3. Выполните `/quit` в консоли Hub.
4. Закройте MongoDB (Ctrl+C в её окне и подтверждение).
5. Закройте Redis, если он используется.

## 5. Игра с друзьями / сервер для других игроков

1. Отредактируйте `cloud/data/cloud.xml`: замените `127.0.0.1:3850` в
   `<Node address="…">` на **адрес, который должны использовать клиенты**
   (локальный или публичный IP/DNS-имя).
2. Перенаправьте/разрешите порты из [архитектуры, §4](https://github.com/jacek-mar/sc-server-under-the-hood/blob/92208619bfea79166f541d909f34c1ec89dc8688/docs/03-architecture/architecture.md#4-ports)
   (как минимум 3850, 3801, 3802 и 3815 для чата; боевые порты ещё уточняются ⚠).
3. На экране входа клиента выберите **`server`** и введите адрес и порт.
4. Прежде чем открывать доступ из Интернета, прочитайте [замечания по безопасности](https://github.com/jacek-mar/sc-server-under-the-hood/blob/92208619bfea79166f541d909f34c1ec89dc8688/docs/07-administration/administration.md#5-security) — штатная конфигурация
   **не усилена для безопасной эксплуатации**.

> Помните об условиях лицензии: без монетизации; обозначьте сервер
> как «Unofficial Server».

<a id="6-optional-leaderboards-redis"></a>

## 6. Необязательно: рейтинги (Redis)

1. Установите и запустите Redis 5.x (или совместимый сервер, например Memurai для Windows).
2. В `cloud/data/common.cfg` раскомментируйте
   `set db_redisHost "127.0.0.1:6379|connpool=5"`.
3. Добавьте команду запуска Redis в `launch_server_and_db.bat`, если нужен
   автоматический запуск. Останавливайте командой `redis-cli SHUTDOWN SAVE`.

## 7. Смена языка

Добавьте `-lang ENGLISH` (также доступны `RUSSIAN, FRENCH, GERMAN, SPANISH, POLISH,
PORTUGUESE, HUNGARIAN, CZECH, UKRAINIAN, CHINESE`) в параметры запуска Steam
или задайте `cl_language` в `%LOCALAPPDATA%\Targem\StarConflict\user_config.xml`.

## 8. Сброс всех данных

Остановите всё и удалите
`%LOCALAPPDATA%\Targem\StarConflict\cloud\mongodb\data` (а также данные Redis,
если он используется). При следующем запуске создаётся новая база данных.
Чтобы начать заново только с одной учётной записью, войдите под новым именем.

## 9. Расположение файлов

| Что | Путь |
|------|------|
| Серверные журналы | `%LOCALAPPDATA%\Targem\StarConflict\cloud\Hub\logs\` |
| Журналы клиента | `%LOCALAPPDATA%\Targem\StarConflict\logs\<timestamp>\` |
| Данные MongoDB | `%LOCALAPPDATA%\Targem\StarConflict\cloud\mongodb\data\` |
| Конфигурация клиента | `%LOCALAPPDATA%\Targem\StarConflict\user_config.xml` |
| Конфигурация сервера | `<depot>\cloud\data\` |

См. также: [устранение неполадок](troubleshooting.md).

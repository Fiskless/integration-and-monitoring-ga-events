# Трекинг событий в GA пробной недели

## Описание
Данный проект состоит из 2 скриптов:
1) tracking.py - скрипт, в котором создаются события в `Google Analytics 4`
и `Google Analytics Universal`. Скрипт использует 
[Google Sheets API](https://developers.google.com/sheets/api?hl=ru),
[Google Drive API](https://developers.google.com/drive/api?hl=ru),
[Google Ananlytics API](https://developers.google.com/analytics/devguides/config/mgmt/v3/quickstart/service-py?hl=ru).
В качестве импровизированной CRM-системы выступает Google-таблица такого [вида](https://docs.google.com/spreadsheets/d/1PYgz15M0hC6jN49fUKNluTacNkbuqmwdUF-2gYfnx5A/edit#gid=0).
Развернут в кластере `Kubernetes`. Запускается каждый час.
2) monitoring.py - скрипт, который проверяет, работает ли скрипт с указанным интервалом времени. 
Он проверяет данные в [таблице](https://docs.google.com/spreadsheets/d/1PYgz15M0hC6jN49fUKNluTacNkbuqmwdUF-2gYfnx5A/edit#gid=0). 
Ищет данные, которые не корректны после работы скрипта трекинга. В случае 
нахождения таких скрипт мониторинга делает вывод, что скрипт трекинга 
не работает по какой-либо причине, после чего падает с `exit code` = 1.

## Как развернуть скрипт по трекингу событий

Все этапы по развороту dev-версии локально и prod-версии в кластере указаны в [инструкции](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/running_tracking_script.md).

Проверка создания событий в GA4 и GAU описана в [инструкции](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/events_creating_test.md).

## Как запустить скрипт по мониторингу

Запуск необходимо выполнять после развертывания скрипта по трекингу событий, 
поскольку используется часть полученных переменных окружения, а именно `CREDENTIALS_FILE`, `SPREADSHEET_ID`.
Для запуска необходимо ввести команду в терминале:
```shell-session
$ python3 tracking.py
```

## Тестирование
Скрипт трекинга покрыт unit-тестами в файле `test.py`.
Для запуска необходимо ввести команду в терминале:
```shell-session
$ python -m unittest test.py
```
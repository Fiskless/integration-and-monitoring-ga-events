# Инструкция по запуску скрипта трекинга событий в GA4 и GAU

## Как запустить dev-версию

Для запуска скрипта у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой 
    ```sh
    pip install -r requirements.txt
    ```
- Запустите сервер командой 
    ```sh
    python3 tracking.py
    ```

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. 
Чтобы их определить, создайте файл `.env` рядом с `main.py` 
и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Используются следующие переменные окружения:
1) `API_SECRET` - секретный ключ MEASUREMENT PROTOCOL API вашего аккаунта GA4. 
Секретный ключ генерируется в интерфейсе Google Analytics. Получить его можно следующим образом:

* Перейдите в раздел **Администратор - Потоки данных**:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic1.png)

* Выберите свой веб-поток. Затем откройте раздел **О Mesurement Protocol API**:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic2.png)

* В открывшемся окне нажмите кнопку **Создать**:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic3.png)

* После ввода псевдонима нажмите кнопку **Создать**:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic8.png)

* После создания ключа он отобразится в списке доступных в столбце **Значение секретного ключа**:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic4.png)

2) `MEASUREMENT_ID` - идентификатор потока данных в GA4
Чтобы найти идентификатор потока данных Google Analytics 4:

* Перейдите в раздел **Администратор - Потоки данных**:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic5.png)

* Выберите свой веб-поток данных:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic6.png)

* В открывшемся окне скопируйте значение, указанное в правом верхнем углу в 
поле **Идентификатор потока данных**:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic7.png)

Это и есть ваш идентификатор отслеживания Google Analytics 4

3) `TID` - идентификатор отслеживания в GAU
Чтобы найти идентификатор отслеживания Google Analytics Universal:

* Перейдите в раздел **Отслеживание - Код отслеживания**:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic22.png)

* В открывшемся окне в графе **Идентификатор отслеживания** и есть ваш 
идентификатор отслеживания Google Analytics Universal

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic23.png)

4) `SPREADSHEET_ID` - id Google-таблицы, берется прямо из url-ссылки на таблицу

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/picid.png)

5) `CREDENTIALS_FILE` - переменная, в которой указан путь к json-файлу. 

В этом файле лежат данные сервисного аккаунта, через который идет 
взаимодействие с Google Drive API. Для его получения: 

* Перейдите по [ссылке](https://console.cloud.google.com/cloud-resource-manager)

* Нажмите **Create Project**:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic9.png)

* Введите название проекта и нажмите **Create**:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic10.png)

* Перейдите в **Dashboard** созданного проекта:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic11.png)

* В разделе APIs нажмите **Go to APIs overview**

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic12.png)

* Нажмите **ENABLE APIS AND SERVICES**

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic13.png)

* Необходимо подключить 2 АПИ: **Google Sheets API**  и **Google Drive API**.
В поисковом окне напишите **Google Sheets API**, после чего нажмите на **ENABLE**

* Затем вернитесь в это же поисковое окно, и напишите **Google Drive API**, после чего нажмите на **ENABLE**

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic14.png)

* Далее необходимо создать сервисный аккаунт. В открывшемся окне нажмите **CREATE CREDENTIALS**

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic15.png)

* Заполните данные как на картинке, после чего нажмите **NEXT**:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic16.png)

* Напишите имя сервисного аккаунта, после чего нажмите **CREATE AND CONTINUE**:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic17.png)

* Добавьте роль, нажмите **Role-Project-Editor**:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic18.png)

Далее нажмите **DONE**

* В открывшемся окне нажмите на ваш только что созданный сервисный аккаунт:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic19.png)

* Далее перейдите во вкладку **KEYS**, далее **ADD KEY - Create new key**.  В открывшемся окне выберите JSON и нажмите CREATE. Далее сохраните этот файл у себя на ПК.

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic21.png)

* В скачанном json файле в ключе **client_email** будет аккаунт, которому нужно будет предоставить доступ в вашей Google-таблице:

![Image alt](https://github.com/Fiskless/integration-and-monitoring-ga-events/blob/master/screenshots/pic20.png)


## Как запустить prod-версию в кластере:

Создайте фал ConfigMap.yaml такого вида:
```shell-session
apiVersion: v1
kind: ConfigMap
metadata:
  name: tracking-ga-freeweek
  labels:
    app: tracking-ga-freeweek
data:
  API_SECRET: XXXXXXXXXXX-XXXXXXXXXX
  MEASUREMENT_ID: G-XXXXXXXXXX
  TID: UA-XXXXXXXXX-X
  CREDENTIALS_FILE: some-filename.json
  SPREADSHEET_ID: 1AdfV45TYnj6jN49fUKNluTacNkbuqmwdUF-2gYfnx5A
  ROLLBAR_TOKEN: 89dsfgsdfg89f8gd9fg89df7gdf7g6dfg
  ENVIRONMENT: production
```

Создайте секрет в кластере, в котором будет находиться `some-filename.json`:
```shell-session
$ kubectl create secret generic google-api-key --from-file some-filename.json
```

Загрузите ConfigMap в кластер:
```shell-session
$ kubectl apply -f ConfigMap.yaml
```

Загрузите cronjob, который будет запускаться 1 раз в час:
```shell-session
$ kubectl apply -f tracking-cronjob.yaml
```
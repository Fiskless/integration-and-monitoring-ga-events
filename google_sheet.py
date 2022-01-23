from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'peaceful-berm-339112-8988ae360f4a.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1PYgz15M0hC6jN49fUKNluTacNkbuqmwdUF-2gYfnx5A'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A1:D4',
    majorDimension='ROWS'
).execute()
pprint(values)
exit()
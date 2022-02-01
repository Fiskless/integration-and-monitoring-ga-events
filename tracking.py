import requests
import httplib2
import apiclient.discovery
import rollbar
import sys

from contextlib import suppress
from environs import Env
from oauth2client.service_account import ServiceAccountCredentials


def create_event_to_ga4(api_secret, measurement_id, credentials_file, spreadsheet_id):

    row_number_to_session_id = get_session_ids_to_create_event(
        credentials_file,
        spreadsheet_id,
        25,
        "Z"
    )

    session_ids = row_number_to_session_id.values()
    row_numbers_for_updating_table = row_number_to_session_id.keys()

    for session_id in session_ids:

        payload = {
            'client_id': session_id,
            'events': [
                {
                    'name': 'freeweek_login',
                }
            ]
        }

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        }

        params = {
            'measurement_id': measurement_id,
            'api_secret': api_secret
        }

        response = requests.post('https://www.google-analytics.com/mp/collect',
                                 headers=headers,
                                 params=params,
                                 json=payload)

        response.raise_for_status()

    return row_numbers_for_updating_table


def create_event_to_gau(tid, credentials_file, spreadsheet_id):

    row_number_to_session_id = get_session_ids_to_create_event(
        credentials_file,
        spreadsheet_id,
        26,
        "AA"
    )

    row_numbers_for_updating_table = row_number_to_session_id.keys()

    for row_number, session_id in row_number_to_session_id.items():

        payload = {
            'v': '1',
            't': 'event',
            'tid': tid,
            'cid': session_id,
            'ec': 'course',
            'ea': 'freeweek',
            'el': 'signup',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }

        response = requests.post('https://www.google-analytics.com/collect',
                                 headers=headers,
                                 data=payload)

        response.raise_for_status()
        status_code = response.status_code

    return row_numbers_for_updating_table


def connect_to_sheets_api(credentials_file):

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    return service


def get_session_ids_to_create_event(credentials_file, spreadsheet_id,
                                    ga_column_number, column_symbol):
    service = connect_to_sheets_api(credentials_file)
    row_values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A2:AB',
        majorDimension='ROWS'
    ).execute()
    session_id_column_number = 27
    row_number_to_session_id = {}
    updating_rows_without_yes_values = []
    for row_number, students_data in enumerate(row_values['values'], start=2):
        with suppress(IndexError):
            if students_data[0] and students_data[27]:
                if students_data[ga_column_number] == 'нет' or students_data[ga_column_number] == 'Нет':
                    row_number_to_session_id[row_number] = students_data[session_id_column_number]
                elif students_data[ga_column_number] == 'да' or students_data[ga_column_number] == 'Да':
                    pass
                elif students_data[ga_column_number] == '':
                    updating_rows_without_yes_values.append(
                        {"range": f"{column_symbol}{row_number}",
                         "values": [['нет']]
                         }
                    )
                    row_number_to_session_id[row_number] = students_data[
                        session_id_column_number]
                else:
                    updating_rows_without_yes_values.append(
                        {"range": f"{column_symbol}{row_number}",
                         "values": [['Некорректное значение для ячейки, должно быть да или нет']]
                         }
                    )

    body = {
        "valueInputOption": "USER_ENTERED",
        "data": updating_rows_without_yes_values
    }
    row_values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body,
    ).execute()

    return row_number_to_session_id


def update_table_after_creating_events(credentials_file, spreadsheet_id,
                                       platform_name, api_secret=None,
                                       measurement_id=None, tid=None):

    service = connect_to_sheets_api(credentials_file)

    if platform_name == "GA4":
        column_name = "Z"
        row_number_to_update = create_event_to_ga4(api_secret,
                                                   measurement_id,
                                                   credentials_file,
                                                   spreadsheet_id)

    if platform_name == "GAU":
        column_name = "AA"
        row_number_to_update = create_event_to_gau(tid,
                                                   credentials_file,
                                                   spreadsheet_id)

    updating_row_values = []
    for row in row_number_to_update:
        updating_row_values.append({"range": f"{column_name}{row}", "values": [['да']]})
    body = {
        "valueInputOption": "USER_ENTERED",
        "data": updating_row_values
    }
    row_values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body,
    ).execute()


if __name__ == '__main__':
    env = Env()
    env.read_env()

    api_secret = env('API_SECRET')
    measurement_id = env('MEASUREMENT_ID')
    tid = env('TID')
    credentials_file = env('CREDENTIALS_FILE', '/etc/google-api/gdrive_key.json')
    spreadsheet_id = env('SPREADSHEET_ID')
    rollbar_token = env('ROLLBAR_TOKEN')
    environment = env('ENVIRONMENT', 'production')

    if environment == 'production':
        rollbar.init(rollbar_token, environment=environment)
        try:
            update_table_after_creating_events(credentials_file, spreadsheet_id,
                                               'GAU', None, None, tid)

            update_table_after_creating_events(credentials_file, spreadsheet_id, 'GA4',
                                               api_secret,
                                               measurement_id,
                                               )
        except:
            rollbar.report_exc_info(sys.exc_info())

    elif environment == 'development':

        update_table_after_creating_events(credentials_file, spreadsheet_id,
                                           'GAU', None, None, tid)

        update_table_after_creating_events(credentials_file, spreadsheet_id,
                                           'GA4',
                                           api_secret,
                                           measurement_id,
                                           )


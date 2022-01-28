import requests
import httplib2
import apiclient.discovery

from environs import Env
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials


def create_event_to_ga4(api_secret, measurement_id, credentials_file, spreadsheet_id):

    row_number_to_session_id = get_session_ids_to_create_event_ga4(
        credentials_file,
        spreadsheet_id
    )

    session_ids = row_number_to_session_id.values()
    row_numbers_for_updating_table = row_number_to_session_id.keys()

    for session_id in session_ids:

        payload = {
            'client_id': session_id,
            'events': [
                {
                    'name': 'freecourse_login_27_Jan_18_37',
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

    row_number_to_session_id = get_session_ids_to_create_event_gau(
        credentials_file,
        spreadsheet_id
    )

    row_numbers_for_updating_table = row_number_to_session_id.keys()

    for row_number, session_id in row_number_to_session_id.items():

        payload = {
            'v': '1',
            't': 'event',
            'tid': tid,
            'cid': session_id,
            'ec': 'course',
            'ea': 'freecourse',
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
        #TODO: добавить проверку по статус коду, если не 200, то написать что событие не создалось, мб в отдельной колонке, либо окрасить просто ячейку

    return row_numbers_for_updating_table


def connect_to_sheets_api(credentials_file):

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    return service


def get_session_ids_to_create_event_ga4(credentials_file, spreadsheet_id):

    service = connect_to_sheets_api(credentials_file)
    row_values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Z2:AA',
        majorDimension='ROWS'
    ).execute()
    row_number_to_session_id = {}
    for row_number, session_id_and_event in enumerate(row_values['values'], start=2):
        try:
            if session_id_and_event[1] != 'нет' or session_id_and_event[1] != 'Нет':
                row_number_to_session_id[row_number] = session_id_and_event[0]
            elif session_id_and_event[1] != 'да' or session_id_and_event[1] != 'Да':
                pass
            else:
                body = {
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": f"AA{row_number}",
                         "values": [[
                             'Некорректное значение для ячейки, должно быть да или нет'
                         ]]
                         },
                    ]
                }
                row_values = service.spreadsheets().values().batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body=body,
                ).execute()
        except IndexError:
            body = {
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"AA{row_number}",
                     "values": [['нет']]
                     },
                ]
            }
            row_values = service.spreadsheets().values().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=body,
            ).execute()
            row_number_to_session_id[row_number] = session_id_and_event[0]

    #TODO: добавить проверки на корректность заполненности ячейки, и подумать, что делать если пустая ячейка
    #TODO: проверить, что только да, нет и [], если другие значения то окрасить в красный либо выдать что ячейка заполнена некорректно.
    #TODO: если пустая ячейка, возможно надо проверить есть ли событие для этого session_id, если нет, то создать, если есть, то пропустить
    return row_number_to_session_id


def get_session_ids_to_create_event_gau(credentials_file, spreadsheet_id):

    service = connect_to_sheets_api(credentials_file)

    row_values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='AB2:AB',
        majorDimension='ROWS'
    ).execute()
    pprint(row_values['values'])
    rows_for_session_id = []
    for row_number, event in enumerate(row_values['values'], start=2):
        try:
            if event[0] == 'нет' or event[0] == 'Нет':
                rows_for_session_id.append(row_number)
            elif event[0] == 'да' or event[0] == 'Да':
                pass
            else:
                body = {
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": f"AB{row_number}",
                         "values": [['Некорректное значение для ячейки, должно быть да или нет']]
                         },
                    ]
                }
                row_values = service.spreadsheets().values().batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body=body,
                ).execute()

        except IndexError:
            body = {
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"AB{row_number}",
                     "values": [['нет']]
                     },
                ]
            }
            row_values = service.spreadsheets().values().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=body,
            ).execute()
            rows_for_session_id.append(row_number)

    # TODO: добавить проверки на корректность заполненности ячейки, и подумать, что делать если пустая ячейка
    # TODO: проверить, что только да, нет и [], если другие значения то окрасить в красный либо выдать что ячейка заполнена некорректно.
    # TODO: если пустая ячейка, возможно надо проверить есть ли событие для этого session_id.

    range_names_to_create_event_gau = []

    for row in rows_for_session_id:
        range_names_to_create_event_gau.append(f'Z{row}')

    session_id_values = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id,
        ranges=range_names_to_create_event_gau
    ).execute()

    session_ids = []

    for session_id in session_id_values['valueRanges']:
        session_ids.append(session_id['values'][0][0])

    row_number_to_session_id = dict(zip(rows_for_session_id, session_ids))

    return row_number_to_session_id


def update_table_after_creating_events(credentials_file, spreadsheet_id,
                                       platform_name, api_secret=None,
                                       measurement_id=None, tid=None):

    service = connect_to_sheets_api(credentials_file)

    if platform_name == "GA4":
        column_name = "AA"
        row_number_to_update = create_event_to_ga4(api_secret,
                                                   measurement_id,
                                                   credentials_file,
                                                   spreadsheet_id)

    if platform_name == "GAU":
        column_name = "AB"
        row_number_to_update = create_event_to_gau(tid,
                                                   credentials_file,
                                                   spreadsheet_id)

    for row in row_number_to_update:

        body = {
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"{column_name}{row}",
                 "values": [['да']]
                 },
            ]
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
    credentials_file = env('CREDENTIALS_FILE')
    spreadsheet_id = env('SPREADSHEET_ID')

    # update_table_after_creating_events(credentials_file, spreadsheet_id,
    #                                    'GAU', None, None, tid)
    #
    # update_table_after_creating_events(credentials_file, spreadsheet_id, 'GA4',
    #                                    api_secret,
    #                                    measurement_id,
    #                                    )

    get_session_ids_to_create_event_ga4(credentials_file, spreadsheet_id)
    # get_session_ids_to_create_event_gau(credentials_file, spreadsheet_id)
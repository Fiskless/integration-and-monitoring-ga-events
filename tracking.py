import requests
import httplib2
import apiclient.discovery
import http.client as httplib

from environs import Env
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials


def create_event_to_ga4(api_secret, measurement_id):

    row_number_to_session_id = get_session_id_to_create_event_ga4(
        CREDENTIALS_FILE,
        SPREADSHEET_ID
    )

    for session_id in row_number_to_session_id.values():

        payload = {
            'client_id': session_id,
            'events': [
                {
                    'name': 'freeweek_login',
                }
            ]
        }

        headers = {
            'Content-Type': 'application/json'
        }

        params = {
            'api_secret': api_secret,
            'measurement_id': measurement_id
        }

        response = requests.post(f'https://www.google-analytics.com/mp/collect',
                                 headers=headers,
                                 params=params,
                                 data=payload)

    return row_number_to_session_id.values()


def create_event_to_gau(tid):

    session_ids = get_session_id_to_create_event_gau(
        CREDENTIALS_FILE,
        SPREADSHEET_ID
    )

    for session_id in session_ids:

        conn = httplib.HTTPConnection("www.google-analytics.com")

        conn.request("POST", "/collect",
                     f"v=1&t=event&tid={tid}&cid={session_id}&&ec=freeweek&ea=freeweek_login{session_id}&el=signup")

        print(conn.getresponse().headers)

        payload = {
            'v': '1',
            't': 'event',
            'tid': tid,
            'cid': session_id,
            'ec': 'freeweek',
            'ea': f'freeweek_login{session_id}',
            'el': 'signup',
        }

        response = requests.post('https://www.google-analytics.com/collect',
                                 data=payload)
        response.raise_for_status()
        pprint(response.url)
        pprint(response.headers)

    return session_ids


def connect_to_sheets_api(credentials_file):

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    return service


def get_session_id_to_create_event_ga4(credentials_file, spreadsheet_id):

    service = connect_to_sheets_api(credentials_file)
    row_values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Z2:AA',
        majorDimension='ROWS'
    ).execute()
    row_number_to_session_id = {}
    for row_number, session_id_and_event in enumerate(row_values['values'], start=2):
        if session_id_and_event[1] != 'да':
            row_number_to_session_id[row_number] = session_id_and_event[0]
    return row_number_to_session_id


def get_session_id_to_create_event_gau(credentials_file, spreadsheet_id):

    service = connect_to_sheets_api(credentials_file)

    row_values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='AB2:AB',
        majorDimension='ROWS'
    ).execute()
    rows_for_session_id = []
    for row_number, event in enumerate(row_values['values'], start=2):
        if event[0] != 'да':
            rows_for_session_id.append(row_number)

    range_names_to_create_event_gau = []

    for row in rows_for_session_id:
        range_names_to_create_event_gau.append(f'Z{row}')

    session_id_values = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id,
        ranges=range_names_to_create_event_gau
    ).execute()

    session_ids = []

    for number, session_id in enumerate(session_id_values['valueRanges']):
        session_ids.append(session_id['values'][0][0])

    return session_ids


def update_table_after_creating_events_ga4(credentials_file, spreadsheet_id):

    service = connect_to_sheets_api(credentials_file)

    session_ids = create_event_to_ga4(api_secret, measurement_id)

    data = []

    for session_id in session_ids:
        data.append(
            {
                'range': f'AA{session_id}',
                'values': 'да'
            }
        )

    body = {
        'valueInputOption': '',
        'data': data
    }
    print(session_ids)
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

    CREDENTIALS_FILE = env('CREDENTIALS_FILE')

    SPREADSHEET_ID = env('SPREADSHEET_ID')

    update_table_after_creating_events_ga4(CREDENTIALS_FILE, SPREADSHEET_ID)

    # create_event_to_gau(tid)

    # get_session_id_to_create_event_ga4(CREDENTIALS_FILE, SPREADSHEET_ID)

    # create_event_to_ga4(api_secret, measurement_id)
    # print(add_event_to_gau(tid))




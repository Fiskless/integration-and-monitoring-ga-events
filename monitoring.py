import datetime
import pytz

from contextlib import suppress
from dateutil import parser
from environs import Env
from tracking import connect_to_sheets_api


def check_script_working_via_send_time(credentials_file, spreadsheet_id):
    service = connect_to_sheets_api(credentials_file)
    row_values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A2:AB',
        majorDimension='ROWS'
    ).execute()
    for row_number, students_data in enumerate(row_values['values'], start=2):
        with suppress(IndexError):
            if students_data[0] and students_data[27]:
                tilda_time_table_str = students_data[4]
                current_moscow_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
                time_to_test_script = current_moscow_time + datetime.timedelta(hours=2, minutes=10)
                if time_to_test_script.timestamp() > parser.parse(tilda_time_table_str).timestamp():
                    if students_data[25] != 'да' or students_data[26] != 'да':
                        raise Exception('Script is not working')


if __name__ == '__main__':
    env = Env()
    env.read_env()

    credentials_file = env('CREDENTIALS_FILE', '/etc/google-api/gdrive_key.json')
    spreadsheet_id = env('SPREADSHEET_ID')

    check_script_working_via_send_time(credentials_file, spreadsheet_id)
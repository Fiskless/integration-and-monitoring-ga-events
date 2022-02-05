import datetime
import sys

import pytz

from contextlib import suppress

import requests
from dateutil import parser
from environs import Env
from tracking_for_py_tests import connect_to_sheets_api, get_sheet_data


def check_tracking_working_via_send_time(credentials_file, spreadsheet_id):
    service = connect_to_sheets_api(credentials_file)
    row_values = get_sheet_data(service, spreadsheet_id)
    for row_number, students_data in enumerate(row_values, start=2):
        with suppress(IndexError):
            if students_data[0] and students_data[27]:
                tilda_time_table_str = students_data[4]
                current_moscow_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
                time_to_test_script = current_moscow_time + datetime.timedelta(hours=2, minutes=10)
                if time_to_test_script.timestamp() > parser.parse(tilda_time_table_str).timestamp():
                    if students_data[25] == 'Ошибка при создании события, обратитесь к программисту' or \
                            students_data[26] == 'Ошибка при создании события, обратитесь к программисту':
                        sys.exit(1)
                    if students_data[25] == 'нет' or \
                            students_data[25] == '' or \
                            students_data[26] == 'нет' or \
                            students_data[26] == '':
                        sys.exit(1)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    credentials_file = env('CREDENTIALS_FILE', '/etc/google-api/gdrive_key.json')
    spreadsheet_id = env('SPREADSHEET_ID')

    check_tracking_working_via_send_time(credentials_file, spreadsheet_id)
    
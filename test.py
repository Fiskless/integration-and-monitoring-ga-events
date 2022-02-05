import unittest
import tracking

from unittest.mock import patch

from environs import Env

env = Env()
env.read_env()

api_secret = env('API_SECRET')
measurement_id = env('MEASUREMENT_ID')
tid = env('TID')
credentials_file = env('CREDENTIALS_FILE', '/etc/google-api/gdrive_key.json')
spreadsheet_id = env('SPREADSHEET_ID')


class TestTrackingScript(unittest.TestCase):

    @patch('tracking.update_sheet_data')
    @patch('tracking.get_sheet_data')
    def test_get_session_ids_to_create_event(self,
                                             get_sheet_data_mock,
                                             update_sheet_data_mock):
        row = [
            ['1', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', '', '', '1'],
            ['2', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'да', '', '2'],
            ['3', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', '', 'да', '3'],
            ['4', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'нет', 'нет', '4'],
            ['5', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'нет', '', '5'],
            ['6', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'да', 'да', '6'],
            ['7', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'значение', 'значение', '7'],
            ['8', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'да', 'значение', '8'],
            ['9', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'значение', 'да', '9'],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'нет', 'нет', ''],
            ['11', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'нет', 'нет', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'нет', 'нет', '12'],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', '', '', ''],
            ['14', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'нет', 'нет', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'нет', 'нет', '15'],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'нет', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', '', 'нет', '17'],
            ['18', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', '', 'значение', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'значение', '', '19'],
            ['20', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', '', 'нет', '20'],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', 'значение', 'значение', ''],
        ]
        get_sheet_data_mock.return_value = row
        update_sheet_data_mock.return_value = {}
        correct_value_1_test = ({2: '1', 4: '3', 5: '4', 6: '5', 21: '20'},
                         [{'range': 'Z2', 'values': [['нет']]},
                          {'range': 'Z4', 'values': [['нет']]},
                          {'range': 'Z8',
                           'values': [['Некорректное значение для ячейки, должно быть да или нет']]},
                          {'range': 'Z10',
                           'values': [['Некорректное значение для ячейки, должно быть да или нет']]},
                          {'range': 'Z21', 'values': [['нет']]}])
        self.assertEqual(
            tracking.get_session_ids_to_create_event(
                credentials_file,
                spreadsheet_id,
                25,
                'Z'
            ),
            correct_value_1_test
        )
        correct_value_2_test = ({2: '1', 3: '2', 5: '4', 6: '5', 21: '20'},
                                [{'range': 'AA2', 'values': [['нет']]},
                                 {'range': 'AA3', 'values': [['нет']]},
                                 {'range': 'AA6', 'values': [['нет']]},
                                 {'range': 'AA8',
                                  'values': [['Некорректное значение для ячейки, должно быть да или нет']]},
                                 {'range': 'AA9',
                                  'values': [['Некорректное значение для ячейки, должно быть да или нет']]}])
        self.assertEqual(
            tracking.get_session_ids_to_create_event(
                credentials_file,
                spreadsheet_id,
                26,
                'AA'
            ),
            correct_value_2_test
        )

    @patch('tracking.create_event_to_gau')
    @patch('tracking.get_session_ids_to_create_event')
    def test_unsuccessful_request_error_message(self,
                                                get_session_ids_to_create_event_mock,
                                                create_event_to_gau_mock):
        get_session_ids_to_create_event_mock.return_value = {2: '1'}, []
        create_event_to_gau_mock.return_value.ok = False
        self.assertEqual(
            tracking.collect_data_to_update_table(
                credentials_file,
                spreadsheet_id,
                'GAU',
                26,
                'AA',
                tid
                ),
            ([{'range': 'AA2', 'values': [['Ошибка при создании события, обратитесь к программисту']]}],
               {2: '1'}.keys())
        )

    @patch('tracking.get_session_ids_to_create_event')
    def test_collect_data_to_update_table(self,
                                          get_session_ids_to_create_event_mock):
        get_session_ids_to_create_event_mock.return_value = {3: '2'}, []
        self.assertEqual(
            tracking.collect_data_to_update_table(credentials_file,
                                                               spreadsheet_id,
                                                               'GAU',
                                                               26,
                                                               'AA',
                                                               tid
                                                               ),
            ([], {3: '2'}.keys())
        )

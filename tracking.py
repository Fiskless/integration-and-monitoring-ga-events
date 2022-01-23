import requests

from environs import Env
from google_measurement_protocol import event, report


def add_event_to_ga4(api_secret, measurement_id):

    payload = {
        'client_id': '607412690.1452476467',
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

    return response.json()


def add_event_to_gau(tid):
    payload = {
        'v': '1',
        't': 'event',
        'tid': tid,
        'cid': '522',
        'ec': 'freeweek',
        'ea': 'freeweek_login1',
        'el': 'signup',
    }

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post('https://www.google-analytics.com/collect',
                             headers=headers,
                             data=payload)
    response.raise_for_status()

    return response.status_code


if __name__ == '__main__':
    env = Env()
    env.read_env()

    api_secret = env('API_SECRET')
    measurement_id = env('MEASUREMENT_ID')
    tid = env('TID')

    print(add_event_to_ga4(api_secret, measurement_id))
    # print(add_event_to_gau(tid))

    # import http.client as httplib
    #
    # conn = httplib.HTTPConnection("www.google-analytics.com")
    #
    # conn.request("POST", "/collect",
    #              "v=1&tid=UA-217725860-1&cid=666&t=event&ec=game&ea=end&ev=0")

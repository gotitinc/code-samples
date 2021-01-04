import json
import requests


HEADERS = {'Content-Type': 'application/json'}

EVENT_BUS_URL = ''
EVENT_BUS_DELAYED_URL = ''


def send_task(task):
    if task.get('delay') is None or task.get('delay') == 0:
        return requests.post(EVENT_BUS_URL, headers=HEADERS, data=json.dumps(task))
    return requests.post(EVENT_BUS_DELAYED_URL, headers=HEADERS, data=json.dumps(task))

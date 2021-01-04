import json

import requests

from eventbus.queue_deferred import queue_deferred


def send_message(url, content):
    queue_deferred(_send_message, url, content, _queue='default')


def _send_message(url, content):
    if not url:
        return

    data = {
        'text': content
    }
    return requests.post(url=url, data=json.dumps(data))

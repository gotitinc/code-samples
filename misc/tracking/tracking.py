from datetime import datetime

import requests
from .errors import EventTrackingServiceException

EVENT_NAMES = []
EVENT_TRACKING_API = ''
TRACKING_SERVICE_VERTICAL = ''
TRACKING_SERVICE_APP_NAME = ''
TRACKING_SERVICE_ENVIRONMENT = ''


def send_event(name, data):
    if name not in EVENT_NAMES:
        raise EventTrackingServiceException('Invalid event name')

    url = EVENT_TRACKING_API

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    payload = {
        'vertical': TRACKING_SERVICE_VERTICAL,
        'app': TRACKING_SERVICE_APP_NAME,
        'env': TRACKING_SERVICE_ENVIRONMENT,
        'name': name,
        'created_timestamp': int(datetime.timestamp(datetime.now()) * 1000),
        **data
    }

    response = requests.post(url=url, json=payload, headers=headers)

    if not response.ok:
        raise EventTrackingServiceException(
            message='Failed to send event to Event Tracking service',
            data={
                'url': url,
                'payload': payload,
                'response': response.json()
            }
        )

import random
import string
from flask import Flask

app = Flask(__name__)
test_app = app.test_client()


def post_data(token, url, data, origin=None,
              http_referer=None):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    if origin:
        headers['origin'] = origin
    if http_referer:
        headers['referer'] = http_referer
    return test_app.post(url,
                         headers=headers,
                         data=data,
                         content_type='application/json')


def put_data(token, url, data):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    return test_app.put(url,
                        headers=headers,
                        data=data,
                        content_type='application/json')


def delete_data(token, url, data=None):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    return test_app.delete(url, headers=headers, data=data, content_type='application/json')


def get_data(token, url, ip=None, **kwargs):
    get_url = url
    first = True
    for key, value in list(kwargs.items()):
        if key != 'headers':
            try:
                if isinstance(value, list):
                    value = ','.join(map(str, value))
                else:
                    value = str(value)
            except UnicodeEncodeError:
                value = str(value)
            if first:
                get_url += '?' + key + '=' + value
            else:
                get_url += '&' + key + '=' + value
            first = False
    headers = {'Authorization': 'Bearer {}'.format(token)}
    if ip:
        headers['X-Forwarded-For'] = ip
    if 'headers' in kwargs:
        headers.update(kwargs['headers'])
    return test_app.get(get_url, headers=headers)


def generate_random_string(num_of_chars=20):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(num_of_chars))


class ResponseMock:
    ok = True

    def __init__(self, *args, **kwargs):
        self.return_value = kwargs.get('return_value', {})
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.status_code = 200
        self.text = 'response text'

    def json(self):
        return self.return_value

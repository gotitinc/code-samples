import http.client
import json
import logging


def fetch_google_first_name_last_name(access_token):
    """
    Fetch google first name and google last name from google plus
    :return: first name, last name
    """
    try:
        conn = http.client.HTTPSConnection('www.googleapis.com')
        conn.request('GET', '/plus/v1/people/me',
                     headers={'Authorization': 'Bearer ' + access_token})
        rs = conn.getresponse()
    except http.client.HTTPException:
        logging.exception('Google API Service exception')
        return '', ''
    if rs.status == 200:
        data = json.loads(rs.read())
        if 'name' in data.keys():
            name = data.get('name')
            last_name = name.get('familyName')
            first_name = name.get('givenName')
            return first_name, last_name
    return '', ''

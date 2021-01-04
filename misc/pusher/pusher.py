import logging
import random
import pusher

PUSHER_APP_ID = ''
PUSHER_KEY = ''
PUSHER_SECRET = ''
PUSHER_CHANNEL_NAMESPACE = ''
EVENT_BUS_PARTITIONS = 1

pusher_client = pusher.Pusher(
    app_id=PUSHER_APP_ID,
    key=PUSHER_KEY,
    secret=PUSHER_SECRET
)


def parse_channel(channel_name):
    """
    Channel name format is:
    presence-<type>-<id>-<namespace>
    or presence-<type>-<namespace>
    """
    channel = channel_name.split('-')
    optional_channel_info = {}
    if len(channel) == 4:
        namespace_index = 3
        try:
            optional_channel_info.update({'id': int(channel[2])})
        except ValueError:
            return None
    else:
        namespace_index = 2
    if channel[namespace_index] != PUSHER_CHANNEL_NAMESPACE:
        return None
    return {'type': channel[1], **optional_channel_info}


def authenticate(request, member):
    channel = parse_channel(request.form['channel_name'])
    if not channel:
        return None
    auth = False
    if channel['id'] == member['id']:
        auth = True
    if not auth:
        return None
    try:
        tmp = pusher_client.authenticate(
            channel=request.form['channel_name'],
            socket_id=request.form['socket_id'],
            custom_data={
                'user_id': member['id'],
            })
    except Exception:
        logging.exception('Pusher exception')
        return None
    if tmp is None:
        logging.error('There was an error while authenticating with Pusher')
    else:
        return tmp


def validate_webhook(request):
    # See this link for more details: https://pusher.com/docs/webhooks
    key = request.headers['X-Pusher-Key']
    signature = request.headers['X-Pusher-Signature']
    try:
        response = pusher_client.validate_webhook(key, signature, request.get_data())
    except Exception:
        logging.exception('Pusher exception')
        return None

    return response


def trigger_pusher(channel_name, event_type, data):
    try:
        pusher_client.trigger(channel_name, event_type, data)
    except Exception:
        logging.exception('Pusher exception')


def _defer_trigger(channel_name, event_type, data):
    info = channel_name.split('-')
    try:
        id = int(info[2])
    except ValueError:
        id = random.randint(0, EVENT_BUS_PARTITIONS)
    core.queue_deferred(
        trigger_pusher,
        channel_name,
        event_type,
        data,
        _queue='pusher',
        _key=id
    )

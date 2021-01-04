import base64
import os
import random

from flask import request, g, has_request_context

from .delayed_deferred import defer
import event_bus


EVENT_BUS_PARTITIONS = ''
API_SERVER = ''


def queue_deferred(*args, **kwargs):
    if has_request_context():
        queue_deferred_after_request(*args, **kwargs)
    else:
        queue_deferred_eventbus(*args, **kwargs)


def queue_deferred_after_request(*args, **kwargs):
    if os.getenv('ENVIRONMENT', 'development') == 'test':
        return None

    task = _build_event_bus_task(*args, **kwargs)
    delayed_tasks = getattr(g, 'delayed_tasks', [])
    delayed_tasks.append(task)
    g.delayed_tasks = delayed_tasks


def queue_deferred_eventbus(*args, **kwargs):
    if os.getenv('ENVIRONMENT', 'development') == 'test':
        return None

    task = _build_event_bus_task(*args, **kwargs)
    event_bus.send_task(task)


def _build_event_bus_task(*args, **kwargs):
    reserved_args = ['countdown', 'eta', 'name', 'target', 'queue', 'retry_options', 'key', 'max_retry', 'timeout']
    taskargs = dict((x, kwargs.pop(('_%s' % x), None)) for x in reserved_args)
    queue = taskargs.get('queue', None)
    func = args[0]
    url = '/_ah/eb_queue/deferred_flask'
    if hasattr(func, '__name__'):
        url = url + '/{}'.format(func.__name__)
    taskargs['_url'] = url
    payload = defer(*args, **kwargs)

    key = taskargs.get('key', None)
    if key is None:
        key = random.randint(0, EVENT_BUS_PARTITIONS)

    task = {
        'payload': base64.encodestring(payload).decode(),
        'topic': queue,
        'key': str(key),
        'url': API_SERVER + url,
    }
    max_retry = taskargs.get('max_retry', None)
    if max_retry is not None:
        task['max_retry'] = max_retry
    timeout = taskargs.get('timeout', None)
    if timeout:
        task['timeout'] = timeout

    countdown = taskargs.get('countdown', None)
    if countdown:
        task['delay'] = str(countdown * 1000)
    return task
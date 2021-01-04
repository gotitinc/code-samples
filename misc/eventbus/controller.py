import base64
import logging
import pickle

from flask import request, jsonify


@app.route('/_ah/eb_queue/deferred_flask', methods=['POST'])
@app.route('/_ah/eb_queue/deferred_flask/<deferred_func>', methods=['POST'])
def run_deferred_eventbus(deferred_func='Unknown'):
    try:
        func, args, kwargs = pickle.loads(base64.decodestring(request.data))
        func(*args, **kwargs)
    except Exception as e:
        logging.exception(str(e))

    return jsonify({})

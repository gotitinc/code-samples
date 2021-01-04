from flask import jsonify, request
from . import pusher


@app.route('/pusher/auth', methods=['POST'])
def auth_pusher(member):
    response = pusher.authenticate(request, member)

    if not response:
        raise errors.Unauthorized()

    return jsonify(response)

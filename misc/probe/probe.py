@app.route('/pings', methods=['GET'])
def ping():
    return jsonify({})


@app.route('/ready', methods=['GET'])
def is_ready():
    return jsonify({})

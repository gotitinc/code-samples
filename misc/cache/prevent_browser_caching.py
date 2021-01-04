@app.after_request
def prevent_browser_caching(response):
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Pragma'] = 'no-cache'
    return response
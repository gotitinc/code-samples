from flask import jsonify
from marshmallow import fields, Schema


class ErrorSchema(Schema):
    error_code = fields.Int()
    error_message = fields.String()
    error_data = fields.Raw()


class Error(Exception):
    status_code = None
    error_code = None
    error_message = None

    def __init__(self, error_data=None):
        super(Error)
        self.error_data = error_data or {}

    def to_response(self):
        resp = jsonify(ErrorSchema().dump(self).data)
        resp.status_code = self.status_code
        return resp


class StatusCode:
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500


class ErrorCode:
    BAD_REQUEST = 40000
    VALIDATION_ERROR = 40001
    UNAUTHORIZED = 40100
    NOT_FOUND = 40400
    METHOD_NOT_ALLOWED = 40500
    INTERNAL_SERVER_ERROR = 50000


class ErrorMessage:
    BAD_REQUEST = 'Bad request.'
    UNAUTHORIZED = 'Unauthorized.'
    NOT_FOUND = 'Not found.'
    METHOD_NOT_ALLOWED = 'Method not allowed.'
    VALIDATION_ERROR = 'Validation error.'
    FORBIDDEN = 'Forbidden.'
    INTERNAL_SERVER_ERROR = 'Internal server error.'


class NotFound(Error):
    status_code = StatusCode.NOT_FOUND

    def __init__(self, code=ErrorCode.NOT_FOUND, message=ErrorMessage.NOT_FOUND, data=None):
        super(self.__class__, self).__init__(data)
        self.error_code = code
        self.error_message = message


class MethodNotAllowed(Error):
    status_code = StatusCode.METHOD_NOT_ALLOWED
    error_code = ErrorCode.METHOD_NOT_ALLOWED
    error_message = ErrorMessage.METHOD_NOT_ALLOWED


class InternalServerError(Error):
    status_code = StatusCode.INTERNAL_SERVER_ERROR

    def __init__(self, code=ErrorCode.INTERNAL_SERVER_ERROR, message=ErrorMessage.INTERNAL_SERVER_ERROR, data=None):
        super(self.__class__, self).__init__(data)
        self.error_code = code
        self.error_message = message


@app.errorhandler(404)
def page_not_found(error):
    return NotFound().to_response()


@app.errorhandler(405)
def method_not_allowed(error):
    return MethodNotAllowed().to_response()


@app.errorhandler(Error)
def error_handler(error):
    return error.to_response()

from flask import jsonify
from marshmallow import (
    Schema,
    ValidationError as MarshmallowValidationError,
    INCLUDE, post_load, fields)
from marshmallow.validate import Validator


class BaseSchema(Schema):
    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))

    class Meta:
        unknown = INCLUDE


class NotEmptyValidator(Validator):
    def __call__(self, value):
        if value.strip() == '':
            raise MarshmallowValidationError(message='Must not be empty.')


class PaginationSchema(BaseSchema):
    items_per_page = fields.Integer()
    page = fields.Integer()
    total_items = fields.Integer()


class FieldsQuerySchema(BaseSchema):
    fields = fields.String(required=False)

    @post_load
    def parse_fields(self, data, **__):
        _fields = data.get('fields', None)
        if _fields:
            data['fields'] = set(_fields.split(','))
        else:
            data['fields'] = set()

        return data

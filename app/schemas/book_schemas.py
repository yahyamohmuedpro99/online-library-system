from marshmallow import Schema, fields, validate
from datetime import datetime

class BookCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    author = fields.String(required=True, validate=validate.Length(min=1, max=100))
    category = fields.String(required=True)
    price = fields.Float(required=True, validate=validate.Range(min=0))
    release_date = fields.Date(required=True)
    description = fields.String()

class BookUpdateSchema(Schema):
    title = fields.String(validate=validate.Length(min=1, max=200))
    author = fields.String(validate=validate.Length(min=1, max=100))
    category = fields.String()
    price = fields.Float(validate=validate.Range(min=0))
    release_date = fields.Date()
    description = fields.String()

class BookResponseSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    author = fields.String()
    category = fields.String()
    price = fields.Float()
    release_date = fields.Date()
    description = fields.String()
    created_at = fields.DateTime()

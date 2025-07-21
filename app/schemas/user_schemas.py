from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.user import User

class UserRegistrationSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[
        validate.Length(min=8),
        validate.Regexp(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])', 
                       error='Password must contain at least one lowercase, uppercase and number')
    ])

    @validates('email')
    def validate_email(self, email):
        if User.query.filter_by(email=email).first():
            raise ValidationError('Email already exists')

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserResponseSchema(Schema):
    id = fields.Integer()
    email = fields.Email()
    created_at = fields.DateTime()

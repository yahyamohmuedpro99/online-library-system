from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.auth_service import AuthService, ValidationError

api = Namespace('auth', description='Authentication operations')

# Models for Swagger documentation
signup_model = api.model('Signup', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

user_response = api.model('UserResponse', {
    'id': fields.Integer(description='User ID'),
    'email': fields.String(description='User email'),
    'created_at': fields.String(description='Creation timestamp')
})

token_response = api.model('TokenResponse', {
    'access_token': fields.String(description='JWT access token'),
    'user': fields.Nested(user_response)
})

@api.route('/signup')
class Signup(Resource):
    @api.expect(signup_model)
    @api.marshal_with(user_response, code=201)
    def post(self):
        """Register a new user"""
        data = request.get_json()
        
        try:
            user = AuthService.signup(data)
            return user, 201
        except ValidationError as e:
            api.abort(400, str(e))

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.marshal_with(token_response)
    def post(self):
        """Login and get JWT token"""
        data = request.get_json()
        
        try:
            result = AuthService.login(data)
            return result
        except ValidationError as e:
            api.abort(401, str(e))

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app import db
from app.models.user import User

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
        
        if not data or not data.get('email') or not data.get('password'):
            api.abort(400, 'Email and password required')
        
        if User.query.filter_by(email=data['email']).first():
            api.abort(400, 'Email already exists')
        
        user = User(email=data['email'])
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return user.to_dict(), 201

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.marshal_with(token_response)
    def post(self):
        """Login and get JWT token"""
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            api.abort(400, 'Email and password required')
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            api.abort(401, 'Invalid credentials')
        
        access_token = create_access_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'user': user.to_dict()
        }

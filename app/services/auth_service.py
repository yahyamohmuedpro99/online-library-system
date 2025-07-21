from flask_jwt_extended import create_access_token
from app import db
from app.models.user import User
from app.schemas.user_schemas import UserRegistrationSchema, UserResponseSchema, UserLoginSchema


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class AuthService:
    @staticmethod
    def signup(data):
        """Create a new user account with validation"""
        schema = UserRegistrationSchema()
        result = schema.load(data)
        
        # Create user
        user = User(email=result['email'])
        user.set_password(result['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return UserResponseSchema().dump(user)
    
    @staticmethod
    def login(data):
        """Authenticate user and return access token"""
        schema = UserLoginSchema()
        result = schema.load(data)
        
        # Find user
        user = User.query.filter_by(email=result['email']).first()
        
        if not user or not user.check_password(result['password']):
            raise ValidationError('Invalid credentials')
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'user': UserResponseSchema().dump(user)
        }
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        user = User.query.get(user_id)
        if not user:
            raise ValidationError(f'User with ID {user_id} not found')
        return UserResponseSchema().dump(user)

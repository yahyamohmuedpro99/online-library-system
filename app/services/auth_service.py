from flask_jwt_extended import create_access_token
from app import db
from app.models.user import User


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class AuthService:
    @staticmethod
    def signup(data):
        """Create a new user account with validation"""
        if not data:
            raise ValidationError("No data provided")
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email:
            raise ValidationError('Email is required')
        
        if not password:
            raise ValidationError('Password is required')
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            raise ValidationError('Invalid email format')
        
        # Password strength validation
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters long')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            raise ValidationError('Email already exists')
        
        # Create user
        user = User(email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user.to_dict()
    
    @staticmethod
    def login(data):
        """Authenticate user and return access token"""
        if not data:
            raise ValidationError("No data provided")
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email:
            raise ValidationError('Email is required')
        
        if not password:
            raise ValidationError('Password is required')
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            raise ValidationError('Invalid credentials')
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'user': user.to_dict()
        }
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        user = User.query.get(user_id)
        if not user:
            raise ValidationError(f'User with ID {user_id} not found')
        return user.to_dict()

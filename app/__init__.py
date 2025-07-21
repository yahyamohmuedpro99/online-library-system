from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    
    # Initialize API with Swagger
    from app.api import api
    api.init_app(app)
    
    # Add JWT security definition for Swagger
    api.authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
        }
    }
    
    # Register health check blueprint
    from app.routes import health_bp
    app.register_blueprint(health_bp)
    
    return app

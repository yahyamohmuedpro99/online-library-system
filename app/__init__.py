from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restx import Api
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    
    api = Api(app, doc='/docs/', title='Online Library API', version='1.0')
    
    # Register blueprints
    from app.routes import health_bp
    app.register_blueprint(health_bp)
    
    return app

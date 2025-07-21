import pytest
import json
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_signup(client):
    response = client.post('/users/signup', 
                          json={'email': 'test@example.com', 'password': 'password123'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'user' in data
    assert data['user']['email'] == 'test@example.com'

def test_login(client):
    # First create a user
    client.post('/users/signup', 
                json={'email': 'test@example.com', 'password': 'password123'})
    
    # Then login
    response = client.post('/users/login',
                          json={'email': 'test@example.com', 'password': 'password123'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data

def test_login_invalid_credentials(client):
    response = client.post('/users/login',
                          json={'email': 'wrong@example.com', 'password': 'wrongpass'})
    assert response.status_code == 401

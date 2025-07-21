from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService, ValidationError

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    try:
        user = AuthService.signup(data)
        return jsonify({'message': 'User created successfully', 'user': user}), 201
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        result = AuthService.login(data)
        return jsonify(result)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

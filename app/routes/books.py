from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.book_service import BookService, ValidationError

books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('', methods=['POST'])
@jwt_required()
def create_book():
    data = request.get_json()
    try:
        book = BookService.create_book(data)
        return jsonify({'message': 'Book created successfully', 'book': book}), 201
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@books_bp.route('', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    filters = {
        'author': request.args.get('author'),
        'category': request.args.get('category'),
        'min_price': request.args.get('min_price'),
        'max_price': request.args.get('max_price'),
        'release_year': request.args.get('release_year')
    }
    
    try:
        result = BookService.get_books_with_filters(page, per_page, filters)
        return jsonify(result)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = BookService.get_book_by_id(book_id)
        return jsonify(book)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@books_bp.route('/<int:book_id>', methods=['PATCH'])
@jwt_required()
def update_book(book_id):
    data = request.get_json()
    try:
        book = BookService.update_book(book_id, data)
        return jsonify({'message': 'Book updated successfully', 'book': book})
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@books_bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    try:
        BookService.delete_book(book_id)
        return jsonify({'message': 'Book deleted successfully'}), 200
    except ValidationError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.book import Book

books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('', methods=['POST'])
@jwt_required()
def create_book():
    data = request.get_json()
    
    required_fields = ['title', 'author', 'category', 'price', 'release_date']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        release_date = datetime.strptime(data['release_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    book = Book(
        title=data['title'],
        author=data['author'],
        category=data['category'],
        price=float(data['price']),
        release_date=release_date,
        description=data.get('description', '')
    )
    
    db.session.add(book)
    db.session.commit()
    
    return jsonify({'message': 'Book created successfully', 'book': book.to_dict()}), 201

@books_bp.route('', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Book.query
    
    # Filters
    if request.args.get('author'):
        query = query.filter(Book.author.ilike(f"%{request.args.get('author')}%"))
    
    if request.args.get('category'):
        query = query.filter(Book.category.ilike(f"%{request.args.get('category')}%"))
    
    if request.args.get('min_price'):
        query = query.filter(Book.price >= float(request.args.get('min_price')))
    
    if request.args.get('max_price'):
        query = query.filter(Book.price <= float(request.args.get('max_price')))
    
    if request.args.get('release_year'):
        year = int(request.args.get('release_year'))
        query = query.filter(db.extract('year', Book.release_date) == year)
    
    books = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'books': [book.to_dict() for book in books.items],
        'total': books.total,
        'pages': books.pages,
        'current_page': page
    })

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@books_bp.route('/<int:book_id>', methods=['PATCH'])
@jwt_required()
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'title' in data:
        book.title = data['title']
    if 'author' in data:
        book.author = data['author']
    if 'category' in data:
        book.category = data['category']
    if 'price' in data:
        book.price = float(data['price'])
    if 'description' in data:
        book.description = data['description']
    if 'release_date' in data:
        try:
            book.release_date = datetime.strptime(data['release_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    db.session.commit()
    
    return jsonify({'message': 'Book updated successfully', 'book': book.to_dict()})

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.book import Book

api = Namespace('books', description='Book management operations')

# Models for Swagger documentation
book_model = api.model('Book', {
    'title': fields.String(required=True, description='Book title'),
    'author': fields.String(required=True, description='Book author'),
    'category': fields.String(required=True, description='Book category'),
    'price': fields.Float(required=True, description='Book price'),
    'release_date': fields.String(required=True, description='Release date (YYYY-MM-DD)'),
    'description': fields.String(description='Book description')
})

book_response = api.model('BookResponse', {
    'id': fields.Integer(description='Book ID'),
    'title': fields.String(description='Book title'),
    'author': fields.String(description='Book author'),
    'category': fields.String(description='Book category'),
    'price': fields.Float(description='Book price'),
    'release_date': fields.String(description='Release date'),
    'description': fields.String(description='Book description'),
    'created_at': fields.String(description='Creation timestamp')
})

book_list_response = api.model('BookListResponse', {
    'books': fields.List(fields.Nested(book_response)),
    'total': fields.Integer(description='Total number of books'),
    'pages': fields.Integer(description='Total pages'),
    'current_page': fields.Integer(description='Current page')
})

@api.route('')
class BookList(Resource):
    @api.marshal_with(book_list_response)
    @api.doc(params={
        'page': 'Page number',
        'per_page': 'Items per page',
        'author': 'Filter by author',
        'category': 'Filter by category',
        'min_price': 'Minimum price',
        'max_price': 'Maximum price',
        'release_year': 'Filter by release year'
    })
    def get(self):
        """Get list of books with pagination and filters"""
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
        
        return {
            'books': [book.to_dict() for book in books.items],
            'total': books.total,
            'pages': books.pages,
            'current_page': page
        }

    @api.expect(book_model)
    @api.marshal_with(book_response, code=201)
    @api.doc(security='Bearer')
    @jwt_required()
    def post(self):
        """Create a new book (requires authentication)"""
        data = request.get_json()
        
        required_fields = ['title', 'author', 'category', 'price', 'release_date']
        if not data or not all(field in data for field in required_fields):
            api.abort(400, 'Missing required fields')
        
        try:
            release_date = datetime.strptime(data['release_date'], '%Y-%m-%d').date()
        except ValueError:
            api.abort(400, 'Invalid date format. Use YYYY-MM-DD')
        
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
        
        return book.to_dict(), 201

@api.route('/<int:book_id>')
class BookDetail(Resource):
    @api.marshal_with(book_response)
    def get(self, book_id):
        """Get book details by ID"""
        book = Book.query.get_or_404(book_id)
        return book.to_dict()

    @api.expect(book_model)
    @api.marshal_with(book_response)
    @api.doc(security='Bearer')
    @jwt_required()
    def patch(self, book_id):
        """Update book (requires authentication)"""
        book = Book.query.get_or_404(book_id)
        data = request.get_json()
        
        if not data:
            api.abort(400, 'No data provided')
        
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
                api.abort(400, 'Invalid date format. Use YYYY-MM-DD')
        
        db.session.commit()
        
        return book.to_dict()

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.book_service import BookService, ValidationError

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
        
        filters = {
            'author': request.args.get('author'),
            'category': request.args.get('category'),
            'min_price': request.args.get('min_price'),
            'max_price': request.args.get('max_price'),
            'release_year': request.args.get('release_year')
        }
        
        try:
            return BookService.get_books_with_filters(page, per_page, filters)
        except ValidationError as e:
            api.abort(400, str(e))

    @api.expect(book_model)
    @api.marshal_with(book_response, code=201)
    @api.doc(security='Bearer')
    @jwt_required()
    def post(self):
        """Create a new book (requires authentication)"""
        data = request.get_json()
        
        try:
            book = BookService.create_book(data)
            return book, 201
        except ValidationError as e:
            api.abort(400, str(e))

@api.route('/<int:book_id>')
class BookDetail(Resource):
    @api.marshal_with(book_response)
    def get(self, book_id):
        """Get book details by ID"""
        try:
            book = BookService.get_book_by_id(book_id)
            return book
        except ValidationError as e:
            api.abort(404, str(e))

    @api.expect(book_model)
    @api.marshal_with(book_response)
    @api.doc(security='Bearer')
    @jwt_required()
    def patch(self, book_id):
        """Update book (requires authentication)"""
        data = request.get_json()
        
        try:
            book = BookService.update_book(book_id, data)
            return book
        except ValidationError as e:
            api.abort(400, str(e))

    @api.doc(security='Bearer')
    @jwt_required()
    def delete(self, book_id):
        """Delete book (requires authentication)"""
        try:
            BookService.delete_book(book_id)
            return {'message': 'Book deleted successfully'}, 200
        except ValidationError as e:
            api.abort(404, str(e))

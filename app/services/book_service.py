from datetime import datetime
from app import db
from app.models.book import Book
from app.schemas.book_schemas import BookCreateSchema, BookResponseSchema, BookUpdateSchema


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class BookService:
    @staticmethod
    def create_book(data):
        """Create a new book with validation"""
        schema = BookCreateSchema()
        result = schema.load(data)
        
        # Create book
        book = Book(
            title=result['title'],
            author=result['author'],
            category=result['category'],
            price=result['price'],
            release_date=result['release_date'],
            description=result.get('description', '')
        )
        
        db.session.add(book)
        db.session.commit()
        
        return BookResponseSchema().dump(book)
    
    @staticmethod
    def get_books_with_filters(page=1, per_page=10, filters=None):
        """Get books with pagination and filters"""
        if filters is None:
            filters = {}
        
        query = Book.query
        
        # Apply filters
        if filters.get('author'):
            query = query.filter(Book.author.ilike(f"%{filters['author']}%"))
        
        if filters.get('category'):
            query = query.filter(Book.category.ilike(f"%{filters['category']}%"))
        
        if filters.get('min_price'):
            try:
                min_price = float(filters['min_price'])
                query = query.filter(Book.price >= min_price)
            except (ValueError, TypeError):
                raise ValidationError('Invalid min_price format')
        
        if filters.get('max_price'):
            try:
                max_price = float(filters['max_price'])
                query = query.filter(Book.price <= max_price)
            except (ValueError, TypeError):
                raise ValidationError('Invalid max_price format')
        
        if filters.get('release_year'):
            try:
                year = int(filters['release_year'])
                query = query.filter(db.extract('year', Book.release_date) == year)
            except (ValueError, TypeError):
                raise ValidationError('Invalid release_year format')
        
        # Paginate
        try:
            books = query.paginate(page=page, per_page=per_page, error_out=False)
        except Exception as e:
            raise ValidationError(f'Pagination error: {str(e)}')
        
        return {
            'books': BookResponseSchema(many=True).dump(books.items),
            'total': books.total,
            'pages': books.pages,
            'current_page': page
        }
    
    @staticmethod
    def get_book_by_id(book_id):
        """Get a single book by ID"""
        book = Book.query.get(book_id)
        if not book:
            raise ValidationError(f'Book with ID {book_id} not found')
        return BookResponseSchema().dump(book)
    
    @staticmethod
    def update_book(book_id, data):
        """Update a book with validation"""
        book = Book.query.get(book_id)
        if not book:
            raise ValidationError(f'Book with ID {book_id} not found')
        
        schema = BookUpdateSchema()
        result = schema.load(data)
        
        # Update fields
        if 'title' in result:
            book.title = result['title']
        
        if 'author' in result:
            book.author = result['author']
        
        if 'category' in result:
            book.category = result['category']
        
        if 'price' in result:
            book.price = result['price']
        
        if 'description' in result:
            book.description = result['description']
        
        if 'release_date' in result:
            book.release_date = result['release_date']
        
        db.session.commit()
        return BookResponseSchema().dump(book)
    
    @staticmethod
    def delete_book(book_id):
        """Delete a book"""
        book = Book.query.get(book_id)
        if not book:
            raise ValidationError(f'Book with ID {book_id} not found')
        
        db.session.delete(book)
        db.session.commit()
        return True

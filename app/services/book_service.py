from datetime import datetime
from app import db
from app.models.book import Book


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class BookService:
    @staticmethod
    def create_book(data):
        """Create a new book with validation"""
        if not data:
            raise ValidationError("No data provided")
        
        required_fields = ['title', 'author', 'category', 'price', 'release_date']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Validate and parse release date
        try:
            release_date = datetime.strptime(data['release_date'], '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError('Invalid date format. Use YYYY-MM-DD')
        
        # Validate price
        try:
            price = float(data['price'])
            if price < 0:
                raise ValidationError('Price cannot be negative')
        except (ValueError, TypeError):
            raise ValidationError('Invalid price format')
        
        # Create book
        book = Book(
            title=data['title'].strip(),
            author=data['author'].strip(),
            category=data['category'].strip(),
            price=price,
            release_date=release_date,
            description=data.get('description', '').strip()
        )
        
        db.session.add(book)
        db.session.commit()
        
        return book.to_dict()
    
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
            'books': [book.to_dict() for book in books.items],
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
        return book.to_dict()
    
    @staticmethod
    def update_book(book_id, data):
        """Update a book with validation"""
        book = Book.query.get(book_id)
        if not book:
            raise ValidationError(f'Book with ID {book_id} not found')
        
        if not data:
            raise ValidationError('No data provided')
        
        # Update fields if provided
        if 'title' in data:
            book.title = data['title'].strip()
        
        if 'author' in data:
            book.author = data['author'].strip()
        
        if 'category' in data:
            book.category = data['category'].strip()
        
        if 'price' in data:
            try:
                price = float(data['price'])
                if price < 0:
                    raise ValidationError('Price cannot be negative')
                book.price = price
            except (ValueError, TypeError):
                raise ValidationError('Invalid price format')
        
        if 'description' in data:
            book.description = data['description'].strip()
        
        if 'release_date' in data:
            try:
                book.release_date = datetime.strptime(data['release_date'], '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError('Invalid date format. Use YYYY-MM-DD')
        
        db.session.commit()
        return book.to_dict()
    
    @staticmethod
    def delete_book(book_id):
        """Delete a book"""
        book = Book.query.get(book_id)
        if not book:
            raise ValidationError(f'Book with ID {book_id} not found')
        
        db.session.delete(book)
        db.session.commit()
        return True

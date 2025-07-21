# Online Library System

A RESTful API for managing an online library system built with Flask, following clean architecture principles with proper separation of concerns.

## 🚀 Features

- **Clean Architecture**: Service layer for business logic, thin controllers
- **User Authentication**: JWT-based authentication system
- **Book Management**: Full CRUD operations with validation
- **Advanced Filtering**: Search books by author, category, price, release year
- **Pagination**: Efficient data loading with pagination support
- **Mock Data Seeding**: Realistic test data generation with famous books
- **API Documentation**: Interactive Swagger/OpenAPI documentation
- **Docker Support**: Containerized deployment ready
- **Comprehensive Testing**: Unit tests for business logic

## 🏗️ Architecture

The application follows a simplified clean architecture:

```
app/
├── models/          # Data models (ORM entities)
├── services/        # Business logic layer
├── routes/          # HTTP controllers (thin layer)
├── api/            # API documentation and controllers
└── config.py       # Configuration

scripts/            # Database seeding utilities
├── mock_generators.py  # Mock data generation
├── seed_data.py       # CLI seeding script
└── run_seeds.py       # Interactive seeding script
```

**Benefits:**
- ✅ Separation of concerns
- ✅ Testable business logic
- ✅ Maintainable codebase
- ✅ Reusable services

## 🛠️ Tech Stack

- **Backend**: Flask, Flask-RESTX
- **Database**: SQLAlchemy (SQLite for development)
- **Authentication**: Flask-JWT-Extended
- **Documentation**: Swagger/OpenAPI
- **Testing**: pytest
- **Mock Data**: Faker library
- **CLI Tools**: Click
- **Containerization**: Docker

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone and start
git clone <https://github.com/yahyamohmuedpro99/online-library-system.git>
cd online-library-system
docker-compose up --build

# Access the API
# Swagger UI: http://localhost:5000/
# API Base: http://localhost:5000/
```

### Local Development

```bash
# Setup
git clone <https://github.com/yahyamohmuedpro99/online-library-system.git>
cd online-library-system
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Seed database with mock data
python scripts/run_seeds.py

# Run application
python run.py
```

## 🌱 Database Seeding

The system includes seeding utilities for generating realistic test data:

### Interactive Seeding
```bash
python scripts/run_seeds.py
```

**Options:**
1. Seed everything (clear + users + books)
2. Seed users only
3. Seed books only  
4. Clear all data
5. Quick seed (10 users + 20 books)
6. Large seed (50 users + 100 books)

### CLI Seeding
```bash
# Basic seeding
python scripts/seed_data.py

# Custom options
python scripts/seed_data.py --users 50 --books 100 --clear

# Help
python scripts/seed_data.py --help
```

### Sample Data Includes
- **Famous Books**: The Great Gatsby, 1984, Harry Potter, etc.
- **Realistic Data**: 20+ categories, famous authors, proper pricing
- **Test Users**: Generated with realistic email addresses

## 📚 API Endpoints

### Authentication
- `POST /auth/signup` - Register a new user
- `POST /auth/login` - Login and get JWT token

### Books
- `GET /books` - Get all books (with pagination and filters)
- `POST /books` - Create a new book (requires authentication)
- `GET /books/{id}` - Get book by ID
- `PATCH /books/{id}` - Update book (requires authentication)
- `DELETE /books/{id}` - Delete book (requires authentication)

### Legacy Routes (for backward compatibility)
- `POST /users/signup` - Register a new user
- `POST /users/login` - Login and get JWT token
- `GET /books` - Get all books
- `POST /books` - Create a new book
- `GET /books/{id}` - Get book by ID
- `PATCH /books/{id}` - Update book

## 💡 API Usage Examples

### Register and Login
```bash
# Register
curl -X POST http://localhost:5000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Book Operations
```bash
# Create a book (requires JWT token)
curl -X POST http://localhost:5000/books \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald", 
    "category": "Fiction",
    "price": 12.99,
    "release_date": "1925-04-10",
    "description": "A classic American novel"
  }'

# Get books with filters
curl "http://localhost:5000/books?author=Fitzgerald&category=Fiction&min_price=10&max_price=20&page=1&per_page=10"

# Get specific book
curl http://localhost:5000/books/1
```

## 🧪 Testing

The clean architecture makes testing straightforward:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

**Test Structure:**
- Business logic can be tested independently
- Services are easily mockable
- Controllers have minimal logic to test

## 📁 Project Structure

```
online-library-system/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/              # Data models
│   │   ├── __init__.py
│   │   ├── book.py
│   │   └── user.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── book_service.py
│   │   └── auth_service.py
│   ├── routes/              # HTTP controllers
│   │   ├── __init__.py
│   │   ├── books.py
│   │   └── users.py
│   └── api/                 # API documentation
│       ├── __init__.py
│       ├── auth.py
│       └── books.py
├── scripts/                 # Database utilities
│   ├── __init__.py
│   ├── mock_generators.py
│   ├── seed_data.py
│   └── run_seeds.py
├── tests/
│   └── test_auth.py
├── instance/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
└── README.md
```

## ⚙️ Environment Variables

Create a `.env` file based on `.env.example`:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///library.db
```

## 🔧 Development

### Adding New Features

1. **Business Logic**: Add to appropriate service in `app/services/`
2. **API Endpoints**: Add to controllers in `app/routes/` or `app/api/`
3. **Data Models**: Add to `app/models/`
4. **Tests**: Add tests for new business logic

### Service Layer Example
```python
# app/services/book_service.py
class BookService:
    @staticmethod
    def create_book(data):
        # Validation and business logic here
        # Returns clean data or raises ValidationError
```

### Controller Example
```python
# app/routes/books.py
@books_bp.route('', methods=['POST'])
def create_book():
    try:
        book = BookService.create_book(request.get_json())
        return jsonify({'book': book}), 201
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the clean architecture patterns
4. Add tests for new business logic
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.



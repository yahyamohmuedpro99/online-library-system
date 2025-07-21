# Online Library System

A REST API for managing an online library system built with Flask.

## Setup

### Using Docker

```bash
docker-compose up --build
```

### Local Development

```bash
pip install -r requirements.txt
python run.py
```

## API Endpoints

### Health
- `GET /health` - Health check

### Authentication
- `POST /users/signup` - Register a new user
- `POST /users/login` - Login and get JWT token

### Books
- `POST /books` - Create a book (requires auth)
- `GET /books` - List books with pagination and filters
- `GET /books/{id}` - Get book details
- `PATCH /books/{id}` - Update book (requires auth)

### Documentation
- `GET /docs/` - Swagger API documentation

## Testing

```bash
pytest
```

## Environment Variables

Copy `.env.example` to `.env` and update values as needed.

The app runs on http://localhost:5000

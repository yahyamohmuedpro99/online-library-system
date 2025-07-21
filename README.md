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

- `GET /health` - Health check
- `GET /docs/` - API documentation

## Environment Variables

Copy `.env.example` to `.env` and update values as needed.

The app runs on http://localhost:5000

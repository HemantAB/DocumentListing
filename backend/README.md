# Document Management System - Backend

A FastAPI-based backend service for managing text documents with SQLite database.

## Setup Instructions

1. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
# Development server with auto-reload
uvicorn app.main:app --reload

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Swagger Documentation: http://localhost:8000/api/docs
- ReDoc Documentation: http://localhost:8000/api/redoc

## Implemented Features

### API Endpoints
- `GET /api/documents` - List all documents with filtering, sorting, and pagination
- `GET /api/documents/{id}` - Get a specific document by ID
- `POST /api/documents` - Create a new document
- `DELETE /api/documents/{id}` - Delete a document

### Core Features
1. **Document Management**
   - CRUD operations for text documents
   - Automatic file size calculation
   - Creation timestamp tracking

2. **Search & Filter**
   - Search documents by name
   - Search by document ID
   - Dynamic sorting by name or date
   - Pagination support

3. **Data Validation**
   - Input validation using Pydantic models
   - Proper error handling
   - Automatic API documentation

4. **Development Features**
   - Automatic sample data generation
   - Request logging
   - CORS support
   - Health check endpoint

## Technical Decisions

1. **FastAPI Framework**
   - High performance with async support
   - Automatic OpenAPI documentation
   - Built-in validation with Pydantic
   - Modern Python type hints

2. **SQLite Database**
   - Simple setup with no external dependencies
   - Good for development and small to medium applications
   - File-based storage for easy deployment
   - Support for SQL queries and indexes

3. **SQLAlchemy ORM**
   - Type-safe database operations
   - Database agnostic code
   - Connection pooling
   - Easy migration support

4. **Project Structure**
   - Modular organization with separate components
   - Clear separation of concerns
   - Easy to test and maintain
   - Scalable architecture

## Assumptions

1. **Data Volume**
   - Moderate document sizes (<10MB)
   - Reasonable number of documents (<10,000)
   - Single server deployment

2. **Security**
   - Basic CORS configuration is sufficient
   - No authentication required (as per requirements)
   - Internal network deployment

3. **Performance**
   - Standard latency requirements
   - No real-time update requirements
   - Basic caching through SQLite

4. **Document Format**
   - Text documents only
   - UTF-8 encoding
   - No special formatting requirements

## Future Improvements

1. **Security**
   - Add authentication
   - Add authorization roles
   - Rate limiting
   - Input sanitization

2. **Features**
   - File upload support
   - Document versioning
   - Document categories
   - Search in content
   - Batch operations

3. **Performance**
   - Caching layer
   - Full-text search
   - Async database operations
   - Query optimization

4. **Infrastructure**
   - Docker support
   - CI/CD pipeline
   - Monitoring setup
   - Backup solution

## Requirements

- Python 3.8+
- SQLite 3
- FastAPI dependencies (see requirements.txt)

## Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── api/
│   │   ├── endpoints/
│   │   │   └── documents.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── models/
│   │   └── document.py
│   └── schemas/
│       └── document.py
├── data/
├── logs/
├── requirements.txt
└── README.md
```

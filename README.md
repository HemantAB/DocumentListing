# Document Listing Application

A full-stack document management system built with React (Frontend) and FastAPI (Backend). This application allows users to manage text documents with features like searching, sorting, and pagination.

## Overview

The project is structured as a monorepo containing both frontend and backend applications:

```
document-listing/
├── frontend/          # React application
├── backend/           # FastAPI application
├── README.md         # This file
└── .gitignore        # Root gitignore file
```

## Features

- 📝 Create, read, and delete text documents
- 🔍 Search documents by name or ID
- 📊 Sort documents by name or creation date
- 📄 Pagination support
- ⚡ Real-time search
- 📱 Responsive design
- 🎨 Clean, modern UI

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm 7+
- SQLite 3

## Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix/macOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at http://localhost:5173

## Project Structure

### Backend

```
backend/
├── app/
│   ├── api/
│   │   └── endpoints/      # API route handlers
│   ├── core/              # Core configurations
│   ├── models/            # SQLAlchemy models
│   └── schemas/           # Pydantic schemas
├── tests/                 # Unit tests
├── data/                  # SQLite database directory
└── requirements.txt       # Python dependencies
```

### Frontend

```
frontend/
├── src/
│   ├── components/        # React components
│   ├── types/            # TypeScript definitions
│   ├── services/         # API services
│   └── lib/              # Utilities
├── public/               # Static assets
└── package.json          # Node.js dependencies
```

## API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Key Endpoints

- `GET /api/documents`: List all documents
- `GET /api/documents/{id}`: Get single document
- `POST /api/documents`: Create new document
- `DELETE /api/documents/{id}`: Delete document

## Testing

### Backend Tests

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

### Frontend Tests

```bash
# Run tests
npm test

# Run tests with coverage
npm run coverage
```

## Technical Details

### Backend
- FastAPI for high-performance API
- SQLite for simple database management
- SQLAlchemy ORM for database operations
- Pydantic for data validation
- pytest for testing

### Frontend
- React with TypeScript
- Vite for fast development
- Tailwind CSS for styling
- Vitest for testing
- Axios for API calls

## Development

### Running Locally

1. Start the backend server:
```bash
cd backend
uvicorn app.main:app --reload
```

2. In a new terminal, start the frontend:
```bash
cd frontend
npm run dev
```

### Environment Variables

Backend (`.env`):
```env
DATABASE_URL=sqlite:///./data/documents.db
```

Frontend (`.env`):
```env
VITE_API_URL=http://localhost:8000/api
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [SQLite](https://www.sqlite.org/)

## Contact

Hemant Bhilwadikar 

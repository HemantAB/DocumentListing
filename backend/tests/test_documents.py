import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app
from app.models.document import Document
from datetime import datetime

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Setup test database
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_documents():
    db = TestingSessionLocal()
    documents = [
        {
            "name": "Meeting Notes.txt",
            "content": "Discussion points from team meeting:\n- Project timeline review\n- Resource allocation\n- Next steps"
        },
        {
            "name": "Project Plan.txt",
            "content": "Q4 Project Timeline:\n1. Requirements gathering\n2. Design phase\n3. Implementation\n4. Testing\n5. Deployment"
        },
        {
            "name": "API Documentation.txt",
            "content": "REST API Endpoints:\n- GET /api/v1/users\n- POST /api/v1/users\n- PUT /api/v1/users/{id}\n- DELETE /api/v1/users/{id}"
        }
    ]
    
    db_docs = []
    for doc in documents:
        db_doc = Document(**doc)
        db.add(db_doc)
        db_docs.append(db_doc)
    
    db.commit()
    for doc in db_docs:
        db.refresh(doc)
    
    yield db_docs
    
    db.close()

def test_create_document():
    response = client.post(
        "/api/documents",
        json={
            "name": "test.txt",
            "content": "test content"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test.txt"
    assert data["content"] == "test content"
    assert "id" in data
    assert "created_at" in data
    assert "size" in data

def test_read_nonexistent_document():
    response = client.get("/api/documents/999")
    assert response.status_code == 404

def test_sort_documents(sample_documents):
    # Test sorting by name ascending
    response = client.get("/api/documents?sort_by=name&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    names = [doc["name"] for doc in data["documents"]]
    assert names == sorted(names)

    # Test sorting by name descending
    response = client.get("/api/documents?sort_by=name&sort_order=desc")
    assert response.status_code == 200
    data = response.json()
    names = [doc["name"] for doc in data["documents"]]
    assert names == sorted(names, reverse=True)

def test_invalid_page_number():
    response = client.get("/api/documents?page=0")
    assert response.status_code == 422

def test_invalid_per_page():
    response = client.get("/api/documents?per_page=0")
    assert response.status_code == 422

def test_invalid_sort_field():
    response = client.get("/api/documents?sort_by=invalid")
    assert response.status_code == 422

def test_create_document_validation():
    # Test empty name
    response = client.post(
        "/api/documents",
        json={"name": "", "content": "test content"}
    )
    assert response.status_code == 422

    # Test missing content
    response = client.post(
        "/api/documents",
        json={"name": "test.txt"}
    )
    assert response.status_code == 422

def test_search_project_plans(sample_documents):
    response = client.get("/api/documents?search=Project")
    assert response.status_code == 200
    data = response.json()
    assert len(data["documents"]) == 5
    assert "Project Plan.txt" in data["documents"][0]["name"]

def test_documents_have_correct_fields(sample_documents):
    response = client.get("/api/documents")
    assert response.status_code == 200
    data = response.json()
    
    for doc in data["documents"]:
        assert all(key in doc for key in ["id", "name", "content", "created_at", "size"])
        assert isinstance(doc["id"], int)
        assert isinstance(doc["name"], str)
        assert isinstance(doc["content"], str)
        assert isinstance(doc["created_at"], str)
        assert isinstance(doc["size"], int)
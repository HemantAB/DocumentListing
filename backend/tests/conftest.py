import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app, create_sample_data
from app.database import Base, get_db
from app.models.document import Document

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def disable_sample_data():
    """Disable sample data creation during tests"""
    app.dependency_overrides[create_sample_data] = lambda: None
    yield
    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def test_engine():
    return engine

@pytest.fixture(scope="function")
def test_db(test_engine):
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    yield
    # Drop tables after test
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def db_session(test_db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def sample_documents(db_session):
    """Create multiple sample documents for testing"""
    documents = [
        Document(name="Test Document 1.txt", content="Content 1"),
        Document(name="Test Document 2.txt", content="Content 2"),
        Document(name="Another Doc.txt", content="Content 3")
    ]
    
    for doc in documents:
        db_session.add(doc)
    db_session.commit()
    
    for doc in documents:
        db_session.refresh(doc)
    
    return documents

@pytest.fixture(scope="function")
def sample_document(db_session):
    """Create a single sample document for testing"""
    document = Document(
        name="Test Document.txt",
        content="This is a test document content."
    )
    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)
    return document
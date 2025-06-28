import os

import pytest
from api.database import Base, get_db
from api.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use dedicated PostgreSQL test database
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://orbitah_test:orbitah_test_password@localhost:5434/orbitah_test_db"
)

@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine for the entire test session"""
    engine = create_engine(TEST_DATABASE_URL)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    yield engine

    # Clean up tables after all tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create a fresh database session for each test"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    # Create a new session
    db = TestingSessionLocal()

    # Start a transaction
    transaction = db.begin_nested()

    yield db

    # Rollback the transaction to undo all changes
    transaction.rollback()
    db.close()

@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with database dependency override"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client

    # Clean up dependency override
    app.dependency_overrides.clear()

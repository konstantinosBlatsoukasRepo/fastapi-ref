import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, engine
from app.database import Base

from app.main import app


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    # create models based on the models, ORM classes
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    # run our code before we run our test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    # run our code after we our test finishes


@pytest.fixture
def test_user(client):
    user_data = {"email": "test_podence@osfp.com", "password": "test"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201

    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

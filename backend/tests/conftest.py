import os

os.environ.setdefault("OWNER_EMAIL", "owner@example.com")
os.environ.setdefault("FIREBASE_PROJECT_ID", "test-project")
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:5173")
os.environ.setdefault("RATE_LIMIT_PER_MINUTE", "100000")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

import app.models  # noqa: E402,F401
from app.auth import deps  # noqa: E402
from app.db.base import Base  # noqa: E402
from app.db.session import get_db  # noqa: E402
from app.main import create_app  # noqa: E402

TOKENS = {
    "owner-token": {"uid": "uid-owner", "email": "owner@example.com", "email_verified": True},
    "stranger-token": {"uid": "uid-x", "email": "stranger@example.com", "email_verified": True},
    "unverified-token": {"uid": "uid-owner", "email": "owner@example.com", "email_verified": False},
    "impostor-token": {"uid": "uid-other", "email": "owner@example.com", "email_verified": True},
}


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, expire_on_commit=False)()
    yield session
    session.close()


@pytest.fixture()
def client(db_session, monkeypatch):
    def fake_verify(token):
        if token not in TOKENS:
            raise ValueError("bad token")
        return TOKENS[token]

    monkeypatch.setattr(deps, "verify_token", fake_verify)
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db_session
    return TestClient(app)


def auth(token="owner-token"):
    return {"Authorization": f"Bearer {token}"}

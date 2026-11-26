import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.dependencies import get_notification_store
from app.infrastructure.database.models import (  # noqa: F401
    MatchModel,
    PlayerModel,
    TeamModel,
    TournamentModel,
)
from app.infrastructure.database.session import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    """Har bir test uchun alohida, toza xotira-baza va TestClient yaratadi."""
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    # Bildirishnomalar lentasini har bir test oldidan tozalaymiz
    get_notification_store().clear()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.main import app


@pytest.fixture(scope='module')
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:
        yield client


@pytest.fixture
async def override_session():
    session = AsyncMock(spec=AsyncSession)
    yield session


@pytest.fixture
def dependency_override(override_session):
    app.dependency_overrides[get_session] = lambda: override_session
    yield override_session
    app.dependency_overrides.pop(get_session, None)


@pytest.fixture
def mock_ticket_get():
    with patch("app.models.ticket.Ticket.get") as mock:
        yield mock


@pytest.fixture
def mock_ticket_get_tickets():
    with patch("app.models.ticket.Ticket.get_tickets") as mock:
        yield mock


@pytest.fixture
def mock_message_create():
    with patch("app.models.message.Message.create") as mock:
        yield mock


@pytest.fixture
def mock_send_email():
    with patch("app.email.handlers.send_email") as mock:
        yield mock

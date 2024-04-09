from models.user import UserCreate
from services.user_services import create_user, get_user, get_user_by_id, get_users_from_db
from unittest.mock import MagicMock, patch
import pytest

@pytest.fixture
def mock_get_db():
    mock_db = MagicMock()
    with patch('services.user_services.get_db', return_value=mock_db):
        yield mock_db

def test_create_user(mock_get_db):
    # Mock UserCreate instance
    mock_user_create = UserCreate(username="testuser", name="Test User", email="test@gmail.com", password="testpassword")

    # Call the function
    created_user = create_user(mock_user_create)

    # Assertions
    assert mock_get_db.add.called_once()
    assert mock_get_db.commit.called_once()
    assert mock_get_db.refresh.called_with(created_user)


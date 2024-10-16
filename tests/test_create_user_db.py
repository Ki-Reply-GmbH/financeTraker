# test_user_services.py
import os
from unittest.mock import MagicMock, patch
os.environ['DATABASE_URL'] = 'postgresql://user:password@localhost/test_db'
import pytest
from app.services.user_services import create_user
from app.models.user import UserCreate


@pytest.fixture(scope='module', autouse=True)
def mock_config():
    with patch('app.config.DATABASE_URL', 'postgresql://user:password@localhost/test_db'):
        yield

@pytest.fixture
def mock_db_session():
    with patch('app.services.user_services.get_db') as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        yield mock_db

def test_create_user(mock_db_session):
    # Mock user data
    user = UserCreate(name="Test User", email="testuser@example.com", password="password123")

    # Mock the add, commit, and refresh methods
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None

    # Call the create_user function
    created_user = create_user(user)

    # Assertions
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert created_user.name == "Test User"
    assert created_user.email == "testuser@example.com"

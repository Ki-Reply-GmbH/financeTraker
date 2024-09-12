import pytest
from app.services.user_services import create_user
from app.models.user import UserCreate
from app.models.models import get_db, User
from unittest.mock import MagicMock

@pytest.fixture
def user_create_data():
    return UserCreate(name='John Doe', email='john.doe@example.com', password='securepassword123')

@pytest.fixture
def mock_db_session(mocker):
    mock_session = mocker.MagicMock()
    mocker.patch('app.models.models.get_db', return_value=mock_session)
    return mock_session
def test_create_user_success(mocker, mock_db_session, user_create_data):
    # Given
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    # When
    created_user = create_user(user_create_data)

    # Then
    assert created_user is not None
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(created_user)

def test_create_user_with_invalid_email(mocker, mock_db_session):
    # Given
    invalid_user_data = UserCreate(name='John Doe', email='invalid-email', password='securepassword123')
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    # When
    with pytest.raises(ValueError):
        create_user(invalid_user_data)

    # Then
    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_called()
    mock_db_session.refresh.assert_not_called()
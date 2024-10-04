import pytest
from app.services.user_services import create_user
from app.models.models import User, get_db
from app.models.user import UserCreate
from unittest.mock import MagicMock

@pytest.fixture
def mock_user_create():
    return UserCreate(name='Test User', email='test@example.com', password='securepassword123')

@pytest.fixture
def mock_db_session(mocker):
    mock_session = mocker.MagicMock()
    mocker.patch('app.models.models.get_db', return_value=mock_session)
    return mock_session

def test_create_user_success(mocker, mock_db_session, mock_user_create):
    # Given
    new_user = User(name='Test User', email='test@example.com', password='securepassword123')
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock(return_value=None)
    mocker.patch('app.models.models.User', return_value=new_user)

    # When
    result = create_user(mock_user_create)

    # Then
    assert result == new_user
    mock_db_session.add.assert_called_once_with(new_user)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(new_user)

def test_create_user_invalid_email(mocker, mock_db_session):
    # Given
    invalid_user_create = UserCreate(name='Test User', email='invalid-email', password='securepassword123')
    mocker.patch('app.models.models.User', side_effect=ValueError('Invalid email format'))

    # When
    with pytest.raises(ValueError) as exc_info:
        create_user(invalid_user_create)

    # Then
    assert str(exc_info.value) == 'Invalid email format'
    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_called()
    mock_db_session.refresh.assert_not_called()
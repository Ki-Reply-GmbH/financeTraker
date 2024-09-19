import pytest
from app.services.user_services import create_user
from app.models.user import UserCreate
from app.models.models import User, get_db
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
    result = create_user(user_create_data)

    # Then
    assert result.name == 'John Doe'
    assert result.email == 'john.doe@example.com'
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(result)

def test_create_user_exception_on_db_failure(mocker, mock_db_session, user_create_data):
    # Given
    mock_db_session.add.side_effect = Exception('DB Error')

    # When
    with pytest.raises(Exception) as exc_info:
        create_user(user_create_data)

    # Then
    assert str(exc_info.value) == 'DB Error'
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_not_called()
    mock_db_session.refresh.assert_not_called()
import pytest
from app.services.user_services import get_user
from app.models.models import User, get_db
from unittest.mock import MagicMock

@pytest.fixture
def mock_user():
	return User(email='test@example.com', name='Test User')

@pytest.fixture
def mock_db_session(mocker):
	mock_session = mocker.MagicMock()
	mock_query = mocker.MagicMock()
	mock_session.query.return_value = mock_query
	mock_query.filter.return_value = mock_query
	mocker.patch('app.models.models.get_db', return_value=mock_session)
	return mock_session


def test_get_user_found(mocker, mock_db_session, mock_user):
	# Given
	mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

	# When
	result = get_user('test@example.com')

	# Then
	assert result == mock_user
	mock_db_session.query.assert_called_once_with(User)
	mock_db_session.query.return_value.filter.assert_called_once_with(User.email == 'test@example.com')


def test_get_user_not_found(mocker, mock_db_session):
	# Given
	mock_db_session.query.return_value.filter.return_value.first.return_value = None

	# When
	result = get_user('notfound@example.com')

	# Then
	assert result is None
	mock_db_session.query.assert_called_once_with(User)
	mock_db_session.query.return_value.filter.assert_called_once_with(User.email == 'notfound@example.com')
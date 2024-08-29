import pytest
from app.services.user_services import get_users_from_db
from app.models.models import get_db
from app.models.user import UserCreate

@pytest.fixture
def mock_db_session(mocker):
	# Mock the database session context manager
	mock_session = mocker.MagicMock()
	mock_query = mocker.MagicMock()
	mock_session.query.return_value = mock_query
	mock_query.all.return_value = [UserCreate(name="John", email="john@example.com", password="securepassword123"), UserCreate(name="Jane", email="jane@example.com", password="anothersecure123")]
	return mock_session

@pytest.fixture
def db_context_manager(mocker, mock_db_session):
	# Patch the get_db to use the mock session
	return mocker.patch('app.models.models.get_db', return_value=mock_db_session)

def test_get_users_from_db(db_context_manager):
	# Given
	expected_users = [UserCreate(name="John", email="john@example.com", password="securepassword123"), UserCreate(name="Jane", email="jane@example.com", password="anothersecure123")]

	# When
	actual_users = get_users_from_db()

	# Then
	assert actual_users == expected_users, "The function should return all users from the database correctly."
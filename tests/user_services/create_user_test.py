import pytest
from app.models.user import UserCreate
from app.services.user_services import create_user
from sqlalchemy.exc import SQLAlchemyError

@pytest.mark.asyncio
async def test_create_user(mocker):
	# Given
	user_data = UserCreate(name="John Doe", email="john.doe@example.com", password="securepassword123")
	mock_db = mocker.MagicMock()
	mock_get_db = mocker.patch('app.models.models.get_db', return_value=mock_db)
	mock_db_user = mocker.MagicMock()
	mock_db.add = mocker.MagicMock()
	mock_db.commit = mocker.MagicMock()
	mock_db.refresh = mocker.MagicMock(return_value=mock_db_user)

	# When
	result = create_user(user_data)

	# Then
	mock_get_db.assert_called_once()
	mock_db.add.assert_called_once_with(mock_db_user)
	mock_db.commit.assert_called_once()
	mock_db.refresh.assert_called_once_with(mock_db_user)
	assert result == mock_db_user

@pytest.mark.asyncio
async def test_create_user_failure(mocker):
	# Given
	user_data = UserCreate(name="John Doe", email="john.doe@example.com", password="securepassword123")
	mock_db = mocker.MagicMock()
	mock_get_db = mocker.patch('app.models.models.get_db', return_value=mock_db)
	mock_db.add.side_effect = SQLAlchemyError("Database error")

	# When/Then
	with pytest.raises(SQLAlchemyError):
		create_user(user_data)
	mock_get_db.assert_called_once()
	mock_db.add.assert_called_once_with(mock_db_user)
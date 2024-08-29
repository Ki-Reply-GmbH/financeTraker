import pytest
from app.services.user_services import get_user_by_id
from app.models.models import User, get_db
from unittest.mock import MagicMock

@pytest.mark.parametrize("test_id, expected_user", [
    ("1", User(id="1", name="John Doe")),
    ("2", None)  # Assuming no user with ID 2
])
async def test_get_user_by_id(test_id, expected_user, mocker):
    # Given
    mock_session = mocker.MagicMock()
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = expected_user
    mocker.patch('app.models.models.get_db', return_value=mock_session)

    # When
    result = get_user_by_id(test_id)

    # Then
    assert result == expected_user
    mock_session.query.assert_called_once_with(User)
    mock_filter.filter.assert_called_once_with(User.id == test_id)
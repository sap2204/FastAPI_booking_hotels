from app.users.dao import UsersDAO
import pytest


# Тест поиска юзера по id, email в БД
@pytest.mark.parametrize("user_id, email, exists", [
    (1, "test@test.com", True),
    (2, "sergei@example.com", True),
    (3, "hgjkhfjk", False)
])
async def test_find_user_by_id(user_id, email, exists):
    user = await UsersDAO.find_by_id(user_id)

    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
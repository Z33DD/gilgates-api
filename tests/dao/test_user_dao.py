import secrets
from gilgates_api.dao.user import UserDAO
from gilgates_api.model.user import User


async def test_create_user():
    email = f"{secrets.token_hex(8)}@example.com"
    dao = UserDAO()
    user = User(name="Pedro Antonio", email=email)
    uuid = await dao.create(user)

    assert uuid is not None


async def test_get_user():
    email = f"{secrets.token_hex(8)}@example.com"
    dao = UserDAO()
    expected = User(name="Test user", email=email)
    uuid = await dao.create(expected)

    user = await dao.get(uuid)

    assert user is not None
    assert user.name == expected.name
    assert user.email == expected.email


async def test_update_user():
    email = f"{secrets.token_hex(8)}@example.com"
    dao = UserDAO()
    expected = User(name="Apple", email=email)
    uuid = await dao.create(expected)

    user: User = await dao.get(uuid)

    user.name = "Banana"
    await dao.update(user)

    del dao
    dao = UserDAO()
    user: User = await dao.get(uuid)
    assert user is not None
    assert user.name == "Banana"


async def test_delete_user():
    email = f"{secrets.token_hex(8)}@example.com"
    dao = UserDAO()
    expected = User(name="Test user", email=email)
    uuid = await dao.create(expected)

    user = await dao.get(uuid)

    assert user is not None

    await dao.delete(uuid)

    user = await dao.get(uuid)

    assert user is None

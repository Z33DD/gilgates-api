import secrets
from pydantic import EmailStr
from gilgates_api.model import User
from gilgates_api import context
from gilgates_api.services.auth.password import hash_password


async def test_create_user():
    email = f"{secrets.token_hex(8)}@example.com"
    password = hash_password(str(secrets.token_hex(8)))
    
    dao = context.get()
    user = User(name="Pedro Antonio", email=EmailStr(email), password=password)
    uuid = await dao.user.create(user)

    assert uuid is not None


async def test_get_user():
    email = f"{secrets.token_hex(8)}@example.com"
    dao = context.get()
    expected = User(name="Test user", email=EmailStr(email))
    uuid = await dao.user.create(expected)

    user = await dao.user.get(uuid)

    assert user is not None
    assert user.name == expected.name
    assert user.email == expected.email


async def test_update_user():
    email = f"{secrets.token_hex(8)}@example.com"
    dao = context.get()
    expected = User(name="Apple", email=EmailStr(email))
    uuid = await dao.user.create(expected)

    user: User | None = await dao.user.get(uuid)
    assert user is not None

    user.name = "Banana"
    await dao.user.update(user)

    dao.user.clear()

    user: User | None = await dao.user.get(uuid)
    assert user is not None
    assert user.name == "Banana"


async def test_delete_user():
    email = f"{secrets.token_hex(8)}@example.com"
    dao = context.get()
    expected = User(name="Test user", email=EmailStr(email))
    uuid = await dao.user.create(expected)

    user = await dao.user.get(uuid)

    assert user is not None

    await dao.user.delete(uuid)

    user = await dao.user.get(uuid)

    assert user is None

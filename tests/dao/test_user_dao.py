import secrets
from pydantic import EmailStr
from sqlmodel import Session, select
from gilgates_api.model import User
from gilgates_api import dao_factory
from gilgates_api.services.auth.password import hash_password


async def test_create_user(session: Session):
    email = f"{secrets.token_hex(8)}@example.com"
    password = hash_password(str(secrets.token_hex(8)))

    dao = dao_factory(session)
    user = User(name="Pedro Antonio", email=EmailStr(email), password=password)
    uuid = await dao.user.create(user)

    assert uuid is not None


async def test_get_user(session: Session):
    email = f"{secrets.token_hex(8)}@example.com"
    dao = dao_factory(session)
    expected = User(name="Test user", email=EmailStr(email))
    uuid = await dao.user.create(expected)

    user = await dao.user.get(uuid)

    assert user is not None
    assert user.name == expected.name
    assert user.email == expected.email


async def test_update_user(session: Session):
    email = f"{secrets.token_hex(8)}@example.com"
    dao = dao_factory(session)
    expected = User(name="Apple", email=EmailStr(email))
    uuid = await dao.user.create(expected)

    user = await dao.user.get(uuid)
    assert user is not None

    user.name = "Banana"
    await dao.user.update(user)
    dao.user.commit()

    dao.user.clear()

    user = await dao.user.get(uuid)
    assert user is not None
    assert user.name == "Banana"

async def test_update_user_without_dao(session: Session):
    email = f"{secrets.token_hex(8)}@example.com"
    user = User(name="Apple", email=EmailStr(email))
    uid = user.uid
    session.add(user)
    session.commit()

    del user
    statement = select(User).where(User.uid == uid)
    user = session.exec(statement).one_or_none()
    assert user is not None

    user.name = "Banana"
    session.add(user)
    session.commit()

    del user
    statement = select(User).where(User.uid == uid)
    user = session.exec(statement).one_or_none()
    assert user is not None

    assert user.name == "Banana"




async def test_delete_user(session: Session):
    email = f"{secrets.token_hex(8)}@example.com"
    dao = dao_factory(session)
    expected = User(name="Test user", email=EmailStr(email))
    uuid = await dao.user.create(expected)

    user = await dao.user.get(uuid)

    assert user is not None

    await dao.user.delete(uuid)

    user = await dao.user.get(uuid)

    assert user is None

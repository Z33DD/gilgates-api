from gilgates_api.model.user import User
from gilgates_api.services.auth.password import hash_password, verify_password
from gilgates_api.services.auth.token import create_access_token, verify_token


async def test_access_token(user: User):
    access_token = create_access_token(user)
    payload = verify_token(access_token)

    assert payload.user.email == user.email

async def test_hash_password(user: User):
    plain_text = "1234567890"
    user.password = hash_password(plain_text)

    assert verify_password(plain_text, user.password)
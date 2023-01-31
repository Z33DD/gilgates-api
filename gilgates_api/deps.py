import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from gilgates_api.dao_factory import dao_factory
from gilgates_api.database import engine
from gilgates_api.models import User
from gilgates_api.models import Role
from gilgates_api.services.auth.token import verify_token
from sqlmodel import Session

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login", scheme_name="JWT", scopes={a.name: a.value for a in Role}
)


async def current_user(
    security_scopes: SecurityScopes, token: str = Depends(reuseable_oauth)
) -> User:

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    claims = verify_token(token)
    user_id = uuid.UUID(claims.sub)

    with Session(engine) as session:
        dao = dao_factory(session)
        user: User | None = await dao.user.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
            headers={"WWW-Authenticate": authenticate_value},
        )

    if not user.ative:
        raise HTTPException(status_code=400, detail="Inactive user")

    for scope in security_scopes.scopes:
        if scope not in claims.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user


def get_session():
    with Session(engine) as session:
        yield session

from datetime import datetime, timedelta
import json
from typing import Any, Dict, List, Optional
from gilgates_api.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
)
from pydantic import ValidationError, BaseModel
from fastapi import HTTPException, status
import jwt

from gilgates_api.model import User


class TokenPayload(BaseModel):
    sub: str
    user: User
    scopes: List[str]
    exp: float


def verify_token(token: str) -> TokenPayload:
    """
    The verify_token function takes a token as an argument and returns the payload
    if the token is valid. If not, it raises an HTTPException with status code 401.

    :param token: str: Pass the token string to the function
    :return: The decoded token payload
    :doc-author: Trelent
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return token_data
    except (jwt.DecodeError, jwt.ExpiredSignatureError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_access_token(
    user: User, expires: Optional[timedelta] = None, scopes: Optional[List[str]] = None
) -> str:
    """
    The create_access_token function creates an access token for a user.
    It takes in the user object and returns a string of the encoded JWT

    :param user: User: Pass in the user object
    :param expires: Optional[timedelta]: Set the expiration time of the token
    :param scopes: Optional[List[str]]: Define the scopes that are allowed to access the token
    :return: A jwt that has the following format:
    :doc-author: Trelent
    """

    if expires is not None:
        exp = datetime.utcnow() + expires
    else:
        exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    if not scopes:
        scopes = [user.role]

    payload = TokenPayload(
        sub=str(user.uid), user=user, exp=exp.timestamp(), scopes=scopes
    )
    dict_payload = __extract_payload(payload)

    encoded_jwt = jwt.encode(dict_payload, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(user: User, expires: timedelta | None = None) -> str:
    """
    The create_refresh_token function creates a refresh token for the user.
    The function takes in two parameters, subject and expires. The subject is the user's id,
    and expires is an optional parameter that defaults to None if not specified. If no value
    is passed into the function for expires then it will default to REFRESH_TOKEN_EXPIRE_MINUTES
    minutes from now.

    :param user: User: Get the user's name and uid
    :param expires: timedelta | None: Set the expiration time of the refresh token
    :return: A refresh token
    :doc-author: Trelent
    """
    if expires is not None:
        exp = datetime.utcnow() + expires
    else:
        exp = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": exp, "sub": str(user.uid)}
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def __extract_payload(payload: TokenPayload) -> Dict[str, Any]:
    str_json_payload = payload.json()
    dict_json_payload = json.loads(str_json_payload)
    return dict_json_payload

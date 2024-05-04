from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from schemes.settings import Settings, get_settings

auth_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')


def create_access_token(data: dict, expires_delta: timedelta | None = None,
                        settings: Settings = Depends(get_settings)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JTW_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(auth_scheme)],
                           settings: Settings = Depends(get_settings)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # user = None

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JTW_ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception

        user = {
            "username": username,
        }

        print(user)

    except JWTError:
        raise credentials_exception

    if user is None:
        raise credentials_exception

    return user

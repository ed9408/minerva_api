from fastapi import Depends
import jwt
import os

from jwt.exceptions import InvalidTokenError
from sqlmodel import Session, select

from ..db import get_session
from ..core.auth import verify_password
from ..core.exceptions import InvalidCredentialsException, InvalidRoleException
from ..dependencies import AuthDep
from ..models.user import User, UserRead, UserRole
from ..models.token import TokenData


def authenticate_user(
    session: Session, username: str, password: str
) -> bool | UserRead:
    statement = select(User).where(User.email == username)
    user = session.exec(statement).one_or_none()

    if not user or not verify_password(password, user.password):
        raise InvalidCredentialsException("Invalid username or password")

    return user


def get_user(session: Session, username: str) -> User | None:
    statement = select(User).where(User.email == username)
    user = session.exec(statement).one_or_none()

    return user


def get_current_user(token: AuthDep, session: Session = Depends(get_session)):
    try:
        payload: dict = jwt.decode(
            token,
            os.environ.get("SECRET_KEY"),
            algorithms=[os.environ.get("HASH_ALGORITHM")],
        )
        username: str = payload.get("sub")

        if username is None:
            raise InvalidCredentialsException("Invalid credentials")

        token_data: TokenData = TokenData(username=username)

    except InvalidTokenError:
        return str(InvalidTokenError)

    user = get_user(session, token_data.username)

    if not user:
        raise InvalidCredentialsException("Invalid credentials")

    return user


def get_admin_user(token: AuthDep, session: Session = Depends(get_session)):
    try:
        payload: dict = jwt.decode(
            token,
            os.environ.get("SECRET_KEY"),
            algorithms=[os.environ.get("HASH_ALGORITHM")],
        )
        username: str = payload.get("sub")

        if username is None:
            raise InvalidCredentialsException("Invalid credentials")

        token_data: TokenData = TokenData(username=username)

    except InvalidTokenError:
        return str(InvalidTokenError())

    user = get_user(session, token_data.username)

    if not user:
        raise InvalidCredentialsException("Invalid credentials")

    if user.role != UserRole.ADMIN:
        raise InvalidRoleException()

    return user

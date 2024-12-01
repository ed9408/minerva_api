from sqlmodel import Session, select
from typing import List

from ..core.auth import make_password
from ..models.user import User, UserCreate, UserRead, UserUpdate


def create_user(session: Session, user_data: UserCreate) -> UserRead | str:
    """Create a new user."""
    try:
        if len(user_data.password.strip()) == 0:
            return "Password cannot be empty"

        user_data.password = make_password(user_data.password)
        user = User.model_validate(user_data.model_dump())

        session.add(user)
        session.commit()
        session.refresh(user)

        return user
    except Exception as e:
        session.rollback()
        return str(e)


def get_users(session: Session) -> List[UserRead]:
    """Get all users."""
    return session.exec(select(User)).all()


def get_user(session: Session, user_id: int) -> UserRead | None | str:
    """Get a user by ID."""
    try:
        return session.get(User, user_id)
    except Exception as e:
        return str(e)


def update_user(
    session: Session, user_id: int, user_data: UserUpdate
) -> UserRead | None | str:
    """Update a user."""
    try:
        user = session.get(User, user_id)

        if not user:
            return None

        user_update_data = user_data.model_dump(exclude_unset=True)
        user.sqlmodel_update(user_update_data)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user
    except Exception as e:
        session.rollback()
        return str(e)


def delete_user(session: Session, user_id: int) -> bool | str:
    """Delete a user."""
    try:
        user = session.get(User, user_id)

        if not user:
            return False

        session.delete(user)
        session.commit()

        return True
    except Exception as e:
        session.rollback()
        return str(e)

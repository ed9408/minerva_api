from sqlmodel import Session, select
from typing import List

from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate
from ..models.user import User


def create_task(session: Session, task_data: TaskCreate) -> TaskRead | str:
    """Create a new task."""
    try:
        task = Task.model_validate(task_data.model_dump())

        session.add(task)
        session.commit()
        session.refresh(task)

        return task
    except Exception as e:
        session.rollback()
        return str(e)


def get_tasks(session: Session, user_id: int) -> List[TaskRead]:
    """Get all tasks for a user."""
    statement = select(Task).join(User).where(User.id == user_id)
    return session.exec(statement).all()


def get_task(session: Session, user_id: int, task_id: int) -> TaskRead | None | str:
    """Get a task by ID."""
    try:
        statement = (
            select(Task).join(User).where(User.id == user_id).where(Task.id == task_id)
        )
        task = session.exec(statement).one_or_none()

        if not task:
            return None

        return task
    except Exception as e:
        return str(e)


def update_task(
    session: Session, user_id: int, task_id: int, task_data: TaskUpdate
) -> TaskRead | None | str:
    """Update a task."""
    try:
        statement = (
            select(Task).join(User).where(User.id == user_id).where(Task.id == task_id)
        )
        task = session.exec(statement).one_or_none()

        if not task:
            return None

        task_update_data = task_data.model_dump(exclude_unset=True)
        task.sqlmodel_update(task_update_data)

        session.add(task)
        session.commit()
        session.refresh(task)

        return task
    except Exception as e:
        session.rollback()
        return str(e)


def delete_task(session: Session, user_id: int, task_id: int) -> bool | str:
    """Delete a task."""
    try:
        statement = (
            select(Task).join(User).where(User.id == user_id).where(Task.id == task_id)
        )
        task = session.exec(statement).one_or_none()

        if not task:
            return False

        session.delete(task)
        session.commit()

        return True
    except Exception as e:
        session.rollback()
        return str(e)

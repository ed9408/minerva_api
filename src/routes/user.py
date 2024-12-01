from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from ..db import get_session
from ..controllers import user as user_controller, task as task_controller
from ..dependencies.user import AdminUserDep, CurrentUserDep
from ..models.user import UserCreate, UserRead, UserUpdate
from ..models.task import TaskCreate, TaskRead, TaskUpdate


router = APIRouter(
    prefix="/users",
)


@router.post("/", status_code=status.HTTP_201_CREATED, tags=["signup"])
async def create_user(
    *, session: Session = Depends(get_session), user_data: UserCreate
) -> UserRead:
    """Create a new user."""
    new_user = user_controller.create_user(session=session, user_data=user_data)

    if isinstance(new_user, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=new_user)

    return new_user


@router.get("/", tags=["admin"])
async def get_users(
    *, session: Session = Depends(get_session), _: AdminUserDep
) -> List[UserRead]:
    """Get all users."""
    return user_controller.get_users(session=session)


@router.get("/{user_id}", tags=["admin"])
async def get_user(
    *, session: Session = Depends(get_session), user_id: int, _: AdminUserDep
) -> UserRead:
    """Get a user by ID."""
    user = user_controller.get_user(session=session, user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif isinstance(user, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=user)

    return user


@router.put("/{user_id}", tags=["admin"])
async def update_user(
    *,
    session: Session = Depends(get_session),
    user_id: int,
    user_data: UserUpdate,
    _: AdminUserDep
) -> UserRead:
    """Update a user."""
    user = user_controller.update_user(
        session=session, user_id=user_id, user_data=user_data
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif isinstance(user, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["admin"])
async def delete_user(
    *, session: Session = Depends(get_session), user_id: int, _: AdminUserDep
) -> None:
    """Delete a user."""
    user = user_controller.delete_user(session=session, user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif isinstance(user, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=user)


@router.get("/me", tags=["users"])
async def get_user(
    *, session: Session = Depends(get_session), current_user: CurrentUserDep
) -> UserRead:
    """Get the current user."""
    user = user_controller.get_user(session=session, user_id=current_user.id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif isinstance(user, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=user)

    return user


@router.put("/me", tags=["users"])
async def update_current_user(
    *,
    session: Session = Depends(get_session),
    user_data: UserUpdate,
    current_user: CurrentUserDep
) -> UserRead:
    """Update the current user."""
    user = user_controller.update_user(
        session=session, user_id=current_user.id, user_data=user_data
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif isinstance(user, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=user)

    return user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_current_user(
    *, session: Session = Depends(get_session), current_user: CurrentUserDep
) -> None:
    """Delete the current user."""
    user = user_controller.delete_user(session=session, user_id=current_user.id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif isinstance(user, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=user)


@router.post("/me/tasks", status_code=status.HTTP_201_CREATED, tags=["tasks"])
async def create_task(
    *, session: Session = Depends(get_session), task_data: TaskCreate, _: CurrentUserDep
) -> TaskRead:
    """Create a new task."""
    new_task = task_controller.create_task(session=session, task_data=task_data)

    if isinstance(new_task, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=new_task)

    return new_task


@router.get("/me/tasks", tags=["tasks"])
async def get_tasks(
    *, session: Session = Depends(get_session), current_user: CurrentUserDep
) -> List[TaskRead]:
    """Get all user tasks."""
    return task_controller.get_tasks(session=session, user_id=current_user.id)


@router.get("/me/tasks/{task_id}", tags=["tasks"])
async def get_task(
    *,
    session: Session = Depends(get_session),
    current_user: CurrentUserDep,
    task_id: int
) -> TaskRead:
    """Get a task by ID."""
    task = task_controller.get_task(
        session=session, user_id=current_user.id, task_id=task_id
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    elif isinstance(task, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=task)

    return task


@router.put("/me/tasks/{task_id}", tags=["tasks"])
async def update_task(
    *,
    session: Session = Depends(get_session),
    current_user: CurrentUserDep,
    task_id: int,
    task_data: TaskUpdate
) -> TaskRead:
    """Update a task."""
    task = task_controller.update_task(
        session=session, user_id=current_user.id, task_id=task_id, task_data=task_data
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    elif isinstance(task, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=task)

    return task


@router.delete(
    "/me/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"]
)
async def delete_task(
    *,
    session: Session = Depends(get_session),
    current_user: CurrentUserDep,
    task_id: int
) -> None:
    """Delete a task."""
    task = task_controller.delete_task(
        session=session, user_id=current_user.id, task_id=task_id
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    elif isinstance(task, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=task)

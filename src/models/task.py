from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class TaskBase(SQLModel):
    title: str = Field(nullable=False)
    description: str | None = Field(default=None)

    user_id: int = Field(foreign_key="user.id")


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user: "User" = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int


class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None

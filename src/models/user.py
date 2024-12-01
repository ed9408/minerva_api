from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserBase(SQLModel):
    name: str = Field(max_length=255, nullable=False)
    email: EmailStr = Field(max_length=255, nullable=False, unique=True, index=True)
    role: UserRole = Field()


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str = Field()

    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str
    role: UserRole


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

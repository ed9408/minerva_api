import os

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..db import get_session
from ..core.auth import create_access_token
from ..controllers import auth as auth_controller
from ..dependencies import AuthFormDep
from ..models.token import Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(*, session: Session = Depends(get_session), form_data: AuthFormDep) -> Token:
    user = auth_controller.authenticate_user(
        session=session, username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token_expires = timedelta(
        minutes=float(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")

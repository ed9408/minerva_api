from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from ..core.auth_schema import oauth2_scheme


AuthDep = Annotated[str, Depends(oauth2_scheme)]
AuthFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]

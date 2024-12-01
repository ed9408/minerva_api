from fastapi import Depends
from typing import Annotated

from ..controllers.auth import get_current_user, get_admin_user
from ..models.user import User

CurrentUserDep = Annotated[User, Depends(get_current_user)]
AdminUserDep = Annotated[User, Depends(get_admin_user)]

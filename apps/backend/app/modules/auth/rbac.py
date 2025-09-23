from fastapi import Depends, HTTPException, status

from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User


def require_superadmin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return current_user

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.domain.entities.user import User, UserRole
from app.infrastructure.database.models import UserModel
from app.infrastructure.database.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Bearer tokenni tekshirib, joriy foydalanuvchi obyektini qaytaradi."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Autentifikatsiya talab qilinadi yoki token yaroqsiz",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise credentials_exception

    username: str = payload["sub"]
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if not db_user:
        raise credentials_exception

    return User(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        role=UserRole(db_user.role),
    )


def require_roles(*allowed_roles: UserRole):
    """Faqat ruxsat etilgan rollarga kirish imkonini beruvchi RBAC tekshiruvi."""

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            allowed_names = ", ".join(r.value for r in allowed_roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Bu amal uchun yetarli vakolat yo'q. Talab qilinadigan rol: {allowed_names}",
            )
        return current_user

    return role_checker
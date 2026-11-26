from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.domain.entities.user import User, UserRole
from app.infrastructure.database.models import UserModel
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/auth", tags=["Autentifikatsiya"])


class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Foydalanuvchi nomi (login)")
    email: str = Field(..., min_length=5, max_length=120, description="Elektron pochta manzili")
    password: str = Field(..., min_length=6, max_length=100, description="Parol (kamida 6 belgi)")
    role: UserRole = Field(default=UserRole.VIEWER, description="Rol: viewer, organizer yoki admin")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "admin_azizjon",
                "email": "azizjon@football.uz",
                "password": "secret123",
                "role": "admin",
            }
        }
    )


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseSchema,
    summary="Yangi foydalanuvchini ro'yxatdan o'tkazish",
)
def register_user(payload: UserRegisterSchema, db: Session = Depends(get_db)):
    exists = (
        db.query(UserModel)
        .filter((UserModel.username == payload.username) | (UserModel.email == payload.email))
        .first()
    )
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu username yoki email allaqachon ro'yxatdan o'tgan",
        )

    db_user = UserModel(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role.value,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponseSchema(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        role=UserRole(db_user.role),
    )


@router.post(
    "/login",
    response_model=TokenResponseSchema,
    summary="Tizimga kirish va JWT token olish",
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login yoki parol noto'g'ri",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": db_user.username, "role": db_user.role})
    return TokenResponseSchema(access_token=token)


@router.get(
    "/me",
    response_model=UserResponseSchema,
    summary="Joriy foydalanuvchi profilini olish",
)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponseSchema(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
    )
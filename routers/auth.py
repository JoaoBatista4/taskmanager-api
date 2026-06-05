from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.auth_schemas import RegisterRequest, LoginRequest, LoginResponse, UserResponse
from services.auth_service import register_user, login_user, create_access_token

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", response_model=UserResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = register_user(data, db)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = login_user(data.email, data.password, db)
        token = create_access_token(str(user.id))
        return LoginResponse(token=token, user=UserResponse.model_validate(user))
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

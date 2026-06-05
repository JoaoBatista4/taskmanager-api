from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.models import User
from schemas.auth_schemas import RegisterRequest
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user_id: str) -> str:
    secret = os.getenv("JWT_SECRET_KEY", "fallback-key")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")
    expires_hours = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    expire = datetime.now(timezone.utc) + timedelta(hours=expires_hours)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, secret, algorithm=algorithm)


def register_user(data: RegisterRequest, db: Session) -> User:
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise ValueError("Email já cadastrado")

    hashed = pwd_context.hash(data.password)
    user = User(name=data.name, email=data.email, password_hash=hashed)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar usuário: {e.orig}")


def login_user(email: str, password: str, db: Session) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("Email ou senha inválidos")
    if not pwd_context.verify(password, user.password_hash):
        raise ValueError("Email ou senha inválidos")
    return user

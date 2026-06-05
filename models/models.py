from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum


class PriorityEnum(str, enum.Enum):
    low = "baixa"
    medium = "media"
    high = "alta"


class StatusEnum(str, enum.Enum):
    pending = "pendente"
    in_progress = "andamento"
    completed = "concluida"
    overdue = "atrasado"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    color = Column(String(7), nullable=False, default="#6366f1")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())

    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="categories")
    tasks = relationship("Task", back_populates="category", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Enum(PriorityEnum, create_constraint=False), nullable=False, default=PriorityEnum.medium)
    due_date = Column(DateTime, nullable=True)
    status = Column(Enum(StatusEnum, create_constraint=False), nullable=False, default=StatusEnum.pending)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")

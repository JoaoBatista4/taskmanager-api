from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str
    color: str = "#6366f1"


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    color: str
    user_id: int
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

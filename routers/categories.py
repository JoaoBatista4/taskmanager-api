from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.category_schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from services.category_service import (
    list_categories,
    list_all_categories,
    list_deleted_categories,
    create_category,
    update_category,
    delete_category,
    soft_delete_category,
)
from routers.dependencies import get_current_user
from models.models import User

category_router = APIRouter(prefix="/categories", tags=["Categories"])


@category_router.get("", response_model=list[CategoryResponse])
def list_user_categories(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_categories(user.id, db)


@category_router.get("/all", response_model=list[CategoryResponse])
def list_all_user_categories(
    db: Session = Depends(get_db),
):
    return list_all_categories(db)


@category_router.get("/deleted", response_model=list[CategoryResponse])
def list_user_deleted_categories(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_deleted_categories(user.id, db)


@category_router.post("", response_model=CategoryResponse)
def create_new_category(
    data: CategoryCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return create_category(user.id, data, db)
    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@category_router.put("/{category_id}", response_model=CategoryResponse)
def update_existing_category(
    category_id: int,
    data: CategoryUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return update_category(category_id, user.id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@category_router.delete("/{category_id}")
def delete_existing_category(
    category_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        delete_category(category_id, user.id, db)
        return {"detail": "Categoria deletada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@category_router.patch("/{category_id}/soft-delete", response_model=CategoryResponse)
def soft_delete_existing_category(
    category_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return soft_delete_category(category_id, user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

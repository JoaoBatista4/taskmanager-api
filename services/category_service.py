from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.models import Category
from schemas.category_schemas import CategoryCreate, CategoryUpdate
from datetime import datetime, timezone
from typing import Optional


def list_all_categories(db: Session) -> list[Category]:
    return (
        db.query(Category)
        .order_by(Category.created_at.desc())
        .all()
    )


def list_deleted_categories(user_id: int, db: Session) -> list[Category]:
    return (
        db.query(Category)
        .filter(Category.user_id == user_id, Category.deleted_at.isnot(None))
        .order_by(Category.deleted_at.desc())
        .all()
    )


def list_categories(user_id: int, db: Session) -> list[Category]:
    return (
        db.query(Category)
        .filter(Category.user_id == user_id, Category.deleted_at.is_(None))
        .all()
    )


def create_category(user_id: int, data: CategoryCreate, db: Session) -> Category:
    if not data.name.strip():
        raise ValueError("O nome da categoria é obrigatório")
    existing = (
        db.query(Category)
        .filter(Category.name == data.name.strip(), Category.user_id == user_id)
        .first()
    )
    if existing:
        raise ValueError("Já existe uma categoria com este nome")
    category = Category(name=data.name.strip(), color=data.color, user_id=user_id)
    db.add(category)
    try:
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar categoria: {e.orig}")


def get_category(category_id: int, user_id: int, db: Session) -> Category:
    cat = (
        db.query(Category)
        .filter(
            Category.id == category_id,
            Category.user_id == user_id,
            Category.deleted_at.is_(None),
        )
        .first()
    )
    if not cat:
        raise ValueError("Categoria não encontrada")
    return cat


def update_category(
    category_id: int, user_id: int, data: CategoryUpdate, db: Session
) -> Category:
    cat = get_category(category_id, user_id, db)
    if "name" in data.model_dump(exclude_unset=True) and data.name is not None:
        if not data.name.strip():
            raise ValueError("O nome da categoria é obrigatório")
        existing = (
            db.query(Category)
            .filter(
                Category.name == data.name.strip(),
                Category.user_id == user_id,
                Category.id != category_id,
            )
            .first()
        )
        if existing:
            raise ValueError("Já existe uma categoria com este nome")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if isinstance(value, str):
            value = value.strip() or None
        if value is not None:
            setattr(cat, key, value)
    try:
        db.commit()
        db.refresh(cat)
        return cat
    except IntegrityError as e:
        db.rollback()
        raise RuntimeError(f"Erro ao atualizar categoria: {e.orig}")


def soft_delete_category(category_id: int, user_id: int, db: Session) -> Category:
    cat = (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == user_id)
        .first()
    )
    if not cat:
        raise ValueError("Categoria não encontrada")
    cat.deleted_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(cat)
    return cat


def delete_category(category_id: int, user_id: int, db: Session) -> None:
    cat = (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == user_id)
        .first()
    )
    if not cat:
        raise ValueError("Categoria não encontrada")
    db.delete(cat)
    db.commit()

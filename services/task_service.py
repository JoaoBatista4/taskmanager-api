from sqlalchemy.orm import Session
from sqlalchemy import func
from models.models import Task, StatusEnum, PriorityEnum
from schemas.task_schemas import TaskCreate, TaskUpdate
from datetime import datetime, timezone
from typing import Optional


def list_all_tasks(db: Session) -> list[Task]:
    return (
        db.query(Task)
        .order_by(Task.created_at.desc())
        .all()
    )


def list_deleted_tasks(user_id: int, db: Session) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.user_id == user_id, Task.deleted_at.isnot(None))
        .order_by(Task.deleted_at.desc())
        .all()
    )


def list_tasks(
    user_id: int,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = None,
) -> list[Task]:
    query = db.query(Task).filter(Task.user_id == user_id, Task.deleted_at.is_(None))
    if status:
        query = query.filter(Task.status == status)
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))
    return query.order_by(Task.created_at.desc()).all()


def create_task(user_id: int, data: TaskCreate, db: Session) -> Task:
    if not data.title.strip():
        raise ValueError("O título da tarefa é obrigatório")
    task = Task(
        title=data.title.strip(),
        description=data.description.strip() if data.description else None,
        priority=data.priority,
        due_date=data.due_date,
        category_id=data.category_id,
        user_id=user_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(task_id: int, user_id: int, db: Session) -> Task:
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == user_id, Task.deleted_at.is_(None))
        .first()
    )
    if not task:
        raise ValueError("Tarefa não encontrada")
    return task


def update_task(task_id: int, user_id: int, data: TaskUpdate, db: Session) -> Task:
    task = get_task(task_id, user_id, db)
    if "title" in data.model_dump(exclude_unset=True) and data.title is not None:
        if not data.title.strip():
            raise ValueError("O título da tarefa é obrigatório")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if isinstance(value, str):
            value = value.strip() or None
        if value is not None:
            setattr(task, key, value)
    task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    return task


def soft_delete_task(task_id: int, user_id: int, db: Session) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise ValueError("Tarefa não encontrada")
    task.deleted_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    return task


def delete_task(task_id: int, user_id: int, db: Session) -> None:
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == user_id)
        .first()
    )
    if not task:
        raise ValueError("Tarefa não encontrada")
    db.delete(task)
    db.commit()


def update_task_status(task_id: int, user_id: int, status: str, db: Session) -> Task:
    task = get_task(task_id, user_id, db)
    task.status = status
    task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    return task


def get_dashboard_stats(user_id: int, db: Session) -> dict:
    now = datetime.now(timezone.utc)
    base = db.query(Task).filter(Task.user_id == user_id, Task.deleted_at.is_(None))
    total = base.count()
    pending = (
        base.filter(Task.status == StatusEnum.pending.value).count()
    )
    in_progress = (
        base.filter(Task.status == StatusEnum.in_progress.value).count()
    )
    completed = (
        base.filter(Task.status == StatusEnum.completed.value).count()
    )
    overdue = base.filter(
        (Task.status == StatusEnum.overdue.value) |
        ((Task.status != StatusEnum.completed.value) & (Task.due_date < now))
    ).count()
    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
        "overdue": overdue,
    }

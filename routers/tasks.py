from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.task_schemas import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskResponse,
)
from services.task_service import (
    list_tasks,
    list_all_tasks,
    list_deleted_tasks,
    create_task,
    update_task,
    delete_task,
    soft_delete_task,
    update_task_status,
)
from routers.dependencies import get_current_user
from models.models import User
from typing import Optional

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_router.get("", response_model=list[TaskResponse])
def list_user_tasks(
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_tasks(user.id, status, search, db)


@task_router.get("/all", response_model=list[TaskResponse])
def list_all_user_tasks(
    db: Session = Depends(get_db),
):
    return list_all_tasks(db)


@task_router.get("/deleted", response_model=list[TaskResponse])
def list_user_deleted_tasks(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_deleted_tasks(user.id, db)


@task_router.post("", response_model=TaskResponse)
def create_new_task(
    data: TaskCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return create_task(user.id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@task_router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from services.task_service import get_task

    try:
        return get_task(task_id, user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@task_router.put("/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: int,
    data: TaskUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return update_task(task_id, user.id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@task_router.delete("/{task_id}")
def delete_existing_task(
    task_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        delete_task(task_id, user.id, db)
        return {"detail": "Tarefa deletada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@task_router.patch("/{task_id}/soft-delete", response_model=TaskResponse)
def soft_delete_existing_task(
    task_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return soft_delete_task(task_id, user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@task_router.patch("/{task_id}/status", response_model=TaskResponse)
def change_task_status(
    task_id: int,
    data: TaskStatusUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return update_task_status(task_id, user.id, data.status, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

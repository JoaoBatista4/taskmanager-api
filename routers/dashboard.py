from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.task_schemas import DashboardStats
from services.task_service import get_dashboard_stats
from routers.dependencies import get_current_user
from models.models import User

dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@dashboard_router.get("/stats", response_model=DashboardStats)
def stats(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return DashboardStats(**get_dashboard_stats(user.id, db))

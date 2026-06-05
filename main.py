from config import app
from routers.auth import auth_router
from routers.tasks import task_router
from routers.categories import category_router
from routers.dashboard import dashboard_router
from database import Base, engine
from models import *
from sqlalchemy import text


def migrate_schema():
    tables_columns = {
        "tasks": "deleted_at",
        "categories": "deleted_at",
    }
    with engine.connect() as conn:
        for table, column in tables_columns.items():
            result = conn.execute(
                text(
                    f"SELECT COUNT(*) FROM pragma_table_info('{table}') WHERE name='{column}'"
                )
            )
            if result.scalar() == 0:
                conn.execute(
                    text(f"ALTER TABLE {table} ADD COLUMN {column} DATETIME")
                )
        conn.commit()


app.include_router(auth_router)
app.include_router(task_router)
app.include_router(category_router)
app.include_router(dashboard_router)


@app.get("/")
def home():
    return {"message": "Task Manager API funcionando"}


Base.metadata.create_all(bind=engine)
migrate_schema()

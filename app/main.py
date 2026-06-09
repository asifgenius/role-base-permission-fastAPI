from app.api.v1.auth import router as auth_router
from fastapi import FastAPI

from app.api.v1.comments import router as comments_router
from app.api.v1.posts import router as posts_router
from app.core.logger import configure_logging
from app.database.base import init_database
from app.exceptions.custom_exception import register_exception_handlers

configure_logging()
init_database()

app = FastAPI(title="Posts API", version="1.0.0")
register_exception_handlers(app)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(posts_router, prefix="/api/v1")
app.include_router(comments_router, prefix="/api/v1")

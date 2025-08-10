import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from app.admin.settings import admin
from app.routers.auth import router as auth_router
from app.routers.projects import router as projects_router
from app.routers.tasks import router as tasks_router
from app.settings import MEDIA_DIR, MEDIA_URL
from app.websocket.manager import WSManager
from app.websocket.routes import router as ws_router

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s - %(asctime)s",
    handlers=[
        logging.StreamHandler(),  # Output to console
    ],
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before
    logger.info("Starting application...")
    ws_manager = WSManager()
    app.state.ws_manager = ws_manager
    yield
    # after
    logger.info("Stopping application...")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def hello():
    return {"detail": "Hello World!"}


app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(ws_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="AGILE Task Management API",
        version="0.1.0",
        description="API with JWT-based Authentication",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

admin.mount_to(app=app)
app.mount(MEDIA_URL, StaticFiles(directory=MEDIA_DIR), name=MEDIA_DIR)

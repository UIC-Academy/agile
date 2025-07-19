from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.admin.settings import admin
from app.routers.auth import router as auth_router
from app.settings import MEDIA_DIR, MEDIA_URL

app = FastAPI()


@app.get("/")
async def hello():
    return {"detail": "Hello World!"}


app.include_router(auth_router)

admin.mount_to(app=app)

app.mount(MEDIA_URL, StaticFiles(directory=MEDIA_DIR), name=MEDIA_DIR)

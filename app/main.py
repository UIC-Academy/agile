from fastapi import FastAPI
from sqladmin import Admin

from app.admin.views import UserAdminView
from app.database import engine
from app.routers.auth import router as auth_router

app = FastAPI()


@app.get("/")
async def hello():
    return {"detail": "Hello World!"}


app.include_router(auth_router)


# SQLAdmin integration
admin = Admin(app=app, engine=engine)

admin.add_model_view(UserAdminView)

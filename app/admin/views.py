from typing import ClassVar

from sqladmin import ModelView

from app.models import User


class UserAdminView(ModelView, model=User):
    column_list: ClassVar = [
        User.id,
        User.email,
        User.password,
        User.fullname,
        User.avatar,
        User.role,
        User.is_active,
        User.is_deleted,
        User.created_at,
        User.updated_at,
    ]
    form_columns: ClassVar = [
        User.email,
        User.password,
        User.fullname,
        User.avatar,
        User.role,
        User.is_active,
        User.is_deleted,
    ]
    name: str = "User"
    name_plural: str = "Users"
    icon: str = "fa-solid fa-user"
    category: str = "accounts"
    category_icon: str = "fa-solid fa-user"

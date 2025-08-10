from starlette_admin.contrib.sqla import Admin

from app.admin.auth import JSONAuthProvider
from app.admin.views import (
    AuditLogAdminView,
    CommentAdminView,
    NotificationAdminView,
    ProjectAdminView,
    ProjectMemberAdminView,
    TaskAdminView,
    UserAdminView,
)
from app.database import engine
from app.models import (
    AuditLog,
    Comment,
    Notification,
    Project,
    ProjectMember,
    Task,
    User,
)

admin = Admin(
    engine=engine,
    title="Bookla Admin",
    base_url="/admin",
    auth_provider=JSONAuthProvider(login_path="/login", logout_path="/logout"),
)

admin.add_view(UserAdminView(User, icon="fa fa-user"))
admin.add_view(ProjectAdminView(Project, icon="fa fa-suitcase"))
admin.add_view(ProjectMemberAdminView(ProjectMember, icon="fa fa-users"))
admin.add_view(TaskAdminView(Task, icon="fa fa-tasks"))
admin.add_view(CommentAdminView(Comment, icon="fa fa-comment"))
admin.add_view(NotificationAdminView(Notification, icon="fa fa-bell"))
admin.add_view(AuditLogAdminView(AuditLog, icon="fa fa-history"))

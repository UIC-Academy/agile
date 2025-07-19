from starlette_admin.contrib.sqla import Admin

from app.admin.views import ProjectAdminView, UserAdminView
from app.database import engine
from app.models import Project, User

admin = Admin(
    engine=engine,
    title="Bookla Admin",
    base_url="/admin",
    # auth_provider=JSONAuthProvider(login_path="/login", logout_path="/logout"),
)

admin.add_view(UserAdminView(User, icon="fa fa-user"))
admin.add_view(ProjectAdminView(Project, icon="fa fa-suitcase"))

from rest_framework.routers import DefaultRouter

from . import views

task_router = DefaultRouter()
task_router.register(r"task", viewset=views.TaskViewSets, base_name="task")
task_router.register(r"var_table", viewset=views.VarTableViewSets, base_name="var_table")

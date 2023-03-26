import xadmin

from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

from applications.flow.urls import flow_router, node_router
from applications.home import views
from applications.home.urls import home_router
from applications.task.urls import task_router
from applications.user.urls import user_router
from dj_flow.views import index

urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('', index),
    path("process/", include(flow_router.urls)),
    path("node/", include(node_router.urls)),
    path("task/", include(task_router.urls)),
    path("home/", include(home_router.urls)),
    path("user/", include(user_router.urls)),
    path('es/stream/', views.stream, name='stream'),
    path(r'token/', obtain_jwt_token),

]

from rest_framework.routers import DefaultRouter

from . import views

home_router = DefaultRouter()
home_router.register(r"overview", viewset=views.OverviewSet, base_name="overview")
home_router.register(r"weekly_job", viewset=views.WeeklyJobViewSet, base_name="weekly_job")
home_router.register(r"top5_agent", viewset=views.TopAgentViewSet, base_name="top5_agent")
home_router.register(r"today_job", viewset=views.TodayJobViewSet, base_name="today_job")
home_router.register(r"job_dynamic", viewset=views.JobDynamicViewSet, base_name="job_dynamic")

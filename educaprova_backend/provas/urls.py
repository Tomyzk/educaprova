from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProvaViewSet, JobViewSet


router = DefaultRouter()
router.register(r"", ProvaViewSet, basename="provas")

jobs_router = DefaultRouter()
jobs_router.register(r"jobs", JobViewSet, basename="jobs")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(jobs_router.urls)),
]

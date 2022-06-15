from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core.views import (
    CreateUserView,
    ProfileViewSet,
    ExerciseViewSet,
    ExerciseLogViewSet,
    NextExerciseView,
)

router = routers.DefaultRouter()

router.register("profile", ProfileViewSet, basename="profile")
router.register("exercises", ExerciseViewSet, basename="exercises")
router.register("exerciselog", ExerciseLogViewSet, basename="exerciselog")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/create/", CreateUserView.as_view(), name="create"),
    path("api/v1/", include(router.urls)),
    path("api/v1/next-exercise/", NextExerciseView.as_view(), name="next-exercise"),
    path("auth/", include("djoser.urls.jwt")),
]

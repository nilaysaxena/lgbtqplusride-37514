from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.api.v1.viewsets import (
    SignupViewSet,
    LoginViewSet, NormalSignupViewSet, UserProfileViewSet,
)

router = DefaultRouter()
router.register("signup", NormalSignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("profile", UserProfileViewSet, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
]

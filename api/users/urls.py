from django.urls import path
from . import routers

urlpatterns = [
    path("auth/sign-up/", routers.SignUpRouter.as_view(), name="sign-up"),
    path("auth/sign-in/", routers.SignInRouter.as_view(), name="sign-in"),
    path("auth/status/", routers.AuthStatusRouter.as_view(), name="status"),
    path("auth/account/", routers.ProfileRouter.as_view(), name="account"),
    path("profile/", routers.ProfileRouter.as_view(), name="profile"),
]

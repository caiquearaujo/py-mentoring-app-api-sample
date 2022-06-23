from django.urls import path
from . import routers

urlpatterns = [path("auth/sign-up", routers.SignUpRouter.as_view(), name="sign-up")]

from rest_framework import views, response, exceptions, permissions

from . import auth
from . import serializer as user_serializer
from . import services


class AuthStatusRouter(views.APIView):
    def get(self, request):
        user = auth.read_token(request)
        status = "non-authenticated"

        if user:
            status = "authenticated"

        return response.Response(data={"status": status})


class SignUpRouter(views.APIView):
    def post(self, request):
        serializer = user_serializer.UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        serializer.instance = services.create_user(user=data)
        return response.Response(data=serializer.data)


class SignInRouter(views.APIView):
    def post(self, request):
        serializer = user_serializer.UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = services.find_by_email(data["email"])

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid credentials, cannot continue")

        if not user.check_password(raw_password=data["password"]):
            raise exceptions.AuthenticationFailed("Invalid credentials, cannot continue")

        payload, token = services.create_token(id=user.id)
        return response.Response(
            {"token_type": "Bearer", "expires_at": payload["exp"], "access_token": token}
        )

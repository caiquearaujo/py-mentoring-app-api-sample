from datetime import datetime
from rest_framework import views, response, exceptions, permissions
from marshmallow import ValidationError, fields

from . import auth
from . import models
from . import services
from . import schemas


class AuthStatusRouter(views.APIView):
    def get(self, request):
        status = "non-authenticated"

        if request.user:
            status = "authenticated"

        return response.Response(data={"status": status})


class ProfileRouter(views.APIView):
    authentication_classes = (auth.UserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user: models.User = request.user
        return response.Response(schemas.UserSchema().dump(user))

    def post(self, request):
        user: models.User = request.user

        try:
            schema = schemas.ProfileCreateSchema().load(request.data)
        except ValidationError as err:
            return response.Response(err.messages)

        data = schemas.UserData(**schema)
        return response.Response(
            data=schemas.UserSchema().dump(services.update_account(user, **data))
        )


class AccountRouter(views.APIView):
    authentication_classes = (auth.UserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user: models.User = request.user

        try:
            schema = schemas.AccountUpdateSchema().load(request.data)
        except ValidationError as err:
            return response.Response(err.messages)

        email = schema["email"]
        password = schema["password"]

        if email and user.email is email["old"] and email["new"]:
            email = email["new"]

        if password and password["new"] and user.check_password(password["old"]):
            password = password["new"]

        return response.Response(
            data=schemas.UserSchema().dump(
                services.update_account(user, email=email, password=password)
            )
        )


class SignUpRouter(views.APIView):
    def post(self, request):
        try:
            schema = schemas.ProfileCreateSchema().load(request.data)
        except ValidationError as err:
            return response.Response(err.messages)

        data = schemas.UserData(**schema)
        return response.Response(
            data=schemas.UserSchema().dump(services.create_new_account(data))
        )


class SignInRouter(views.APIView):
    def post(self, request):
        try:
            schema = schemas.LoginSchema().load(request.data)
        except ValidationError as err:
            return response.Response(err.messages)

        user = services.find_by_email(schema["email"])

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid credentials, cannot continue")

        if not user.check_password(schema["password"]):
            raise exceptions.AuthenticationFailed("Invalid credentials, cannot continue")

        user.last_login = datetime.utcnow()
        user.save()

        payload, token = services.create_token(id=user.id)
        return response.Response(
            {"token_type": "Bearer", "expires_at": payload["exp"], "access_token": token}
        )

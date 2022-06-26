from django.conf import settings
from rest_framework import authentication, exceptions
import re

import core.jwt as jwt
from . import models


class UserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user = read_token(request)

        if user is None:
            raise exceptions.AuthenticationFailed("Unauthorized")

        return (user, None)


def read_token(request):
    token = request.headers.get("Authorization")

    if not token:
        return None

    try:
        pattern = "Bearer (.*)"
        matches = re.findall(pattern, token)
        token = matches[0]

        if not token:
            return None

        payload = jwt.decode(token)
    except:
        return None

    return models.User.objects.filter(id=payload["sub"]).first()

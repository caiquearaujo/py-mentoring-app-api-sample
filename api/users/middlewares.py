from typing import TYPE_CHECKING
from . import auth

if TYPE_CHECKING:
    from .models import User


class FetchUserMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        request.user: "User" = auth.read_token(request)
        response = self.get_response(request)
        return response

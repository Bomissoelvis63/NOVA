# apps/authentication/services.py
# Services metier pour l'authentification NOVA.
# Ils isolent la logique de login, logout et blacklist JWT.
# Ils gardent les vues fines et orientees transport HTTP.
# Ils centralisent les erreurs attendues des bibliotheques externes.
# Son but est d'appliquer une separation claire des responsabilites.
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class InvalidRefreshToken(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Refresh token invalide."
    default_code = "invalid_refresh_token"


class TokenService:
    @staticmethod
    def blacklist_refresh_token(raw_token):
        if not raw_token:
            return

        try:
            RefreshToken(raw_token).blacklist()
        except TokenError as exc:
            raise InvalidRefreshToken() from exc


class SessionService:
    @staticmethod
    def login(request, user):
        login(request, user)

    @staticmethod
    def logout(request):
        logout(request)
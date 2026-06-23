# Vues API d'authentification de NOVA.
# Elles exposent JWT et sessions serveur selon le besoin client.
# Elles emettent des tokens ou creent une session Django en base.
# Elles gerent logout, refresh et profil courant de facon separee.
# Son but est de fournir deux strategies d'authentification claires.
from typing import Any, cast

from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.serializers import RegisterSerializer, UserSerializer

from .serializers import LoginSerializer, SessionLoginSerializer
from .services import SessionService, TokenService


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]


class RefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class LogoutView(APIView):
    def post(self, request):
        TokenService.blacklist_refresh_token(request.data.get("refresh"))
        SessionService.logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class SessionCSRFView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        return Response({"detail": "CSRF cookie set."})


@method_decorator(csrf_protect, name="dispatch")
class SessionLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = SessionLoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        validated_data = cast(dict[str, Any], serializer.validated_data)
        SessionService.login(request, validated_data["user"])
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name="dispatch")
class SessionLogoutView(APIView):
    def post(self, request):
        SessionService.logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SessionMeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)

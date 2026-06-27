# # Vues API d'authentification de NOVA.
# # Elles exposent JWT et sessions serveur selon le besoin client.
# # Elles emettent des tokens ou creent une session Django en base.
# # Elles gerent logout, refresh et profil courant de facon separee.
# # Son but est de fournir deux strategies d'authentification claires.
# from typing import Any, cast

# from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
# from django.utils.decorators import method_decorator
# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from apps.accounts.serializers import RegisterSerializer, UserSerializer

# from .serializers import LoginSerializer, SessionLoginSerializer
# from .services import SessionService, TokenService


# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer
#     permission_classes = [permissions.AllowAny]


# class LoginView(TokenObtainPairView):
#     serializer_class = LoginSerializer
#     permission_classes = [permissions.AllowAny]


# class RefreshView(TokenRefreshView):
#     permission_classes = [permissions.AllowAny]


# class LogoutView(APIView):
#     def post(self, request):
#         TokenService.blacklist_refresh_token(request.data.get("refresh"))
#         SessionService.logout(request)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class MeView(APIView):
#     def get(self, request):
#         return Response(UserSerializer(request.user).data)


# @method_decorator(ensure_csrf_cookie, name="dispatch")
# class SessionCSRFView(APIView):
#     permission_classes = [permissions.AllowAny]
#     authentication_classes = []

#     def get(self, request):
#         return Response({"detail": "CSRF cookie set."})


# @method_decorator(csrf_protect, name="dispatch")
# class SessionLoginView(APIView):
#     permission_classes = [permissions.AllowAny]
#     authentication_classes = []

#     def post(self, request):
#         serializer = SessionLoginSerializer(data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         validated_data = cast(dict[str, Any], serializer.validated_data)
#         SessionService.login(request, validated_data["user"])
#         return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


# @method_decorator(csrf_protect, name="dispatch")
# class SessionLogoutView(APIView):
#     def post(self, request):
#         SessionService.logout(request)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class SessionMeView(APIView):
#     def get(self, request):
#         return Response(UserSerializer(request.user).data)


# Vues API d'authentification de NOVA.
# Elles exposent JWT et sessions serveur selon le besoin client.
# Elles emettent des tokens ou creent une session Django en base.
# Elles gerent logout, refresh et profil courant de facon separee.
# Son but est de fournir deux strategies d'authentification claires.
from typing import Any, cast

from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Ajout des nouveaux serializers ici
from apps.accounts.serializers import (
    RegisterSerializer, 
    UserSerializer,
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    PasswordResetConfirmSerializer
)
from apps.accounts.models import PasswordResetOTP, User

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


# ==============================================================================
# VUES POUR LA PROCÉDURE DE MOT DE PASSE OUBLIÉ (OTP EMAIL)
# ==============================================================================

class PasswordResetRequestView(APIView):
    """Étape 1 : Valider l'email, générer l'OTP et envoyer le mail (en console)"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)
        
        # Génère et sauvegarde l'OTP à 6 chiffres
        otp_record = PasswordResetOTP.objects.create(user=user)
        
        # Simulation d'envoi d'email (apparaîtra dans la console VS Code)
        send_mail(
            subject="[NOVA] Code de réinitialisation de mot de passe",
            message=f"Bonjour,\n\nVoici votre code OTP de réinitialisation : {otp_record.code}\nIl expire dans 10 minutes.",
            from_email="NOVA Support <noreply@nova.ci>",
            recipient_list=[email],
            fail_silently=False,
        )
        
        return Response(
            {"detail": "Un code OTP a été envoyé à votre adresse email."},
            status=status.HTTP_200_OK
        )


class PasswordResetVerifyView(APIView):
    """Étape 2 : Valider que l'OTP saisi par le marchand sur Flutter est correct"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"detail": "Code OTP valide. Vous pouvez modifier votre mot de passe."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(APIView):
    """Étape 3 : Appliquer le nouveau mot de passe et consommer définitivement l'OTP"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = cast(dict[str, Any], serializer.validated_data)
        otp_record = validated_data["otp_record"]
        user = otp_record.user
        
        # Hachage et mise à jour sécurisée du mot de passe
        user.set_password(validated_data["new_password"])
        user.save()
        
        # Invalidation du code OTP utilisé
        otp_record.is_used = True
        otp_record.save()
        
        return Response(
            {"detail": "Votre mot de passe a été réinitialisé avec succès."},
            status=status.HTTP_200_OK
        )


# ==============================================================================
# STRATÉGIE D'AUTHENTIFICATION BASÉE SUR LES SESSIONS (WEB / ADMIN)
# ==============================================================================

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

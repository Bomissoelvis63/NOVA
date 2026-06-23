# Serializers d'authentification de NOVA.
# Ils couvrent le login JWT et le login par session serveur.
# Ils valident les credentials sans exposer les mots de passe.
# Ils retournent les donnees utilisateur utiles aux clients.
# Son but est de normaliser les flux d'authentification.
from typing import Any

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.serializers import UserSerializer


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        data: dict[str, Any] = dict(super().validate(attrs))
        data["user"] = UserSerializer(self.user).data
        return data


class SessionLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        request = self.context.get("request")
        user = authenticate(request=request, username=attrs["email"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Identifiants invalides.")
        if not user.is_active:
            raise serializers.ValidationError("Compte utilisateur desactive.")
        attrs["user"] = user
        return attrs

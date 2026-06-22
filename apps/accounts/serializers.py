# Serializers API pour les utilisateurs NOVA.
# Ils exposent le profil utilisateur et ses roles en lecture.
# Ils valident l'inscription avec mot de passe hache par Django.
# Ils limitent les champs modifiables pour proteger l'etat interne.
# Son but est de convertir proprement users entre JSON et modeles.
from rest_framework import serializers

from apps.authorization.serializers import RoleSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "is_active", "roles", "created_at")
        read_only_fields = ("id", "is_active", "roles", "created_at")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name")
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)

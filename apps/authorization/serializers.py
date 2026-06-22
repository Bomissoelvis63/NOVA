# Serializers API pour le RBAC NOVA.
# Ils convertissent roles et permissions entre JSON et modeles.
# Ils gerent l'affectation de permissions actives a un role.
# Ils valident l'association d'un role a un utilisateur actif.
# Son but est de securiser les entrees API d'autorisation.
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Permission, Role


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("id", "code", "name", "description", "is_active", "created_at")
        read_only_fields = ("id", "created_at")


class RoleSerializer(serializers.ModelSerializer):
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.filter(is_active=True),
        source="permissions",
        many=True,
        write_only=True,
        required=False,
    )
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ("id", "key", "name", "description", "permissions", "permission_ids", "is_active", "created_at")
        read_only_fields = ("id", "permissions", "created_at")


class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    role_key = serializers.SlugField()

    def validate(self, attrs):
        User = get_user_model()
        try:
            attrs["user"] = User.objects.get(id=attrs["user_id"], is_active=True)
            attrs["role"] = Role.objects.get(key=attrs["role_key"], is_active=True)
        except (User.DoesNotExist, Role.DoesNotExist) as exc:
            raise serializers.ValidationError("Utilisateur ou role invalide.") from exc
        return attrs

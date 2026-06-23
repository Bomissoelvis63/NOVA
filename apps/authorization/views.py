# Vues API d'autorisation de NOVA.
# Elles exposent le CRUD roles et permissions pour les admins.
# Elles permettent d'assigner un role actif a un utilisateur actif.
# Elles s'appuient sur les serializers pour valider les donnees.
# Son but est de fournir l'administration RBAC minimale du MVP.
from typing import Any, cast

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Permission, Role
from .serializers import AssignRoleSerializer, PermissionSerializer, RoleSerializer
from .services import RoleAssignmentService


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.prefetch_related("permissions").all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAdminUser]


class AssignRoleView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast(dict[str, Any], serializer.validated_data)
        RoleAssignmentService.assign_role(
            user=validated_data["user"],
            role=validated_data["role"],
        )
        return Response({"detail": "Role assigne."}, status=status.HTTP_200_OK)

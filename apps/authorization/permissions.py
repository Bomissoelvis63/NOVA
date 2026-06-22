# Permission DRF reutilisable pour le RBAC NOVA.
# Elle lit un code de permission requis depuis la vue.
# Elle delegue la verification au modele User custom.
# Elle permet de proteger finement des endpoints specifiques.
# Son but est d'offrir un controle RBAC simple cote DRF.
from rest_framework.permissions import BasePermission


class HasRBACPermission(BasePermission):
    required_permission = None

    def has_permission(self, request, view):
        code = getattr(view, "required_permission", self.required_permission)
        if not code:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.has_rbac_permission(code))

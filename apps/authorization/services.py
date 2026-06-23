# Services metier pour l'autorisation NOVA.
# Ils isolent les operations RBAC reutilisables.
# Ils evitent de placer la logique d'affectation dans les vues.
# Ils fournissent un point d'extension pour les regles futures.
# Son but est de garder l'autorisation claire et maintenable.
from django.db import transaction


class RoleAssignmentService:
    @staticmethod
    @transaction.atomic
    def assign_role(user, role):
        user.roles.add(role)
        return user

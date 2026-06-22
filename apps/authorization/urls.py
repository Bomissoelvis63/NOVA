# Routes de l'application authorization.
# Elles publient le CRUD roles et permissions via un router DRF.
# Elles ajoutent l'endpoint dedie a l'assignation de role utilisateur.
# Elles restent groupees sous le prefixe global /authorization/.
# Son but est d'exposer l'API RBAC du serveur NOVA.
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AssignRoleView, PermissionViewSet, RoleViewSet

router = DefaultRouter()
router.register("roles", RoleViewSet, basename="roles")
router.register("permissions", PermissionViewSet, basename="permissions")

urlpatterns = [
    path("users/assign-role/", AssignRoleView.as_view(), name="assign-role"),
]
urlpatterns += router.urls

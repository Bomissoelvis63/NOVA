# Middleware de journalisation d'audit NOVA.
# Il cree une trace apres chaque requete API traitee.
# Il ignore les routes admin et fichiers statiques pour limiter le bruit.
# Il capture l'utilisateur, l'adresse IP et le user-agent.
# Son but est d'assurer une visibilite minimale sur les acces.
import logging

from django.db import DatabaseError

from .models import AuditLog

logger = logging.getLogger(__name__)


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith(("/admin/", "/static/")):
            return response

        try:
            user = (
                request.user
                if getattr(request, "user", None) and request.user.is_authenticated
                else None
            )
            AuditLog.objects.create(
                user=user,
                action=self._action(request),
                path=request.path[:255],
                method=request.method,
                status_code=response.status_code,
                ip_address=self._ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:255],
            )
        except DatabaseError:
            logger.exception("Unable to write audit log.")

        return response

    def _action(self, request):
        if request.path.startswith("/auth/login/"):
            return "login"
        if request.path.startswith("/auth/logout/"):
            return "logout"
        if request.path.startswith("/auth/register/"):
            return "register"
        return "api_request"

    def _ip(self, request):
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

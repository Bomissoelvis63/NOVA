# Middleware RBAC global de NOVA.
# Il compare methode et chemin aux regles NOVA_RBAC_RULES.
# Il authentifie via JWT si l'utilisateur n'est pas encore resolu.
# Il bloque les requetes sans permission applicative requise.
# Son but est d'appliquer des controles d'acces transverses.
from django.conf import settings
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class RBACMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authentication = JWTAuthentication()

    def __call__(self, request):
        code = settings.NOVA_RBAC_RULES.get(f"{request.method}:{request.path_info}")
        if not code:
            return self.get_response(request)

        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            try:
                authenticated = self.jwt_authentication.authenticate(request)
            except AuthenticationFailed:
                return JsonResponse({"detail": "Authentification invalide."}, status=401)

            if authenticated:
                user, _ = authenticated
                request.user = user

        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return JsonResponse({"detail": "Authentification requise."}, status=401)

        if not user.has_rbac_permission(code):
            return JsonResponse({"detail": "Permission refusee."}, status=403)

        return self.get_response(request)

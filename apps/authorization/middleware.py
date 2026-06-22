# Middleware RBAC global de NOVA.
# Il compare methode et chemin aux regles NOVA_RBAC_RULES.
# Il authentifie via JWT si l'utilisateur n'est pas encore resolu.
# Il bloque les requetes sans permission applicative requise.
# Son but est d'appliquer des controles d'acces transverses.
from django.conf import settings
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication


class RBACMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authentication = JWTAuthentication()

    def __call__(self, request):
        code = settings.NOVA_RBAC_RULES.get(f"{request.method}:{request.path}")
        if not code:
            return self.get_response(request)

        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            authenticated = self.jwt_authentication.authenticate(request)
            if authenticated:
                user, _ = authenticated
                request.user = user

        if not request.user.is_authenticated or not request.user.has_rbac_permission(code):
            return JsonResponse({"detail": "Permission refusee."}, status=403)

        return self.get_response(request)

# Point d'entree ASGI du projet NOVA.
# Il expose l'application Django aux serveurs compatibles async.
# Il charge config.settings avant de creer l'application.
# Il prepare le projet a des usages temps reel futurs si necessaire.
# Son but est de fournir l'interface serveur ASGI standard.
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()

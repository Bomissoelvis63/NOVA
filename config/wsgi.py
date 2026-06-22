# Point d'entree WSGI du projet NOVA.
# Il expose l'application Django aux serveurs Python classiques.
# Il charge config.settings avant de creer l'application.
# Il sert aux deploiements avec Gunicorn ou plateformes similaires.
# Son but est de fournir l'interface serveur WSGI standard.
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

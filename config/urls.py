# Routes globales du backend NOVA.
# Elles connectent l'admin Django et les apps API principales.
# Elles exposent les endpoints auth et authorization du noyau IAM.
# Elles gardent le routage global simple et lisible.
# Son but est de centraliser les points d'entree HTTP du projet.
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("apps.authentication.urls")),
    path("authorization/", include("apps.authorization.urls")),
]

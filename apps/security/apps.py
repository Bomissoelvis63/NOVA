# # apps/security/apps.py
# from django.apps import AppConfig
# from django.db.models.signals import post_migrate

# class SecurityConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'apps.security'

#     def ready(self):
#         # 1. Import de notre fonction de synchronisation
#         from apps.security.utils import synchroniser_les_droits
        
#         # 2. Sécurité : On l'exécute DIRECTEMENT au démarrage du serveur
#         try:
#             synchroniser_les_droits(sender=self)
#         except Exception:
#             # On met un try/except au cas où les tables n'existent pas encore du tout
#             pass
        
#         # 3. On laisse le signal pour les futures migrations
#         post_migrate.connect(synchroniser_les_droits)


# apps/security/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class SecurityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.security'

    def ready(self):
        # On importe la fonction proprement
        from apps.security.utils import synchroniser_les_droits
        
        # On la connecte UNIQUEMENT au signal. Pas d'appel direct ici !
        post_migrate.connect(synchroniser_les_droits)
        
        
        
        
        
        
# apps/security/permissions.py
from rest_framework.permissions import DjangoModelPermissions

class StrictDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        # On ajoute le GET dans la carte des permissions à vérifier obligatoirement
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
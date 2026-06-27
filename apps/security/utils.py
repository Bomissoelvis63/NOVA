# apps/security/utils.py
from django.contrib.auth.models import Group, Permission
from apps.security.fixtures import GROUPS_CONFIG

def synchroniser_les_droits(sender, **kwargs):
    """
    Parcourt GROUPS_CONFIG pour créer les groupes et synchroniser 
    leurs permissions associées après les migrations.
    Gère les chemins d'applications complexes et normalise la casse.
    """
    for nom_du_groupe, configuration in GROUPS_CONFIG.items():
        
        # A) Création ou récupération du groupe
        groupe, cree = Group.objects.get_or_create(name=nom_du_groupe)
        
        # B) Extraction et récupération des objets de permissions
        liste_des_permissions = configuration.get("permissions", [])
        objets_permissions = []
        
        for perms in liste_des_permissions:
            # 🎯 Sécurise le découpage si le chemin contient plusieurs points (ex: apps.merchants.codename)
            parts = perms.rsplit('.', 1)
            if len(parts) != 2:
                continue
                
            app_label, codename = parts
            
            # 🎯 Normalise en minuscules pour correspondre aux codenames natifs de Django
            codename = codename.lower()
            
            try:
                p = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                objets_permissions.append(p)
            except Permission.DoesNotExist:
                # La permission n'existe pas encore ou l'application n'est pas chargée
                continue 
        
        # C) Application des permissions (mise à jour automatique sans doublons)
        groupe.permissions.set(objets_permissions)
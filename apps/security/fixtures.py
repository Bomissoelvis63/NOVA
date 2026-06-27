# apps/security/fixtures.py
"""
Configuration centrale des groupes et permissions de NOVA.
Toutes les permissions doivent respecter le format Django : app_label.codename
"""

GROUP_ADMIN = "Administrateur"
GROUP_MARCHAND = "Marchand"
GROUP_LIVREUR = "Livreur"
GROUP_CLIENT = "Client"

GROUPS_CONFIG = {
    GROUP_ADMIN: {
        "permissions": [
            # Accounts / User
            "accounts.view_user",
            "accounts.add_user",
            "accounts.change_user",
            "accounts.delete_user",
            
            # Merchants / PaymentMethod

        ]
    },

    GROUP_MARCHAND: {
        "permissions": [
            # Accounts
            "accounts.view_user",
            "accounts.add_user",
            "accounts.change_user",
            "accounts.delete_user",
            
            # Merchants / PaymentMethod
            # "merchants.add_paymentMethod",
            "merchants.view_paymentMethod",
            # "merchants.change_paymentMethod",
        ]
    },

    GROUP_LIVREUR: {
        "permissions": [
            # Remplir plus tard
        ]
    },
    
    GROUP_CLIENT: {
        "permissions": [
            # Remplir plus tard
        ]
    },
}
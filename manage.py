#!/usr/bin/env python
# Point d'entree CLI du projet Django NOVA.
# Il charge la configuration principale depuis config.settings.
# Il permet d'executer migrations, serveur local et commandes admin.
# Il reste volontairement minimal pour suivre le standard Django.
# Son but est de piloter le backend IAM depuis la ligne de commande.
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

import django
import os


def init_django_env():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()

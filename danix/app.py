import os, sys, django

sys.dont_write_bytecode = True

# Django specific settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()
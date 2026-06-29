# -*- coding: utf-8 -*-
"""
Initialisation production (idempotente), lancee au build sur l'hebergeur.
- Cree le compte admin s'il n'existe pas.
- Remplit les donnees de demo UNIQUEMENT si la base est vide
  (donc rien n'est ecrase aux redeploiements).
"""
import os
import sys
import subprocess
import django

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.agencies.models import Agency

# ── Compte admin ──
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Atlas2026')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@atlas-location.ma')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"[init_prod] Compte admin '{username}' cree.")
else:
    print(f"[init_prod] Compte admin '{username}' deja present.")

# ── Donnees de demo (seulement si base vide) ──
if not Agency.objects.exists():
    print("[init_prod] Base vide -> remplissage des donnees de demo...")
    for script in ('seed_demo.py', 'assign_photos.py', 'seed_phase2.py'):
        chemin = os.path.join(BASE, 'scripts', script)
        print(f"[init_prod] Execution de {script}...")
        subprocess.run([sys.executable, chemin], check=True)
    print("[init_prod] Donnees de demo creees.")
else:
    print("[init_prod] Donnees deja presentes -> seed ignore.")

print("[init_prod] Termine.")

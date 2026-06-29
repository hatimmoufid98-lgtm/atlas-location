import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.cars.models import Car

assignments = {
    "Renault":    ("Clio",     "cars/renault-clio.jpg"),
    "Volkswagen": ("Golf",     "cars/volkswagen-golf.jpg"),
    "Hyundai":    ("Tucson",   "cars/vw-tiguan.jpg"),
    "Dacia":      ("Logan",    "cars/opel-corsa.png"),
    "Peugeot":    ("308",      "cars/cupra-leon.avif"),
    "BMW":        ("Serie 5",  "cars/voiture-1.avif"),
}

for marque, (modele, photo_path) in assignments.items():
    try:
        car = Car.objects.get(marque=marque, modele=modele)
        car.photo = photo_path
        car.save()
        print(f"OK {marque} {modele} -> {photo_path}")
    except Car.DoesNotExist:
        print(f"Voiture non trouvee : {marque} {modele}")

print("Photos assignees.")

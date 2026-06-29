# -*- coding: utf-8 -*-
"""
Script de donnees de demo : Atlas Location, Fes.
"""
import os
import sys
import django
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.agencies.models import Agency
from apps.cars.models import Car
from apps.bookings.models import Booking, BlockedPeriod

print("Nettoyage des donnees existantes...")
BlockedPeriod.objects.all().delete()
Booking.objects.all().delete()
Car.objects.all().delete()
Agency.objects.all().delete()

print("Creation de l'agence Atlas Location...")
agency = Agency.objects.create(
    nom="Atlas Location",
    slug="atlas-location",
    couleur_principale="#C8A96E",
    telephone="0535 12 34 56",
    ville="Fes",
    adresse="12 Avenue Hassan II, Fes-Medina, Fes 30000",
    actif=True,
)

print("Creation des voitures...")
voitures_data = [
    dict(marque="Dacia", modele="Logan", categorie="economique", transmission="manuelle",
         carburant="diesel", nombre_places=5, prix_par_jour=200,
         description="Voiture economique fiable, ideale pour les longs trajets."),
    dict(marque="Renault", modele="Clio", categorie="economique", transmission="manuelle",
         carburant="essence", nombre_places=5, prix_par_jour=220,
         description="Citadine pratique et maniable. Parfaite pour la ville."),
    dict(marque="Dacia", modele="Sandero", categorie="economique", transmission="manuelle",
         carburant="essence", nombre_places=5, prix_par_jour=210,
         description="Spacieuse et economique, le meilleur rapport qualite-prix."),
    dict(marque="Citroen", modele="C3", categorie="economique", transmission="manuelle",
         carburant="diesel", nombre_places=5, prix_par_jour=230,
         description="Confortable et sobre, ideale pour les familles."),
    dict(marque="Peugeot", modele="308", categorie="normale", transmission="manuelle",
         carburant="diesel", nombre_places=5, prix_par_jour=380,
         description="Berline moderne avec equipements complets."),
    dict(marque="Hyundai", modele="Tucson", categorie="normale", transmission="automatique",
         carburant="diesel", nombre_places=5, prix_par_jour=450,
         description="SUV moderne, spacieux et confortable."),
    dict(marque="Toyota", modele="Corolla", categorie="normale", transmission="automatique",
         carburant="hybride", nombre_places=5, prix_par_jour=420,
         description="Hybride fiable et economique."),
    dict(marque="Volkswagen", modele="Golf", categorie="normale", transmission="automatique",
         carburant="essence", nombre_places=5, prix_par_jour=400,
         description="La reference des berlines compactes."),
    dict(marque="Mercedes-Benz", modele="Classe C", categorie="luxe", transmission="automatique",
         carburant="essence", nombre_places=5, prix_par_jour=900,
         description="Berline de prestige. Interieur cuir, climatisation bizone."),
    dict(marque="BMW", modele="Serie 5", categorie="luxe", transmission="automatique",
         carburant="diesel", nombre_places=5, prix_par_jour=1100,
         description="Le summum du confort et de la performance."),
    dict(marque="Range Rover", modele="Evoque", categorie="luxe", transmission="automatique",
         carburant="diesel", nombre_places=5, prix_par_jour=1300,
         description="SUV de luxe britannique. Ideal pour explorer le Maroc."),
    dict(marque="Audi", modele="A6", categorie="luxe", transmission="automatique",
         carburant="diesel", nombre_places=5, prix_par_jour=950,
         description="Elegance et technologie allemandes."),
]

voitures = []
for data in voitures_data:
    v = Car.objects.create(agency=agency, **data)
    voitures.append(v)
    print(f"  OK {v.marque} {v.modele} ({v.get_categorie_display()}) - {v.prix_par_jour} MAD/j")

today = date.today()
logan   = voitures[0]
clio    = voitures[1]
sandero = voitures[2]
p308    = voitures[4]
tucson  = voitures[5]
merc    = voitures[8]

print("\nCreation des reservations de demo...")
bookings_data = [
    dict(car=logan,   nom_client="Mohammed Alami",  telephone_client="0661 23 45 67",
         email_client="m.alami@gmail.com",
         date_debut=today + timedelta(days=2), date_fin=today + timedelta(days=5),
         statut="confirmee"),
    dict(car=clio,    nom_client="Fatima Benali",   telephone_client="0672 34 56 78",
         email_client="f.benali@hotmail.com",
         date_debut=today + timedelta(days=1), date_fin=today + timedelta(days=4),
         statut="en_attente"),
    dict(car=p308,    nom_client="Youssef Chraibi", telephone_client="0655 45 67 89",
         email_client="y.chraibi@gmail.com",
         date_debut=today + timedelta(days=3), date_fin=today + timedelta(days=8),
         statut="confirmee"),
    dict(car=tucson,  nom_client="Nadia Tazi",      telephone_client="0644 56 78 90",
         email_client="n.tazi@gmail.com",
         date_debut=today + timedelta(days=5), date_fin=today + timedelta(days=10),
         statut="confirmee"),
    dict(car=merc,    nom_client="Khalid El Fassi", telephone_client="0660 12 34 56",
         email_client="k.elfassi@email.com",
         date_debut=today + timedelta(days=7), date_fin=today + timedelta(days=9),
         statut="confirmee"),
    dict(car=sandero, nom_client="Samira Idrissi",  telephone_client="0671 89 01 23",
         email_client="s.idrissi@gmail.com",
         date_debut=today - timedelta(days=10), date_fin=today - timedelta(days=7),
         statut="confirmee"),
]

for b_data in bookings_data:
    b = Booking.objects.create(**b_data)
    print(f"  OK {b.car} -> {b.nom_client} ({b.date_debut} -> {b.date_fin}) [{b.get_statut_display()}]")

print("\nCreation des periodes bloquees...")
BlockedPeriod.objects.create(
    car=voitures[6],
    date_debut=today + timedelta(days=2),
    date_fin=today + timedelta(days=4),
    raison="Revision annuelle"
)
BlockedPeriod.objects.create(
    car=voitures[10],
    date_debut=today + timedelta(days=1),
    date_fin=today + timedelta(days=3),
    raison="Entretien carrosserie"
)

print("\n=== DONNEES DE DEMO CREEES AVEC SUCCES ===")
print(f"  1 agence  : {agency.nom} ({agency.ville})")
print(f"  {Car.objects.count()} voitures")
print(f"  {Booking.objects.count()} reservations")
print(f"  {BlockedPeriod.objects.count()} periodes bloquees")

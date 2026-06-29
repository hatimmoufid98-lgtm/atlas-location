# -*- coding: utf-8 -*-
"""
Script de donnees de demo Phase 2 : maintenance + finances.
Assurances, vignettes, lavages, pleins carburant, revisions, depenses.
"""
import os
import sys
import django
import random
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.agencies.models import Agency
from apps.cars.models import Car
from apps.bookings.models import Booking
from apps.maintenance.models import Assurance, Vignette, Lavage, PleinCarburant, Revision
from apps.finance.models import CategorieDepense, Depense

today = date.today()

print("Nettoyage des donnees Phase 2 existantes...")
Assurance.objects.all().delete()
Vignette.objects.all().delete()
Lavage.objects.all().delete()
PleinCarburant.objects.all().delete()
Revision.objects.all().delete()
Depense.objects.all().delete()
CategorieDepense.objects.all().delete()

agency = Agency.objects.first()
cars = list(Car.objects.all())
if not cars:
    print("ERREUR : aucune voiture. Lancez d'abord seed_demo.py")
    sys.exit(1)

# ─── ASSURANCES ──────────────────────────────────────────────────────────────
print("Creation des assurances...")
compagnies = ["Wafa Assurance", "AXA Maroc", "RMA Watanya", "Saham Assurance", "Atlanta Assurance"]
# Echelonnees : certaines deja expirees, certaines bientot, certaines OK
offsets_fin = [-15, 12, 25, 70, 150, 200, 8, 45, 300, 18, 120, 90]
for i, car in enumerate(cars):
    fin = today + timedelta(days=offsets_fin[i % len(offsets_fin)])
    Assurance.objects.create(
        car=car,
        compagnie=random.choice(compagnies),
        numero_police=f"POL-{2025}-{1000 + i}",
        date_debut=fin - timedelta(days=365),
        date_fin=fin,
        montant_annuel=random.choice([3500, 4200, 4800, 5500, 6200, 7800]),
    )
print(f"  OK {Assurance.objects.count()} assurances")

# ─── VIGNETTES ───────────────────────────────────────────────────────────────
print("Creation des vignettes...")
montants_vignette = {"economique": 700, "normale": 1500, "luxe": 6000}
for car in cars:
    Vignette.objects.create(
        car=car,
        annee=today.year,
        date_paiement=date(today.year, 1, random.randint(5, 28)),
        date_expiration=date(today.year, 12, 31),
        montant=montants_vignette.get(car.categorie, 1500),
    )
print(f"  OK {Vignette.objects.count()} vignettes")

# ─── LAVAGES ─────────────────────────────────────────────────────────────────
print("Creation des lavages...")
types_lavage = ['exterieur', 'interieur', 'complet', 'detailing']
prix_lavage = {'exterieur': 30, 'interieur': 40, 'complet': 60, 'detailing': 250}
stations = ["Station Shell Atlas", "Lavage Express Fes", "Auto Clean Saiss"]
for car in cars:
    for _ in range(random.randint(2, 4)):
        t = random.choice(types_lavage)
        Lavage.objects.create(
            car=car,
            date=today - timedelta(days=random.randint(1, 120)),
            type_lavage=t,
            montant=prix_lavage[t],
            prestataire=random.choice(stations),
        )
print(f"  OK {Lavage.objects.count()} lavages")

# ─── PLEINS CARBURANT ────────────────────────────────────────────────────────
print("Creation des pleins carburant...")
stations_carb = ["Afriquia", "Shell", "Total", "Petrom", "Winxo"]
for car in cars:
    carb = 'diesel' if car.carburant in ('diesel',) else ('essence' if car.carburant in ('essence', 'hybride') else 'electrique')
    km = random.randint(40000, 120000)
    # Plusieurs pleins successifs avec km croissant
    for j in range(random.randint(3, 5)):
        km += random.randint(450, 750)
        litres = round(random.uniform(38, 55), 2)
        prix_litre = 15.2 if carb == 'diesel' else 14.5
        PleinCarburant.objects.create(
            car=car,
            date=today - timedelta(days=(5 - j) * random.randint(8, 15)),
            km_compteur=km,
            litres=litres,
            montant=round(litres * prix_litre, 2),
            type_carburant=carb,
            station=random.choice(stations_carb),
        )
print(f"  OK {PleinCarburant.objects.count()} pleins")

# ─── REVISIONS ───────────────────────────────────────────────────────────────
print("Creation des revisions...")
types_rev = ['vidange', 'revision', 'freins', 'pneus', 'courroie', 'climatisation']
prix_rev = {'vidange': 600, 'revision': 1800, 'freins': 1200, 'pneus': 3200, 'courroie': 2500, 'climatisation': 800}
garages = ["Garage Central Fes", "Auto Service Saiss", "Mecano Plus", "Garage Atlas Motors"]
for car in cars:
    for _ in range(random.randint(1, 3)):
        t = random.choice(types_rev)
        km = random.randint(50000, 130000)
        Revision.objects.create(
            car=car,
            date=today - timedelta(days=random.randint(10, 300)),
            type_revision=t,
            description=f"{dict(Revision.TYPE_CHOICES)[t]} effectuee",
            km_compteur=km,
            montant=prix_rev[t],
            garage=random.choice(garages),
            prochaine_revision_km=km + 10000,
            prochaine_revision_date=today + timedelta(days=random.randint(30, 180)),
        )
print(f"  OK {Revision.objects.count()} revisions")

# ─── CATEGORIES DE DEPENSES ──────────────────────────────────────────────────
print("Creation des categories de depenses...")
categories_data = [
    ("Loyer agence", "🏢"),
    ("Salaires", "👥"),
    ("Electricite & Eau", "💡"),
    ("Internet & Telephone", "📞"),
    ("Marketing & Publicite", "📢"),
    ("Fournitures bureau", "📎"),
    ("Frais bancaires", "🏦"),
    ("Taxes & Impots", "📋"),
]
categories = {}
for nom, icone in categories_data:
    categories[nom] = CategorieDepense.objects.create(nom=nom, icone=icone)
print(f"  OK {CategorieDepense.objects.count()} categories")

# ─── DEPENSES ────────────────────────────────────────────────────────────────
print("Creation des depenses...")
depenses_recurrentes = [
    ("Loyer agence", "Loyer mensuel local commercial", 6000),
    ("Salaires", "Salaire employe - agent comptoir", 4500),
    ("Salaires", "Salaire employe - chauffeur livreur", 3800),
    ("Electricite & Eau", "Facture electricite", 850),
    ("Internet & Telephone", "Abonnement fibre + lignes mobiles", 600),
]
# Generer pour les 6 derniers mois
for mois_offset in range(6):
    mois_date = today.replace(day=1) - timedelta(days=mois_offset * 30)
    for cat_nom, desc, montant in depenses_recurrentes:
        Depense.objects.create(
            agency=agency,
            categorie=categories[cat_nom],
            date=mois_date.replace(day=random.randint(1, 28)),
            description=desc,
            montant=montant + random.randint(-100, 200),
        )

# Quelques depenses ponctuelles
depenses_ponctuelles = [
    ("Marketing & Publicite", "Campagne publicitaire Facebook/Instagram", 1500),
    ("Marketing & Publicite", "Impression flyers et cartes de visite", 800),
    ("Fournitures bureau", "Achat papeterie et consommables", 450),
    ("Frais bancaires", "Frais de tenue de compte trimestriels", 350),
    ("Taxes & Impots", "Taxe professionnelle", 4200),
]
for cat_nom, desc, montant in depenses_ponctuelles:
    Depense.objects.create(
        agency=agency,
        categorie=categories[cat_nom],
        date=today - timedelta(days=random.randint(5, 90)),
        description=desc,
        montant=montant,
    )
print(f"  OK {Depense.objects.count()} depenses")

# ─── RESERVATIONS REALISTES SUR L'ANNEE (pour un bilan coherent) ─────────────
print("Creation de reservations confirmees reparties sur l'annee...")
MARQUEUR = "[DEMO-BILAN]"
Booking.objects.filter(notes_agence=MARQUEUR).delete()

clients = [
    ("Mohammed Alami", "0661234567", "m.alami@gmail.com"),
    ("Fatima Benali", "0672345678", "f.benali@hotmail.com"),
    ("Youssef Chraibi", "0655456789", "y.chraibi@gmail.com"),
    ("Nadia Tazi", "0644567890", "n.tazi@gmail.com"),
    ("Khalid El Fassi", "0660123456", "k.elfassi@email.com"),
    ("Samira Idrissi", "0671890123", "s.idrissi@gmail.com"),
    ("Omar Bennani", "0662345678", "o.bennani@gmail.com"),
    ("Leila Saidi", "0673456789", "l.saidi@gmail.com"),
    ("Karim Lahlou", "0654567890", "k.lahlou@gmail.com"),
    ("Hind Berrada", "0645678901", "h.berrada@gmail.com"),
]

# Generation par voiture : on remplit le calendrier jour par jour avec des
# locations non chevauchantes separees de petits intervalles (voiture au parc).
debut_annee = date(today.year, 1, 1)
nb_bookings = 0
for car in cars:
    curseur = debut_annee
    while curseur < today:
        # Intervalle "voiture disponible / non louee" avant la prochaine location
        curseur += timedelta(days=random.randint(2, 11))
        if curseur >= today:
            break
        duree = random.randint(2, 7)
        d_fin = curseur + timedelta(days=duree)
        if d_fin > today:
            d_fin = today
        if (d_fin - curseur).days < 1:
            break
        nom, tel, mail = random.choice(clients)
        Booking.objects.create(
            car=car,
            nom_client=nom,
            telephone_client=tel,
            email_client=mail,
            date_debut=curseur,
            date_fin=d_fin,
            statut="confirmee",
            notes_agence=MARQUEUR,
        )
        nb_bookings += 1
        curseur = d_fin  # la prochaine location commence apres le retour
print(f"  OK {nb_bookings} reservations confirmees (annee {today.year})")

print("\n=== DONNEES PHASE 2 CREEES AVEC SUCCES ===")
print(f"  {Assurance.objects.count()} assurances")
print(f"  {Vignette.objects.count()} vignettes")
print(f"  {Lavage.objects.count()} lavages")
print(f"  {PleinCarburant.objects.count()} pleins carburant")
print(f"  {Revision.objects.count()} revisions")
print(f"  {CategorieDepense.objects.count()} categories de depenses")
print(f"  {Depense.objects.count()} depenses")
print(f"  {Booking.objects.filter(notes_agence=MARQUEUR).count()} reservations de bilan")

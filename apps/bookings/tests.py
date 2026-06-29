"""
Tests de la logique de disponibilité.
Prouvent que :
  1. Une voiture réservée n'apparaît plus disponible sur ces dates.
  2. On ne peut pas créer deux réservations qui se chevauchent.
  3. Un BlockedPeriod empêche aussi la disponibilité.
  4. Des dates adjacentes (non-chevauchantes) restent disponibles.
"""
from datetime import date
from django.test import TestCase
from django.db import IntegrityError

from apps.agencies.models import Agency
from apps.cars.models import Car
from apps.cars.availability import get_available_cars, is_car_available
from apps.bookings.models import Booking, BlockedPeriod


def make_agency():
    return Agency.objects.create(
        nom="Test Agence",
        telephone="0600000000",
        ville="Fès",
        adresse="123 Rue Test",
    )


def make_car(agency, prix=300):
    return Car.objects.create(
        agency=agency,
        marque="Dacia",
        modele="Logan",
        categorie="economique",
        prix_par_jour=prix,
        actif=True,
    )


def make_booking(car, debut, fin, statut="confirmee"):
    return Booking.objects.create(
        car=car,
        nom_client="Client Test",
        telephone_client="0600000001",
        email_client="test@test.com",
        date_debut=debut,
        date_fin=fin,
        statut=statut,
    )


class DisponibiliteTestCase(TestCase):

    def setUp(self):
        self.agency = make_agency()
        self.car = make_car(self.agency)

    # ------------------------------------------------------------------ #
    # 1. Voiture réservée (confirmée) → plus disponible sur ces dates
    # ------------------------------------------------------------------ #
    def test_voiture_reservee_confirmee_non_disponible(self):
        make_booking(self.car, date(2025, 8, 1), date(2025, 8, 7), statut="confirmee")

        dispo = is_car_available(self.car, date(2025, 8, 3), date(2025, 8, 5))
        self.assertFalse(dispo, "La voiture doit être indisponible (réservation confirmée chevauche)")

    # ------------------------------------------------------------------ #
    # 2. Voiture réservée (en_attente) → aussi indisponible
    # ------------------------------------------------------------------ #
    def test_voiture_reservee_en_attente_non_disponible(self):
        make_booking(self.car, date(2025, 8, 1), date(2025, 8, 7), statut="en_attente")

        dispo = is_car_available(self.car, date(2025, 8, 1), date(2025, 8, 7))
        self.assertFalse(dispo, "La voiture doit être indisponible (réservation en_attente chevauche)")

    # ------------------------------------------------------------------ #
    # 3. Réservation annulée → voiture redevient disponible
    # ------------------------------------------------------------------ #
    def test_voiture_reservee_annulee_disponible(self):
        make_booking(self.car, date(2025, 8, 1), date(2025, 8, 7), statut="annulee")

        dispo = is_car_available(self.car, date(2025, 8, 1), date(2025, 8, 7))
        self.assertTrue(dispo, "La voiture doit être disponible (réservation annulée ne bloque pas)")

    # ------------------------------------------------------------------ #
    # 4. Dates adjacentes → pas de chevauchement
    # ------------------------------------------------------------------ #
    def test_dates_adjacentes_disponible(self):
        # Réservé du 1 au 7 août
        make_booking(self.car, date(2025, 8, 1), date(2025, 8, 7))

        # Du 7 au 10 : doit être disponible (chevauchement si debut < fin_existante ET fin > debut_existante)
        # 7 < 7 est FAUX → pas de chevauchement
        dispo = is_car_available(self.car, date(2025, 8, 7), date(2025, 8, 10))
        self.assertTrue(dispo, "Des dates adjacentes ne doivent pas se chevaucher")

    # ------------------------------------------------------------------ #
    # 5. BlockedPeriod bloque la disponibilité
    # ------------------------------------------------------------------ #
    def test_blocked_period_rend_indisponible(self):
        BlockedPeriod.objects.create(
            car=self.car,
            date_debut=date(2025, 9, 1),
            date_fin=date(2025, 9, 5),
            raison="Maintenance"
        )

        dispo = is_car_available(self.car, date(2025, 9, 2), date(2025, 9, 4))
        self.assertFalse(dispo, "Un BlockedPeriod doit rendre la voiture indisponible")

    # ------------------------------------------------------------------ #
    # 6. get_available_cars exclut les voitures réservées
    # ------------------------------------------------------------------ #
    def test_get_available_cars_exclut_reservees(self):
        car2 = make_car(self.agency, prix=400)
        make_booking(self.car, date(2025, 10, 1), date(2025, 10, 5))

        dispo = get_available_cars(self.agency, date(2025, 10, 1), date(2025, 10, 5))

        ids = list(dispo.values_list('id', flat=True))
        self.assertNotIn(self.car.id, ids, "La voiture réservée ne doit pas apparaître dans les résultats")
        self.assertIn(car2.id, ids, "La voiture libre doit apparaître dans les résultats")

    # ------------------------------------------------------------------ #
    # 7. Voiture inactive → n'apparaît pas dans les résultats
    # ------------------------------------------------------------------ #
    def test_voiture_inactive_non_affichee(self):
        self.car.actif = False
        self.car.save()

        dispo = get_available_cars(self.agency, date(2025, 11, 1), date(2025, 11, 5))
        ids = list(dispo.values_list('id', flat=True))
        self.assertNotIn(self.car.id, ids, "Une voiture inactive ne doit pas apparaître")

    # ------------------------------------------------------------------ #
    # 8. Filtre par catégorie fonctionne
    # ------------------------------------------------------------------ #
    def test_filtre_categorie(self):
        car_luxe = Car.objects.create(
            agency=self.agency, marque="Mercedes", modele="Classe C",
            categorie="luxe", prix_par_jour=900, actif=True
        )

        dispo = get_available_cars(self.agency, date(2025, 12, 1), date(2025, 12, 5), categorie="luxe")
        ids = list(dispo.values_list('id', flat=True))
        self.assertIn(car_luxe.id, ids)
        self.assertNotIn(self.car.id, ids)  # car self.car est économique

    # ------------------------------------------------------------------ #
    # 9. Chevauchement partiel : début de la nouvelle période dans l'existante
    # ------------------------------------------------------------------ #
    def test_chevauchement_partiel_debut(self):
        make_booking(self.car, date(2025, 8, 1), date(2025, 8, 10))

        # Début dans la réservation, fin après
        dispo = is_car_available(self.car, date(2025, 8, 8), date(2025, 8, 15))
        self.assertFalse(dispo, "Chevauchement partiel (début dans existante) doit bloquer")

    # ------------------------------------------------------------------ #
    # 10. Chevauchement partiel : fin de la nouvelle période dans l'existante
    # ------------------------------------------------------------------ #
    def test_chevauchement_partiel_fin(self):
        make_booking(self.car, date(2025, 8, 5), date(2025, 8, 12))

        # Début avant, fin dans la réservation
        dispo = is_car_available(self.car, date(2025, 8, 1), date(2025, 8, 8))
        self.assertFalse(dispo, "Chevauchement partiel (fin dans existante) doit bloquer")

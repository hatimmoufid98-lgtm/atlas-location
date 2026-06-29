"""
Logique de disponibilité — cœur du produit.

Règle de chevauchement entre [A_debut, A_fin] et [B_debut, B_fin] :
  chevauchement si (A_debut < B_fin) ET (A_fin > B_debut)

Cette vérification est faite côté base de données (pas en Python),
ce qui garantit les performances même avec des milliers de réservations.
"""
from django.db.models import Q


def get_overlapping_filter(date_debut, date_fin):
    """
    Retourne un filtre Q Django qui détecte un chevauchement avec [date_debut, date_fin].
    S'applique à tout modèle ayant les champs date_debut et date_fin.
    """
    return Q(date_debut__lt=date_fin) & Q(date_fin__gt=date_debut)


def get_available_cars(agency, date_debut, date_fin, categorie=None):
    """
    Retourne les voitures disponibles pour une agence sur la période demandée.
    Une voiture est disponible si :
      - elle est active
      - aucune réservation (en_attente ou confirmée) ne chevauche la période
      - aucun BlockedPeriod ne chevauche la période
    """
    from apps.cars.models import Car
    from apps.bookings.models import Booking, BlockedPeriod

    overlap = get_overlapping_filter(date_debut, date_fin)

    cars_with_booking = Booking.objects.filter(
        overlap,
        statut__in=['en_attente', 'confirmee']
    ).values_list('car_id', flat=True)

    cars_blocked = BlockedPeriod.objects.filter(overlap).values_list('car_id', flat=True)

    qs = Car.objects.filter(agency=agency, actif=True)
    qs = qs.exclude(id__in=cars_with_booking)
    qs = qs.exclude(id__in=cars_blocked)

    if categorie:
        qs = qs.filter(categorie=categorie)

    return qs


def is_car_available(car, date_debut, date_fin, exclude_booking_id=None):
    """
    Vérifie si une voiture spécifique est disponible sur la période.
    exclude_booking_id permet d'exclure la réservation en cours de modification.
    """
    from apps.bookings.models import Booking, BlockedPeriod

    overlap = get_overlapping_filter(date_debut, date_fin)

    booking_qs = Booking.objects.filter(
        overlap,
        car=car,
        statut__in=['en_attente', 'confirmee']
    )
    if exclude_booking_id:
        booking_qs = booking_qs.exclude(id=exclude_booking_id)

    if booking_qs.exists():
        return False

    if BlockedPeriod.objects.filter(overlap, car=car).exists():
        return False

    return True

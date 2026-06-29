from django.db import models
from apps.cars.models import Car


class Booking(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
    ]

    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name='bookings', verbose_name="Voiture")
    nom_client = models.CharField(max_length=200, verbose_name="Nom complet")
    telephone_client = models.CharField(max_length=20, verbose_name="Téléphone")
    email_client = models.EmailField(verbose_name="Email")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name="Statut")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Créée le")
    notes_agence = models.TextField(blank=True, verbose_name="Notes internes")

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.car} — {self.nom_client} ({self.date_debut} → {self.date_fin})"

    @property
    def nombre_jours(self):
        return (self.date_fin - self.date_debut).days

    @property
    def prix_total(self):
        return self.nombre_jours * self.car.prix_par_jour


class BlockedPeriod(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='blocked_periods', verbose_name="Voiture")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    raison = models.CharField(max_length=300, verbose_name="Raison", help_text="Ex: Maintenance, Révision, Réservé agence")

    class Meta:
        verbose_name = "Période bloquée"
        verbose_name_plural = "Périodes bloquées"
        ordering = ['date_debut']

    def __str__(self):
        return f"{self.car} bloquée du {self.date_debut} au {self.date_fin} ({self.raison})"

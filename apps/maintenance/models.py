from django.db import models
from django.utils import timezone
from apps.cars.models import Car


class Assurance(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='assurances', verbose_name="Voiture")
    compagnie = models.CharField(max_length=200, verbose_name="Compagnie d'assurance")
    numero_police = models.CharField(max_length=100, verbose_name="Numéro de police", blank=True)
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date d'expiration")
    montant_annuel = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant annuel (MAD)")
    document = models.FileField(upload_to='assurances/', blank=True, null=True, verbose_name="Document (PDF)")
    notes = models.TextField(blank=True, verbose_name="Notes")

    class Meta:
        verbose_name = "Assurance"
        verbose_name_plural = "Assurances"
        ordering = ['-date_fin']

    def __str__(self):
        return f"{self.car} — {self.compagnie} (expire {self.date_fin})"

    @property
    def est_active(self):
        return self.date_debut <= timezone.now().date() <= self.date_fin

    @property
    def jours_restants(self):
        delta = self.date_fin - timezone.now().date()
        return delta.days

    @property
    def expire_bientot(self):
        return 0 <= self.jours_restants <= 30


class Vignette(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='vignettes', verbose_name="Voiture")
    annee = models.PositiveIntegerField(verbose_name="Année")
    date_paiement = models.DateField(verbose_name="Date de paiement")
    date_expiration = models.DateField(verbose_name="Date d'expiration")
    montant = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Montant (MAD)")
    recu = models.FileField(upload_to='vignettes/', blank=True, null=True, verbose_name="Reçu (PDF/photo)")

    class Meta:
        verbose_name = "Vignette"
        verbose_name_plural = "Vignettes"
        ordering = ['-annee']
        unique_together = [('car', 'annee')]

    def __str__(self):
        return f"{self.car} — Vignette {self.annee}"

    @property
    def jours_restants(self):
        return (self.date_expiration - timezone.now().date()).days

    @property
    def expire_bientot(self):
        return 0 <= self.jours_restants <= 30


class Lavage(models.Model):
    TYPE_CHOICES = [
        ('exterieur', 'Extérieur'),
        ('interieur', 'Intérieur'),
        ('complet', 'Complet'),
        ('detailing', 'Détailing'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='lavages', verbose_name="Voiture")
    date = models.DateField(verbose_name="Date")
    type_lavage = models.CharField(max_length=20, choices=TYPE_CHOICES, default='complet', verbose_name="Type")
    montant = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Montant (MAD)")
    prestataire = models.CharField(max_length=200, blank=True, verbose_name="Prestataire / Station")

    class Meta:
        verbose_name = "Lavage"
        verbose_name_plural = "Lavages"
        ordering = ['-date']

    def __str__(self):
        return f"{self.car} — Lavage {self.get_type_lavage_display()} le {self.date}"


class PleinCarburant(models.Model):
    CARBURANT_CHOICES = [
        ('essence', 'Essence'),
        ('diesel', 'Diesel'),
        ('electrique', 'Électrique'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='pleins', verbose_name="Voiture")
    date = models.DateField(verbose_name="Date")
    km_compteur = models.PositiveIntegerField(verbose_name="Kilométrage au compteur")
    litres = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Litres")
    montant = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Montant (MAD)")
    type_carburant = models.CharField(max_length=20, choices=CARBURANT_CHOICES, default='diesel', verbose_name="Carburant")
    station = models.CharField(max_length=200, blank=True, verbose_name="Station-service")

    class Meta:
        verbose_name = "Plein carburant"
        verbose_name_plural = "Pleins carburant"
        ordering = ['-date']

    def __str__(self):
        return f"{self.car} — {self.litres}L le {self.date} ({self.km_compteur} km)"

    @property
    def consommation_aux_100(self):
        pleins = list(
            PleinCarburant.objects.filter(car=self.car, km_compteur__lt=self.km_compteur)
            .order_by('-km_compteur')[:1]
        )
        if pleins:
            km_parcourus = self.km_compteur - pleins[0].km_compteur
            if km_parcourus > 0:
                return round(float(self.litres) / km_parcourus * 100, 2)
        return None


class Revision(models.Model):
    TYPE_CHOICES = [
        ('vidange', 'Vidange'),
        ('revision', 'Révision complète'),
        ('freins', 'Freins'),
        ('pneus', 'Pneus'),
        ('courroie', 'Courroie de distribution'),
        ('climatisation', 'Climatisation'),
        ('autre', 'Autre'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='revisions', verbose_name="Voiture")
    date = models.DateField(verbose_name="Date")
    type_revision = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name="Type")
    description = models.TextField(blank=True, verbose_name="Description des travaux")
    km_compteur = models.PositiveIntegerField(verbose_name="Kilométrage")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant (MAD)")
    garage = models.CharField(max_length=200, blank=True, verbose_name="Garage / Prestataire")
    prochaine_revision_km = models.PositiveIntegerField(blank=True, null=True, verbose_name="Prochaine révision (km)")
    prochaine_revision_date = models.DateField(blank=True, null=True, verbose_name="Prochaine révision (date)")
    facture = models.FileField(upload_to='revisions/', blank=True, null=True, verbose_name="Facture")

    class Meta:
        verbose_name = "Révision / Entretien"
        verbose_name_plural = "Révisions / Entretiens"
        ordering = ['-date']

    def __str__(self):
        return f"{self.car} — {self.get_type_revision_display()} le {self.date} ({self.km_compteur} km)"

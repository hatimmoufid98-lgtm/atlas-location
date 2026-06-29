from django.db import models
from apps.agencies.models import Agency


class Car(models.Model):
    CATEGORIE_CHOICES = [
        ('economique', 'Économique'),
        ('normale', 'Normale'),
        ('luxe', 'Luxe'),
    ]
    TRANSMISSION_CHOICES = [
        ('manuelle', 'Manuelle'),
        ('automatique', 'Automatique'),
    ]
    CARBURANT_CHOICES = [
        ('essence', 'Essence'),
        ('diesel', 'Diesel'),
        ('hybride', 'Hybride'),
        ('electrique', 'Électrique'),
    ]

    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='cars', verbose_name="Agence")
    marque = models.CharField(max_length=100, verbose_name="Marque")
    modele = models.CharField(max_length=100, verbose_name="Modèle")
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, verbose_name="Catégorie")
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='manuelle', verbose_name="Transmission")
    carburant = models.CharField(max_length=20, choices=CARBURANT_CHOICES, default='diesel', verbose_name="Carburant")
    nombre_places = models.PositiveSmallIntegerField(default=5, verbose_name="Nombre de places")
    prix_par_jour = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prix par jour (MAD)")
    photo = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name="Photo principale")
    description = models.TextField(blank=True, verbose_name="Description")
    actif = models.BooleanField(default=True, verbose_name="Disponible à la location")

    class Meta:
        verbose_name = "Voiture"
        verbose_name_plural = "Voitures"
        ordering = ['categorie', 'marque', 'modele']

    def __str__(self):
        return f"{self.marque} {self.modele}"

    @property
    def nom_complet(self):
        return f"{self.marque} {self.modele}"

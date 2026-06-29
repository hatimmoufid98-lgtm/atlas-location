from django.db import models
from django.utils.text import slugify


class Agency(models.Model):
    nom = models.CharField(max_length=200, verbose_name="Nom de l'agence")
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Logo")
    couleur_principale = models.CharField(
        max_length=7, default='#C8A96E',
        verbose_name="Couleur principale (hex)",
        help_text="Ex: #C8A96E"
    )
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    adresse = models.TextField(verbose_name="Adresse complète")
    actif = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Agence"
        verbose_name_plural = "Agences"

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

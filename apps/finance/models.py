from django.db import models
from apps.agencies.models import Agency


class CategorieDepense(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Catégorie")
    icone = models.CharField(max_length=10, blank=True, default='💼', verbose_name="Icône")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Catégorie de dépense"
        verbose_name_plural = "Catégories de dépenses"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Depense(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='depenses', verbose_name="Agence")
    categorie = models.ForeignKey(CategorieDepense, on_delete=models.PROTECT, verbose_name="Catégorie")
    date = models.DateField(verbose_name="Date")
    description = models.CharField(max_length=300, verbose_name="Description")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant (MAD)")
    justificatif = models.FileField(upload_to='depenses/', blank=True, null=True, verbose_name="Justificatif (facture/reçu)")
    notes = models.TextField(blank=True, verbose_name="Notes")

    class Meta:
        verbose_name = "Dépense"
        verbose_name_plural = "Dépenses"
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} — {self.categorie} : {self.montant} MAD"

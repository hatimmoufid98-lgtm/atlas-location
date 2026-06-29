from django.contrib import admin
from django.utils.html import format_html
from .models import Booking, BlockedPeriod


class BlockedPeriodInline(admin.TabularInline):
    model = BlockedPeriod
    extra = 1
    verbose_name = "Période bloquée"
    verbose_name_plural = "Périodes bloquées (maintenance, etc.)"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('car', 'nom_client', 'telephone_client', 'date_debut', 'date_fin', 'nombre_jours_display', 'prix_total_display', 'badge_statut', 'date_creation')
    list_filter = ('statut', 'car__agency', 'car__categorie', 'date_debut')
    search_fields = ('nom_client', 'telephone_client', 'email_client', 'car__marque', 'car__modele')
    readonly_fields = ('date_creation', 'prix_total_display', 'nombre_jours_display')
    date_hierarchy = 'date_debut'

    fieldsets = (
        ('Voiture et dates', {
            'fields': ('car', 'date_debut', 'date_fin', 'nombre_jours_display', 'prix_total_display')
        }),
        ('Client', {
            'fields': ('nom_client', 'telephone_client', 'email_client')
        }),
        ('Gestion', {
            'fields': ('statut', 'notes_agence', 'date_creation')
        }),
    )

    def badge_statut(self, obj):
        couleurs = {
            'en_attente': '#f59e0b',
            'confirmee': '#10b981',
            'annulee': '#ef4444',
        }
        couleur = couleurs.get(obj.statut, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:2px 10px;border-radius:12px;font-size:12px;">{}</span>',
            couleur, obj.get_statut_display()
        )
    badge_statut.short_description = "Statut"

    def prix_total_display(self, obj):
        return f"{obj.prix_total} MAD"
    prix_total_display.short_description = "Prix total"

    def nombre_jours_display(self, obj):
        return f"{obj.nombre_jours} jour(s)"
    nombre_jours_display.short_description = "Durée"


@admin.register(BlockedPeriod)
class BlockedPeriodAdmin(admin.ModelAdmin):
    list_display = ('car', 'date_debut', 'date_fin', 'raison')
    list_filter = ('car__agency', 'car')
    search_fields = ('car__marque', 'car__modele', 'raison')
    date_hierarchy = 'date_debut'

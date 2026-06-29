from django.contrib import admin
from django.utils.html import format_html
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('apercu_photo', 'marque', 'modele', 'categorie', 'transmission', 'carburant', 'prix_par_jour', 'actif')
    list_filter = ('agency', 'categorie', 'transmission', 'carburant', 'actif')
    search_fields = ('marque', 'modele')
    list_editable = ('actif', 'prix_par_jour')
    list_display_links = ('marque',)

    fieldsets = (
        ('Informations générales', {
            'fields': ('agency', 'marque', 'modele', 'categorie', 'actif')
        }),
        ('Caractéristiques techniques', {
            'fields': ('transmission', 'carburant', 'nombre_places')
        }),
        ('Tarif et médias', {
            'fields': ('prix_par_jour', 'photo', 'description')
        }),
    )

    def apercu_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.photo.url)
        return "—"
    apercu_photo.short_description = "Photo"

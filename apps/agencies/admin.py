from django.contrib import admin
from django.utils.html import format_html
from .models import Agency


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'telephone', 'apercu_couleur', 'actif')
    list_filter = ('actif', 'ville')
    search_fields = ('nom', 'ville')
    prepopulated_fields = {'slug': ('nom',)}

    def apercu_couleur(self, obj):
        return format_html(
            '<span style="display:inline-block;width:24px;height:24px;'
            'background:{};border-radius:4px;border:1px solid #ccc;"></span> {}',
            obj.couleur_principale, obj.couleur_principale
        )
    apercu_couleur.short_description = "Couleur"

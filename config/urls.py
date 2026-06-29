from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as media_serve

admin.site.site_header = "Atlas Location — Administration"
admin.site.site_title = "Atlas Location"
admin.site.index_title = "Tableau de bord"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestion/', include('apps.dashboard.urls')),
    path('', include('apps.public.urls')),
    path('reservation/', include('apps.bookings.urls')),
]

# Service des médias (photos voitures) — en local ET en ligne (démo, faible trafic)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', media_serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

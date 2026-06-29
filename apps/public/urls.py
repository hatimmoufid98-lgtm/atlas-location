from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('voitures/', views.catalogue, name='catalogue'),
    path('recherche/', views.resultats, name='resultats'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('voiture/<int:car_id>/', views.reserver, name='reserver'),
    path('confirmation/<int:booking_id>/', views.confirmation, name='confirmation'),
]

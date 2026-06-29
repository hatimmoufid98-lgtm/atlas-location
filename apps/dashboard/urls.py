from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.tableau_bord, name='tableau_bord'),
    path('bilan/excel/', views.export_bilan_excel, name='export_bilan_excel'),
    path('planning/', views.planning_annuel, name='planning_annuel'),
]

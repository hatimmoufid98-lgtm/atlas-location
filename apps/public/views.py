from django.shortcuts import render
from django.utils.dateparse import parse_date
from apps.agencies.models import Agency
from apps.cars.models import Car
from apps.cars.availability import get_available_cars


def home(request):
    agency = Agency.objects.filter(actif=True).first()
    voitures_vedette = Car.objects.filter(actif=True).order_by('?')[:6] if agency else []

    # Slides du hero : une voiture avec photo par categorie (luxe d'abord)
    slides = []
    if agency:
        ordre = [
            ('luxe', 'Le luxe, sans compromis', "Berlines et SUV haut de gamme pour vos déplacements d'exception."),
            ('normale', 'Confort & polyvalence', 'Des véhicules modernes, spacieux et fiables pour tous vos trajets.'),
            ('economique', 'Malin & économique', 'Le meilleur rapport qualité-prix pour rouler en toute liberté.'),
        ]
        for cat, titre, sous_titre in ordre:
            car = (Car.objects.filter(actif=True, categorie=cat)
                   .exclude(photo='').exclude(photo__isnull=True)
                   .order_by('?').first())
            if car:
                slides.append({'car': car, 'cat': cat, 'titre': titre, 'sous_titre': sous_titre})

    # Repli : si aucune photo par categorie, prendre les premieres voitures avec photo
    if not slides and agency:
        for car in Car.objects.filter(actif=True).exclude(photo='').exclude(photo__isnull=True)[:3]:
            slides.append({'car': car, 'cat': car.categorie,
                           'titre': 'Roulez en toute confiance',
                           'sous_titre': 'Réservez votre véhicule en quelques clics.'})

    nb_voitures = Car.objects.filter(actif=True).count() if agency else 0

    return render(request, 'public/home.html', {
        'voitures_vedette': voitures_vedette,
        'slides': slides,
        'nb_voitures': nb_voitures,
    })


def catalogue(request):
    """Vitrine de tout le parc — navigation libre, sans dates."""
    agency = Agency.objects.filter(actif=True).first()
    categorie = request.GET.get('categorie', '')

    voitures = Car.objects.filter(actif=True)
    if categorie in ('economique', 'normale', 'luxe'):
        voitures = voitures.filter(categorie=categorie)
    voitures = voitures.order_by('categorie', 'marque', 'modele')

    return render(request, 'public/catalogue.html', {
        'voitures': voitures,
        'categorie': categorie,
        'nb_total': Car.objects.filter(actif=True).count() if agency else 0,
    })


def resultats(request):
    agency = Agency.objects.filter(actif=True).first()
    date_debut_str = request.GET.get('date_debut', '')
    date_fin_str = request.GET.get('date_fin', '')
    categorie = request.GET.get('categorie', '')

    voitures = []
    erreur = None

    if date_debut_str and date_fin_str:
        date_debut = parse_date(date_debut_str)
        date_fin = parse_date(date_fin_str)

        if not date_debut or not date_fin:
            erreur = "Dates invalides. Veuillez saisir des dates correctes."
        elif date_fin <= date_debut:
            erreur = "La date de retour doit être après la date de prise en charge."
        elif agency:
            voitures = get_available_cars(agency, date_debut, date_fin, categorie or None)
            nombre_jours = (date_fin - date_debut).days
            for v in voitures:
                v.prix_total = v.prix_par_jour * nombre_jours
                v.duree = nombre_jours

    return render(request, 'public/results.html', {
        'voitures': voitures,
        'date_debut': date_debut_str,
        'date_fin': date_fin_str,
        'categorie': categorie,
        'erreur': erreur,
    })

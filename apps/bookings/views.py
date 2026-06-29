from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from apps.cars.models import Car
from apps.cars.availability import is_car_available
from .models import Booking
from .forms import BookingForm


def reserver(request, car_id):
    car = get_object_or_404(Car, id=car_id, actif=True)

    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')

    initial = {}
    if date_debut:
        initial['date_debut'] = date_debut
    if date_fin:
        initial['date_fin'] = date_fin

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            d_debut = form.cleaned_data['date_debut']
            d_fin = form.cleaned_data['date_fin']

            # Vérification atomique pour éviter les doubles réservations (race condition)
            with transaction.atomic():
                # Verrouille les lignes concernant cette voiture pendant la transaction
                Car.objects.select_for_update().get(id=car.id)

                if not is_car_available(car, d_debut, d_fin):
                    messages.error(
                        request,
                        "Désolé, cette voiture vient d'être réservée sur ces dates. "
                        "Veuillez choisir d'autres dates ou une autre voiture."
                    )
                    return render(request, 'public/car_detail.html', {
                        'car': car,
                        'form': form,
                        'date_debut': date_debut,
                        'date_fin': date_fin,
                    })

                booking = form.save(commit=False)
                booking.car = car
                booking.save()

            return redirect('confirmation', booking_id=booking.id)
    else:
        form = BookingForm(initial=initial)

    return render(request, 'public/car_detail.html', {
        'car': car,
        'form': form,
        'date_debut': date_debut,
        'date_fin': date_fin,
    })


def confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'public/confirmation.html', {'booking': booking})

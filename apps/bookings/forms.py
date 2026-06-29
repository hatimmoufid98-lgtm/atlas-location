from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['nom_client', 'telephone_client', 'email_client', 'date_debut', 'date_fin']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary'}),
            'nom_client': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary', 'placeholder': 'Votre nom complet'}),
            'telephone_client': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary', 'placeholder': '06 XX XX XX XX'}),
            'email_client': forms.EmailInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary', 'placeholder': 'votre@email.com'}),
        }
        labels = {
            'nom_client': 'Nom complet',
            'telephone_client': 'Téléphone',
            'email_client': 'Email',
            'date_debut': 'Date de prise en charge',
            'date_fin': 'Date de retour',
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')

        if date_debut and date_fin:
            if date_fin <= date_debut:
                raise forms.ValidationError("La date de retour doit être après la date de prise en charge.")

        return cleaned_data

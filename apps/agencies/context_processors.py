from .models import Agency


def agency_context(request):
    agency = Agency.objects.filter(actif=True).first()
    return {'agency': agency}

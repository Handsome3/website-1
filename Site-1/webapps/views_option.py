from django.http import JsonResponse

from .models import CarBrand, CarModel


def getCarBrand(request):
    records = []
    for brand in CarBrand.objects.all():
        record = {'id': brand.id, 'text': brand.__str__()}
        records.append(record)
    return JsonResponse({'status': 'success', 'records': records})


def getCarModel(request):
    brand_id = request.GET['brand_id']
    records = []
    for model in CarModel.objects.filter(brand_id=brand_id):
        record = {'id': model.id, 'text': model.__str__()}
        records.append(record)
    return JsonResponse({'status': 'success', 'records': records})

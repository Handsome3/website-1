import datetime

from django.http import JsonResponse
from django.shortcuts import render

from .models import Deal, UsedCar


def searchDeal(config):
    deals = Deal.objects.all();
    if 'user' in config:
        deals = deals.filter(posted_user=config['user'])
    if 'type' in config:
        deals = deals.filter(type=config['type'])
    if 'field' in config:
        for k, v in config['field']:
            deals = deals.filter(k=v)
    if 'order_by' in config:
        deals = deals.order_by(config['order_by'])
    start = 0 if config['end'] - 10 < 0 else config['end'] - 10
    deals = deals[start: config['end']]
    return deals


def usedcarPage(request):
    searchConfig = {'type': 'usedcar', 'end': 10, 'order_by': 'create_time'}
    deals = searchDeal(searchConfig)
    records = []
    for deal in deals:
        record = {
            'id': deal.id,
            'title': deal.__str__(),
            'year': deal.usedcar.year,
            'car_brand': deal.usedcar.car_brand,
            'car_model': deal.usedcar.car_model,
            'img': deal.image_set.first(),
        }
        records.append(record)
    if len(deals) == 10:
        config = {'has_next': True}
    else:
        config = {'has_next': False}
    return render(request, 'webapps/search/usedCar.html', {'records': records, 'config': config})


def ajaxSearchUsedcar(request):
    searchConfig = {'year': int(request.GET['year']),
                    'mileage': int(request.GET['mileage']),
                    'car_brand': request.GET['car_brand'],
                    'car_model': request.GET['car_model'],
                    'price': int(request.GET['price']),
                    'start': int(request.GET['end']),
                    }
    cars = searchUsedcar(searchConfig)
    records = []
    for car in cars:
        record = {
            'id': car.deal.id,
            'title': car.__str__(),
            'year': car.year,
            'car_brand': car.car_brand,
            'car_model': car.car_model,
        }
        if car.deal.image_set.first():
            record.update({'img_url': car.deal.image_set.first().image.url})
        else:
            record.update({'img_url': '/static/webapps/image/image_error.svg'})
        records.append(record)
    if len(cars) == 10:
        has_next = True
    else:
        has_next = False
    return JsonResponse(
        {'status': 'success', 'records': records, 'has_next': has_next, 'end': searchConfig['start'] + 10})


def searchUsedcar(config):
    cars = UsedCar.objects.all()
    curyear = datetime.datetime.now().year
    if config['year'] != 0:
        if config['year'] == 1:
            cars = cars.filter(year__gte=curyear - 1)
        if config['year'] == 2:
            cars = cars.filter(year__lt=curyear - 1).filter(year__gte=curyear - 3)
        if config['year'] == 3:
            cars = cars.filter(year__lt=curyear - 3).filter(year__gte=curyear - 5)
        if config['year'] == 4:
            cars = cars.filter(year__lt=curyear - 5).filter(year__gte=curyear - 10)
        if config['year'] == 5:
            cars = cars.filter(year__lt=curyear - 10)
    if config['car_brand'] != '无限制':
        cars = cars.filter(car_brand=config['car_brand'])
    if config['car_model'] != '无限制':
        cars = cars.filter(car_model=config['car_model'])
    if config['mileage'] != 0:
        if config['mileage'] == 1:
            cars = cars.filter(mileage__lt=10000)
        if config['mileage'] == 2:
            cars = cars.filter(mileage__lt=30000).filter(mileage__gte=10000)
        if config['mileage'] == 3:
            cars = cars.filter(mileage__lt=50000).filter(mileage__gte=30000)
        if config['mileage'] == 4:
            cars = cars.filter(mileage__lt=100000).filter(mileage__gte=50000)
        if config['mileage'] == 5:
            cars = cars.filter(mileage__gte=100000)
    if config['price'] != 0:
        if config['price'] == 1:
            cars = cars.filter(price__lt=5000)
        if config['mileage'] == 2:
            cars = cars.filter(price__lt=10000).filter(price__gte=5000)
        if config['mileage'] == 3:
            cars = cars.filter(price__lt=15000).filter(price__gte=10000)
        if config['mileage'] == 4:
            cars = cars.filter(price__lt=20000).filter(price__gte=15000)
        if config['mileage'] == 5:
            cars = cars.filter(price__gte=20000)
    cars = cars[config['start']:config['start'] + 10]
    return cars

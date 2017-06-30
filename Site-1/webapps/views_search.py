import datetime

from django.http import JsonResponse
from django.shortcuts import render

from .models import *
from .views_option import *

d = {
        'carpool': Carpool.objects.all(),
        'usedcar': UsedCar.objects.all(),
        'useditem': UsedItem.objects.all(),
        'sublease': Sublease.objects.all(),
        'mergeorder': MergeOrder.objects.all(),
        'houserent': HouseRent.objects.all(),
    }

def searchDeal(config):
    deals = Deal.objects.filter(expire_time__gte=datetime.datetime.now().date())
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

def searchUsedcar(config):
    cars = UsedCar.objects.filter(deal__expire_time__gte=datetime.datetime.now().date())
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
        cars = cars.filter(car_brand_id=int(config['car_brand']))
    if config['car_model'] != '无限制':
        cars = cars.filter(car_model_id=int(config['car_model']))
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

def generateRecords(deals, type):
    res=[]
    if type =='useditem' or type == 'usedcar':
        for deal in deals:
            record = {
                'id' : deal.deal.id,
                'price' : deal.price,
                'title' : deal.__str__(),
                'post_date' : deal.deal.create_time,
            }
            if deal.deal.image_set.first():
                record.update({'img_url': deal.deal.image_set.first().image.url})
            else:
                record.update({'img_url': '/static/webapps/image/image_error.svg'})
            res.append(record)
    if type == 'carpool':
        for deal in deals:
            record= {
                'id': deal.deal.id,
                'price': deal.price,
                'title': deal.__str__(),
                'post_date': deal.deal.create_time,
            }
            res.append(record)
    if type == 'mergeorder':
        for deal in deals:
            record= {
                'id': deal.deal.id,
                'order_type': deal.order_type,
                'title': deal.__str__(),
                'post_date': deal.deal.create_time,
            }
            res.append(record)
    if type == 'sublease' or type == 'houserent':
        for deal in deals:
            record= {
                'id': deal.deal.id,
                'rent': deal.rent,
                'title': deal.__str__(),
                'post_date': deal.deal.create_time,
            }
            if deal.deal.image_set.first():
                record.update({'img_url': deal.deal.image_set.first().image.url})
            else:
                record.update({'img_url': '/static/webapps/image/image_error.svg'})
            res.append(record)
    return res

def transferSearchConfig(options):
    sconfig = []
    for t in options:
        if t[0] == 'end': continue
        field = t[0][:-2]
        type = t[1][0]
        if type == 'between':
            config= {'field': field, 'type': type, 'min': t[1][2], 'max': t[1][3]}
        elif type == 'exact':
            config= {'field': field, 'type': type, 'value': t[1][2]}
        else:
            config= {'field': field, 'type': type, 'q': t[1][2]}
        config.update({'format': t[1][1]})
        sconfig.append(config)
    return sconfig

def tranFormat(val, format):
    if format == 'int':
        return int(val)
    if format == 'str':
        return str(val)
    if format == 'time':
        return str(val)
    if format == 'float':
        return float(val)
    if format == 'date':
        return str(val)
    if format =='bool':
        return True if val=='true' else False

def search(config):
    deals= d[config['type']]
    if config['is_overdue']:
        deals= deals.filter(deal__expire_time__lt=datetime.datetime.now().date())
    else:
        deals= deals.filter(deal__expire_time__gte=datetime.datetime.now().date())
    for s in config['sconfig']:
        kwargs= {}
        if s['type'] == 'between':
            min= tranFormat(s['min'], s['format'])
            max= tranFormat(s['max'], s['format'])
            kwargs= {
                '{0}__{1}'.format(s['field'], 'gte'): min,
                '{0}__{1}'.format(s['field'], 'lt'): max,
            }
        if s['type'] == 'exact':
            if s['value'] == '无限制': continue
            value= tranFormat(s['value'], s['format'])
            kwargs= {'{0}'.format(s['field']): value }
        deals= deals.filter(**kwargs)
    start= int(config['start'])
    deals= deals.order_by(config['order_by'])[start : start+12]
    return deals

#usedcar
def usedcarPage(request):
    config = {'type': 'usedcar',
              'is_overdue': False,
              'sconfig': '',
              'order_by': '-deal__create_time',
              'start': 0,
              }
    deals = search(config)
    records = generateRecords(deals, 'usedcar')
    config = {'end': 12}
    if deals.count() == 12:
        config.update({'has_next': True})
    else:
        config.update({'has_next': False})
    options = usedcarSearchOptions()
    return render(request, 'webapps/search/usedCar.html', {'records': records, 'config': config, 'options': options})

def ajaxUsedcarSearch(request):
    sconfig = transferSearchConfig(request.GET.lists())
    config = {'type': 'usedcar',
              'is_overdue': False,
              'sconfig': sconfig,
              'order_by': '-deal__create_time',
              'start': request.GET.get('end', 0),
              }
    deals = search(config)
    if deals.count() == 12:
        has_next = True
    else:
        has_next = False
    records = generateRecords(deals, 'usedcar')
    return JsonResponse({'records': records, 'has_next': has_next, 'end': int(config['start']) + 12})

#useditem
def useditemPage(request):
    deals = UsedItem.objects.all().filter(deal__expire_time__gte=datetime.datetime.now().date()).order_by('-deal__create_time')[:12]
    records = generateRecords(deals, 'useditem')
    config = {'end' : 12 }
    if deals.count()==12:
        config.update({'has_next' : True})
    else:
        config.update({'has_next' : False})
    options = useditemSearchOptions()
    return render(request, 'webapps/search/usedItem.html', {'records' : records, 'config' : config, 'options' : options})

def ajaxUseditemSearch(request):
    sconfig= transferSearchConfig(request.GET.lists())
    config= {'type': 'useditem',
             'is_overdue': False,
             'sconfig': sconfig,
             'order_by': '-deal__create_time',
             'start': request.GET.get('end',0),
            }
    deals= search(config)
    if deals.count()==12:
        has_next = True
    else:
        has_next = False
    records = generateRecords(deals, 'useditem')
    return JsonResponse({'records' : records, 'has_next' : has_next, 'end' : int(config['start'])+12})

#carpool
def carpoolPage(request):
    config = {'type': 'carpool',
              'is_overdue': False,
              'sconfig': '',
              'order_by': '-deal__create_time',
              'start': 0,
              }
    deals= search(config)
    records = generateRecords(deals, 'carpool')
    config = {'end' : 12 }
    if deals.count()==12:
        config.update({'has_next' : True})
    else:
        config.update({'has_next' : False})
    options = carpoolSearchOptions()
    return render(request, 'webapps/search/carpool.html',{'records' : records, 'config' : config, 'options' : options})

def ajaxCarpoolSearch(request):
    sconfig= transferSearchConfig(request.GET.lists())
    config= {'type': 'carpool',
             'is_overdue': False,
             'sconfig': sconfig,
             'order_by': '-deal__create_time',
             'start': request.GET.get('end',0),
            }
    deals= search(config)
    if deals.count()==12:
        has_next = True
    else:
        has_next = False
    records = generateRecords(deals, 'carpool')
    return JsonResponse({'records' : records, 'has_next' : has_next, 'end' : int(config['start'])+12})

#mergeorder
def mergeorderPage(request):
    config = {'type': 'mergeorder',
              'is_overdue': False,
              'sconfig': '',
              'order_by': '-deal__create_time',
              'start': 0,
              }
    deals = search(config)
    records = generateRecords(deals, 'mergeorder')
    config = {'end': 12}
    if deals.count() == 12:
        config.update({'has_next': True})
    else:
        config.update({'has_next': False})
    options = mergeorderSearchOptions()
    return render(request, 'webapps/search/mergeOrder.html', {'records' : records, 'config' : config, 'options' : options})

def ajaxMergeOrderSearch(request):
    sconfig = transferSearchConfig(request.GET.lists())
    config = {'type': 'mergeorder',
              'is_overdue': False,
              'sconfig': sconfig,
              'order_by': '-deal__create_time',
              'start': request.GET.get('end', 0),
              }
    deals = search(config)
    if deals.count() == 12:
        has_next = True
    else:
        has_next = False
    records = generateRecords(deals, 'mergeorder')
    return JsonResponse({'records': records, 'has_next': has_next, 'end': int(config['start']) + 12})

# Sublease
def subleasePage(request):
    config = {'type': 'sublease',
              'is_overdue': False,
              'sconfig': '',
              'order_by': '-deal__create_time',
              'start': 0,
              }
    deals = search(config)
    records = generateRecords(deals, 'sublease')
    config = {'end': 12}
    if deals.count() == 12:
        config.update({'has_next': True})
    else:
        config.update({'has_next': False})
    options = subleaseSearchOptions()
    return render(request, 'webapps/search/sublease.html', {'records': records, 'config': config, 'options': options})

def ajaxSubleaseSearch(request):
    sconfig = transferSearchConfig(request.GET.lists())
    config = {'type': 'sublease',
              'is_overdue': False,
              'sconfig': sconfig,
              'order_by': '-deal__create_time',
              'start': request.GET.get('end', 0),
              }
    deals = search(config)
    if deals.count() == 12:
        has_next = True
    else:
        has_next = False
    records = generateRecords(deals, 'sublease')
    return JsonResponse({'records': records, 'has_next': has_next, 'end': int(config['start']) + 12})

# House Rent
def houserentPage(request):
    config = {'type': 'houserent',
              'is_overdue': False,
              'sconfig': '',
              'order_by': '-deal__create_time',
              'start': 0,
              }
    deals = search(config)
    records = generateRecords(deals, 'houserent')
    config = {'end': 12}
    if deals.count() == 12:
        config.update({'has_next': True})
    else:
        config.update({'has_next': False})
    options = houserentSearchOptions()
    return render(request, 'webapps/search/house.html', {'records': records, 'config': config, 'options': options})

def ajaxHouseRentSearch(request):
    sconfig = transferSearchConfig(request.GET.lists())
    config = {'type': 'houserent',
              'is_overdue': False,
              'sconfig': sconfig,
              'order_by': '-deal__create_time',
              'start': request.GET.get('end', 0),
              }
    deals = search(config)
    if deals.count() == 12:
        has_next = True
    else:
        has_next = False
    records = generateRecords(deals, 'houserent')
    return JsonResponse({'records': records, 'has_next': has_next, 'end': int(config['start']) + 12})


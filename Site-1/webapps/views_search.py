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
        'deal': Deal.objects.all(),
    }

typeDic = {'usedcar': '二 手 车',
           'carpool': 'Carpool',
           'useditem': '二 手 商 品',
           'houserent': '合 租',
           'sublease': 'Sublease',
           'mergeorder': '拼 单',
           }

def generateRecords(deals, type):
    res=[]
    if type =='useditem' or type == 'usedcar':
        for deal in deals:
            record = {
                'id' : deal.deal.id,
                'caption' : deal.price,
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
                'caption': deal.price,
                'title': deal.__str__(),
                'post_date': deal.deal.create_time,
            }
            res.append(record)
    if type == 'mergeorder':
        for deal in deals:
            record= {
                'id': deal.deal.id,
                'caption': deal.order_type,
                'title': deal.__str__(),
                'post_date': deal.deal.create_time,
            }
            res.append(record)
    if type == 'sublease' or type == 'houserent':
        for deal in deals:
            record= {
                'id': deal.deal.id,
                'caption': deal.rent,
                'title': deal.__str__(),
                'post_date': deal.deal.create_time,
            }
            if deal.deal.image_set.first():
                record.update({'img_url': deal.deal.image_set.first().image.url})
            else:
                record.update({'img_url': '/static/webapps/image/image_error.svg'})
            res.append(record)
    if type == 'deal' :
        for deal in deals:
            record= {
                'id': deal.id,
                'caption': typeDic[deal.type]+' '+deal.__str__(),
                'title': getattr(deal, deal.type).note,
                'post_date': deal.create_time,
            }
            if deal.image_set.first():
                record.update({'img_url': deal.image_set.first().image.url})
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
    j= 'lt' if config['is_overdue'] else 'gte'
    i= '' if config['type'] == 'deal' else 'deal__'
    kwargs= {'{0}expire_time__{1}'.format(i, j) : datetime.datetime.now().date()}
    deals= deals.filter(**kwargs)
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
        if s['type'] == 'contain':
            if not s['q']: continue
            kwargs= {'{0}__contains'.format(s['field']): s['q']}
        deals= deals.filter(**kwargs)
    deals= deals.order_by(config['order_by'])
    return deals

def searchPage(request, type):
    config = {'type': type,
              'is_overdue': False,
              'sconfig': '',
              'order_by': '-deal__create_time',
              'start': 0,
              }
    deals = search(config)
    records = generateRecords(deals, type)
    config = {'end': 12}
    if deals.count() == 12:
        config.update({'has_next': True})
    else:
        config.update({'has_next': False})
    options = getSearchOptions(type)
    return render(request, 'webapps/search/'+type+'.html', {'records': records, 'config': config, 'options': options})

def ajaxSearch(request, type):
    sconfig = transferSearchConfig(request.GET.lists())
    config = {'type': type,
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
    records = generateRecords(deals, type)
    return JsonResponse({'records': records, 'has_next': has_next, 'end': int(config['start']) + 12, 'type': type})

def siteSearch(request):
    type = request.GET.get('type', 'deal')
    page = int(request.GET.get('page', '1'))
    sconfig = [{'field': 'kw', 'type': 'contain', 'q': request.GET['q'].lower()}]
    if type!= 'deal': sconfig.append({'field': 'type', 'type': 'exact', 'value': type, 'format': 'str'})
    config = {'type': 'deal',
              'is_overdue': False,
              'sconfig': sconfig,
              'order_by': '-create_time',
              }
    deals = search(config)
    pages= []
    num= page-2
    while num*10-deals.count()<10:
        if num>0:
            pages.append(num)
            if len(pages) == 5:
                break
        num+=1
    config = {'page': page, 'type': type, 'q': request.GET['q'], 'count': deals.count(), 'pages': pages , 'pre': page-1, 'next': page+1}
    if len(pages)>0 and pages[len(pages)-1] != page:
        config.update({'has_next': True})
    else:
        config.update({'has_next': False})
    deals=deals[(page-1)*10 : page*10]
    records = generateRecords(deals, 'deal')
    return render(request, 'webapps/search/sitesearch.html', {'records': records, 'config': config})
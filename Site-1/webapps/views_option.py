from django.http import JsonResponse

from .models import CarBrand, CarModel

maxint= 99999

def useditemSearchOptions():
    options = [{ 'type' : 'exact',
                        'field' : 'item_type',
                        'name' : '宝贝类型',
                        'options' : [{'label' : '无限制', 'value' : '无限制'},
                                    {'label' : '家具', 'value' : '家具'},
                                    {'label': '化妆品', 'value': '化妆品'},
                                    {'label': '服饰', 'value': '服饰'},
                                    {'label': '数码产品', 'value': '数码产品'}
                                    ],
                 },
               {'type': 'between',
                'field': 'price',
                'name': '售价范围',
                'options': [{'label': '无限制', 'min': 0, 'max': maxint},
                           {'label': '$0-5', 'min': 0, 'max': 5},
                           {'label': '$6-10', 'min': 5, 'max': 10},
                           {'label': '$11-50', 'min': 10, 'max': 50},
                           {'label': '$51-100', 'min': 50, 'max': 100},
                           {'label': '$100以上', 'min': 100, 'max': maxint},
                           ],
                },
               {'type': 'exact',
                'field': 'condition',
                'name': '宝贝状态',
                'options':  [{'label' : '无限制', 'value' : '无限制'},
                            {'label' : '全新', 'value' : '全新'},
                            {'label': '九成新', 'value': '九成新'},
                            {'label': '七成新', 'value': '七成新'},
                            {'label': '五成新', 'value': '五成新'},
                            {'label': '五成新以下', 'value': '五成新以下'},
                            ],
                },
    ]
    return options

def getCarBrand(request):
    records = []
    for brand in CarBrand.objects.all():
        record = {'id': brand.id, 'text': brand.__str__()}
        records.append(record)
    return JsonResponse({'status': 'success', 'records': records})


def getCarModel(request):
    brand_id = request.GET.get('brand_id', '')
    if not brand_id:
        return JsonResponse({'status': 'fail'})
    records = []
    for model in CarModel.objects.filter(brand_id=brand_id):
        record = {'id': model.id, 'text': model.__str__()}
        records.append(record)
    return JsonResponse({'status': 'success', 'records': records})

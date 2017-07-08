from django.http import JsonResponse

from .models import CarBrand, CarModel,State,City,Location
import datetime, time

maxint= 999999

def usedcarSearchOptions() :
    year= datetime.datetime.now().year
    options= [
            {'type': 'exact',
             'field': 'car_brand_id',
             'name': '车辆品牌',
             'format': 'int',
             'options': [{'label' : '无限制', 'value' : '无限制'}]
                },
            {'type': 'exact',
             'field': 'car_model_id',
             'name': '车辆型号',
             'format': 'int',
             'options': [{'label' : '无限制', 'value' : '无限制'}]
                },
            {'type': 'between',
             'field': 'price',
             'name': '售价范围',
             'format': 'float',
             'options':[{'label': '无限制', 'min': 0, 'max': maxint},
                        {'label': '$5000以内', 'min': 0, 'max': 5000},
                        {'label': '$5000-10000', 'min': 5000, 'max': 10000},
                        {'label': '$10000-15000', 'min': 10000, 'max': 15000},
                        {'label': '$15000-20000', 'min': 15000, 'max': 20000},
                        {'label': '$20000以上', 'min': 20000, 'max': maxint}
                        ]
                },
        {'type': 'between',
         'field': 'year',
         'name': '车龄',
         'format': 'int',
         'options': [
             {'label': '无限制', 'min': 0, 'max': maxint},
             {'label': '1年以内', 'min': year-1, 'max': maxint},
             {'label': '1-3年', 'min': year-3, 'max': year-1},
             {'label': '3-5年', 'min': year-5, 'max': year-3},
             {'label': '5-10年', 'min': year-10, 'max': year-5},
             {'label': '10年以上', 'min': 0, 'max': year-10}
            ]
        },
        {'type': 'between',
         'field': 'mileage',
         'name': '里程',
         'format': 'int',
         'options': [
             {'label': '无限制', 'min': 0, 'max': maxint},
             {'label': '1万迈以内', 'min': 0, 'max': 10000},
             {'label': '1-3万迈', 'min': 10000, 'max': 30000},
             {'label': '3-5万迈', 'min': 30000, 'max': 50000},
             {'label': '5-10万迈', 'min': 50000, 'max': 100000},
             {'label': '10万迈以上', 'min': 100000, 'max': maxint}
            ]
         },
    ]
    for brand in CarBrand.objects.all():
        t= {'label': brand, 'value': brand.id}
        options[0]['options'].append(t)
    for model in CarModel.objects.all():
        t= {'label': model, 'value': model.id}
        options[1]['options'].append(t)
    return options

def useditemSearchOptions():
    options = [{ 'type' : 'exact',
                'field' : 'item_type',
                'name' : '宝贝类型',
                'format' : 'str',
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
                'format': 'int',
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
                'format': 'str',
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

def carpoolSearchOptions() :
    options= [
            {'type': 'between',
             'field': 'time',
             'name': '出发时间',
             'format': 'time',
             'options':[{'label': '无限制', 'min': datetime.time(0,0,0).isoformat(), 'max': datetime.time(23,59,59).isoformat()},
                        {'label': '上午', 'min': datetime.time(0,0,0).isoformat(), 'max': datetime.time(12,0,0).isoformat()},
                        {'label': '下午', 'min': datetime.time(12,0,0).isoformat(), 'max': datetime.time(23,59,59).isoformat()},
                        ],
            },
            {'type': 'exact',
             'field': 'car_type',
             'name': '车型选择',
             'format': 'str',
             'options':[{'label': '无限制', 'value': '无限制'},
                        {'label': '两门轿车', 'value': 'couple'},
                        {'label': '四门轿车 ', 'value': 'sedan'},
                        {'label': '五座SUV', 'value': 'suv'},
                        {'label': '七座SUV', 'value': '7suv'},
                        {'label': '皮卡或其他', 'value': 'truck'},]
            },
            {'type': 'between',
             'field': 'price',
             'name': '是否免费',
             'format': 'float',
             'options': [{'label': '无限制', 'min': 0, 'max': maxint},
                         {'label': '是', 'min': 0, 'max': 0.1},
                         {'label': '否', 'min': 0.1, 'max': maxint},
                        ]
             }
    ]
    return options

def mergeorderSearchOptions() :
    options= [
            {'type': 'exact',
             'field': 'order_type',
             'name': '商品类型',
             'format': 'str',
             'options': [{'label': '无限制', 'value': '无限制'},
                         {'label': '化妆品', 'value': '化妆品'},
                         {'label': '零食', 'value': '零食'},
                        ]
             },
    ]
    return options

def subleaseSearchOptions() :
    options=[
        {'type': 'exact',
         'field': 'community',
         'name': '小区名称',
         'format': 'str',
         'options': [{'label': '无限制', 'value': '无限制'},
                     {'label': 'Campus Lodge', 'value': 'Campus Lodge'},
                     {'label': 'Pavilion', 'value': 'Pavilion'},
                     ]
        },
        {'type': 'between',
         'field': 'rent',
         'name': '月租范围',
         'format': 'float',
         'options': [{'label': '无限制', 'min': 0, 'max': maxint},
                    {'label': '$200以下', 'min': 0, 'max': 200},
                    {'label': '$200-300', 'min': 200, 'max': 300},
                    {'label': '$300-400', 'min': 300, 'max': 400},
                    {'label': '$400-500', 'min': 400, 'max': 500},
                    {'label': '$500以上', 'min': 500, 'max': maxint},
                    ],
        },
        {'type': 'exact',
         'field': 'bedroom_num',
         'name': '卧室数量',
         'format': 'int',
         'options':[{'label': '无限制', 'value': '无限制'},
                    {'label': '1', 'value': '1'},
                    {'label': '2', 'value': '2'},
                    {'label': '3', 'value': '3'},
                    {'label': '4', 'value': '4'},
                    {'label': '5', 'value': '5'},
                    ],
        },
        {'type': 'exact',
         'field': 'bathroom_num',
         'name': '浴室数量',
         'format': 'int',
         'options': [{'label': '无限制', 'value': '无限制'},
                     {'label': '1', 'value': '1'},
                     {'label': '2', 'value': '2'},
                     {'label': '3', 'value': '3'},
                     {'label': '4', 'value': '4'},
                     {'label': '5', 'value': '5'},
                     ],
         },
        {'type':'exact',
         'field': 'renewal',
         'name': '可否续租',
         'format': 'bool',
         'options': [{'label': '无限制', 'value': '无限制'},
                     {'label': '是', 'value': 'true'},
                     {'label': '否', 'value': 'false'},
                     ]
         }
    ]
    return options

def houserentSearchOptions() :
    options = [
        {'type': 'exact',
         'field': 'community',
         'name': '小区名称',
         'format': 'str',
         'options': [{'label': '无限制', 'value': '无限制'},
                     {'label': 'Campus Lodge', 'value': 'Campus Lodge'},
                     {'label': 'Pavilion', 'value': 'Pavilion'},
                     ]
         },
        {'type': 'between',
         'field': 'rent',
         'name': '月租范围',
         'format': 'float',
         'options': [{'label': '无限制', 'min': 0, 'max': maxint},
                     {'label': '$200以下', 'min': 0, 'max': 200},
                     {'label': '$200-300', 'min': 200, 'max': 300},
                     {'label': '$300-400', 'min': 300, 'max': 400},
                     {'label': '$400-500', 'min': 400, 'max': 500},
                     {'label': '$500以上', 'min': 500, 'max': maxint},
                     ],
         },
        {'type': 'exact',
         'field': 'bedroom_num',
         'name': '卧室数量',
         'format': 'int',
         'options': [{'label': '无限制', 'value': '无限制'},
                     {'label': '1', 'value': '1'},
                     {'label': '2', 'value': '2'},
                     {'label': '3', 'value': '3'},
                     {'label': '4', 'value': '4'},
                     {'label': '5', 'value': '5'},
                     ],
         },
        {'type': 'exact',
         'field': 'bathroom_num',
         'name': '浴室数量',
         'format': 'int',
         'options': [{'label': '无限制', 'value': '无限制'},
                     {'label': '1', 'value': '1'},
                     {'label': '2', 'value': '2'},
                     {'label': '3', 'value': '3'},
                     {'label': '4', 'value': '4'},
                     {'label': '5', 'value': '5'},
                     ],
         },
        {'type': 'exact',
         'field': 'roommate_gender',
         'name': '性别要求',
         'format': 'str',
         'options':[{'label': '无限制', 'value': '无限制'},
                    {'label': '男女均可', 'value': 'both'},
                    {'label': '仅男生', 'value': 'male'},
                    {'label': '仅女生', 'value': 'female'},
                    ]
         },
    ]
    return options

def getCarBrand(request):
    records = []
    for brand in CarBrand.objects.all():
        record = {'id': brand.id, 'text': brand.name}
        records.append(record)
    return JsonResponse({'status': 'success', 'records': records})

def getCarModel(request):
    brand_id = request.GET.get('brand_id', '')
    if not brand_id:
        return JsonResponse({'status': 'fail'})
    records = []
    for model in CarModel.objects.filter(brand_id=brand_id):
        record = {'id': model.id, 'text': model.name}
        records.append(record)
    return JsonResponse({'status': 'success', 'records': records})

def getState(request):
    records=[]
    states=State.objects.all()
    for state in states:
        record={'id':state.id, 'text': state.abbr}
        records.append(record)
    return JsonResponse({'status': 'success','records': records})

def getCity(request):
    state_id = request.GET.get('state_id','')
    keyword = request.GET.get('keyword','')
    if not state_id:
        return JsonResponse({'status':'fail'})
    else:
        records=[]
        cities = City.objects.filter(state_id=state_id)
        for city in cities:
            if keyword.lower() in str(city.name).lower():
                record={'id':city.id, 'text': city.name}
                records.append(record)
        return JsonResponse({'status': 'success','records': records})

def getLocation(request):
    state_id = request.GET.get('state_id','')
    city_id = request.GET.get('city_id','')
    keyword = request.GET.get('keyword','')
    if not state_id:
        return JsonResponse({'status':'fail'})
    else:
        records=[]
        locations = Location.objects.filter(state_id=state_id,city_id=city_id)
        for location in locations:
            if keyword.lower() in str(location.name).lower():
                record={'id':location.id, 'text': location.name}
                records.append(record)
        return JsonResponse({'status': 'success','records': records})

def getSearchOptions(type) :
    d = {'usedcar': usedcarSearchOptions,
         'useditem': useditemSearchOptions,
         'sublease': subleaseSearchOptions,
         'houserent': houserentSearchOptions,
         'carpool': carpoolSearchOptions,
         'mergeorder': mergeorderSearchOptions,
         }
    return d[type]()
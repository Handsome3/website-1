import datetime
import traceback

from dateutil import relativedelta
from django.contrib.auth.decorators import login_required
from django.db import transaction
import sys, traceback
from django.http import JsonResponse
from django.shortcuts import render

from . import views
from .models import *

d = {
    'usedcar': UsedCar,
    'useditem': UsedItem,
    'sublease': Sublease,
    'houserent': HouseRent,
    'carpool': Carpool,
    'mergeorder': MergeOrder,
}


@login_required
def postPage(request, type):
    userPro = UserPro.objects.get(user=request.user)
    phone = '' if userPro.phone == '1234567890' else userPro.phone
    wechat = '' if userPro.wechat == 'None' else userPro.wechat
    return render(request, 'webapps/publishInfo/' + type + '.html', {'phone': phone, 'wechat': wechat})


@login_required
def submitPost(request, type):
    if request.method == 'POST':
        create_time = datetime.date.today()
        if type == 'carpool':
            expire_time= request.POST['date']
        else:
            expire_time = create_time + relativedelta.relativedelta(months=1)
        user = request.user
        contact = request.POST.getlist('contact_type[]')
        contact_type = ""
        for i in contact:
            contact_type += i
        t = d[type]._meta.get_fields()
        kwargs = {}

        car=None
        if type=='usedcar':
            car=getCar(request,type)

        with transaction.atomic():
            # specific deals are saved below
            deal = Deal(type=type, create_time=create_time, expire_time=expire_time, posted_user=user,
                        contact_type=contact_type)
            deal.save()

            for f in t:
                key = f.name
                if key == 'deal':
                    value = deal
                elif f.is_relation:
                    key += '_id'
                    if key=='depart_place_id':
                        value=getLocation(request,type,key)
                    elif key=='destination_id':
                        value=getLocation(request,type,key)
                    elif key=='community_id':
                        value=getLocation(request,type,key)
                    elif key=='car_brand_id':
                        value=car['car_brand_id']
                    elif key=='car_model_id':
                        value=car['car_model_id']
                    else:
                        value = request.POST[key]
                else:
                    value = request.POST[key]
                kwargs.update({'%s' % key: value})
            record = d[type](**kwargs)
            record.save()
            deal.kw= deal.__str__().lower()
            deal.save()
        if deal:
            if type=='houserent' or type=='sublease':
                record.community.is_community=True
            return JsonResponse({"deal_id": deal.id, "status": "success"})
        else:
            return JsonResponse({'status': 'fail'})

def getCar(request,type):
    if type=='usedcar':
        car_brand_id=''
        car_model_id=''
        if request.POST['have_new_car']=='1':
            car_brand = ''
            car_model = ''
            car_brand_name=toTitleFormat(request.POST['new_car_brand_name'])
            car_brands=CarBrand.objects.filter(name=car_brand_name)
            with transaction.atomic():
                if len(car_brands)==0:
                    #Create new car brand
                    car_brand=CarBrand(name=car_brand_name)
                    car_brand.save()
                else:
                    car_brand=car_brands[0]

                car_brand_id=car_brand.id
                #Create new car model
                car_model_name=toTitleFormat(request.POST['new_car_model_name'])
                car_model=CarModel(name=car_model_name,brand_id=car_brand_id)
                car_model.save()
                car_model_id=car_model.id
        else:
            car_model_id=request.POST.get('car_model_id','')
            car_brand_id=request.POST.get('car_brand_id','')

        return{'car_model_id':car_model_id,'car_brand_id':car_brand_id}
    else:
        return ''


def getLocation(request, type, locationName):
    if type == 'carpool':
        if locationName == 'depart_place_id':
            #for new depart_place
            if request.POST['have_new_location_s'] == '1':
                state_id = request.POST['new_state_s_id']
                city_name = toTitleFormat(request.POST['new_city_s'])
                city = None
                cities=City.objects.filter(name=city_name)
                with transaction.atomic():
                    if len(cities) == 0:
                        city = City(name=city_name, state_id=state_id)
                        city.save()
                    else:
                        city = cities[0]
                    new_depart = toTitleFormat(request.POST['new_depart'])
                    new_address_s = toTitleFormat(request.POST['new_address_s'])
                    location = Location(name=new_depart, city=city, state_id=state_id, address=new_address_s)
                    location.save()
                    return location.id
            else:
                return request.POST.get('depart_place_id','')

        if locationName == 'destination_id':
            #for new destination
            if request.POST['have_new_location_d'] == '1':
                state_id = request.POST['new_state_d_id']
                city_name = toTitleFormat(request.POST['new_city_d'])
                city = None
                cities = City.objects.filter(name=city_name)
                with transaction.atomic():
                    if len(cities) == 0:
                        city = City(name=city_name, state_id=state_id)
                        city.save()
                    else:
                        city = cities[0]
                    new_destination = toTitleFormat(request.POST['new_destination'])
                    new_address_d = toTitleFormat(request.POST['new_address_d'])
                    location = Location(name=new_destination, city=city, state_id=state_id, address=new_address_d)
                    location.save()
                return location.id
            else:
                return request.POST.get('destination_id','')


    if (type=='houserent' or type=='sublease'):
        #for new community
        if request.POST['have_new_location'] == '1':
            state_id = request.POST['new_state_id']
            city_name = toTitleFormat(request.POST['new_city'])
            city = None
            cities = City.objects.filter(name=city_name)
            with transaction.atomic():
                if len(cities) == 0:
                    city = City(name=city_name, state_id=state_id)
                    city.save()
                else:
                    city = cities[0]
                new_community = toTitleFormat(request.POST['new_community'])
                new_address = toTitleFormat(request.POST['new_address'])
                location = Location(name=new_community, city=city, state_id=state_id, address=new_address, is_community=True)
                location.save()
            return location.id
        else:
            return request.POST.get('community_id','')

def toTitleFormat(str):
    strings=str.split()
    new_str=''
    for string in strings:
        string=string.title()
        new_str+=(string+' ')
    return new_str
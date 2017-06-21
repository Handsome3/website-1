import datetime
import traceback

from dateutil import relativedelta
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Deal, Carpool, MergeOrder, UsedCar, Image, HouseRent, Sublease, UsedItem, UserPro
import sys, traceback
from django.http import JsonResponse
from django.shortcuts import render

from . import views
from .models import *



@login_required
def getCarpoolPage(request):
    userPro = UserPro.objects.get(user=request.user)
    phone = '' if userPro.phone == '1234567890' else userPro.phone
    wechat = '' if userPro.wechat == 'None' else userPro.wechat
    return render(request, 'webapps/publishInfo/carpool.html', {'phone': phone, 'wechat': wechat})


@login_required
def carpoolPost(request):
    if request.method == 'POST':
        type = 'carpool'
        create_time = datetime.date.today()
        expire_time = create_time + relativedelta.relativedelta(months=1)
        user = request.user
        contact = request.POST.getlist('contact_type[]')
        contact_type = ""
        for i in contact:
            contact_type += i
        # carpool fields
        date = request.POST['date']
        time = request.POST['time']
        depart = request.POST['depart']
        destination = request.POST['destination']
        passenger_num = request.POST['passenger_num']
        price = request.POST['price']
        car_type = request.POST['car_type']
        note = request._post['note']

        # transaction
        with transaction.atomic():
            deal = Deal(type=type, create_time=create_time, expire_time=expire_time, posted_user=user,
                        contact_type=contact_type)
            deal.save()
            carpool = Carpool(deal=deal, date=date, time=time, depart_place=depart, destination=destination,
                              passenger_num=passenger_num, price=price, car_type=car_type, note=note)
            carpool.save()

            if deal:
                return JsonResponse({"deal_id": deal.id, "status": "success"})
            else:
                return JsonResponse({'status': 'fail'})

    #     return views.confirmaAndRedirect(request, "发布成功", "/user/getuserinfo")
    #
    # return render(request, 'webapps/carpool_post.html')
    #
    # except Exception as e:
    #     error_type = repr(e)
    #     tb = traceback.format_exc()
    #     return render(request, 'webapps/carpool_post.html',{'error_message': error_type,'tb':tb})
    #


@login_required
def getUsercarPage(request):
    userPro = UserPro.objects.get(user=request.user)
    phone = '' if userPro.phone == '1234567890' else userPro.phone
    wechat = '' if userPro.wechat == 'None' else userPro.wechat
    return render(request, 'webapps/publishInfo/usedCar.html', {'phone': phone, 'wechat': wechat})


@login_required
def usedcarPost(request):
        if request.method == 'POST':
            type = 'usedcar'
            create_time = datetime.date.today()
            expire_time = create_time + relativedelta.relativedelta(months=1)
            ### need to be changed
            user = request.user
            contact = request.POST.getlist('contact_type[]')
            contact_type = ""
            for i in contact:
                contact_type += i
            # usedcar fields
            year = request.POST['year']
            price = request.POST['price']
            mileage = request.POST['mileage']
            car_model_id = request.POST['car_model']
            car_brand_id = request.POST['car_brand']
            note = request.POST['note']
            # transaction
            with transaction.atomic():
                deal = Deal(type=type, create_time=create_time, expire_time=expire_time, posted_user=user, contact_type=contact_type)
                deal.save()
                usedcar = UsedCar(deal=deal, year=year, car_brand=CarBrand.objects.get(id=car_brand_id),
                                  car_model=CarModel.objects.get(id=car_model_id),
                                  price=price, mileage=mileage, note=note)
                usedcar.save()
            # redirect to a new URL:
            if deal:
                return JsonResponse({"deal_id": deal.id, "status":"success"})
            else:
                return JsonResponse({'status':'fail'})


@login_required
def getHouseRentPage(request):
    userPro = UserPro.objects.get(user=request.user)
    phone = '' if userPro.phone == '1234567890' else userPro.phone
    wechat = '' if userPro.wechat == 'None' else userPro.wechat
    return render(request, 'webapps/publishInfo/house.html', {'phone': phone, 'wechat': wechat})


@login_required
def houseRentPost(request):
    if request.method == 'POST':
        type = 'houserent'
        create_time = datetime.date.today()
        expire_time = create_time + relativedelta.relativedelta(months=1)
        user = request.user
        contact = request.POST.getlist('contact_type[]')
        contact_type = ""
        for i in contact:
            contact_type += i

        # houserent fields
        start_date = request.POST['start_date']
        community = request.POST['community']
        bedroom_num = request.POST['bedroom_num']
        bathroom_num = request.POST['bathroom_num']
        roommate_num = request.POST['roommate_num']
        roommate_gender = request.POST['roommate_gender']
        rent = request.POST['rent']
        duration = request.POST['duration']
        note = request._post['note']

        # transaction
        with transaction.atomic():
            deal = Deal(type=type, create_time=create_time, expire_time=expire_time, posted_user=user,
                        contact_type=contact_type)
            deal.save()
            houserent = HouseRent(deal=deal, start_date=start_date, community=community, bathroom_num=bathroom_num,
                                  bedroom_num=bedroom_num,
                                  roommate_num=roommate_num, roommate_gender=roommate_gender, rent=rent,
                                  duration=duration, note=note)
            houserent.save()
        # redirect to a new URL:
        if deal:
            return JsonResponse({"deal_id": deal.id, "status": "success"})
        else:
            return JsonResponse({'status': 'fail'})



@login_required
def getSubleasePage(request):
    userPro = UserPro.objects.get(user=request.user)
    phone = '' if userPro.phone == '1234567890' else userPro.phone
    wechat = '' if userPro.wechat == 'None' else userPro.wechat
    return render(request, 'webapps/publishInfo/sublease.html', {'phone': phone, 'wechat': wechat})


@login_required
def subleasePost(request):
    if request.method == 'POST':
        type = 'sublease'
        create_time = datetime.date.today()
        expire_time = create_time + relativedelta.relativedelta(months=1)
        user = request.user
        contact = request.POST.getlist('contact_type[]')
        contact_type = ""
        for i in contact:
            contact_type += i

        # sublease fields
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        community = request.POST['community']
        bedroom_num = request.POST['bedroom_num']
        bathroom_num = request.POST['bathroom_num']
        renewal = request.POST['renewal']
        rent = request.POST['rent']
        note = request._post['note']

        # transaction
        with transaction.atomic():
            deal = Deal(type=type, create_time=create_time, expire_time=expire_time, posted_user=user,
                        contact_type=contact_type)
            deal.save()
            sublease = Sublease(deal=deal, start_date=start_date, end_date=end_date, community=community,
                                bathroom_num=bathroom_num, bedroom_num=bedroom_num,
                                renewal=renewal, rent=rent, note=note)
            sublease.save()
        # redirect to a new URL:
        if deal:
            return JsonResponse({"deal_id": deal.id, "status": "success"})
        else:
            return JsonResponse({'status': 'fail'})


@login_required
def getMergeOrderPage(request):
    userPro = UserPro.objects.get(user=request.user)
    phone = '' if userPro.phone == '1234567890' else userPro.phone
    wechat = '' if userPro.wechat == 'None' else userPro.wechat
    return render(request, 'webapps/publishInfo/mergeOrder.html', {'phone': phone, 'wechat': wechat})


@login_required
def mergeOrderPost(request):
        if request.method == 'POST':
            type = 'houserent'
            create_time = datetime.date.today()
            expire_time = create_time + relativedelta.relativedelta(months=1)
            user = request.user
            contact = request.POST.getlist('contact_type[]')
            contact_type = ""
            for i in contact:
                contact_type += i
            # carpool fields
            website = request.POST['website']
            order_type = request.POST['order_type']
            duedate = request.POST['duedate']
            note = request._post['note']

            # transaction
            with transaction.atomic():
                deal = Deal(type=type, create_time=create_time, expire_time=expire_time, posted_user=user,
                            contact_type=contact_type)
                deal.save()
                mergeorder = MergeOrder(deal=deal, duedate=duedate,website=website,order_type=order_type, note=note)
                mergeorder.save()

            if deal:
                return JsonResponse({"deal_id": deal.id, "status": "success"})
            else:
                return JsonResponse({'status': 'fail'})


@login_required
def getUsedItemPage(request):
    userPro = UserPro.objects.get(user=request.user)
    phone = '' if userPro.phone == '1234567890' else userPro.phone
    wechat = '' if userPro.wechat == 'None' else userPro.wechat
    return render(request, 'webapps/publishInfo/usedItem.html', {'phone': phone, 'wechat': wechat})


@login_required
def usedItemPost(request):
    if request.method == 'POST':
        type = 'useditem'
        create_time = datetime.date.today()
        expire_time = create_time + relativedelta.relativedelta(months=1)
        user = request.user
        contact = request.POST.getlist('contact_type[]')
        contact_type = ""
        for i in contact:
            contact_type += i
        # useditem fields
        item_type = request.POST['item_type']
        item_name = request.POST['item_name']
        price = request.POST['price']
        condition = request.POST['condition']
        note = request._post['note']

        # transaction
        with transaction.atomic():
            deal = Deal(type=type, create_time=create_time, expire_time=expire_time, posted_user=user,
                        contact_type=contact_type)
            deal.save()
            useditem = UsedItem(deal=deal, item_type=item_type, condition=condition, item_name=item_name,
                                price=price, note=note)
            useditem.save()

        if deal:
            return JsonResponse({"deal_id": deal.id, "status": "success"})
        else:
            return JsonResponse({'status': 'fail'})

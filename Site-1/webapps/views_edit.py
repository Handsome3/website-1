import datetime
import os

from dateutil import relativedelta
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from mysite.settings import MEDIA_ROOT
from .models import *
from .views import confirmaAndRedirect
from .views_detail import getContact
from .views_post import getLocation,toTitleFormat,getCar


@login_required
def deleteDeal(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    next = request.GET.get('next', '/')
    if request.user != deal.posted_user:
        return confirmaAndRedirect(request, '出错啦！您不是发布者，无法删除', '/')
    else:
        for img in deal.image_set.all():
            img.image.delete()
        s = "_"
        path = os.path.join(MEDIA_ROOT, "images", s.join(['user', str(deal.posted_user.id)]),
                            s.join(['deal', str(deal.id), str(deal.type)]))
        path = path.replace('\\', '/')
        try:
            os.rmdir(path)
        except Exception:
            pass
        deal.delete()
        return confirmaAndRedirect(request, '删除成功！', next)


@login_required
def editDeal(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    next = request.GET.get('next', '/')
    if request.user != deal.posted_user:
        return confirmaAndRedirect(request, '出错啦！您不是发布者，无法修改', next)
    else:
        userPro = UserPro.objects.get(user=request.user)
        phone = '' if userPro.phone == '1234567890' else userPro.phone
        wechat = '' if userPro.wechat == 'None' else userPro.wechat
        contact = getContact(deal)
        images = deal.image_set.all()
        if deal.type == 'usedcar':
            return render(request, 'webapps/edit/usedCarEdit.html',
                          {'deal': deal, 'phone': phone, 'wechat': wechat, 'images': images})
        elif deal.type=='mergeorder':
            return render(request,'webapps/edit/mergeOrderEdit.html',
                          {'deal' : deal,'phone': phone, 'wechat':wechat})
        elif deal.type=='carpool':
            return render(request,'webapps/edit/carpoolEdit.html',
                          {'deal': deal,'phone': phone,'wechat': wechat})
        elif deal.type=='houserent':
            return render(request,'webapps/edit/houseEdit.html',
                          {'deal': deal,'phone': phone,'wechat': wechat,'images':images})
        elif deal.type=='sublease':
            return render(request,'webapps/edit/subleaseEdit.html',
                          {'deal': deal,'phone': phone,'wechat': wechat,'images':images})
        elif deal.type=='useditem':
            return render(request,'webapps/edit/usedItemEdit.html',
                          {'deal': deal,'phone': phone,'wechat': wechat,'images':images})
        else:
            pass


@login_required
def stopDeal(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    next = request.GET.get('next', '/')
    if request.user != deal.posted_user:
        return confirmaAndRedirect(request, '出错啦！您不是发布者，无法修改', '/')
    else:
        deal.expire_time = datetime.datetime.now() - relativedelta.relativedelta(days=1)
        deal.save()
        return confirmaAndRedirect(request, '信息下架成功！', next)


@login_required
def repostDeal(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    next = request.GET.get('next', '/')
    if request.user != deal.posted_user:
        return confirmaAndRedirect(request, '出错啦！您不是发布者，无法修改', '/')
    else:
        deal.expire_time = datetime.datetime.now() + relativedelta.relativedelta(months=1)
        deal.save()
        return confirmaAndRedirect(request, '信息重新发布成功！', next)

@login_required
def deleteImage(request):
    img = Image.objects.get(id=request.POST['key'])
    if request.user != img.user:
        return JsonResponse({'status': 'error'})
    else:
        img.image.delete()
        img.delete()
        return JsonResponse({'status': 'success'})

@login_required
def changeDealInfo(request):
    deal = Deal.objects.get(id=request.POST['deal_id'])
    if deal:
        contact = request.POST.getlist('contact_type[]')
        contact_type = ""
        for i in contact:
            contact_type += i
        with transaction.atomic():
            deal.contact_type = contact_type
            deal.save()
    return deal

@login_required
def editUsedcar(request):
    type='usedcar'
    if request.method == 'POST':
        deal = changeDealInfo(request)
        car=getCar(request,type)
        if deal:
            year = request.POST['year']
            price = request.POST['price']
            mileage = request.POST['mileage']
            car_model_id = car['car_model_id']
            car_brand_id = car['car_brand_id']
            note = request.POST['note']
            with transaction.atomic():
                deal.usedcar.year = year
                deal.usedcar.price = price
                deal.usedcar.mileage = mileage
                deal.usedcar.note = note
                if car_model_id:
                    deal.usedcar.car_model = CarModel.objects.get(id=car_model_id)
                if car_brand_id:
                    deal.usedcar.car_brand = CarBrand.objects.get(id=car_brand_id)
                deal.usedcar.save()
            return JsonResponse({'status': 'success'})

@login_required
def editCarpool(request):
    type='carpool'
    if request.method == 'POST':
        deal = changeDealInfo(request)
        if deal:
            date = request.POST['date']
            time = request.POST['time']
            depart_place_id = getLocation(request,type,'depart_place_id')
            destination_id = getLocation(request,type,'destination_id')
            passenger_num = request.POST['passenger_num']
            price = request.POST['price']
            car_type = request.POST['car_type']
            note = request._post['note']
            with transaction.atomic():
                deal.carpool.date= date
                deal.carpool.price = price
                deal.carpool.time = time
                if depart_place_id:
                    deal.carpool.depart_place_id = depart_place_id
                if destination_id:
                    deal.carpool.destination_id = destination_id
                deal.carpool.passenger_num = passenger_num
                deal.carpool.car_type = car_type
                deal.carpool.note = note
                deal.carpool.save()
            return JsonResponse({'status': 'success'})

@login_required
def editUseditem(request):
    if request.method == 'POST':
        deal = changeDealInfo(request)
        if deal:
            item_type = request.POST['item_type']
            item_name = request.POST['item_name']
            price = request.POST['price']
            condition = request.POST['condition']
            note = request.POST['note']
            with transaction.atomic():
                deal.useditem.item_type=item_type
                deal.useditem.item_name=item_name
                deal.useditem.price=price
                deal.useditem.condition=condition
                deal.useditem.note=note
                deal.useditem.save()
            return JsonResponse({'status': 'success'})

@login_required
def editMergeorder(request):
    if request.method == 'POST':
        deal = changeDealInfo(request)
        if deal:
            website = request.POST['website']
            order_type = request.POST['order_type']
            duedate = request.POST['duedate']
            note = request._post['note']
            with transaction.atomic():
                deal.mergeorder.website=website
                deal.mergeorder.order_type=order_type
                deal.mergeorder.duedate=duedate
                deal.mergeorder.note = note
                deal.mergeorder.save()
            return JsonResponse({'status': 'success'})

@login_required
def editHouserent(request):
    type='houserent'
    if request.method == 'POST':
        deal = changeDealInfo(request)
        if deal:
            start_date = request.POST['start_date']
            community_id = getLocation(request,type,'community_id')
            bedroom_num = request.POST['bedroom_num']
            bathroom_num = request.POST['bathroom_num']
            roommate_num = request.POST['roommate_num']
            roommate_gender = request.POST['roommate_gender']
            rent = request.POST['rent']
            duration = request.POST['duration']
            note = request._post['note']
            with transaction.atomic():
                deal.houserent.start_date=start_date
                if community_id:
                    deal.houserent.community_id=community_id
                deal.houserent.bedroom_num=bedroom_num
                deal.houserent.bathroom_num=bathroom_num
                deal.houserent.roommate_num=roommate_num
                deal.houserent.roommate_gender=roommate_gender
                deal.houserent.rent=rent
                deal.houserent.duration=duration
                deal.houserent.note=note
                deal.houserent.save()
            return JsonResponse({'status': 'success'})

@login_required
def editSublease(request):
    type='sublease'
    if request.method == 'POST':
        deal = changeDealInfo(request)
        if deal:
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            community_id = getLocation(request,type,'community_id')
            bedroom_num = int(request.POST['bedroom_num'])
            bathroom_num = int(request.POST['bathroom_num'])
            renewal = request.POST['renewal']
            rent = request.POST['rent']
            note = request._post['note']
            with transaction.atomic():
                deal.sublease.start_date=start_date
                deal.sublease.end_date=end_date
                if community_id:
                    deal.sublease.community_id=community_id
                deal.sublease.bedroom_num=bedroom_num
                deal.sublease.bathroom_num=bathroom_num
                deal.sublease.renewal=renewal
                deal.sublease.rent=rent
                deal.sublease.note=note
                deal.sublease.save()
            return JsonResponse({'status': 'success'})


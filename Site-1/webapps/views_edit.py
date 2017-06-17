from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import *
from .views import confirmaAndRedirect
from .views_detail import getContact


@login_required
def deleteDeal(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    if request.user != deal.posted_user:
        return confirmaAndRedirect(request, '出错啦！您不是发布者，无法删除', '/')
    else:
        for img in deal.image_set.all():
            img.image.delete()
        deal.delete()
        return confirmaAndRedirect(request, '删除成功！', reverse('webapps:getuserinfo'))


@login_required
def editDeal(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    if request.user != deal.posted_user:
        return confirmaAndRedirect(request, '出错啦！您不是发布者，无法修改', '/')
    else:
        userPro = UserPro.objects.get(user=request.user)
        phone = '' if userPro.phone == '1234567890' else userPro.phone
        wechat = '' if userPro.wechat == 'None' else userPro.wechat
        contact = getContact(deal)
        images = deal.image_set.all()
        if deal.type == 'usedcar':
            return render(request, 'webapps/edit/usedCar.html',
                          {'deal': deal, 'phone': phone, 'wechat': wechat, 'images': images})
        else:
            pass


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
def ajaxEditDeal(request):
    if request.method == 'POST':
        deal = Deal.objects.get(id=request.POST['deal_id'])
        if deal:
            contact = request.POST.getlist('contact_type[]')
            contact_type = ""
            for i in contact:
                contact_type += i
            year = request.POST['year']
            price = request.POST['price']
            mileage = request.POST['mileage']
            car_model_id = request.POST.get('car_model', '')
            car_brand_id = request.POST.get('car_brand', '')
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
                deal.contact_type = contact_type
                deal.save()
                deal.usedcar.save()
            return JsonResponse({'status': 'success'})

import datetime
from . import views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dateutil import relativedelta
from django.db import transaction
from .models import Deal,Carpool,MergeOrder,UsedCar,Image,HouseRent,Sublease,UsedItem, UserPro
import sys, traceback
from django.http import JsonResponse

@login_required
def carpoolPage(request):
    userPro=UserPro.objects.get(user=request.user)
    phone='' if userPro.phone=='1234567890' else userPro.phone
    wechat='' if userPro.wechat=='None' else userPro.wechat
    return render(request, 'webapps/publishInfo/carpool.html', {'phone':phone, 'wechat':wechat})

@login_required
def carpoolPost(request):
    try:
        if request.method=='POST':
            type = 'carpool'
            create_time = datetime.date.today()
            expire_time = create_time+ relativedelta.relativedelta(months=1)
            user=request.user
            contact= request.POST.getlist('contact_type[]')
            contact_type=""
            for i in contact:
                contact_type+=i
            # carpool fields
            date = request.POST['date']
            time = request.POST['time']
            depart= request.POST['depart']
            destination = request.POST['destination']
            passenger_num = request.POST['passenger_num']
            price = request.POST['price']
            car_type = request.POST['car_type']
            note = request._post['note']

            #transaction
            with transaction.atomic():
                deal = Deal(type=type,create_time=create_time,expire_time=expire_time,posted_user=user, contact_type=contact_type)
                deal.save()
                carpool = Carpool(deal = deal,date = date, time=time,depart_place = depart,destination=destination,
                                  passenger_num=passenger_num,price=price, car_type=car_type,note=note)
                carpool.save()

            return views.confirmaAndRedirect(request, "发布成功", "/user/getuserinfo")

        return render(request,'webapps/carpool_post.html')

    except Exception as e:
        error_type = repr(e)
        tb = traceback.format_exc()
        return render(request, 'webapps/carpool_post.html',{'error_message': error_type,'tb':tb})

@login_required
def usercarPage(request):
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
            car_model = request.POST['car_model']
            car_brand = request.POST['car_brand']
            note = request.POST['note']
            # transaction
            with transaction.atomic():
                deal = Deal(type=type, create_time=create_time, expire_time=expire_time, posted_user=user, contact_type=contact_type)
                deal.save()
                usedcar = UsedCar(deal=deal, year=year, car_brand=car_brand, car_model=car_model,
                                  price=price, mileage=mileage, note=note)
                usedcar.save()
            # redirect to a new URL:
            if deal:
                return JsonResponse({"deal_id": deal.id, "status":"success"})
            else:
                return JsonResponse({'status':'fail'})

'''def usedcarPost(request):
    try:
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = UsedCarForm(request.POST,request.FILES)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # deal fields
                type = 'usedcar'
                create_time = datetime.date.today()
                expire_time = create_time + relativedelta.relativedelta(months=1)
                ### need to be changed
                user = request.user
                city = form.cleaned_data['city']
                state = form.cleaned_data['state']
                #usedcar fields
                year = form.cleaned_data['year']
                price = form.cleaned_data['price']
                mileage = form.cleaned_data['mileage']
                car_model = form.cleaned_data['car_model']
                car_brand = form.cleaned_data['car_brand']
                note = form.cleaned_data['note']

                #images
                images = request.FILES.getlist('images')

                #transaction
                with transaction.atomic():
                    deal = Deal(type=type, create_time=create_time, expire_time=expire_time, posted_user=user,
                                city=city,state=state)
                    deal.save()
                    usedcar = UsedCar(deal_id=deal.id, year=year, car_brand=car_brand, car_model=car_model,
                                        price=price,mileage=mileage,note=note)
                    usedcar.save()
                for image in images:
                    instance = Image(image_path='x', image=image, deal=deal)
                    instance.image_path = instance.image.path
                    instance.save()

                # redirect to a new URL:
                return views.confirmaAndRedirect(request, "发布成功", "/user/getuserinfo")
            else:
                return HttpResponse("form error")
        # if a GET (or any other method) we'll create a blank form

    except Exception as e:
        error_type = repr(e)
        tb = traceback.format_exc()
        return render(request, 'webapps/publishInfo/usedCar.html',{'error_message': error_type,'tb':tb,'form':form})'''

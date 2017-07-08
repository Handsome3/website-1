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

@login_required
def postPage(request, type) :
    userPro = UserPro.objects.get(user=request.user)
    phone = '' if userPro.phone == '1234567890' else userPro.phone
    wechat = '' if userPro.wechat == 'None' else userPro.wechat
    return render(request, 'webapps/publishInfo/'+type+'.html', {'phone': phone, 'wechat': wechat})

@login_required
def submitPost(request, type) :
    d= {
        'usedcar': UsedCar,
        'useditem': UsedItem,
        'sublease': Sublease,
        'houserent': HouseRent,
        'carpool': Carpool,
        'mergeorder': MergeOrder,
    }
    if request.method == 'POST':
        create_time = datetime.date.today()
        expire_time = create_time + relativedelta.relativedelta(months=1)
        user = request.user
        contact = request.POST.getlist('contact_type[]')
        contact_type = ""
        for i in contact:
            contact_type += i
        t= d[type]._meta.get_fields()
        kwargs = {}
        with transaction.atomic():
            deal = Deal(type=type, create_time=create_time, expire_time=expire_time, posted_user=user,
                        contact_type=contact_type)
            deal.save()
            for f in t:
                key= f.name
                if key == 'deal':
                    value= deal
                elif f.is_relation:
                    key+= '_id'
                    value= request.POST[key]
                else:
                    value= request.POST[key]
                kwargs.update({'%s' % key: value})
            record= d[type](**kwargs)
            record.save()
            deal.kw= deal.__str__()
            deal.save()
        if deal:
            return JsonResponse({"deal_id": deal.id, "status": "success"})
        else:
            return JsonResponse({'status': 'fail'})



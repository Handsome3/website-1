from django.shortcuts import render, get_object_or_404
from .models import Deal,Carpool,MergeOrder,UsedCar,Image,HouseRent,Sublease,UsedItem, UserPro
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def getCarpool(text):
    pass

def getUsedCar(deal):
    car=UsedCar.objects.get(deal=deal)
    res={
        "年份": car.year,
        "品牌": car.car_brand,
        "型号": car.car_model,
        "里程数" : car.mileage,
        "售价" : car.price,
        "补充说明" : car.note,
    }
    return res

def getContact(deal):
    user=deal.posted_user
    res={}
    userpro=UserPro.objects.get(user=user)
    if "1" in deal.contact_type:
        res.update({'email': user.username})
    if "2" in deal.contact_type:
        res.update({'phone' : userpro.phone})
    if "3" in deal.contact_type:
        res.update({'wechat': userpro.wechat})
    return res

def getDealDetail(request, deal_id):
    deal=get_object_or_404(Deal, id=deal_id)

    d = {
        'carpool': getCarpool,
        'usedcar': getUsedCar,
    }
    text = {"发布时间": deal.create_time}
    text.update(d[deal.type](deal))
    images=Image.objects.filter(deal=deal)

    if (request.user.is_authenticated() and (deal.saved_users.filter(id=request.user.id) or request.user==deal.posted_user)):
        config={'is_saved': True}
        contact = getContact(deal)
        config.update(contact)
    else:
        config={'is_saved': False}
    config.update({'deal_id' : deal.id})

    return render(request, 'webapps/detail.html', {'text': text, 'images': images, 'config' : config })

@login_required
def saveDeal(request):
    deal_id=request.GET['deal_id']
    deal=Deal.objects.get(id=deal_id)
    deal.saved_users.add(request.user)
    deal.save()
    contact=getContact(deal)
    return JsonResponse({'status' : 'success', 'contact' :contact})

@login_required
def unsaveDeal(request):
    deal_id=request.GET['deal_id']
    deal=Deal.objects.get(id=deal_id)
    deal.saved_users.remove(request.user)
    deal.save()
    return JsonResponse({'status': 'success'})

@login_required
def loadMoreDeal(request):
    res={}
    type=request.GET['type']
    start=int(request.GET['end'])
    deals = Deal.objects.filter(posted_user=request.user).order_by('create_time')
    if type:
        deals = deals.filter(type=type)
    deals=deals[start:start+10]
    res['has_next']=True if deals.count()==10 else False
    res['end']=start+10
    res['type']=type
    records = []
    for deal in deals:
        record = {'id': deal.id,
                  'title': deal.__str__(),
                  'type': deal.type,
                  'create_time': deal.create_time,
                  'expire_time': deal.expire_time,
                  'hot_index': deal.hot_index,
                  }
        records.append(record)
    res['records']=records
    res['status']='success'
    return JsonResponse(res)

import datetime

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from . import views
from .models import UserPro, Deal

typeDic = {'usedcar': '二手车',
           'carpool': 'Carpool',
           'useditem': '二手商品',
           'houserent': '合租',
           'sublease': 'Sublease',
           'mergeorder': '拼单',
           }

def loginPage(request):
    if request.user.is_authenticated:
        return views.confirmaAndRedirect(request, '您已登录，请先退出登录', '/')
    return render(request, 'webapps/login.html')

def signup(request):
    if request.user.is_authenticated:
        return views.confirmaAndRedirect(request, '您已登录，请先退出登录', '/')
    return render(request, 'webapps/signup.html')

def register(request):
    if request.method=="POST":
        username=request.POST['email']
        password=request.POST['password']
        firstname=request.POST['username']
        if request.POST['phone']=='':
            phone='1234567890'
        else:
            phone=request.POST['phone']
        if request.POST['wechat']=='':
            wechat='None'
        else:
            wechat=request.POST['wechat']
        with transaction.atomic():
            user=User.objects.create_user(username=username, password=password, first_name=firstname)
            userPro= UserPro(user=user, phone=phone, wechat=wechat)
            userPro.save()
        return views.confirmaAndRedirect(request, '注册成功', '/user/loginpage')
    return render(request, 'webapps/login.html')

def userlogin(request):
    if request.method=="POST":
        username=request.POST['email']
        password=request.POST['password']
        next= request.POST['next']
        if next=='':
            next='/'
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return views.confirmaAndRedirect(request, '登录成功', next)
        else:
            return render(request, 'webapps/login.html', {'info': '用户名或密码错误！'})

def userlogout(request):
    if not request.user.is_authenticated:
        return views.confirmaAndRedirect(request, '您尚未登录', '/')
    else:
        logout(request)
        return views.confirmaAndRedirect(request, '您已经退出登录', '/')

def changeUser(request):
    if not request.user.is_authenticated:
        return views.confirmaAndRedirect(request, '您尚未登录', '/')
    else:
        logout(request)
        return loginPage(request)

def checkEmail(request):
    if request.method=="GET":
        currentEmail=request.GET['email']
        user=User.objects.filter(username=currentEmail)
        if user:
            return JsonResponse({'valid' : 'false'})
        else:
            return JsonResponse({'valid' : 'true'})


def countDeal(request):
    countPost = {'usedcar': 0, 'carpool': 0, 'houserent': 0, 'sublease': 0, 'mergeorder': 0, 'useditem': 0}
    countSave = {'usedcar': 0, 'carpool': 0, 'houserent': 0, 'sublease': 0, 'mergeorder': 0, 'useditem': 0}
    for k in countPost.keys():
        countPost[k] = Deal.objects.filter(posted_user=request.user, type=k).count()
        countSave[k] = request.user.saved_by_users.all().filter(type=k).count()
    sumPost = Deal.objects.filter(posted_user=request.user).count()
    sumSave = request.user.saved_by_users.all().count()
    countPost.update({'total': sumPost})
    countSave.update({'total': sumSave})
    return {'countPost': countPost, 'countSave': countSave}


@login_required
def getUserInfo(request):
    type = request.GET.get('type', '')
    is_save = False if request.GET.get('saved', 'False') == 'False' else True
    is_overdue = False if request.GET.get('overdue', 'False') == 'False' else True

    # filter the deals which fulfill the requirements of request
    config = {'type': type, 'is_save': is_save, 'is_overdue': is_overdue}
    if is_save:
        deals = request.user.saved_by_users.all()
    else:
        deals = Deal.objects.filter(posted_user=request.user).order_by('create_time')
    if is_overdue:
        deals = deals.filter(expire_time__lt=datetime.datetime.now())
    else:
        deals = deals.filter(expire_time__gte=datetime.datetime.now())
    if type:
        deals = deals.filter(type=type)
    deals = deals[:10]
    config['has_next'] = True if deals.count() == 10 else False

    # count the number of posts and saved posts
    config.update(countDeal(request))

    records = []
    for deal in deals:
        record={'id':deal.id,
                'title': deal,
                'type': typeDic[deal.type],
                'create_time' : deal.create_time,
                'expire_time' : deal.expire_time,
                'hot_index' : deal.hot_index,
                }
        records.append(record)

    return render(request, 'webapps/userInfo.html', {'records': records, 'config': config})


@login_required
def editProfile(request):
    config = {}
    config.update(countDeal(request))
    return render(request, 'webapps/personInfo.html', {'config': config})


@login_required
def changePw(request):
    if request.method == "POST":
        oldpw = request.POST['oldpw']
        newpw = request.POST['newpw']
        user = authenticate(username=request.user.username, password=oldpw)
        if user is not None:
            user.set_password(newpw)
            user.save()
            update_session_auth_hash(request, user)
            return JsonResponse({'status': 'success', 'info': '密码修改成功，请牢记！'})
        else:
            return JsonResponse({'status': 'fail', 'info': '旧密码输入错误'})


@login_required
def changeProfile(request):
    if request.method == 'POST':
        username = request.POST['username']
        wechat = request.POST['wechat']
        phone = request.POST['phone']
        user = User.objects.get(id=request.user.id)
        with transaction.atomic():
            user.first_name = username
            user.userpro.wechat = wechat
            user.userpro.phone = phone
            user.save()
            user.userpro.save()
        return JsonResponse({'status': 'success'})

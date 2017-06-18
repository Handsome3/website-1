from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from . import views
from .models import UserPro, Deal


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

@login_required
def getUserInfo(request):
    type=request.GET.get('type', '')
    config={'type' : type}
    deals = Deal.objects.filter(posted_user=request.user).order_by('create_time')
    if type:
        deals = deals.filter(type=type)
    deals = deals[:10]
    config['has_next'] = True if deals.count() == 10 else False
    records=[]
    countPost = {'usedcar': 0, 'carpool': 0, 'houserent': 0, 'sublease': 0, 'mergeorder': 0, 'useditem': 0}
    for k in countPost.keys():
        countPost[k] = Deal.objects.filter(posted_user=request.user, type=k).count()
    for deal in deals:
        record={'id':deal.id,
                'title': deal.__str__(),
                'type': deal.type,
                'create_time' : deal.create_time,
                'expire_time' : deal.expire_time,
                'hot_index' : deal.hot_index,
                }
        records.append(record)
    config.update({'countPost': countPost})
    return render(request, 'webapps/userInfo.html', {'records': records, 'config': config})
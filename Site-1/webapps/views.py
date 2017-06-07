from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect


def index(request):
    return render(request, 'webapps/index.html')

#Search Pages
def searchCarpool(request):
    return HttpResponse("Search carpool")

def searchUsedItem(request):
    return HttpResponse("searchUsedItem")

def searchHouse(request):
    return HttpResponse("searchHouse")

def searchUsedCar(request):
    return HttpResponse("searchUsedCar")

def searchMergeOrder(request):
    return HttpResponse("searchMergeOrder")

# Inform user information and Redirect page
def confirmaAndRedirect(request, info, redirect_path):
    return render(request, 'webapps/success.html', {'info' : info, 'redirect_path' : redirect_path})

def getPostResult(request):
        return render(request,'webapps/postsuccessfully.html')

#Item Detail Pages
def getItem(request):
    return HttpResponse("getItemDetail")

def redirect(request):
    info=request.GET['info']
    redirect_path=request.GET['next']
    return confirmaAndRedirect(request, info, redirect_path)



# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'webapps/index.html')

#Search Pages


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



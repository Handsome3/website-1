from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'webapps/index.html')

# Inform user information and Redirect page
def confirmaAndRedirect(request, info, redirect_path):
    return render(request, 'webapps/success.html', {'info' : info, 'redirect_path' : redirect_path})

def redirect(request):
    info=request.GET['info']
    redirect_path=request.GET['next']
    return confirmaAndRedirect(request, info, redirect_path)



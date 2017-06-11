from django.shortcuts import render
from .models import Deal, Carpool, MergeOrder, UsedCar, Image, HouseRent, Sublease, UsedItem, UserPro
from django.contrib.auth.models import User


def searchDeal(config):
    pass


def searchUsedcar(request):
    return render(request, 'webapps/search/usedCar.html')

from django.shortcuts import render

def getDealDetail(request, deal_id):

    return render(request, 'webapps/detail.html')
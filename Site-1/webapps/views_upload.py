from django.contrib.auth.decorators import login_required
from .models import Deal,Carpool,MergeOrder,UsedCar,Image,HouseRent,Sublease,UsedItem, UserPro
from django.http import JsonResponse

@login_required
def usedcar(request):
        images=request.FILES.getlist('images')
        print(request.POST['deal_id'])
        deal=Deal.objects.get(id=request.POST['deal_id'])
        user=request.user
        img_seq=1
        for img in images:
            instance=Image(image=img, deal=deal,user=user,img_seq=img_seq)
            instance.save()
            img_seq=img_seq+1
        return JsonResponse({'status': 'success', 'deal_id': deal.id})




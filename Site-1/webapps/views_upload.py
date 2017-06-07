from django.contrib.auth.decorators import login_required
from .models import Deal,Carpool,MergeOrder,UsedCar,Image,HouseRent,Sublease,UsedItem, UserPro
from django.http import JsonResponse

@login_required
def usedcar(request):
        images=request.FILES.getlist('images')
        print(request.POST['deal_id'])
        deal=Deal.objects.get(id=request.POST['deal_id'])
        user=request.user
        for img in images:
            instance=Image(image_path='x', image=img, deal=deal)
            instance.image_path=instance.image.path
            instance.save()
        return JsonResponse({'status': 'success', 'deal_id': deal.id})




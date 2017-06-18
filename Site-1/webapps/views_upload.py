from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Deal, Image


@login_required
def usedcar(request):
        images=request.FILES.getlist('images')
        deal=Deal.objects.get(id=request.POST['deal_id'])
        user=request.user
        for img in images:
            instance = Image(image=img, deal=deal, user=user)
            instance.save()
        return JsonResponse({'status': 'success', 'deal_id': deal.id})





def submitPost(request, type):
    if request.method == 'POST':
        create_time = datetime.date.today()
        if type == 'carpool':
            expire_time= request.POST['date']
        else:
            expire_time = create_time + relativedelta.relativedelta(months=1)
        user = request.user
        contact = request.POST.getlist('contact_type[]')
        contact_type = ""
        for i in contact:
            contact_type += i
        t = d[type]._meta.get_fields()
        kwargs = {}

        car=None
        if type=='usedcar':
            car=getCar(request,type)

        with transaction.atomic():
            # specific deals are saved below
            deal = Deal(type=type, create_time=create_time, expire_time=expire_time, posted_user=user,
                        contact_type=contact_type)
            deal.save()

            for f in t:
                key = f.name
                if key == 'deal':
                    value = deal
                elif f.is_relation:
                    key += '_id'
                    if key=='depart_place_id':
                        value=getLocation(request,type,key)
                    elif key=='destination_id':
                        value=getLocation(request,type,key)
                    elif key=='community_id':
                        value=getLocation(request,type,key)
                    elif key=='car_brand_id':
                        value=car['car_brand_id']
                    elif key=='car_model_id':
                        value=car['car_model_id']
                    else:
                        value = request.POST[key]
                else:
                    value = request.POST[key]
                kwargs.update({'%s' % key: value})
            record = d[type](**kwargs)
            record.save()
            deal.kw= deal.__str__().lower()
            deal.save()
        if deal:
            if type=='houserent' or type=='sublease':
                record.community.is_community=True
            return JsonResponse({"deal_id": deal.id, "status": "success"})
        else:
            return JsonResponse({'status': 'fail'})
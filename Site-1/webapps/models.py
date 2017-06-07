from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserPro(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    wechat = models.CharField(max_length=30, default='None')
    phone = models.CharField(max_length=10, default='1234567890')

class Deal(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)
    saved_users = models.ManyToManyField(User,related_name="saved_by_users",verbose_name="users_deals")
    posted_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posted_by_user")
    create_time = models.DateField()
    expire_time = models.DateField()
    contact_type = models.CharField(max_length=20,default='1')
    state = models.CharField(max_length=30,default="florida")
    city = models.CharField(max_length = 30,default="gainesville")
    def __str__(self):
        return "deal_id: " + str(self.id) +" type:" +str(self.type)

class Carpool(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    date = models.DateField()
    time = models.TimeField(default="00:00:00")
    depart_place = models.CharField(max_length=128)
    destination = models.CharField(max_length=128)
    passenger_num = models.IntegerField()
    price = models.FloatField()
    car_type = models.CharField(max_length=20,default="sedan")
    note = models.TextField(null=True, blank=True)
    def __str__(self):
        return "deal_id: "+ str(self.deal_id) + " from: "+ str(self.depart_place)+" to: " + str(self.destination)

class UsedCar(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    year = models.IntegerField()
    car_brand = models.CharField(max_length=30)
    car_model = models.CharField(max_length=30)
    mileage = models.IntegerField()
    price = models.IntegerField()
    note = models.TextField(null=True)
    def __str__(self):
        return "deal_id: "+ str(self.deal_id) + " brand: "+ str(self.car_brand)

class UsedItem(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    item_type = models.CharField(max_length=20,default='electronic_default')
    item_name = models.CharField(max_length=20,default='monitor_default')
    condition = models.CharField(max_length=20)
    price = models.IntegerField()
    note = models.TextField(null=True)
    def __str__(self):
        return "deal_id: "+ str(self.deal_id) + " item_type: "+ str(self.item_type)

class Sublease(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    community = models.CharField(max_length=40)
    house_type = models.CharField(max_length=20)
    rent = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    renew = models.BooleanField(default=True)
    note = models.TextField(null=True)
    def __str__(self):
        return"deal_id: "+ str(self.deal_id) + " community: "+ str(self.community)

class HouseRent(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    community = models.CharField(max_length=40)
    house_type = models.CharField(max_length=20)
    rent = models.FloatField()
    start_date = models.DateField()
    duration = models.CharField(max_length=20,default='6 months')
    roommate_gender = models.CharField(max_length=6)

    roommate_num = models.IntegerField()
    note = models.TextField(null=True)
    def __str__(self):
        return "deal_id: " + str(self.deal_id) + " community: " + str(self.community)

class MergeOrder(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    website = models.URLField(max_length=100,default='www.google.com')
    order_type = models.CharField(max_length=30)
    duedate = models.DateField(default='2017-12-31')
    note = models.TextField(null=True)
    def __str__(self):
        return str(self.deal_id) + " " + str(self.website)

class Image(models.Model):
    image_path = models.CharField(max_length=120)
    image = models.ImageField(upload_to='temp', default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    deal = models.ForeignKey(Deal,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.image)



from django.contrib.auth.models import User
from django.db import models

from .utilities import upload_to_path
import time


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
    hot_index=models.FloatField(default=0)
    title=models.CharField(max_length=50, default='deal')
    kw= models.CharField(max_length=200, default="")

    def __str__(self):
        if self.type == 'carpool':
            return self.carpool.__str__()
        elif self.type == 'usedcar':
            return self.usedcar.__str__()
        elif self.type == 'useditem':
            return self.useditem.__str__()
        elif self.type == 'sublease':
            return self.sublease.__str__()
        elif self.type == 'houserent':
            return self.houserent.__str__()
        elif self.type == 'mergeorder':
            return self.mergeorder.__str__()

class CarBrand(models.Model):
    name = models.CharField(max_length=20)
    icon = models.ImageField(upload_to='carbrand', blank=True, null=True)

    def __str__(self):
        return str(self.name)

class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
            return str(self.name)


class State(models.Model):
    name=models.CharField(max_length=25)
    abbr=models.CharField(max_length=4)

    def __str__(self):
        return str(self.name)+"("+str(self.abbr)+")"

class City(models.Model):
    name=models.CharField(max_length=35)
    state=models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Location(models.Model):
    name=models.CharField(max_length=50)
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    city=models.ForeignKey(City,on_delete=models.CASCADE)
    address=models.CharField(max_length=80,blank=True,null=True)

    def __str__(self):
        return str(self.name)+" "+str(self.city)+" "+str(self.state)

class ItemType(models.Model):
    name_ch=models.CharField(max_length=20)

    def __str__(self):
        return str(self.name_ch)

class Carpool(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    date = models.DateField()
    time = models.TimeField(default="00:00:00")
    depart_place = models.ForeignKey(Location,on_delete=models.CASCADE,related_name="depart_place")
    destination = models.ForeignKey(Location,on_delete=models.CASCADE,related_name="destination")
    passenger_num = models.IntegerField()
    price = models.FloatField()
    car_type = models.CharField(max_length=20,default="sedan")
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        d= {'couple': '双门轿车',
            'sedan': '四门轿车',
            'suv': '五座SUV',
            '7suv': '七座SUV',
            'truck': '皮卡或其他',
        }
        return "%s %s, 从 %s 到 %s, 车型为 %s" % (self.date, str(self.time)[:-3], self.depart_place.name,
                                             self.destination.name, d[self.car_type])

class UsedCar(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    year = models.IntegerField()
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    mileage = models.IntegerField()
    price = models.IntegerField()
    note = models.TextField(null=True)

    def __str__(self):
        return "%d %s %s %d迈" % (self.year, self.car_brand.name, self.car_model.name, self.mileage)

class UsedItem(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    item_type = models.ForeignKey(ItemType,on_delete=models.CASCADE)
    item_name = models.CharField(max_length=20,default='monitor')
    condition = models.CharField(max_length=20)
    price = models.IntegerField()
    note = models.TextField(null=True)

    def __str__(self):
        return str(self.item_name)+' '+str(self.condition)

class Sublease(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    community = models.ForeignKey(Location,max_length=50,on_delete=models.CASCADE)
    bedroom_num=models.IntegerField(default=1)
    bathroom_num=models.IntegerField(default=1)
    rent = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    renewal = models.BooleanField(default=True)
    note = models.TextField(null=True)

    def __str__(self):
        return "%s 从 %s 到 %s %db%db" % (str(self.community.name), self.start_date, self.end_date, self.bedroom_num, self.bathroom_num)

class HouseRent(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    community = models.ForeignKey(Location,max_length=50,on_delete=models.CASCADE)
    bedroom_num=models.IntegerField(default=1)
    bathroom_num=models.IntegerField(default=1)
    rent = models.FloatField()
    start_date = models.DateField()
    duration = models.CharField(max_length=20,default='6 months')
    roommate_gender = models.CharField(max_length=6)
    roommate_num = models.IntegerField()
    note = models.TextField(null=True)

    def __str__(self):
        return '%s 从 %s 开始 租期 %s %db%db %s' % (self.community.name, self.start_date, self.duration, self.bedroom_num,
                                               self.bathroom_num, self.roommate_gender)

class MergeOrder(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    website = models.URLField(max_length=100,default='www.google.com')
    order_type = models.ForeignKey(ItemType,on_delete=models.CASCADE)
    duedate = models.DateField(default='2017-12-31')
    note = models.TextField(null=True)

    def __str__(self):
        return "活动网址为 %s, 截止于 %s" % (str(self.website), self.duedate)

class Image(models.Model):
    image = models.ImageField(upload_to=upload_to_path, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    deal = models.ForeignKey(Deal,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return str(self.image)




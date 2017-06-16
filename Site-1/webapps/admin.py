from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from webapps.models import UserPro
from .models import Deal, Carpool, UsedItem, UsedCar, HouseRent, Sublease, MergeOrder, Image, CarBrand, CarModel


class UserProInline(admin.StackedInline):
    model = UserPro
    can_delete = False
    verbose_name_plural = 'UserPro'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProInline, )

# Register your models here.
admin.site.register(Deal)
admin.site.register(Carpool)
admin.site.register(UsedItem)
admin.site.register(UsedCar)
admin.site.register(HouseRent)
admin.site.register(Sublease)
admin.site.register(MergeOrder)
admin.site.register(Image)
admin.site.register(CarBrand)
admin.site.register(CarModel)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

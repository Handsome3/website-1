from django import forms

class UsedCarForm(forms.Form):
    year = forms.IntegerField()
    car_brand = forms.CharField(max_length=30)
    car_model = forms.CharField(max_length=30)
    mileage = forms.IntegerField()
    price = forms.IntegerField()
    contact_type = forms.CharField(max_length=16,initial='wechat')
    state = forms.CharField(max_length=30,initial='florida')
    city = forms.CharField(max_length = 30,initial='gainesville')
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    note = forms.CharField(required=False)


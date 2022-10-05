from django import forms
from .models import *


class couponForm(forms.ModelForm):
    
    class Meta:
        model = coupon
        fields = '__all__'
      
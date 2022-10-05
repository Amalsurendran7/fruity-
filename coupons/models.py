from django.db import models
from pro.models import *

# Create your models here.

class coupon(models.Model):

    code=models.CharField(max_length=30,unique=True)
    valid_from=models.DateField(null=True)
    valid_to=models.DateField(null=True)
    discount=models.IntegerField(null=True)
    user=models.ForeignKey(customer,on_delete=models.CASCADE,null=True)
    minimum_amount=models.IntegerField(null=True)

class productoffer(models.Model):
    productname=models.CharField(max_length=30)
    valid_from=models.DateField(null=True) 
    valid_to=models.DateField(null=True)
    percentage=models.IntegerField(null=True)
    product=models.ForeignKey(produc,on_delete=models.CASCADE)
    user=models.ForeignKey(customer,on_delete=models.CASCADE,null=True)
    is_active=models.BooleanField(default=False)


class categoryoffer(models.Model):
    categoryname=models.CharField(max_length=30)
    valid_from=models.DateField(null=True) 
    valid_to=models.DateField(null=True)
    percentage=models.IntegerField(null=True)
  
    user=models.ForeignKey(customer,on_delete=models.CASCADE,null=True)
    is_active=models.BooleanField(default=False)    
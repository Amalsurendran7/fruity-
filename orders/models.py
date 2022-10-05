from django.db import models

# Create your models here.


from pro.models import *




class Payment(models.Model):
    user = models.ForeignKey(customer, on_delete=models.CASCADE,null=True)
   
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    payment_signature=models.CharField(max_length=100,null=True,blank=True)
    payment_method = models.CharField(max_length=100,null=True)
    amount_paid = models.FloatField(max_length=100,null=True) # this is the total amount paid
    status = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    razor_order_id=models.CharField(max_length=100,null=True)
    razor_pay_id=models.CharField(max_length=100,null=True)
    razor_pay_signature=models.CharField(max_length=100,null=True)





class Order(models.Model):
    STATUS = (
        ('confirmed', 'confrimed'),
        ('shipped', 'shipped'),
        ('out of delivery', 'out of delivery'),
        ('delivered', 'delivered'),
    )
    
    user = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=100,default=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    
    status = models.CharField(max_length=100, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'


        


class OrderProduct(models.Model):
    STATUS = (
        ('confirmed', 'confrimed'),
        ('shipped', 'shipped'),
        ('out of delivery', 'out of delivery'),
        ('delivered', 'delivered'),
    )
 
    status = models.CharField(max_length=100, choices=STATUS, default='New')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    returned=models.CharField(max_length=100,default="False")
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(customer, on_delete=models.CASCADE)
    product = models.ForeignKey(produc, on_delete=models.CASCADE)

    
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


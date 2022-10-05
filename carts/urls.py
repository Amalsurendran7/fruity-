
from django.urls import path,include
from .views import *

urlpatterns = [

    path('cartpage/',cart,name='cart'),
    
    path('addcart/<int:product_id>',add_cart,name='addcart'),
    path('removecart/<int:product_id>/<int:cart_item_id>/',removecart,name='removecart'),
    path('minus/<int:product_id>/<int:cart_item_id>/',minus,name='minus'),
    path('plus/<int:product_id>/<int:cart_item_id>/',plus,name='plus'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',remove_cart_item,name='remove_cart_item'),
    
    path('checkout/',checkout,name='checkout'),
    
        
    



]
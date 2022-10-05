from django.urls import path,include
from .views import *


urlpatterns = [

    path('addcoupon/',addcoupon,name='addcoupon'),
    path('applycoupon/',applycoupon,name='applycoupon'),
    path('offer/',off,name='offer'),
    path('productoffer/',productoffers,name='productoffers'),
        path('categoryoffer/',coffer,name='coffer'),
                path('delpoffer/<int:id>',delpoffer,name='delpoffer'),
                path('delcoffer/<int:id>',delcoffer,name='delcoffer'),
                 path('couponpage',couponpage,name='couponpage'),
    
    
    



]
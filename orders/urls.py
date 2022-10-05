from django.urls import path,include
from .import views


urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
      path('payments', views.payments, name='payments'),
       path('chart', views.chart, name='chart'),
           path('success', views.success, name='success'),
               path('sales', views.sales, name='salesreport'),
               path('apply',views.applywallet,name='applywalet'),
                path('rsuccess',views.rsuccess,name='rsuccess'), 
              

     
    
    

]

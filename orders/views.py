from django.shortcuts import render,redirect
from carts.models import *

from pro.forms import *
from .forms import *
from .models import *
from pro.models import *
import datetime
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
import json
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from coupons.models import *
from django.http import HttpResponseRedirect
from django.views.decorators.csrf  import csrf_exempt
# import JsonResponse


def sales(request):
    o=Order.objects.filter(is_ordered=True)
    
    for i in o:
      print(i)  
      l=OrderProduct.objects.get(order=i)
    context={'sales':l}

    return render(request,"store/sales.html",context)



def payments(request):

    print('payment')
    body=json.loads(request.body)
    

    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    print(body)
    
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
    
        amount_paid = order.order_total,
        status = body['status'],
        
    )
    payment.save()
    


    amount=request.session.get('am')
    
    
   
    # Store transaction details inside Payment model
    
    
    kp=payment.payment_id
    print(kp)

    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items:
        product = produc.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save() 

     
    CartItem.objects.filter(user=request.user).delete()    

    


    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

    

def success(request):
    return render(request,"store/success.html")

@csrf_exempt
def rsuccess(request):
            ay=Payment()
            order = Order.objects.get(user=request.user, is_ordered=False, order_number=request.session.get('o'))
    
            ay.amount_paid=request.session.get('ji')
            ay.user=request.user
            ay.status='COMPLETED'
            ay.save()
            order.payment = ay
            order.is_ordered = True
            order.save()

            cart_items=CartItem.objects.filter(user=request.user)
            for item in cart_items:
               product = produc.objects.get(id=item.product_id)
               product.stock -= item.quantity
               product.save() 

     
            CartItem.objects.filter(user=request.user).delete()    

          
            return render(request,"store/rsuccess.html")
    


    
# Create your views here.

def applywallet(request):
     if request.method == "POST":
            print("wallet")
            amount=request.POST.get('money')
            wi=Wallet.objects.get(user_e=request.user)

            print("amunt red",amount)
            if amount:
               print("amount",amount)
               if wi.w_amount >=int(amount):
                   request.session['am']=amount
                   return redirect('place_order')
                
               else:
                  print("no wallet")
                  request.session['am']=0
                  messages.info(request,"not enough wallet balance")
                  return  redirect('place_order')

       

def place_order(request, total=0, quantity=0,):
    current_user = request.user
    wallet=Wallet.objects.get(user_e=request.user)

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('uhome')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        
               total += (cart_item.product.price * cart_item.quantity)
               quantity += cart_item.quantity
              


    tax = (2 * total)/100
    if 'co_id'  in request.session:
            print('working')
            print('coupon id',request.session.get('co_id'))
            co=coupon.objects.get(id=request.session.get('co_id'))
            print('minimum',co.minimum_amount)
            if co.minimum_amount >total:
                print('minimum vslur required')
                grand_total = total+ tax

                messages.info(request,"minimum value required")
            else:
                print("else")
                print(co.discount)
                
                grand = total+ tax
                discount=co.discount
                grand_total=grand-discount
                user=customer.objects.get(email=request.user)
                k=coupon.objects.get(id=request.session.get('co_id'))
                k.user=user
                k.save()
                del request.session['co_id']
      

    elif 'am' in request.session:
        grand_total=total+tax
        amount=request.session.get('am')
        grand_total -= float(amount)
        wi=Wallet.objects.get(user_e=request.user)  
        wi.w_amount -=int(amount )
        wi.save() 

    else:
        print("normal")
        grand_total=total+tax

     

    dollar=int(grand_total/78)

    if dollar < 0:
        k=1
    else:
        k=dollar    

    if request.method == 'POST':
        print("hlooo working")
        form = OrderForm(request.POST)
        if form.is_valid():

            print("inside valid")
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
       
            
            data.address_line_2 = form.cleaned_data['address_line_2']
            
            data.payment_method=form.cleaned_data['payment_method']
        
            
            
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            print(data.payment_method)
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            request.session['o']=order_number
            
            
            data.save()
            
           

            
            cart_items = CartItem.objects.filter(user=request.user)
            order = Order.objects.get(user=request.user, is_ordered=False, order_number=data.order_number)
            
        

            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
                
                orderproduct.user_id = request.user.id
                orderproduct.product_id= item.product_id
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.price
                orderproduct.ordered = True
                orderproduct.save()
           
                if data.payment_method == "cod":

                    product = produc.objects.get(id=item.product_id)
                    product.stock -= item.quantity
                    product.save()  

            if data.payment_method == "cod":
                CartItem.objects.filter(user=request.user).delete()

   

            # razorpay
            client = razorpay.Client(auth=("rzp_test_yVjd4tSs6Vs4T1", "euLpnyMJQeTbyanQFHNdIdpO"))
            paymen=client.order.create({'amount':grand_total*100,'currency':'INR','payment_capture':1})
            request.session['ji']=grand_total
            

        
            

         

              
      

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'payment':paymen,
                'wallet':wallet,
              
                'dollar':k
                

        
                
            }
    
            return render(request,'store/payment.html',context)
    else:
            

           return redirect("checkout")


              

               

                
     

         



def chart(request):
    labels=[]
    data=[]
    pay=Payment.objects.all()
    for p in pay:
        labels.append(p.user.fname)
        data.append(p.amount_paid)
    context={'labels':labels,'data':data}
    return render(request,"store/chart.html",context)     

        
              
           
                
                



            
            
            
    
            



# def order_complete(request):
#     order_number = request.GET.get('order_number')
#     transID = request.GET.get('payment_id')

#     try:
#         order = Order.objects.get(order_number=order_number, is_ordered=True)
#         ordered_products = OrderProduct.objects.filter(order_id=order.id)

#         subtotal = 0
#         for i in ordered_products:
#             subtotal += i.product_price * i.quantity

#         payment = Payment.objects.get(payment_id=transID)

#         context = {
#             'order': order,
#             'ordered_products': ordered_products,
#             'order_number': order.order_number,
#             'transID': payment.payment_id,
#             'payment': payment,
#             'subtotal': subtotal,
#         }
#         return render(request, 'orders/order_complete.html', context)
#     except (Payment.DoesNotExist, Order.DoesNotExist):
#         return redirect('home')        

        


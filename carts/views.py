from http.client import HTTPResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required

from coupons.models import *
from .models import *
from pro.models import *
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here
# 
# .


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    #get the product
    # If the user is authenticated
    
    product= produc.objects.get(id=product_id)
    if request.user.is_authenticated:
        try:
            cart= Cart.objects.get(cart_id =_cart_id(request))
        except:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
            cart.save()
        try:
            cart_item = CartItem.objects.get(product=product,cart=cart,user=request.user)
            cart_item.quantity += 1 #pressing first time cart button
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=request.user,
                cart=cart,
            )
            cart_item.save()       
    else:
    
        try:    
                print('t')
                cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
                print('l')
                cart = Cart.objects.create(
                    cart_id = _cart_id(request)
                )
        cart.save()

        try: 
            print('s')
            cart_item=CartItem.objects.get(product=product,cart=cart)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:
            print('y')
            cart_item=CartItem.objects.create(product=product,quantity=1,cart=cart,)
            cart_item.save()

        
    return redirect('cart')     






       

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        
        if request.user.is_authenticated:
            
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
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
                print(grand_total)

                messages.error(request,"minimum value required")
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
                


        else:
            print('not working')
            
            grand_total = total+ tax

        
        
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
        
    }
    return render(request, 'store/cart.html', context)





def removecart(request, product_id, cart_item_id):

    product = get_object_or_404(produc, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')




def minus(request, product_id, cart_item_id):

    product = get_object_or_404(produc, id=product_id)
    
    if request.user.is_authenticated:
            print('helloo')
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    if cart_item.quantity > 1:
            print('decrement')

            cart_item.quantity -= 1
            cart_item.save()
            print(cart_item.quantity)
            return HttpResponse(cart_item.quantity)
    

    return HttpResponse(1)        

       

def plus(request, product_id, cart_item_id):

    product = get_object_or_404(produc, id=product_id)
    
    if request.user.is_authenticated:
            print('hellooyy')
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    if cart_item.quantity < 10 :
            print('increment')

            cart_item.quantity += 1
            cart_item.save()
            print(cart_item.quantity)
            return HttpResponse(cart_item.quantity)


    return HttpResponse(1)        

       
      
    

     
   






def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(produc, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()

    return redirect('cart')


    

def remove(request, product_id, cart_item_id):
    product = get_object_or_404(produc, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return render

        




@login_required(login_url='ulog')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
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
                


        else:
            print('not working')
            
            grand_total = total+ tax

            
        a=Address.objects.filter(useradd=request.user)
        
                
       
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
        'address':a,
        
        
        
        
    }
    return render(request, 'store/checkout.html', context)
   


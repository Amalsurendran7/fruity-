
from django.shortcuts import render,redirect
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from carts.models import *
from .models import *
from pro.forms import *
import datetime
import sweetify

# Create your views here.



 # Create

def off(request):
    p=produc.objects.all()
      
    c=productoffer.objects.all()
    d=categoryoffer.objects.all()
    context={'product':p,"poffer":c,"coffer":d}
    

    return render(request,"store/offer.html",context)

def productoffers(request):

    if request.method=='POST':

        productnam=request.POST.get('offer')
        print(productnam)
        
        first=request.POST.get('start')
        last=request.POST.get('end')
        
        percentage=request.POST.get('per')
        product=produc.objects.get(name=productnam)
        print(product.price)
        
        if productoffer.objects.filter(productname=productnam):
            messages.error(request,'This product already has an offer')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            if int(percentage) <=70:
                if first == datetime.datetime.now().strftime ("%Y-%m-%d") and last >datetime.datetime.now().strftime ("%Y-%m-%d") and product.p_offer is not True :  
                
                    c=productoffer(productname=productnam,valid_from=first,valid_to=last,percentage=percentage,product=product,is_active=True)
                    c.save()
                    request.session['prooffer']=c.id

                else:
                    if first < datetime.datetime.now().strftime ("%Y-%m-%d") or first > datetime.datetime.now().strftime ("%Y-%m-%d"):
                        sweetify.warning(request,"date must start from today")
                        messages.info(request,"offer date must start from today")

                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                    elif last <= datetime.datetime.now().strftime ("%Y-%m-%d"):
                        messages.info(request,"offer end date must be set greater than  today")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    elif product.p_offer is True:
                        messages.info(request,"This product already has an offer")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            else:
                  print("lower the offer percentage") 
                  messages.info(request,"lower the offer percentage")
                  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))            


        check=productoffer.objects.filter(productname=productnam,valid_from__lte=datetime.datetime.now().strftime ("%Y-%m-%d"),valid_to__gte=datetime.datetime.now().strftime ("%Y-%m-%d"),is_active=True)
        if check:

                for i in check:

                     if i.product.c_offer is True:
                            ca=category.objects.get(id=i.product.cate_id.id)
                            print(i.product.cate_id.id)
                            print(ca.category_name)
                            cr=categoryoffer.objects.get(categoryname=ca.category_name)
                            if cr.percentage > i.percentage:
                                print("category offer already applied to the product")
                                messages.info(request,"category offer already applied to the product")
                            else:
                                
                                print(i.product.offer)
                                print(i.product.price)
                                print('tutu')
                            
                        
                                product.offer= i.product.offer
                            
                                product.price -=  int(i.product.offer )* int(( i.percentage/100))
                                product.p_offer=True
                                product.o_percentage=i.percentage
                                product.save()
                                print('success')  

                     else:
                     
                            print(i.product.offer)
                            print(i.product.price)
                            print('tu')
                    
                            product.offer= product.price
                            product.price -= product.price * ( i.percentage/100)
                            product.p_offer=True
                            product.o_percentage=i.percentage
                            product.save()
                            print('success')  

        else:
            print("else")
            messages.info(request,"offer expired")
            product.offer = "None"
            product.p_offer=False
            product.o_percentage=0
            
            product.save()
            for j in check:
        
                j.is_active=False
                j.save()   
        
        return redirect('offer')

def coffer(request):

    if request.method=='POST':

        categoryname=request.POST.get('coffer')
        
        first=request.POST.get('start')
        last=request.POST.get('end')
        
        percentage=request.POST.get('per')
 
        if categoryoffer.objects.filter(categoryname=categoryname):
            messages.error(request,'already exits')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            if int(percentage) <=70: 
               
                if first == datetime.datetime.now().strftime ("%Y-%m-%d") and last >datetime.datetime.now().strftime ("%Y-%m-%d") :  
                        d=categoryoffer(categoryname=categoryname,valid_from=first,valid_to=last,percentage=percentage,is_active=True)
                        d.save()
                        print('added')
                        messages.info(request,"category offer added")
                        request.session['c_offer']=d.id

                else:
                        if first < datetime.datetime.now().strftime ("%Y-%m-%d") or first > datetime.datetime.now().strftime ("%Y-%m-%d"):
                            messages.info(request,"coupon date must start from today")
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                        elif last <= datetime.datetime.now().strftime ("%Y-%m-%d"):
                            messages.info(request,"coupon end date must be set greater than  today")
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                
                    print("lower the offer percentage") 
                    messages.info(request,"lower the offer percentage")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))              

        check=categoryoffer.objects.filter(categoryname=categoryname,valid_from__lte=datetime.datetime.now().strftime ("%Y-%m-%d"),valid_to__gte=datetime.datetime.now().strftime ("%Y-%m-%d"),percentage=percentage,is_active=True)
        c=category.objects.get(category_name=categoryname)
        p=produc.objects.filter(cate_id=c.id)
        
        if  check:
            
                for i in p:

                    if i.p_offer is True:
                        print(i.p_offer)
                        prod=productoffer.objects.get(productname=i.name)
                        if int(prod.percentage) > int(d.percentage):
                            print("p_offer percentage is bigger") 
                            pass
                        else:
                            i.offer=i.price*(100/prod.percentage)
                            i.save()
                            print("has product offeer")
                            print('total price',i.offer)
                            print(d.percentage)
                            print("type",type(d.percentage))
                            kp=int(d.percentage)
                            print('kp',kp)
                            i.c_offer=True
                            i.o_percentage=kp
                    
                            print("target",prod.product.offer)
                            print(type(prod.product.offer))
                            offer= (i.price*(100/prod.percentage))-((i.price*(100/prod.percentage))*(kp/100))
                         

                            i.price =offer
                            i.save()
                            print('price after offer',i.price)

                    else:

                        i.offer=i.price
                        i.save()
                        print("no offers")
                        print('total price',i.offer)
                        print(d.percentage)
                        print("type",type(d.percentage))
                        kp=int(d.percentage)
                        print('kp',kp)
                        i.c_offer=True
                        i.o_percentage=kp
                    
                        offer=i.price-(i.price*(kp/100))
                        i.price =offer
                        i.save()
                        print('price after offer',i.price)

        else:
            print('else')
            for y in check:
                y.is_active=False
                y.save()
            for i in p:
                i.offer= "None"
                i.save()
                i.c_offer=False
                i.o_percentage=0

        return redirect('offer')        


def delpoffer(request,id):
    c=productoffer.objects.get(id=id)
    name=c.productname
    p=produc.objects.get(name=name)
    p.p_offer=False
    p.o_percentage=0
    p.price=p.offer
    p.offer="None"
    p.save()

    c.delete()
 
    
    
       
        

    
   
    return redirect('offer')

def delcoffer(request,id):
    c=categoryoffer.objects.filter(id=id)
    for i in c:
      name=i.categoryname
      j=category.objects.get(category_name=name)
      p=produc.objects.filter(cate_id=j.id)
      for k in p:
        k.c_offer=False
        k.o_percentage=0
        k.save()
        if k.offer !="None":
           k.price=k.offer
           k.offer ="None"
           k.save()
           
       
      
      
    c.delete()
    

    return redirect('offer')  

def couponpage(request):
    c=coupon.objects.all()
    context={'coupons':c}
    return render(request,"store/couponpage.html",context)      

def addcoupon(request):
    
    if request.method=='POST':

        code=request.POST.get('code')
        
        first=request.POST.get('start')
        last=request.POST.get('end')
        
        discount=request.POST.get('discount')
        
        min=request.POST.get('min')

        if coupon.objects.filter(code=code) :
            messages.error(request,'already exits')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else: 
            if first == datetime.datetime.now().strftime ("%Y-%m-%d") and last >datetime.datetime.now().strftime ("%Y-%m-%d"):  

                c=coupon(code=code,valid_from=first,valid_to=last,discount=discount,minimum_amount=min)
                c.save()
                return redirect('couponpage') 

            else:
                if first < datetime.datetime.now().strftime ("%Y-%m-%d") or first > datetime.datetime.now().strftime ("%Y-%m-%d"):
                    messages.info(request,"coupon date must start from today")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                elif last <= datetime.datetime.now().strftime ("%Y-%m-%d"):
                      messages.info(request,"coupon end date must be set greater than  today")
                      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                     

import datetime
def applycoupon(request):

    if request.method =='POST':
        print('post')
        cupon=request.POST.get('coupon')
        print(cupon)
        user=customer.objects.get(email=request.user)

        s=coupon.objects.filter(user=user,code=cupon)
        print(s)
        i=coupon()
        
        c=coupon.objects.filter(code=cupon,valid_to__gte=datetime.datetime.now().strftime ("%Y-%m-%d"))
        print(c)
        if s:

            print('already used')
            messages.error(request,'already used')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif c :
             for i in c:
                request.session['co_id']=i.id
               
                return redirect('cart')
         
        else:
            t=coupon.objects.filter(valid_from__lte=datetime.datetime.now().strftime ("%Y-%m-%d"),valid_to__gte=datetime.datetime.now().strftime ("%Y-%m-%d"))

            if t:
                messages.error(request,'invalid coupon')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  

            else:
                messages.error(request,'coupon period expired')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))          

    else:   
        print('not post')      

        return render(request,"store/coupon.html")






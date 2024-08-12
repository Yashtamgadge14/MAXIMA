from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from maximaapp.models import product
from maximaapp.models import Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return HttpResponse('this is home page')
def index(request):
   context={}
   p=product.objects.filter(is_active=True)
   print(p)
   context['products']=p

   return render(request,'index.html',context)
def user_logout(request):
    logout(request)
    return redirect('/index')
def user_login(request):
    context={}
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pass']
        print(u)
        print(p)
        if u==""or p=="":
            context["errmsg"]="feild cannot be empty"
            return render(request,"login.html",context)
        else:
            a=authenticate(username=u,password=p)
            if a is not None:
                login(request,a)
                return redirect('/index')
            else:
                context['errmsg']='user not match'
                return render(request,'login.html',context)
        return HttpResponse('data fetched')
    else:
      return render(request,'login.html')
def register(request):
    context={}
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pass']
        cp=request.POST['cpass']
        print(u)
        print(p)
        print(cp)
        if u==""or p==""or cp=="":
            context['errmsg']="feilds cannot be empty"
            return render(request,'register.html',context)
        elif p!=cp:
            context['errmsg']="password does not match"
            return render(request,'register.html',context)
        else:
            try:
             u=User.objects.create(password=p,username=u,email=u)
             u.set_password(p)
             u.save()
             context['success']="user created successfully"
             return render(request,'register.html',context)
            except Exception:
                context['errmsg']='same user name already exist'
                return render(request,'register.html',context)

        
    return render(request,'register.html')
def po(request):
      userid=request.user.id
      c=Cart.objects.filter(uid=userid)
      oid=random.randrange(1000,9999)
      for x in c:
          o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
          o.save()
          x.delete()
      orders=Order.objects.filter(uid=request.user.id)
      
      s=0
      q=0
      for x in orders:
       print('qty:',x.qty)
       q=q+x.qty
    
    

      for x in orders:
        print(x.pid.price)
        s=s+x.pid.price*x.qty
      context={}
      context['total']=s
      context['products']=orders
      context['np']=q
      return render(request,'place_order.html',context)
def product_details(request,pid):
    context={}
    p=product.objects.filter(id=pid)
    context['products']=p
    return render(request,'product_detail.html',context)
def cart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    n=len(c)
    s=0
    q=0
    for x in c:
       print('qty:',x.qty)
       q=q+x.qty
    
    

    for x in c:
        print(x.pid.price)
        s=s+x.pid.price*x.qty
    context={}
    context['total']=s
    context['products']=c
    context['np']=q
    
    return render(request,'cart.html',context)
def catfilter(request,cv):
    context={}
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1 & q2)
    context['products']=p
    return render(request,'index.html',context)
def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    p=product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)
def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1&q2&q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)
def addtocart(request,pid):
     if request.user.is_authenticated:
         u=User.objects.filter(id=request.user.id)
         print(u)
         p=product.objects.filter(id=pid)
         print(p)
         q1=Q(uid=u[0])
         q2=Q(pid=p[0])
         c=Cart.objects.filter(q1&q2)
         print(c)
         n=len(c)
         context={}
         context['products']=p
         if n==1:
             context['msg']='product already exist in cart!!'
             return render(request,'product_detail.html',context)
         else:
             c=Cart.objects.create(uid=u[0],pid=p[0])
             c.save()
             context['success']='product added successfully!!'
             return render(request,'product_detail.html',context)
     else:
         return redirect('/login')
     
def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')
def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    
    return redirect('/cart')
def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        #print(x.pid.price)
        s=s+x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_JM0SkW0nxa2Y3H", "1mzaSsWVkahmQaOWh56rllFF"))
    data = { "amount": s*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    return render(request,'pay.html',context)
def sendusermail(request):
    uemail=request.user.email
    send_mail(
    "MAXIMA-Order Placed successfully",
    "Here is the message.",
    "yashtamgadge14@gmail.com",
    [uemail],
    fail_silently=False,
    
)
    return HttpResponse("mail")
    
    






       

        
          
        
      
    
    
   




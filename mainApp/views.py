from django import http
from django.conf import settings
from django.contrib.messages.api import error
from django.db.models.lookups import IContains
from django.http.response import Http404
from django.shortcuts import redirect, render,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from Fashi.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
import razorpay


from random import randint
count=0
from mainApp.models import *
def home(request):
    if(request.method=="POST"):
        s = Subscribe()
        s.email= request.POST.get("email")
        s.save()
        subject = 'Thanks to Subscribe'
        message = "Thanks {}!!!!\nIt mean a lot to us\nNow you can get email when anew product is uploaded in our site\nVisite http://localhost:8000".format(s.email)
        recipient_list = [s.email, ]
        send_mail( subject, message, "karmaproject@gmail.com", recipient_list)

        return HttpResponseRedirect('/')
    global count
    cart = request.session.get('cart',None)
    if(cart):
        count=len(cart)
    return render(request,"index.html",{"Count":count})

def search(request):
    mainCat = MainCat.objects.all()
    subCat = SubCat.objects.all()
    brand = Brand.objects.all()
    product  = []
    if(request.method=="POST"): 
        search = request.POST.get('search')
        product = Product.objects.filter(Q(name__icontains=search)|Q(description__icontains=search))
    return render(request,"shop.html",{
                                "mainCat":mainCat,
                                "subCat":subCat,
                                "Brand":brand,
                                "Product":product,
                                "MC":'d',
                                "BR":'d',
                                "SC":'d',
                                "Count":count
    })

client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
@login_required(login_url='/login/')
def checkoutPage(request):
    buyer = Buyer.objects.get(username=request.user)
    cart = request.session.get("cart",None)
    product = []
    total = 0
    shipping = 0
    final = 0
    if(cart):
        for i in cart.keys():
            p = Product.objects.get(pid=int(i))
            product.append(p)
            total = total+int(cart[i])*p.finalPrice
        if(total<1000):
            shipping=150
        final = total+shipping
    if(request.method=="POST"):
        cart = request.session.get("cart",None)
        ch = Checkout()
        ch.buyer = buyer
        ch.total = total
        ch.shipping=shipping
        ch.final=final
        ch.product=""
        for i in cart.keys():
            p = Product.objects.get(pid=int(i))
            ch.product=ch.product+str(p)+"="+str(cart[i])+"\n"
        if(request.POST.get('mode')=='cod'):
            ch.mode="COD"
            ch.save()
            subject = "Your Order is placed Successfully"
            body =  """
                        Hello!!!!
                        Thank to for Shopping with US
                        Team:   Fashi
                        http://localhost:8000
                        """
            send_mail(subject, body,"karmadjango@gmail.com",[buyer.email,], fail_silently=False)
            return HttpResponseRedirect("/confirmation/")
        else:
            orderAmount = ch.final*100
            orderCurrency = "INR"
            paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
            paymentId = paymentOrder['id']
            ch.order_id=paymentId
            ch.mode="online"
            ch.save()
            return render(request,"pay.html",{
                "amount":orderAmount,
                "api_key":RAZORPAY_API_KEY,
                "order_id":paymentId,
                "User":buyer
            })
    return render(request,"check-out.html",{"Count":count,
                                            "User":buyer,
                                            "Product":product,
                                            "Total":total,
                                            "Shipping":shipping,
                                            "Final":final
                                            })

@login_required(login_url='/login/')
def paymentSuccesss(request,rppid,rpoid,rpsid):
    buyer = Buyer.objects.get(username=request.user)
    check = Checkout.objects.filter(buyer=buyer)
    check=check[::-1]
    check=check[0]
    check.razorpay_payment_id=rppid
    check.razorpay_order_id=rpoid
    check.razorpay_signature=rpsid
    check.payment_status=1
    check.save()
    subject = "Your Order is placed Successfully"
    body =  """
                Hello!!!!
                Thank to for Shopping with US
                Team:   Fashi
                http://localhost:8000
                """
    send_mail(subject, body,"karmadjango@gmail.com",[buyer.email,], fail_silently=False)
    return HttpResponseRedirect('/confirmation/')
def contactPage(request):
    if(request.method=="POST"):
        c = ContactUs()
        c.name = request.POST.get("name")
        c.email = request.POST.get("email")
        c.subject = request.POST.get("subject")
        c.message = request.POST.get("message")
        c.save()
        return HttpResponseRedirect("/")
    return render(request,"contact.html",{"Count":count})

def fagPage(request):
    return render(request,"faq.html",{"Count":count})

def productPage(request,num):
    global count
    product = Product.objects.get(pid=num)
    if(request.method=="POST"):
        q = int(request.POST.get('q'))
        cart = request.session.get('cart',None)
        if(cart):
            keys = cart.keys()
            if(str(product.pid) in keys):
                cart[str(product.pid)]=cart[str(product.pid)]+q
            else:
                count=count+1
                cart.setdefault(str(product.pid),q)
        else:
            cart = {str(product.pid):q}
            count=count+1
        request.session['flush']=False
        request.session['cart']=cart
        return HttpResponseRedirect('/cart/')
    return render(request,"product.html",{"Product":product,
                                            "Count":count})

def registerPage(request):
    if(request.method=="POST"):
        if(request.POST.get('actype')=="seller"):
            s = Seller()
            s.name = request.POST.get('name')
            s.username = request.POST.get('username')
            s.email = request.POST.get('email')
            s.phone = request.POST.get('phone')
            s.pic = request.FILES.get('pic')
            pward = request.POST.get('password')
            cpward = request.POST.get('cpassword')
            if(pward==cpward):
                try:
                    user = User.objects.create_user(username=s.username,
                                                password=pward,
                                                email=s.email,
                                                first_name=s.name
                                                        )
                    user.save()
                    s.save()
                    return HttpResponseRedirect("/login/")
                except:
                    messages.error(request,"User Name is Already Taken")
            else:
                messages.error(request,"Password and Confirm Password Does not Match")
        else:
            b = Buyer()
            b.name = request.POST.get('name')
            b.username = request.POST.get('username')
            b.email = request.POST.get('email')
            b.phone = request.POST.get('phone')
            b.pic = request.FILES.get('pic')
            pward = request.POST.get('password')
            cpward = request.POST.get('cpassword')
            if(pward==cpward):
                try:
                    user = User.objects.create_user(username=b.username,
                                                password=pward,
                                                email=b.email,
                                                first_name=b.name
                                                        )
                    user.save()
                    b.save()
                    return HttpResponseRedirect("/login/")
                except:
                    messages.error(request,"User Name is Already Taken")
            else:
                messages.error(request,"Password and Confirm Password Does not Match")        
    return render(request,"register.html")

def loginPage(request):
    if(request.method=="POST"):
        username = request.POST.get("username")
        password = request.POST.get("pass")
        user = auth.authenticate(username=username,password=password)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
        else:
            messages.error(request,"Invalid UserName or Password")
    return render(request,"login.html")

@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def profile(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        try:
            seller = Seller.objects.get(username=request.user)
            return HttpResponseRedirect("/sellerProfile/")
        except:
            return HttpResponseRedirect("/buyerProfile/")

@login_required(login_url='/login/')
def sellerProfile(request):
    seller = Seller.objects.get(username=request.user)
    product = Product.objects.filter(seller=seller)
    return render(request,"sellerProfile.html",{'User':seller,
                                                "Product":product
                                                })
@login_required(login_url='/login/')
def buyerProfile(request):
    buyer = Buyer.objects.get(username=request.user)
    wishlist = Wishlist.objects.filter(buyer=buyer)
    return render(request,"buyerProfile.html",{'User':buyer,
                                                'Wishlist':wishlist,
                                                "Count":count
                                                })

@login_required(login_url='/login/')
def editProfileSeller(request):
    s = Seller.objects.get(username=request.user)
    if(request.method=="POST"):
        s.name = request.POST.get('name')
        s.email = request.POST.get('email')
        s.phone = request.POST.get('phone')
        s.addressline1 = request.POST.get('addressline1')
        s.addressline2 = request.POST.get('addressline2')
        s.addressline3 = request.POST.get('addressline3')
        s.pin = request.POST.get('pin')
        s.city = request.POST.get('city')
        s.state = request.POST.get('state')
        if(not request.FILES.get('pic')==None):
            s.pic = request.FILES.get('pic')
        s.save()
        return HttpResponseRedirect('/sellerProfile/')
    return render(request,"editProfile.html",{'User':s})

@login_required(login_url='/login/')
def editProfileBuyer(request):
    b = Buyer.objects.get(username=request.user)
    if(request.method=="POST"):
        b.name = request.POST.get('name')
        b.email = request.POST.get('email')
        b.phone = request.POST.get('phone')
        b.addressline1 = request.POST.get('addressline1')
        b.addressline2 = request.POST.get('addressline2')
        b.addressline3 = request.POST.get('addressline3')
        b.pin = request.POST.get('pin')
        b.city = request.POST.get('city')
        b.state = request.POST.get('state')
        if(not request.FILES.get('pic')==None):
            b.pic = request.FILES.get('pic')
        b.save()
        return HttpResponseRedirect('/buyerProfile/')
    return render(request,"editProfileBuyer.html",{'User':b,
                                                "Count":count})

def shopPage(request,MC,SC,BR):
    mainCat = MainCat.objects.all()
    subCat = SubCat.objects.all()
    brand = Brand.objects.all()
    if(MC=="d" and SC=="d" and BR=="d"):
        product = Product.objects.all()
    elif(MC!="d" and SC=="d" and BR=="d"):
        product = Product.objects.filter(mainCat=MainCat.objects.get(name=MC))
    elif(MC=="d" and SC!="d" and BR=="d"):
        product = Product.objects.filter(subCat=SubCat.objects.get(name=SC))    
    elif(MC=="d" and SC=="d" and BR!="d"):
        product = Product.objects.filter(brand=Brand.objects.get(name=BR))        
    elif(MC!="d" and SC!="d" and BR=="d"):
        product = Product.objects.filter(mainCat=MainCat.objects.get(name=MC),
                                         subCat=SubCat.objects.get(name=SC))
    elif(MC!="d" and SC=="d" and BR!="d"):
        product = Product.objects.filter(mainCat=MainCat.objects.get(name=MC),
                                         brand=Brand.objects.get(name=BR))
    elif(MC=="d" and SC!="d" and BR!="d"):
        product = Product.objects.filter(subCat=SubCat.objects.get(name=SC),
                                         brand=Brand.objects.get(name=BR))
    else:
        product = Product.objects.filter(mainCat=MainCat.objects.get(name=MC),
                                         subCat=SubCat.objects.get(name=SC),
                                         brand=Brand.objects.get(name=BR))
    product=product[::-1]
    return render(request,"shop.html",{
                                "mainCat":mainCat,
                                "subCat":subCat,
                                "Brand":brand,
                                "Product":product,
                                "MC":MC,
                                "BR":BR,
                                "SC":SC,
                                "Count":count
                            })

def cartPage(request):
    if(request.session.get('flush')==True):
        request.session['cart']={}
    cart = request.session.get("cart",None)
    if(request.method=="POST"):
        q = int(request.POST.get('q'))
        if(q>0):
            pid = str(request.POST.get('pid'))
            cart[pid]=q
            request.session['cart']=cart
    cart = request.session.get("cart",None)
    products = []
    subtotal = 0
    total = 0
    shipping = 0
    if(cart and len(cart.keys())>0):
        for i in cart.keys():
            p = Product.objects.get(pid=int(i))
            products.append(p)
            subtotal=subtotal+p.finalPrice*cart[i]
        if(subtotal<1000):
            shipping=150
        total = subtotal+shipping
    return render(request,"shopping-cart.html",
                                 {"Products":products,
                                 "SubTotal":subtotal,
                                 "Shipping":shipping,
                                 "Total":total,
                                 "Count":count})
def confirmation(request):
    cart = request.session.get("cart",None)
    request.session['flush']=True
    products = []
    subtotal = 0
    total = 0
    shipping = 0
    if(cart):
        for i in cart.keys():
            p = Product.objects.get(pid=int(i))
            products.append(p)
            subtotal=subtotal+p.finalPrice*cart[i]
        if(subtotal<1000):
            shipping=150
        total = subtotal+shipping
    return render(request,"confirmation.html",
                                 {"Products":products,
                                 "SubTotal":subtotal,
                                 "Shipping":shipping,
                                 "Total":total,
                                 "Count":count})


def deleteCart(request,pid):
    global count
    cart = request.session.get('cart',None)
    if(cart):
        cart.pop(str(pid))
        request.session['cart']=cart
        count=count-1
        return HttpResponseRedirect("/cart/")
@login_required(login_url='/login/')
def addProduct(request):
    mainCat = MainCat.objects.all()
    subCat = SubCat.objects.all()
    brand = Brand.objects.all()
    if(request.method=="POST"):
        p = Product()
        p.name = request.POST.get("name")
        p.mainCat = MainCat.objects.get(name = request.POST.get("maincat"))
        p.subCat = SubCat.objects.get(name = request.POST.get("subcat"))
        p.brand = Brand.objects.get(name = request.POST.get("brand"))
        p.seller = Seller.objects.get(username=request.user)
        p.basePrice = int(request.POST.get("baseprice"))
        p.discount = int(request.POST.get("discount"))
        p.finalPrice = p.basePrice-p.basePrice*p.discount/100
        p.color = request.POST.get("color")
        p.size = request.POST.get("size")
        p.stock = bool(request.POST.get("stock"))
        p.description = request.POST.get("description")
        p.specification = request.POST.get("specification")
        p.pic1 = request.FILES.get("pic1")
        p.pic2 = request.FILES.get("pic2")
        p.pic2 = request.FILES.get("pic2")
        p.pic3 = request.FILES.get("pic3")
        p.pic4 = request.FILES.get("pic4")
        p.save()
        
        subject = 'New Product Uploaded on Fashi!!!Chechout Now!!!'
        message = """
                    Hello User!!!
                    Welcom To Fashi!!!!
                    Cheout our Latest products!!!!!
                    http://localhost:8000/product/{}/
                  """.format(p.pid)
        emails = Subscribe.objects.all()
        for i in emails:
            recipient_list = [i.email,]
            send_mail( subject, message, "karmaproject@gmail.com", recipient_list)
        return HttpResponseRedirect("/sellerProfile/")
    return render(request,"addProduct.html",{
                                    "MC":mainCat,
                                    "SC":subCat,
                                    "BR":brand
                                    })

@login_required(login_url='/login/')
def editProduct(request,num):
    mainCat = MainCat.objects.all()
    subCat = SubCat.objects.all()
    brand = Brand.objects.all()
    p = Product.objects.get(pid=num)
    if(request.method=="POST"):
        p.name = request.POST.get("name")
        p.mainCat = MainCat.objects.get(name = request.POST.get("maincat"))
        p.subCat = SubCat.objects.get(name = request.POST.get("subcat"))
        p.brand = Brand.objects.get(name = request.POST.get("brand"))
        p.seller = Seller.objects.get(username=request.user)
        p.basePrice = int(request.POST.get("baseprice"))
        p.discount = int(request.POST.get("discount"))
        p.finalPrice = p.basePrice-p.basePrice*p.discount/100
        p.color = request.POST.get("color")
        p.size = request.POST.get("size")
        p.stock = bool(request.POST.get("stock"))
        p.description = request.POST.get("description")
        p.specification = request.POST.get("specification")
        if(not request.FILES.get("pic1")==None):
            p.pic1 = request.FILES.get("pic1")
        if(not request.FILES.get("pic2")==None):
            p.pic2 = request.FILES.get("pic2")
        if(not request.FILES.get("pic3")==None):    
            p.pic3 = request.FILES.get("pic3")
        if(not request.FILES.get("pic4")==None):
           p.pic4 = request.FILES.get("pic4")
        p.save()
        return HttpResponseRedirect("/sellerProfile/")
    return render(request,"editProduct.html",{
                                    "MC":mainCat,
                                    "SC":subCat,
                                    "BR":brand,
                                    "Product":p
                                    })

@login_required(login_url='/login/')
def deleteProduct(request,num):
    product = Product.objects.get(pid=num)
    seller = Seller.objects.get(username=request.user)
    if(product.seller==seller):
        product.delete()
    return HttpResponseRedirect('/sellerProfile/')

@login_required(login_url='/login/')
def addToWishlist(request,num):
    product = Product.objects.get(pid=num)
    buyer = Buyer.objects.get(username=request.user)
    wishlist = Wishlist.objects.filter(buyer=buyer)
    flag = False
    for i in wishlist:
        if(product==i.product):
            flag = True
    if(flag==False):
        w = Wishlist()
        w.product=product
        w.buyer=buyer
        w.save()
    return HttpResponseRedirect('/buyerProfile/')


@login_required(login_url='/login/')
def deleteWishlist(request,num):
    wishlist = Wishlist.objects.get(wid=num)
    buyer = Buyer.objects.get(username=request.user)
    if(wishlist.buyer==buyer):
        wishlist.delete()
    return HttpResponseRedirect('/buyerProfile/')


def forgotPassword(request):
    if(request.method=="POST"):
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)                
            try:
                user = Buyer.objects.get(username=username)
            except:
                try:
                    user = Seller.objects.get(username=username)                    
                except:
                    return HttpResponseRedirect("/admin/")
                
            user.otp= randint(1000,9999)
            user.save()
            subject = 'OTP to Reset Password'
            message = """
                        Hello User!!!!
                        Your OTP is {} to reset password
                    """.format(user.otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, "karmaproject@gmail.com", recipient_list)
            return HttpResponseRedirect("/otp/"+username+"/")
        except:
            messages.error(request,"Invalid Username")
    return render(request,"forgetPassword.html")

def otp(request,username):
    if(request.method=="POST"):
        otp = int(request.POST.get('OTP'))
        try:
            user = Buyer.objects.get(username=username)
        except:
            user = Seller.objects.get(username=username)
        
        if(otp == user.otp):
            return HttpResponseRedirect("/resetPassword/"+username+"/")
        else:
            messages.error(request,"Invalid OTP")
    return render(request,"otp.html")

def resetPassword(request,username):
    if(request.method=="POST"):
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        if(pass1==pass2):
            user = User.objects.get(username=username)
            user.set_password(pass1)
            user.save()
            return HttpResponseRedirect('/login/')
        else:
            messages.error(request,"Password and Confirm Password does't Match")
    return render(request,"resetpassword.html")
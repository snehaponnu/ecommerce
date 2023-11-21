import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import get_object_or_404

from .forms import CustomerRegistrationForm, CustomerProfileForm
from .models import Product, Customer, Cart, Payment, OrderPlaced, Whishlist


# Create your views here.
@login_required
def home(request):
    totalitem = 0
    whishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        whishitem = len(Whishlist.objects.filter(user=request.user))
    return render(request,'home.html',locals())

@login_required
def about(request):
    totalitem = 0
    whishitem = 0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        whishitem = len(Whishlist.objects.filter(user=request.user))
    return render(request,'about.html',locals())

@login_required
def contact(request):
    totalitem = 0
    whishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        whishitem = len(Whishlist.objects.filter(user=request.user))
    return render(request,'contact.html',locals())

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        whishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            whishitem = len(Whishlist.objects.filter(user=request.user))
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,'category.html',locals())

@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        totalitem = 0
        whishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            whishitem = len(Whishlist.objects.filter(user=request.user))
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,'category.html',locals())

@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        whishlist=Whishlist.objects.filter(Q(product=product)& Q(user=request.user))
        totalitem = 0
        whishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            whishitem = len(Whishlist.objects.filter(user=request.user))
        return render(request,'productdetail.html',locals())


class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'customerregistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration is successful')
        else:
            messages.error(request,'Invalid input data')
        return render(request,'customerregistration.html',locals())

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            whishitem = len(Whishlist.objects.filter(user=request.user))
        return render(request, 'profile.html', locals())
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'profile save successfully')
        else:
            messages.warning(request,'Invalid Input')
        return render(request, 'profile.html', locals())

@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    totalitem = 0
    whishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        whishitem = len(Whishlist.objects.filter(user=request.user))
    return render(request, 'address.html', locals())

@method_decorator(login_required,name='dispatch')
class UpdateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            whishitem = len(Whishlist.objects.filter(user=request.user))
        return render(request, 'update_address.html', locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,'profile updated successfully')
        else:
            messages.warning(request,'Invalid Input')
        return redirect('address')

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')


@login_required
def showcart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity* p.product.discounted_price
        amount=amount+value
    totalamount=amount+2
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        whishitem = len(Whishlist.objects.filter(user=request.user))
    return render(request,'addtocart.html',locals())

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            whishitem = len(Whishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value=p.quantity* p.product.discounted_price
            famount=famount+value
        totalamount=famount+2
        razoramount=int(totalamount * 100)
        client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data={'amount':razoramount,'currency':'INR','receipt':'order_rcptid_12'}
        payment_response=client.order.create(data=data)
        print(payment_response)
        order_id=payment_response['id']
        order_status=payment_response['status']
        if order_status=='created':
            payment=Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request,'checkout.html',locals())


@login_required
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    print(f"Order ID: {order_id}, Payment ID: {payment_id}, Customer ID: {cust_id}")
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect('orders')


@login_required
def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    totalitem = 0
    wishitem= 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        whishitem = len(Whishlist.objects.filter(user=request.user))
    return render(request,'orders.html',locals())
def pluscart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.discounted_price
            amount=amount+value
        totalamount=amount+2
        data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':totalamount
        }
        return JsonResponse(data)

def minuscart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.discounted_price
            amount=amount+value
        totalamount=amount+2
        data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':totalamount
        }
        return JsonResponse(data)

def removecart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.discounted_price
            amount=amount+value
        totalamount=amount+2
        data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':totalamount
        }
        return JsonResponse(data)

def plus_whishlist(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Whishlist(user=user,product=product).save()
        data={
            'message':'Whishlist added successfully',
        }
        return JsonResponse(data)

def minus_whishlist(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Whishlist(user=user,product=product).delete()
        data={
            'message':'Whishlist removed successfully',
        }
        return JsonResponse(data)

@login_required
def search(request):
    query=request.GET.get('search','')
    totalitem=0
    whishlistitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        whishitem = len(Whishlist.objects.filter(user=request.user))
    product=Product.objects.filter(Q(title__icontains=query))
    return render(request,'search.html',locals())


@login_required
def wishlist(request):
    user=request.user
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        whishitem = len(Whishlist.objects.filter(user=request.user))
    product=Whishlist.objects.filter(user=user)
    return render(request,'wishlist.html',locals())
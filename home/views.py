from django.shortcuts import render, redirect
from more_itertools import quantify
from home.models import Product
from django.http import JsonResponse
from .forms import CreateUserForm, CustomerAddressForm, LoginUserForm, MySetPasswordForm, MyPasswordResetForm, MyPasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from .models import Cart, Customer, OrderPlaced
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



def home(request):
    return render(request, 'home.html')


def all_products(request):
    apple_product = Product.objects.filter(brand = 'apple')
    samsung_product = Product.objects.filter(brand = 'samsung')
    return render(request, 'products.html', {'apple_product':apple_product, 'samsung_product':samsung_product})


def product_detail(request, id):
    product = Product.objects.get(id = id)
    product_in_cart = False
    related_product = Product.objects.filter(brand = product.brand).exclude(id = product.id)
    if request.user.is_authenticated:
        product_in_cart = Cart.objects.filter(Q(product = product)& Q(user = request.user)).exists()
    return render(request, 'product_details.html', {'product':product, 'related_product':related_product, 'product_in_cart':product_in_cart})


def search_product(request):
    if request.is_ajax():
        res = None
        product = request.POST.get('product')
        qs = Product.objects.filter(title__icontains = product)
        if len(qs) > 0 and len(product) > 0:
            data = []
            for pos in qs:
                item = {
                    'pk':pos.pk,
                    'title':pos.title,
                    'product_image':str(pos.product_image.url)
                }
                data.append(item)
            res = data
        else:
            res = 'Sorry! No Product Found'
        return JsonResponse({'data':res})
    return JsonResponse({})


def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('id')
        product = Product.objects.get(id = product_id)
        crt = Cart(user = user, product = product)
        crt.save()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})

def buy_now(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        user = request.user
        product = Product.objects.get(id = product_id)
        crt = Cart(user = user, product = product)
        crt.save()
    return redirect('checkout')


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount        
            return render(request, 'add_to_cart.html', {'cart':cart, 'total_amount':total_amount, 'amount':amount})
        else:
            return render(request, 'add_to_cart.html', {'data':'your cart is empty!'})
    else:
        return redirect('accountlogin')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':amount + shipping_amount  
        } 
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity -= 1
        if c.quantity < 1:
            c.quantity = 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount  
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':amount + shipping_amount
        } 
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount  
        data = {
            'amount':amount,
            'total_amount':amount + shipping_amount
        } 
        return JsonResponse(data)


@login_required(login_url='/account/login')
def checkout(request):
    address = Customer.objects.filter(user = request.user)
    cart_items = Cart.objects.filter(user = request.user)
    amount = 0.0
    shipping_amount = 70.00
    total_amount = 0.00
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount  
        total_amount = amount + shipping_amount
    return render(request, 'checkout.html',{'address':address, 'cart':cart_items, 'total_amount':total_amount})


@login_required(login_url='/account/login')
def payment_done(request):
    usr = request.user
    address_id = request.GET.get('address_id')
    address = Customer.objects.get(id = address_id)
    cart = Cart.objects.filter(user = usr)
    for c in cart:
        OrderPlaced(user = usr, customer = address, product = c.product, quantity = c.quantity, status = 'Accepted').save()
        c.delete()
    return redirect('orders')


@login_required(login_url='/account/login')
def orders(request):
    obj = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'orders.html', {'obj':obj})

def order_cancel(request, id):
    order = OrderPlaced.objects.filter(id = id)
    order.delete()
    return redirect('orders')


def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

@login_required(login_url='/account/login')
def account(request):
    all_addresses = Customer.objects.filter(user = request.user)
    return render(request, 'account.html',{'all_addresses':all_addresses})

def AccountRegister(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            form = CreateUserForm()
    else:
        form = CreateUserForm()
    return render(request, 'account_register.html', {'form':form})

def AccountLogin(request):
    if request.method == 'POST':
        form = LoginUserForm(request = request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginUserForm(request.POST)
    return render(request, 'account_login.html', {'form':form})

def AccountLogout(request):
    logout(request)
    return redirect('accountlogin')

# def ResetPassword(request):
#     fm = MyPasswordResetForm()
#     return render('reset_password.html', {'fm':fm})

# def SetPassword(request):
#     form = MySetPasswordForm(request.user)
#     return render(request, 'set_password.html', {'form':form})

@login_required(login_url='/account/login')
def AddCustomerAddress(request):
    if request.method == 'POST':
        form = CustomerAddressForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user = usr, name = name, locality = locality, city = city, state = state, zipcode = zipcode)
            reg.save()
            return redirect('/account/')
    else:
        form = CustomerAddressForm()
    return render(request, 'add_address.html', {'form':form})

@login_required(login_url='/account/login')
def DeleteCustomerAddress(request, id):
    pi = Customer.objects.get(id = id)
    pi.delete()
    return redirect('/account/')

@login_required(login_url='/account/login')
def ChangePassword(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(user = request.user ,data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account/')
    else:
        form = MyPasswordChangeForm(request.POST)
    return render(request, 'password_change.html', {'form':form})
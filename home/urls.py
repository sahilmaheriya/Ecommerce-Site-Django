from re import template
from unicodedata import name
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import MyPasswordResetForm, MySetPasswordForm, PasswordResetForm


urlpatterns = [
    path('', views.home, name="home"),
    
    path('products/', views.all_products, name="products"),
    
    path('products_detail/<int:id>/', views.product_detail, name="product_detail"),
    
    path('search_product/', views.search_product, name="search_product"),

    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),

    path('cart/', views.show_cart, name="cart"),

    path('buynow/', views.buy_now, name="buynow"),

    path('plus_cart/', views.plus_cart, name="plus_cart"),

    path('minus_cart/', views.minus_cart, name="minus_cart"),

    path('remove_cart/', views.remove_cart, name="remove_cart"),

    path('checkout/', views.checkout, name="checkout"),

    path('payment_done/', views.payment_done, name="payment_done"),

    path('orders/', views.orders, name="orders"),

    path('order_cancel/<int:id>/', views.order_cancel, name="order_cancel"),
    
    path('contact/', views.contact, name="contact"),
    
    path('about/', views.about, name="about"),
    
    path('account/', views.account, name="account"),
    
    path('account/registration', views.AccountRegister, name="accountregister"),
    
    path('account/login', views.AccountLogin, name="accountlogin"),
    
    path('account/logout', views.AccountLogout, name="logout"),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'password_reset.html', form_class = MyPasswordResetForm), name="password_reset"),
    
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'), name="password_reset_done"),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html', form_class = MySetPasswordForm), name="password_reset_confirm"),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'), name="password_reset_complete"),

    # path('set_password/', views.SetPassword, name="setpassword"),


    path('add_address/', views.AddCustomerAddress, name="add_address"),

    path('del_address/<int:id>/', views.DeleteCustomerAddress, name="del_address"),

    path('change_password/', views.ChangePassword, name="change_password"),

]

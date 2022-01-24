from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, SetPasswordForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Customer

class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control fs-4 p-2'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control fs-4 p-2'}))
    email = forms.CharField(required=True, label='Email', widget=forms.EmailInput(attrs={'class':'form-control fs-4 p-2'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {'username':forms.TextInput(attrs={'class':'form-control fs-4 p-2'})}


class LoginUserForm(AuthenticationForm):
    username = UsernameField(widget = forms.TextInput(attrs={'class':'form-control fs-4 p-2'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control fs-4 p-2'}))
    class Meta:
        model = User


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label= 'Email', max_length = 222, widget = forms.EmailInput(attrs={'class':'form-control fs-4 p-2'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', strip=False, widget= forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label='New Password', strip=False, widget= forms.PasswordInput(attrs={'class':'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', strip=False, widget= forms.PasswordInput(attrs={'class':'form-control fs-4 p-2'}))
    new_password1 = forms.CharField(label='New Password', strip=False, widget= forms.PasswordInput(attrs={'class':'form-control fs-4 p-2'}))
    new_password2 = forms.CharField(label='Confirm New Password', strip=False, widget= forms.PasswordInput(attrs={'class':'form-control fs-4 p-2'}))
    


class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control fs-4 p-2'}),
                    'locality':forms.TextInput(attrs={'class':'form-control fs-4 p-2'}),
                    'city':forms.TextInput(attrs={'class':'form-control fs-4 p-2'}),
                    'state':forms.TextInput(attrs={'class':'form-control fs-4 p-2'}),
                    'zipcode':forms.NumberInput(attrs={'class':'form-control fs-4 p-2'}),
                }
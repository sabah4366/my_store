from django import forms
from api.models import Products
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class RegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']


class ProductForm(forms.ModelForm):
    class Meta:
        model=Products
        fields="__all__"

#is there any creation u can use ModelForm class
#is there  not any creation use Form class
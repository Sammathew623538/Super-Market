from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from.models import Category,Product
from.models import profile
import re
from .models import Buy



class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].required = True

        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })

        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")

        # Allow only letters (no numbers or symbols)
        if not re.match(r'^[A-Za-z_ ]+$', username):
            raise forms.ValidationError("Username should contain only letters.")

        return username

def clean(self):
    cleaned_data = super().clean()
    password1 = cleaned_data.get("password1")
    password2 = cleaned_data.get("password2")

    if password1 and password2 and password1 != password2:
        raise forms.ValidationError("Passwords do not match.")


class ProfileForm(forms.ModelForm):
    class Meta:
        model=profile
        fields="__all__"
        exclude=['user']






class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields="__all__"


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields="__all__"





class BuyForm(forms.ModelForm):
    class Meta:
        model = Buy
        fields = ['quantity', 'address', 'phone_number','Email', ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
           
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
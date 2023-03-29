from django import forms
from .models import Clients
from django.contrib.auth.models import User


class ClientRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    email    = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Clients
        fields = [
            'username',
            'full_name',
            'email',
            'password',
            'address'
        ]
    def clean_username(self):
        user_name = self.cleaned_data['username']
        if User.objects.filter(username = user_name).exists():
            raise forms.ValidationError('Client with username already exists.')
        return user_name

class ClientLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    
    def clean_username(self):
        user_name = self.cleaned_data['username']
        if User.objects.filter(username = user_name).exists():
            pass
        else:
            raise forms.ValidationError('Client with username is not exists.')
        return user_name

class ClientProfileUpdate(forms.ModelForm):
    class Meta:
        model = Clients
        fields = [
            'full_name',
            'address',
            'image',
            'phone'
        ]

class PasswordForgetForm(forms.Form):
    email    = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class":"form-control",
            "placeholder":"Enter your email here .."
        }
    ))
    def clean_email(self):
        user_email = self.cleaned_data['email']
        if Clients.objects.filter(user__email = user_email).exists():
            pass
        else:
            raise forms.ValidationError('Client with this email is not exists.')
        return user_email
    
class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
       "class":"form-control",
       "autocomplete":"new-password",
       "placeholder":"Enter your new password" 
    }),label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
       "class":"form-control",
       "autocomplete":"new-password",
       "placeholder":"Confirm your new password" 
    }),label="Confirm New Password")
    
    def clean_confirm_new_password(self):
        newpassword = self.cleaned_data.get('new_password')
        confirmnewpassword = self.cleaned_data.get('confirm_new_password')
        if newpassword != confirmnewpassword:
            raise forms.ValidationError('Passwords Not Match. Try Agin..')
        return confirmnewpassword
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['full_name','address','image','phone']
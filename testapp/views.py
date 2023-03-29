from django.shortcuts import render,redirect
from django.urls import reverse
from .models import *
from .forms import *
from django.views.generic import CreateView,FormView,TemplateView,UpdateView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .utils import password_reset_token
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
class HomePageView(TemplateView):
    template_name = "home.html"


class ClientRegisterationView(CreateView):
    template_name = 'clients/signup.html'
    form_class = ClientRegisterForm
    success_url = '/home/'
    
    def form_valid(self,form):
        username  = form.cleaned_data.get('username')
        full_name = form.cleaned_data.get('full_name') 
        email     = form.cleaned_data.get('email') 
        password  = form.cleaned_data.get('password')
        user = User.objects.create_user(username=username, 
                                        email=email,
                                        password=password,
                                        first_name =full_name.split(' ')[0],
                                        last_name =full_name.split(' ')[-1])
        form.instance.user = user
        login(self.request,user)
        return super().form_valid(form)
       
class ClientLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('test:login')

class ClientLoginView(FormView):
    template_name = 'clients/login.html'
    form_class = ClientLoginForm
    success_url = '/home/'
    def form_valid(self,form):
        username  = form.cleaned_data.get('username')
        password  = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and Clients.objects.filter(user=user).exists():
            login(self.request,user)
        else:
            return render(self.request,self.template_name,{'form':self.form_class})
        return super().form_valid(form)
    
    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url

class ForgetPasswordView(FormView):
    template_name = 'clients/forgot_password.html'
    form_class = PasswordForgetForm
    success_url = '/forgot-password/?m=s'
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        url = self.request.META['HTTP_HOST']
        client = Clients.objects.get(user__email = email)
        user = client.user
        text_content = 'Please click the link below to reset your password. '
        html_message = url+'/reset-password/'+email+'/'+password_reset_token.make_token(user)+'/'
        send_mail(
            'Password Reset Link | From Django Learning Website',
            text_content+html_message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False, 
        )
        print(text_content+html_message)
        return super().form_valid(form)

class ResetPasswordView(FormView):
    template_name='clients/reset_password.html'
    form_class = PasswordResetForm
    success_url = '/login/'
    
    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get('email')
        user = User.objects.get(email=email)
        token = self.kwargs.get('token')
        if user is not None and password_reset_token.check_token(user,token):
            pass
        else:
            return redirect(reverse('test:forgot_password')+'?m=e')
        return super().dispatch(request,*args,**kwargs)
    
    def form_valid(self,form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get('email')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)

class ChangePasswordView(PasswordChangeView):
    template_name = "clients/change_password.html"
    success_url = '/home/'
    
class ClinetProfileView(TemplateView):
    template_name = 'clients/profile.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.clients:
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cprofile"] = Clients.objects.get(user=self.request.user)
        return context

class UpdateClientProfileView(UpdateView):
    model = Clients
    form_class = ProfileUpdateForm
    template_name = "clients/update_profile.html"
    success_url = "/profile/"
    
    
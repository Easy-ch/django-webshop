from .forms import  RegisterForm,EmailAuthenticationForm,ProfileForm,PasswordResetFormCustom,CustomChangePasswordForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from django.contrib.auth import login,get_user_model,logout
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.template.loader import render_to_string 
from .token import account_activation_token 
from django.core.mail import EmailMessage 
import threading
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import SetPasswordForm 
from .models import User
# Create your views here.

# Создаем отображение пользователя
@login_required(login_url=reverse_lazy('login'))
def profile_view(request):
        redirect_url = reverse('profile')
        if request.method == 'POST':
            form=ProfileForm(instance=request.user, data=request.POST,files=request.FILES)
            if form.is_valid():
                form.save()  
                return redirect (redirect_url)   
        else:
            form=ProfileForm(instance=request.user)
        return render(request,'app_auth/profile.html',{'form':form})

# Создаем авторизацию пользователя
def login_view(request):
    redirect_url = reverse('profile')
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None and user.is_active:
                login(request, user)
                return redirect(redirect_url)
            else:
                messages.error(request, 'Пользователь не активен')
        else:
            messages.error(request, 'Неверный email пользователя или пароль')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'app_auth/login.html', {'form': form})
# Создаем регистрацию пользователя 
def register_view(request):
    if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid(): 
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Ссылка активации отправлена на ваш email'
                message = render_to_string('app_auth/activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                my_thread = threading.Thread(target=send_email, args=(email, ))
                my_thread.start()
                return HttpResponse('Пожалуйста,подтвердите ваш адрес электронной почты! ')
            else:
                return render(request, 'app_auth/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'app_auth/register.html', {'form': form})

def activate(request, uidb64, token): 
    User = get_user_model() 
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(pk=uid) 
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): 
        user = None 
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True 
        user.is_verified_email = True 
        user.save() 
        return HttpResponse('Спасибо за подтверждение ') 
    else: 
        return HttpResponse('Ссылка истекла') 
    
def send_email(email):
    email.send()
# Создание капчи
def captcha_login(request):
    redirect_url = reverse('profile')
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            return redirect(redirect_url) 
        else:
            return HttpResponse("OOPS! Bot suspected.")  
    else:
        form = EmailAuthenticationForm()
    return render(request, 'app_auth/login.html', {'form': form})

def recaptcha_register(request):
    redirect_url = reverse('profile')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            return redirect(redirect_url)
        else: 
            return HttpResponse("OOPS! Bot suspected.")  
    else:
        form = RegisterForm()
    return (request, 'app_auth/register.html', {'form': form})

# Создаем выход из профиля
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))
# Логика по восстановлению пароля
class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'app_auth/password_reset.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'app_auth/password_reset_email.html'
    form_class = PasswordResetFormCustom
    success_message = "Instructions for resetting your password have been sent to your email."
    
    def form_valid(self,form):
        print('ААААААААААААААААААААААААААААААААААААААА')
        email = form.cleaned_data.get('email')
        if email:
            self.request.session['email'] = form.cleaned_data['email']
        return super().form_valid(form)

class CustomPasswordResetDoneView(SuccessMessageMixin, TemplateView):
    template_name = 'app_auth/password_reset_done.html'
    success_message = "Instructions for resetting your password have been sent to your email."
    success_url = reverse_lazy('password_reset_confirm')

class CustomPasswordResetConfirmView(SuccessMessageMixin,FormView):
    template_name = 'app_auth/password_reset_confirm.html'
    success_message = "Your password has been reset successfully."
    form_class = CustomChangePasswordForm
    success_url = reverse_lazy('login')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['email'] = self.request.session.get('email')
        return kwargs
    def form_valid(self,form):
        if form.is_valid():
            new_password1 = form.cleaned_data.get('new_password1')
            email = form.cleaned_data.get('email')
            user = get_user_model().objects.get(email=email)
            user.set_password(new_password1)
            user.save()
        return super().form_valid(form)


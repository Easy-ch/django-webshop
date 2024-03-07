from .forms import  RegisterForm,EmailAuthenticationForm,ProfileForm
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
from .models import User
from django.db import IntegrityError
from django import forms
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
    # and user.is_verified_email
# Создаем регистрацию пользователя 
def register_view(request):
    if request.method == 'POST':
        # try:
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
            # else:
            #     raise IntegrityError

        # except forms.ValidationError as e:
        #     messages.error(request,e)
        #     messages.error(request, 'Пользователь с данным email уже зарегестрирован на сайте!')
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

def captcha_login(request):
    redirect_url = reverse('profile')
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            return redirect(redirect_url) 
    else:
        form = EmailAuthenticationForm()
    return render(request, 'app_auth/login.html', {'form': form})

# def captcha_register(request):
#     redirect_url = reverse('profile')
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.captcha.is_valid():
#             return redirect(redirect_url)
#         else:
#             return HttpResponse('Капча неверна!')
#     else:
#         form = EmailAuthenticationForm()
#     return render(request, 'app_auth/login.html', {'form': form})



# Создаем выход из профиля
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))




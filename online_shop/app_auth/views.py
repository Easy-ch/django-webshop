from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import  RegisterForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.

# Создаем отображение пользователя
@login_required(login_url=reverse_lazy('login'))
def profile_view(request):
    return render(request,'app_auth/profile.html')
# Создаем аутентификацию пользователя
def login_view(request):
    redirect_url = reverse('profile')
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(redirect_url)
    else:
        return render(request,'app_auth/login.html')
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
    else:
        return render(request, 'app_auth/login.html', {
                'error_message': 'Please enter your username and password.'
                })
    # проверка, что комбинация логина и пароля нашлась
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(redirect_url)
    # если не нашлась - пользователь не найден
    return render(request,'app_auth/login.html',{'error':'Пользователь не найден'})
# Создаем регистрацию пользователя
def register_view(request): 
    redirect_url = reverse('profile')
    if request.user.is_anonymous:
        if request.method == 'POST': 
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1') 
                form.save() 
                new_user = authenticate(request,username=username,password=password)
                if new_user is not None:
                    login(request,new_user)
                    return redirect(redirect_url)    
    else:
        return render('register')
    form = RegisterForm()
    return render(request,'app_auth/register.html',{'form':form})
# Создаем выход из профиля
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))




from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import  RegisterForm,LoginForm,ProfileForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
        form = LoginForm(data=request.POST) 
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect (redirect_url)
        else:
            messages.error(request,'Неверное имя пользователя или пароль')
    else:
        form = LoginForm()
    return render(request,'app_auth/login.html',{'form':form})
    
# Создаем регистрацию пользователя
def register_view(request): 
    redirect_url = reverse('profile')
    if request.user.is_anonymous:
        if request.method == 'POST': 
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                name = form.cleaned_data.get('name')
                surname = form.cleaned_data.get('surname')
                password = form.cleaned_data.get('password1') 
                form.save() 
                new_user = authenticate(request,username=username,name=name,surname=surname,password=password)
                if new_user is not None:
                    login(request,new_user)
                    return redirect(redirect_url)    
        else:
            form = RegisterForm()
        return render(request,'app_auth/register.html',{'form':form})
    else:
        return redirect(redirect_url)

# Создаем выход из профиля
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))




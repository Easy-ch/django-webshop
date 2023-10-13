from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import OnlineShop
from .forms import Advertisementform
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    title = request.GET.get('query')
    if title:
        online_shops = OnlineShop.objects.filter(title=title)
    else:
        online_shops = OnlineShop.objects.all()
    context = {'online_shops': online_shops }
    return render(request, 'app_advertisement/index.html', context)
def top_sellers(request):
    return render(request,'app_advertisement/top-sellers.html')
@login_required(login_url=reverse_lazy('login'))
def advertisement_post(request):
    if request.method == 'POST':
        form = Advertisementform(request.POST,request.FILES)
        if form.is_valid():
            # advertisement = OnlineShop(**form.cleaned_data)
            advertisement = form.save(commit=False)
            advertisement.user = request.user
            advertisement.save()
            url = reverse('main-page')
            return redirect(url)
    else:
        form = Advertisementform()
    context = {'form':form}
    return render(request, 'app_advertisement/advertisement-post.html',context)
def register(request):
    return render(request,'app_auth/register.html')
def login(request):
    return render(request,'app_auth/login.html')
def profile(request):
    return render(request,'app_auth/profile.html')




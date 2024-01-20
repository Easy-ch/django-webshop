from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import OnlineShop
from .forms import Advertisementform
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from app_auth.models import User
from django.views.generic import DetailView
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
# class AdvertisementView(DetailView):
#     model = User
#     template_name = 'app_advertisement/advertisement.html'
#     context_object_name = 'user'
#      # получаем объект пользователя по его имени
#     def get_object(self):
#         return get_object_or_404(User, username=self.kwargs['username'])
def profileview (request,username):
    user = get_object_or_404(User,username=username)
    return render(request,'app_advertisement/advertisement.html',{'user':user})



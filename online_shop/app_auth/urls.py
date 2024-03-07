from django.urls import path
from .views import profile_view,register_view,logout_view,login_view,activate

urlpatterns = [
    path('profile/',profile_view,name='profile'),
    path('register/',register_view,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate')


]

from django.urls import path
from .views import profile_view,register_view,logout_view,login_view

urlpatterns = [
    path('profile/',profile_view,name='profile'),
    path('register/',register_view,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    
    

]

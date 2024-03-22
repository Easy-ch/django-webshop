from django.urls import path
from .views import profile_view,register_view,logout_view,login_view,activate
from .decorators import check_recaptcha
from .views import(
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetDoneView,
    
)
urlpatterns = [
    path('profile/',profile_view,name='profile'),
    path('register/',check_recaptcha(register_view),name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('password_reset/', CustomPasswordResetView.as_view(),name='password_reset'),
    path('password_reset_done/',CustomPasswordResetDoneView .as_view(),name='password_reset_done'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/',CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
]

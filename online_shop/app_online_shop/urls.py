from django.urls import path
from .views import index,top_sellers,advertisement_post,register,login,profile,profileview
urlpatterns=[
    path('',index, name='main-page'),
    path('top_sellers/',top_sellers, name='top-sellers'),
    path('advertisement-post/',advertisement_post, name='advertisement-post'),
    path('register/',register, name='register'),
    path('login/',login, name='login'),
    path('profile/',profile, name='profile'),
    path(r"^advertisement/(?P<username>[\w-]+)/$",profileview,name='advertisement'),
]
    
# AdvertisementView
#    path('advertisement/<str:username>/',AdvertisementView.as_view(),name='advertisement'),
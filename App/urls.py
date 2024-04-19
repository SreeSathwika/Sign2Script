from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),  
    path('register/',views.register,name='register'), 
    path('index/', views.index, name='index'),
    path('video_feed/', views.video_feed, name='video_feed'), 
]

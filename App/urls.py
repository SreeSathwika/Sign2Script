from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),  
    path('register/',views.register,name='register'), 
    path('home/', views.home, name='home'),
    path('interpreter/', views.video_feed, name='interpreter'), 
    path('profile/', views.view_profile, name='profile'),
    path('logout', views.logout_user, name='logout'),
] 
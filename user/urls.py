from django.urls import path
from . import views



urlpatterns = [
    path("register/", views.register, name = 'register'),
    path("login/", views.loginuser, name = 'login'),
    path('logout/', views.logoutuser, name='logout'),
    path('profile', views.profile, name='profile')
]
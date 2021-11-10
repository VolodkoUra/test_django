from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.base, name='base'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.logout, name='logout'),
    path('shorten_url/', views.shorten_url, name='shorten_url'),
]

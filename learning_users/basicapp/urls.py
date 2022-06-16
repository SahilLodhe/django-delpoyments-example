from operator import index
from django.shortcuts import render
from basicapp import views
from django.contrib import admin
from django.urls import path
from numpy import r_
from django.conf.urls import include

app_name = 'basicapp'

urlpatterns = [
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name = 'user_login')
]
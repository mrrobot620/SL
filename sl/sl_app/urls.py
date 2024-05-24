from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path("login_api" , views.login_api , name="login_api")
]
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('user/',include('api.user.urls')),
    path('reset_password/',auth_views.PasswordResetView.as_view()),
   
]
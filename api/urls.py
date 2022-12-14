from django.contrib import admin
from django.urls import path, include
import api.user.views as Userviews

urlpatterns = [
    path('user/',include('api.user.urls')), 
    path('post/',include('api.post.urls')),
    path('group/',include('api.group.urls')),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
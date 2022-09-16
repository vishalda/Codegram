from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('user/',include('api.user.urls')),
    path('post/',include('api.post.urls'))
]
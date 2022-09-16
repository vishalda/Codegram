from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers
from rest_framework import generics
from .views import createPost

#router = routers.DefaultRouter()
#router.register(r'',views.UserViewSet)


urlpatterns = [
    path('create-post/<int:userId>/',createPost,name='createPost'),
#    path('',include(router.urls)),
]
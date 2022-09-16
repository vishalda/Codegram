from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers
from rest_framework import generics
from . import views

#router = routers.DefaultRouter()
#router.register(r'',views.UserViewSet)


urlpatterns = [
    path('create-post/<int:userId>/',views.createPost,name='createPost'),
    path('delete-post/<int:postId>/',views.deletePost,name='deletePost'),
#    path('',include(router.urls)),
]
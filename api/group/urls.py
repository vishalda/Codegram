from django.urls import path, include
from rest_framework.authtoken import views
#from rest_framework import routers
#from rest_framework import generics
from . import views

#router = routers.DefaultRouter()
#router.register(r'',views.UserViewSet)


urlpatterns = [   
    path('create-group/',views.createGroup, name='createGroup'),
    path('update-group/<int:groupId>/',views.updateGroup, name='updateGroup'),
    path('delete-group/<int:groupId>/',views.deleteGroup,name='deleteGroup'),
#    path('',include(router.urls)),
]
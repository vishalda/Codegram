from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers
from rest_framework import generics
from . import views

router = routers.DefaultRouter()
router.register(r'',views.UserViewSet)


urlpatterns = [
    path('login/',views.login, name='signin'),
    path('logout/<int:id>/',views.signout,name='signout'),
    path('',include(router.urls)),
]
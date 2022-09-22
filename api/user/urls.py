from django.urls import path, include
from rest_framework.authtoken import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from rest_framework import generics
from . import views

router = routers.DefaultRouter()
router.register(r'',views.UserViewSet)


urlpatterns = [
    path('login/',views.login, name='signin'),
    path('logout/<int:id>/',views.signout,name='signout'),
    path('create-friend-request/<int:toUserId>/<int:fromUserId>/',views.createFriendRequest,name='createFriendRequest'),
    path('update-friend-request/<int:requestId>/<str:status>/',views.updateFriendRequestStatus,name='updateFriendRequest'),
    path('',include(router.urls)),
]
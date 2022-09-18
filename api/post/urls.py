from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers
from rest_framework import generics
from . import views

router = routers.DefaultRouter()
router.register(r'comments',views.CommentViewSet)
router.register(r'likes',views.LikeViewSet)
router.register(r'',views.PostDetailViewSet)

urlpatterns = [
    path('create-post/<int:userId>/',views.createPost,name='createPost'),
    path('delete-post/<int:postId>/',views.deletePost,name='deletePost'),
    path('update-post/<int:postId>/',views.updatePost,name='updatePost'),
    path('create-comment/<int:postId>/<int:userId>/',views.createComment,name='createComment'),
    path('update-comment-vote/<int:commentId>/',views.updateCommentVote,name='updateCommentVote'),
    path('update-like/<int:postId>/<int:userId>/',views.updateLike,name='updateLike'),
    path('fork-post/<int:postId>/<int:userId>/',views.createFork,name="createFork"),
    path('',include(router.urls)),
]
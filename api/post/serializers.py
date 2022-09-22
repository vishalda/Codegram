from rest_framework import serializers
from .models import CommentPost, LikePost, Post ,ForkedPost,PullRequest
from api.user.serializers import RegisterSerializer

class PostDetailListSerializer(serializers.ModelSerializer):
    UserID = RegisterSerializer(read_only = True)
    Image = serializers.ImageField(max_length=None,allow_empty_file = True,allow_null = True,required = False)
    class Meta:
        model = Post
        fields = ('id','PostTitle','Description','Image','UserID','CodeSnippet','CodeBlock','PostType','CodeLanguage','Created_at')

class CommentListSerializer(serializers.ModelSerializer):
    UserID = RegisterSerializer(read_only = True)
    class Meta:
        model = CommentPost
        fields = ('id','Content','isAReply','ReplyID','Vote','UserID','PostID')

class LikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = ('id','PostID','UserID','Created_at')
class ForkPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ForkedPost
        fields=('id','UserID','PostID','PostTitle','Description','CodeBlock')
class PullRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=PullRequest
        fields=('id','ForkID','ToUserID','FromUserID','PRStatus')
        
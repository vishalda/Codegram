from rest_framework import serializers
from .models import Post
from api.user.serializers import RegisterSerializer

class PostDetailListSerializer(serializers.ModelSerializer):
    UserID = RegisterSerializer(read_only = True)
    Image = serializers.ImageField(max_length=None,allow_empty_file = True,allow_null = True,required = False)
    class Meta:
        model = Post
        fields = ('id','PostTitle','Description','Image','UserID','CodeSnippet','CodeBlock','PostType','CodeLanguage','Created_at')
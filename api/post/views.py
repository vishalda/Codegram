from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from api.post.serializers import PostDetailListSerializer
from .models import Post
from api.user.models import User

@csrf_exempt
def createPost(request,userId):
    if request.method!="POST":
        return JsonResponse({'error':'Accepting only POST request\'s'})
    
    Description = request.POST['Description']
    PostTitle = request.POST['PostTitle']
    PostType = request.POST['PostType']
    CodeBlock = request.POST['CodeBlock'] if 'CodeBlock' in request.POST.keys() else None 
    Image = request.FILES['Image'] if 'Image' in request.FILES.keys() else None 
    CodeSnippet = request.POST['CodeSnippet'] if 'CodeSnippet' in request.POST.keys() else None
    CodeLanguage = request.POST['CodeLanguage'] if 'CodeLanguage' in request.POST.keys() else None 
    GroupId = request.POST['GroupId'] if 'GroupId' in request.POST.keys() else None 

    Created_at = timezone.now()
    author = get_object_or_404(User,pk=userId)
    group = get_object_or_404(pk=GroupId) if GroupId is not None else None

    instance = Post.objects.create(PostTitle=PostTitle,Description=Description,PostType=PostType,CodeBlock=CodeBlock,Image=Image,CodeSnippet=CodeSnippet,CodeLanguage=CodeLanguage,Created_at=Created_at,UserID=author,GroupId=group)
    instance.save()
    return JsonResponse({'success':'Post created successfully'})

@csrf_exempt
def deletePost(request,postId):
    try:
        instance = Post.objects.get(pk=postId)
        instance.delete()

        return JsonResponse({'success':'Deleted post successfully'})
    except:
        return JsonResponse({'error':'Post doesn\'t exist'})

class PostDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Post.objects.all().order_by('-Created_at')
    serializer_class = PostDetailListSerializer
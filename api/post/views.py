from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.post.serializers import CommentListSerializer, PostDetailListSerializer, LikeListSerializer
from .models import CommentPost, ForkedPost, LikePost, Post
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
def updatePost(request,postId):
    if request.method != "POST":
        return JsonResponse({'error':'Accepting only POST request\'s'})

    try:
        instance = get_object_or_404(Post,pk=postId)
        if instance.PostType == 'CodeBlock' and 'CodeBlock' in request.POST.keys():
            instance.CodeBlock = request.POST['CodeBlock']
        else:
            instance.PostTitle = request.POST['PostTitle']
            instance.Description = request.POST['Description']
        instance.save()
        return JsonResponse({'success':'Updated post successfully'})
    except:
        return JsonResponse({'error':'Failed to update post'})

@csrf_exempt
def deletePost(request,postId):
    try:
        instance = get_object_or_404(Post,pk=postId)
        instance.delete()

        return JsonResponse({'success':'Deleted post successfully'})
    except:
        return JsonResponse({'error':'Post doesn\'t exist'})

@csrf_exempt
def createComment(request,postId,userId):
    if request.method != "POST":
        return JsonResponse({'error':'Accepting only POST request'})

    try:
        Content = request.POST['Content']
        ReplyID = get_object_or_404(CommentPost,pk=int(request.POST['ReplyID'])) if 'ReplyID' in request.POST.keys() else None
        isAReply = True if ReplyID is not None else False
        
        PostID = get_object_or_404(Post,pk=postId)
        UserID = get_object_or_404(User,pk=userId)

        instance = CommentPost.objects.create(PostID=PostID,UserID=UserID,Content=Content,isAReply=isAReply,ReplyID=ReplyID)
        instance.save()
        return JsonResponse({'success':'Comment created successfully'})
    except:
        return JsonResponse({'error':'Couldn\'t add comment. Please try again!'})

@csrf_exempt
def updateCommentVote(request,commentId):
    if request.method != 'POST':
        return JsonResponse({'error':'Accepting only POST request'})

    try:
        upVote = request.POST['upVote']
        instance = get_object_or_404(CommentPost,pk=commentId)
        if upVote == 'True':
            instance.Vote+=1
        else:
            instance.Vote+=-1
        instance.save()
        return JsonResponse({'success':'Vote Updated successfully'})
    except:
        return JsonResponse({'error':'Couldn\'t update the vote'})
    
def updateLike(request,postId,userId):
    try:
        if not LikePost.objects.filter(PostID=postId,UserID=userId).exists():
            Created_at = timezone.now()
            PostID = get_object_or_404(Post,pk=postId)
            UserID = get_object_or_404(User,pk=userId)
            instance = LikePost.objects.create(PostID=PostID,UserID=UserID,Created_at=Created_at)
            instance.save()
        else:
            instance = LikePost.objects.get(PostID=postId,UserID=userId)
            instance.delete()

        return JsonResponse({'success':'Like Updated'})
    except:
        return JsonResponse({'error':'Unable to like. Please try again'})

@csrf_exempt
def createFork(request,postId,userId):
    if request.method != "POST":
        return JsonResponse({'error':'Accepting only Post request'})
    
    try:
        UserID = get_object_or_404(User,pk=userId)
        PostID = get_object_or_404(Post,pk=postId)
        PostTitle = PostID.PostTitle
        Description = PostID.Description
        Created_at = timezone.now()
        CodeBlock = PostID.CodeBlock
        instance = ForkedPost.objects.create(UserID=UserID,PostID=PostID,PostTitle=PostTitle,Description=Description,Created_at=Created_at,CodeBlock=CodeBlock)
        instance.save()
        return JsonResponse({'success':'Post forked successfully'})
    except:
        return JsonResponse({'error':'Failed to fork a post'})


class PostDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Post.objects.all().order_by('-Created_at')
    serializer_class = PostDetailListSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = CommentPost.objects.all().order_by('id')
    serializer_class = CommentListSerializer

class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    queryset = LikePost.objects.all().order_by('id')
    serializer_class = LikeListSerializer
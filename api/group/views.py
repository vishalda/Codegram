from json import JSONDecodeError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from api.group.models import FollowGroup, Group
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from api.group.serializers import GroupListSerializer
from api.user.models import User

@csrf_exempt
def createGroup(request,userId):
    if request.method != "POST":
        return JsonResponse({'error':'Accepting only POST request'})
    try:
        Title = request.POST['Title']
        Description = request.POST['Description']
        Image = request.FILES['Image'] if 'Image' in request.FILES.keys() else None
        admin = get_object_or_404(User,pk=userId)

        instance = Group.objects.create(Title=Title,Description=Description,Image=Image,admin=admin)
        instance.save()
        return JsonResponse({'success':'Group Created'})
    except:
        return JsonResponse({'error':'Unable to create group'})

@csrf_exempt
def updateGroup(request,groupId):
    if request.method != "POST":
        return JsonResponse({'error':'Accepting only POST request'})
    
    try:
        instance = get_object_or_404(Group,pk=groupId)
        instance.Title = request.POST['Title']
        instance.Description = request.POST['Description']
        instance.Image = request.FILES['Image'] if 'Image' in request.FILES.keys() else None
        instance.save()
        return JsonResponse({'success':'Group updated successfully'})

    except:
        return JsonResponse({'error':'Unable to update group'})

def deleteGroup(request,groupId):
    try:
        instance = get_object_or_404(Group,pk=groupId)
        instance.delete()
        return JsonResponse({'success':'Group deleted successfully'})
    except:
        return JsonResponse({'error':'Unable to find group'})

def followGroup(request,userId,groupId):
    try:
        UserID = get_object_or_404(User,pk=userId)
        GroupID = get_object_or_404(Group,pk=groupId)
        instance = FollowGroup.objects.create(UserID=UserID,GroupID=GroupID)
        instance.save()
        return JsonResponse({'success':'Group followed'})
    except:
        return JsonResponse({'error':'Error occurred while following, please try again'})

def unFollowGroup(request,userId,groupId):
    try:
        instance = get_object_or_404(FollowGroup,UserID=userId,GroupID=groupId)
        instance.delete()
        return JsonResponse({'success':'Group unfollowed successfully'})
    except:
        return JsonResponse({'error':'Unable to unfollow group'})
class GroupViewSet(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupListSerializer
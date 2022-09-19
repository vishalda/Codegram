from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from api.group.models import Group

@csrf_exempt
def createGroup(request):
    if request.method != "POST":
        return JsonResponse({'error':'Accepting only POST request'})
    
    try:
        Title = request.POST['Title']
        Description = request.POST['Description']
        Image = request.FILES['Image'] if 'Image' in request.FILES.keys() else None

        instance = Group.objects.create(Title=Title,Description=Description,Image=Image)
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
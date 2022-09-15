from django.http import JsonResponse
from django.contrib.auth import get_user_model,login as auth_login,logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from api.user.models import User
from .serializers import RegisterSerializer
from rest_framework.decorators import permission_classes
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
import random
import re



#Generating Session tokens
def generateSessionToken(length=10):
    return ''.join(random.SystemRandom().choice([chr(i)  for i in range(97,123)] + [str(i) for i in range(10)]) for _ in range(length))

def validateRequest(username,password):    
    #Checking valid username using regex
    if not re.match('^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}$',str(username)):
        return JsonResponse({'error':'Please enter a valid username'})

    #Checking length of password
    if len(password) < 4:
        return JsonResponse({'error':'Password length should not be less than 4'})



@csrf_exempt
# Signin function
def login(request):
    if not request.method == 'POST':
        return JsonResponse({'error':'Accepting only POST request'})

    #Get data from request.POST
    username=request.POST['username']
    password=request.POST['password']
    #username=request.POST.get('username')
    #password=request.POST.get('password')

    validateRequest(username,password)
    UserModal=get_user_model()
    
    try:
        user=UserModal.objects.get(username=username)
        #Check for password correctness
        if user.check_password(password):
            data=UserModal.objects.filter(username=username).values().first()
            data.pop('password')

            if user.session_token != '0':
                user.session_token = '0'
                user.save()
                return JsonResponse({'error':'Session already exists, login again'})
            
            token = generateSessionToken()
            user.session_token = token
            auth_login(request,user)
            user.save()
            return JsonResponse({'token':token,'data':data})
        else:
            return JsonResponse({'error':'Invalid credentials'})
    except UserModal.DoesNotExist:
        return JsonResponse({'error':'Username doesn\'t exist'})

# Logout function
@csrf_exempt
def signout(request,id):
    auth_logout(request)

    UserModal = get_user_model()

    try:
        user = UserModal.objects.get(pk=id)
        user.session_token = '0'
        user.save()
        
    except UserModal.DoesNotExist:
        return JsonResponse({'error':'User doesn\'t exist'})

    return JsonResponse({'success':'Logged out successfully'})

class UserViewSet(viewsets.ModelViewSet):
    #permission_classes_by_action = {'create':[AllowAny]}
    permission_classes=[AllowAny,]
    queryset = User.objects.all().order_by('id')
    serializer_class = RegisterSerializer

    def get_permission(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except:
            return [permission() for permission in self.permission_classes]
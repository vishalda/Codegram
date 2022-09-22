from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from models import Message
from rest_framework.permissions import IsAuthenticated
User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
  username=serializers.CharField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all()),UnicodeUsernameValidator]
    )

  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]


  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)

  phone=serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all()),RegexValidator(regex=r'^[6-9]\d{9}$')]
  

  )
  
  class Meta:
    model = User
    fields = ('username', 'password', 'password2','email', 'phone')
    extra_kwargs = {
      'email': {'required': True},
      'phone': {'required': True},
    }

  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs

  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      phone=validated_data['phone'],
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

class MessageDetailSerializer(serializers.ModelSerializer):
  class Meta:
      model = Message
      fields = ('Index','Content','ChatId','UserID1','UserID2','Created_at')
class MessageDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all().order_by('Created_at')
    serializer_class = MessageDetailSerializer



def createChat(request,UserID_2):
  if request.method != "POST":
        return JsonResponse({'error':'Accepting only Post request'})
    try:
        if request.user_is_authenticated:
            UserID2=get_object_or_404(User,pk=UserID_2)
            UserID_1=request.current_user.id
            UserID_2=UserID2.id
            created_at=timezone.now()

        else:
            return JsonResponse({'error': 'Please Login and Try again'})

        instance = Chat.objects.create(UserID_1=UserID_1,UserID_2=UserID_2,created_at=created_at)
        instance.save()
        return JsonResponse({'success':'Chat initiated successfully'})
    except:
        return JsonResponse({'error':'Failed to initiate a chat'})












    





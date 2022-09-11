from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager

#Base User model
class User(AbstractUser):
    name = models.CharField(max_length=50, default='Anonymous')
    username = models.CharField(max_length=30,unique=True)
    email = models.EmailField(max_length=254, unique=True)
    session_token = models.CharField(max_length=10,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=15,blank = True,null=True)
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username

class FriendRequest(models.Model):
    StatusID = models.BooleanField(null=True)
    SentTime = models.DateTimeField(auto_now_add=True)
    ResponseTime = models.DateTimeField(auto_now=True)
    FromUserID = models.ForeignKey(User,on_delete=models.CASCADE, related_name='FromUserRequest')
    ToUserID = models.ForeignKey(User,on_delete=models.CASCADE, related_name='ToUserRequest')
    def __str__(self):
        return "%s wants to follow %s"%(User.objects.values_list('username', flat=True).get(pk=self.FromUserID.id),User.objects.values_list('username', flat=True).get(pk=self.ToUserID.id))

class Chat(models.Model):
    TotalMessage = models.IntegerField(default=0)
    UserID_1 = models.ForeignKey(User,on_delete=models.CASCADE, related_name='FirstUserChat')
    UserID_2 = models.ForeignKey(User,on_delete=models.CASCADE, related_name='SecondUserChat')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s and %s"%(User.objects.values_list('username', flat=True).get(pk=self.UserID_1.id),User.objects.values_list('username', flat=True).get(pk=self.UserID_2.id))

class Message(models.Model):
    Index = models.IntegerField(default=-1)
    Content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    UserID_1 = models.ForeignKey(User,on_delete=models.CASCADE, related_name='FirstUserMessage')
    UserID_2 = models.ForeignKey(User,on_delete=models.CASCADE, related_name='SecondUserMessage')
    ChatId = models.ForeignKey(Chat, related_name='chat',on_delete=models.CASCADE)

    def __str__(self):
        return "from %s to %s"%(User.objects.values_list('username', flat=True).get(pk=self.UserID_1.id),User.objects.values_list('username', flat=True).get(pk=self.UserID_2.id))
    
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
from django.db import models

from api.user.models import User

# Create your models here.
class Group(models.Model):
    Title = models.CharField(max_length=50)
    Description = models.TextField(null=True)
    Image = models.ImageField(null=True,blank=True)

class FollowGroup(models.Model):
    UserID = models.ForeignKey(User, related_name='user',on_delete=models.CASCADE)
    GroupID = models.ForeignKey(Group, related_name='group',on_delete=models.CASCADE)
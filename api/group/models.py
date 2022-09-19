from django.db import models

from api.user.models import User

# Create your models here.
class Group(models.Model):
    Title = models.CharField(max_length=50)
    Description = models.TextField(null=True,blank=True)
    Image = models.ImageField(null=True,blank=True)
    admin = models.ForeignKey(User,related_name='admin',on_delete=models.CASCADE)

    def __str__(self):
        return self.Title

class FollowGroup(models.Model):
    UserID = models.ForeignKey(User, related_name='user',on_delete=models.CASCADE)
    GroupID = models.ForeignKey(Group, related_name='group',on_delete=models.CASCADE)
    def __str__(self):
        return "%s follows %s" %(User.objects.values_list('username', flat=True).get(pk=self.UserID.id) ,Group.objects.values_list('Title', flat=True).get(pk=self.GroupID.id))
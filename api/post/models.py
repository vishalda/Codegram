from django.db import models
from api.user.models import User
from django.contrib.auth import get_user_model
from api.group.models import Group
from datetime import datetime
# Create your models here.
def get_deleted():
    return get_user_model().objects.get_or_create(username='Deleted User')[0]
class Post(models.Model):
	GroupId=models.ForeignKey(Group,on_delete=models.CASCADE,null=True,blank=True)
	UserID=models.ForeignKey(User,on_delete=models.CASCADE)
	PostTitle=models.CharField(max_length=50,null=False)
	Description=models.TextField(null=True)
	PostType=models.CharField(max_length=15)
	CodeBlock=models.TextField(blank=True,null=True)
	Image=models.ImageField(blank=True,null=True)
	CodeSnippet=models.TextField(blank=True,null=True)
	CodeLanguage=models.CharField(max_length=15,null=True,blank=True)
	Created_at=models.DateTimeField(null=False)

	class Meta:
		ordering=['-Created_at']
	def __str__(self):
		return "%s posted a %s"%(User.objects.values_list('username', flat=True).get(pk=self.UserID.id),self.PostType)

class LikePost(models.Model):
	UserID=models.ForeignKey(User,on_delete=models.SET(get_deleted))
	PostID=models.ForeignKey(Post,on_delete=models.CASCADE)
	Created_at=models.DateTimeField(null=False)

	def __str__(self):
		return "%s liked %d"%(User.objects.values_list('username', flat=True).get(pk=self.UserID.id),Post.objects.values_list('id', flat=True).get(pk=self.PostID.id))
class CommentPost(models.Model):
	PostID=models.ForeignKey(Post,on_delete=models.CASCADE)
	UserID=models.ForeignKey(User,on_delete=models.SET(get_deleted))
	ReplyID=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='replyid')
	Content=models.TextField(null=False)
	isAReply=models.BooleanField(default=False)
	Vote=models.IntegerField(default=0)

	def __str__(self):
		if self.isAReply:
			return "%s replied to a comment on %d"%(User.objects.values_list('username', flat=True).get(pk=self.UserID.id),Post.objects.values_list('id', flat=True).get(pk=self.PostID.id))

		else:
			return "%s commented on %d"%(User.objects.values_list('username', flat=True).get(pk=self.UserID.id),Post.objects.values_list('id', flat=True).get(pk=self.PostID.id))
class ForkedPost(models.Model):
	UserID=models.ForeignKey(User,on_delete=models.CASCADE)
	PostID=models.ForeignKey(Post,on_delete=models.CASCADE)
	PostTitle=models.CharField(max_length=50,null=False)
	Description=models.TextField(null=True)
	Created_at=models.DateTimeField(null=False)
	CodeBlock=models.TextField(blank=True,null=True)

	def __str__(self):
		return "%s forked %d"%(User.objects.values_list('username', flat=True).get(pk=self.UserID.id),Post.objects.values_list('id', flat=True).get(pk=self.PostID.id))

class PullRequest(models.Model):
	ForkID=models.ForeignKey(ForkedPost,on_delete=models.CASCADE)
	ToUserID=models.ForeignKey(User,on_delete=models.CASCADE,related_name='toUser')
	FromUserID=models.ForeignKey(User,on_delete=models.CASCADE,related_name='fromUser')
	PRstatus=models.BooleanField(null=True,default=None)

	def __str__(self):
		return "%s is requesting a pull to %s"%(User.objects.values_list('username', flat=True).get(pk=self.ToUserID.id),User.objects.values_list('username', flat=True).get(pk=self.FromUserID.id))


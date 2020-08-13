from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	nickname = models.CharField(max_length=20,verbose_name='昵称')

	def __str__(self):
		return '<Profile:%s for %s>' % (self.nickname,self.user.username)

def get_nickname(self):
	if Profile.objects.filter(user=self).exists():
		profile = Profile.objects.get(user=self)
		return profile.nickname
	else:
		return ''

def get_nickname_or_username(self):
	if Profile.objects.filter(user=self).exists():
		profile = Profile.objects.get(user=self)
		return profile.nickname
	else:
		return self.username

def has_nickname(self):
	return Profile.objects.filter(user=self).exists()

class FriendsSystem(models.Model):
	user1 = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user1")
	user2 = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user2")
	agreesender = models.ForeignKey(User,on_delete=models.CASCADE,related_name = "agreesender",null=True,blank=True,default = None)
	agreereceiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name="agreereceiver",null=True,blank=True,default = None)
	agree = models.SmallIntegerField(default = 0)
	ifprocess = models.BooleanField(default=False)

User.get_nickname = get_nickname
User.get_nickname_or_username = get_nickname_or_username
User.has_nickname = has_nickname
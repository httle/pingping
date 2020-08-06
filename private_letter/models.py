from django.db import models
from django.contrib.auth.models import User
from notifications.models import Notification
# Create your models here.

class Chat(models.Model):
	user1 = models.ForeignKey(User, on_delete=models.CASCADE,related_name="chat_user1")
	user2 = models.ForeignKey(User, on_delete =models.CASCADE,related_name="chat_user2")

	unreadNum = models.IntegerField(default = 0)
	def __str__(self):
		return '%s and %s'% (self.user1.username,self.user2.username)
class PrivateLetter(models.Model):
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add = True)
	text = models.TextField()
	sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
	receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver")
	image = models.ImageField(upload_to = 'privateLetterImg',null=True,blank=True)


	class Meta:
		ordering = ['time']
			
		
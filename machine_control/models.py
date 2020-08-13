from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Practice(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	created_time = models.DateTimeField(auto_now_add = True)
	practice_num = models.IntegerField(default = 0)
	hit_percent = models.FloatField(default = 0.0)
	data = models.TextField()
	def __str__(self):
		return '<practice:%s>' % self.user

	class Meta:
		ordering=['-created_time']


class PracticeImg(models.Model):
	practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
	img = models.ImageField(upload_to='practiceImg')
	
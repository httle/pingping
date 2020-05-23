from django.db import models

# Create your models here.

class Instructor(models.Model):
    title = models.CharField(max_length=50)
    url = models.URLField()
    video_url = models.URLField()
    inframe_url = models.URLField()
    img_url = models.URLField()
    created_time = models.DateTimeField(auto_now_add=True)
    havemp4 = models.IntegerField(default=0)


    def __str__(self):
        return '<Instructor:%s>' % self.title

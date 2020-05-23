from django.db import models

# Create your models here.
class SportsNews(models.Model):
    title = models.CharField(max_length=100)
    time = models.CharField(max_length=20)
    created_time = models.DateTimeField(auto_now_add=True)
    url = models.URLField(default='')
    content = models.TextField(default='')
    img = models.URLField(default='')
    img_describe = models.CharField(max_length=50)

    def __str__(self):
        return '<News:%s>' % self.title

# class DetailNews(models.Model):
#     sportsnews = models.ForeignKey(SportsNews,on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     time = models.CharField(max_length=20)
#     created_time = models.DateField(auto_created=True)
#     content = models.TextField()
#     img = models.URLField()

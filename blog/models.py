from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod,ReadDetail

# Create your models here.

class test():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

class BlogType(models.Model):
    type_name=models.CharField(max_length=15)

    def __str__(self):
        return self.type_name
        
class Blog(models.Model,ReadNumExpandMethod):
    title=models.CharField(max_length=50)
    blog_type=models.ForeignKey(BlogType,on_delete=models.CASCADE)
    content=RichTextUploadingField()
    style = models.TextField(default=0)
    script = models.TextField(default=0)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    read_details= GenericRelation(ReadDetail)
    created_time=models.DateTimeField(auto_now_add=True)
    last_updated_time=models.DateTimeField(auto_now=True)
    canread = models.IntegerField(default=1)

    def get_url(self):
        return reverse('blog_detail',kwargs={'blog_pk':self.pk})

    def get_name(self):
        return self.author.username

    def get_user(self):
        return self.author

    def get_email(self):
        return self.author.email

    # 新方法
    def __str__(self):
        return '<Blog:%s>'% self.title

    class Meta:
        # 这是django的内嵌类
        ordering=['-created_time']

'''class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE)
''' 

class BlogImage(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    img = models.ImageField(upload_to='blogImg')
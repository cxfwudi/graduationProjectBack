from django.db import models
from user.models import UserProfile
# Create your models here.
#列表页简介处理
#1、后端给前端全部内容，前端自己截取（浪费带宽）
#2、后端从数据库里获取全部文章内容，截取好后，相应给前端（后端与数据库之间通过内网获取数据）
#3、数据库冗余一个字段[简介]，后端只取简介字段内容

class Topic(models.Model):
    title = models.CharField(max_length=50,verbose_name='文章标题')
    # tec & no-tec
    category = models.CharField(max_length=20,verbose_name='文章分类')
    #public & private
    limit = models.CharField(max_length=20,verbose_name='文章权限')
    introduce = models.CharField(max_length=90,verbose_name='文章简介')
    content = models.TextField(verbose_name='文章内容')
    content_text = models.TextField(verbose_name='带样式的文章内容')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    has_photos = models.BooleanField(default=False)
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

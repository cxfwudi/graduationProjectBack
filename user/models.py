from django.db import models
import random


def default_sign():
    signs = ['遇事不决,可问春风','齐先生']
    return random.choice(signs)


# Create your models here.
class UserProfile(models.Model):

    username = models.CharField(max_length=11,verbose_name='用户名',
     primary_key = True)
    nickname = models.CharField(max_length=30,verbose_name='昵称')
    password = models.CharField(max_length=32)
    email = models.EmailField()
    role = models.CharField(max_length=2)   #用户的身份类型 0代表普通用户 1代表管理员
    phone = models.CharField(max_length=11)
    avatar = models.ImageField(upload_to='avatar', null=True)
    sign = models.CharField(max_length=50, verbose_name='个人签名',default=default_sign)
    info = models.CharField(max_length=150, verbose_name='个人简介',
                            default='')
    create_time = models.DateTimeField(auto_now_add=True)  #创建时间
    updated_time = models.DateTimeField(auto_now=True)  #修改时间

    class Meta:
        db_table = 'user_user_profile'  #给数据库起别名


from django.db import models
from user.models import UserProfile
from permissions.models import Permissions

class userPerm(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    permission = models.ForeignKey(Permissions,on_delete=models.CASCADE)
    class Meta:
        db_table = 'user_perm'  #给数据库起别名

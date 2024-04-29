from django.db import models

class Permissions(models.Model):
    code = models.CharField(max_length=10,verbose_name='权限编号')
    # 0：可查看 1：可发布 2：可修改 3：可评论 4：已封禁
    name = models.CharField(max_length=100,verbose_name='权限名称')
    class Meta:
        db_table = 'permissions'  #给数据库起别名
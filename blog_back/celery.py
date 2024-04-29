from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','blog_back.settings')

app = Celery('blog_back')
app.conf.update(
    BROKER_URL = 'redis://:@192.168.186.128:6379/1', #消息传输的中间件，消息一旦有发出，则存储在broker中
)
app.autodiscover_tasks(settings.INSTALLED_APPS)   #自动去注册的应用下去找worker函数


#注意：将cmd切换到项目的目录下，使用celery -A blog_back worker -l info -P eventlet启动celery服务(前台启动)
#blog_back是项目名，在window10环境下，要安装eventlet（pip install eventlet）才能启动celery
#则在启动命令后加上 -P eventlet 进行启动,启动服务之前需将redis启动

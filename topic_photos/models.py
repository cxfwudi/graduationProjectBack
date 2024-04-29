from django.db import models
from topic.models import Topic
# Create your models here.

class Photos(models.Model):
    content = models.ImageField(upload_to='topic_photo', null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)   #外键
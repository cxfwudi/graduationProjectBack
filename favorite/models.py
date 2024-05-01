from django.db import models
from user.models import UserProfile
from topic.models import Topic

class Favorite(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)

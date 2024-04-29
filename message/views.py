import json

from message.models import Message
from django.http import JsonResponse
from django.shortcuts import render
from tools.logging_dec import logging_check
from topic.models import Topic
#10400-10499 异常码
# Create your views here.
@logging_check
def message_view(request, topic_id):
    user = request.myuser   #装饰器校验身份，在request中添加了用户名
    json_str = request.body
    json_obj = json.loads(json_str)
    content = json_obj['content']
    parent_id = json_obj.get('parent_id', 0) #parent_id可能有可能没有，没有则给个0

    try:
        topic = Topic.objects.get(id=topic_id)
    except Exception as e:
        result = {'code':10400, 'error':'The Topic is not existed'}
        return JsonResponse(result)
    Message.objects.create(topic = topic, content=content,parent_message=parent_id,publisher=user)

    return JsonResponse({'code':200})
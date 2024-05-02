from django.shortcuts import render
import json
from django.utils.decorators import method_decorator  #转换装饰器，视图类到函数,函数可以直接@加装饰器，类要加个转换器
from tools.logging_dec import logging_check,get_user_by_request    #token校验
from django.views import View
from django.http import JsonResponse
from user.models import UserProfile
from topic.models import Topic
from collect.models import Collect

class UserCollect(View):
    def get(self,request):  #用于查询文章是否被该用户收藏了
        userName = request.GET.get('userName')
        topicId = request.GET.get('topicId')
        topicUser = UserProfile.objects.filter(username=userName).first()
        topic = Topic.objects.filter(id=topicId).first()
        print(topicUser,topic)
        try:
            hasCollect = Collect.objects.get(user = topicUser,topic = topic)
        except Exception as e:
            res = {'code': 200, 'data': 0}
            return JsonResponse(res)
        res = {'code':200,'data':1}
        return JsonResponse(res)

    def post(self,request):  #增加用户文章点赞记录
        collectInfo = request.body
        collectInfoJson = json.loads(collectInfo)
        userName = collectInfoJson['userName']
        topicId = collectInfoJson['topicId']
        topicUser = UserProfile.objects.get(username=userName)
        topic = Topic.objects.get(id=topicId)
        Collect.objects.create(user = topicUser,topic = topic)
        res = {'code':200}
        return JsonResponse(res)

    def delete(self,request):
        collectInfo = request.body
        collectInfoJson = json.loads(collectInfo)
        userName = collectInfoJson['userName']
        topicId = collectInfoJson['topicId']
        topicUser = UserProfile.objects.get(username=userName)
        topic = Topic.objects.get(id=topicId)
        Collect.objects.filter(user=topicUser, topic=topic).delete()
        res = {'code': 200}
        return JsonResponse(res)
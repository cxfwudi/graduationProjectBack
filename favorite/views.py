from django.shortcuts import render
import json
from django.utils.decorators import method_decorator  #转换装饰器，视图类到函数,函数可以直接@加装饰器，类要加个转换器
from tools.logging_dec import logging_check,get_user_by_request    #token校验
from django.views import View
from django.http import JsonResponse
from user.models import UserProfile
from topic.models import Topic
from favorite.models import Favorite

class UserFavorite(View):
    def get(self,request):  #用于查询文章是否被该用户点赞了
        userName = request.GET.get('userName')
        topicId = request.GET.get('topicId')
        topicUser = UserProfile.objects.filter(username=userName).first()
        topic = Topic.objects.filter(id=topicId).first()
        print(topicUser,topic)
        try:
            hasFavorite = Favorite.objects.get(user = topicUser,topic = topic)
        except Exception as e:
            res = {'code': 200, 'data': 0}
            return JsonResponse(res)
        res = {'code':200,'data':1}
        return JsonResponse(res)

    def post(self,request):  #增加用户文章点赞记录
        favoriteInfo = request.body
        favoriteInfoJson = json.loads(favoriteInfo)
        userName = favoriteInfoJson['userName']
        topicId = favoriteInfoJson['topicId']
        topicUser = UserProfile.objects.get(username=userName)
        topic = Topic.objects.get(id=topicId)
        Favorite.objects.create(user = topicUser,topic = topic)
        res = {'code':200}
        return JsonResponse(res)

    def delete(self,request):
        favoriteInfo = request.body
        favoriteInfoJson = json.loads(favoriteInfo)
        userName = favoriteInfoJson['userName']
        topicId = favoriteInfoJson['topicId']
        topicUser = UserProfile.objects.get(username=userName)
        topic = Topic.objects.get(id=topicId)
        Favorite.objects.filter(user=topicUser, topic=topic).delete()
        res = {'code': 200}
        return JsonResponse(res)
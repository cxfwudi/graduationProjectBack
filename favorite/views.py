from django.shortcuts import render
import json
from django.utils.decorators import method_decorator  #转换装饰器，视图类到函数,函数可以直接@加装饰器，类要加个转换器
from tools.logging_dec import logging_check,get_user_by_request    #token校验
from django.views import View
from django.http import JsonResponse
from user.models import UserProfile
from topic.models import Topic

class UserFavorite(View):
    def get(self,request):  #用于查询文章是否被该用户点赞了
        pass
    def post(self,request):  #增加用户文章点赞记录
        pass
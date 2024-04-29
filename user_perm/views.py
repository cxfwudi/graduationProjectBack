from django.shortcuts import render
import json
from django.utils.decorators import method_decorator  #转换装饰器，视图类到函数,函数可以直接@加装饰器，类要加个转换器
from django.views.decorators.cache import cache_page
from tools.cache_dec import cache_set
from tools.logging_dec import logging_check,get_user_by_request    #token校验
from django.views import View
from user_perm.models import userPerm
from django.http import JsonResponse
from user.models import UserProfile
from permissions.models import Permissions

class PermissionManage(View):
    #获取用户权限列表
    def get(self,request):
        userName = request.GET.get('userName')
        permissionList = userPerm.objects.filter(user = userName)
        res = {'code':200,'data':[]}
        print(permissionList)
        for item in permissionList:
            perId = item.permission
            res['data'].append(perId.code)
        return JsonResponse(res)

    #为用户添加权限
    def post(self,request):
        json_str = request.body
        json_msg = json.loads(json_str)
        userName = json_msg['userName']
        perCode  = json_msg['userCode']
        userObj = UserProfile.objects.get(username=userName)
        perObj = Permissions.objects.get(code=perCode)
        userPerm.objects.create(user=userObj,permission=perObj)
        return JsonResponse({'code': 200})

    #删除用户权限
    def delete(self,request):
        json_str = request.body
        json_msg = json.loads(json_str)
        userName = json_msg['userName']
        perCode = json_msg['userCode']
        userObj = UserProfile.objects.get(username=userName)
        perObj = Permissions.objects.get(code=perCode)
        userPerm.objects.filter(user=userObj,permission=perObj).delete()
        return JsonResponse({'code': 200})

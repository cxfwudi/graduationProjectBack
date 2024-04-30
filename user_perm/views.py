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
    def getUserPermissions(self,userName):
        data = []
        permissionList = userPerm.objects.filter(user=userName)
        for item in permissionList:
            perId = item.permission
            data.append(perId.code)
        return data

    #获取用户权限列表
    def get(self,request):
        userName = request.GET.get('userName')
        if(userName):
            userPermData = self.getUserPermissions(userName)
            res = {'code':200,'data':userPermData}
            return JsonResponse(res)
        else: #获取所用用户权限，用户管理员权限展示
            page = request.GET.get('page')
            page = int(page)
            userList = UserProfile.objects.filter(role = 0)
            pagingUserList = UserProfile.objects.filter(role = 0).order_by('-updated_time')[(page-1)*3:(page-1)*3+3]
            allUserPermissions = []
            for item in pagingUserList:
                singleUserPermInfo = {}
                singleUserPermInfo['userName'] = item.username
                singleUserPermInfo['userAvatar'] = str(item.avatar)
                singleUserPermInfo['permList'] = self.getUserPermissions(item.username)
                allUserPermissions.append(singleUserPermInfo)
            res = {'code':200,'total':len(userList),'data':allUserPermissions}
            return JsonResponse(res)


    #为用户添加权限
    def post(self,request):
        json_str = request.body
        json_msg = json.loads(json_str)
        userName = json_msg['userName']
        perCode  = json_msg['roleCode']
        userObj = UserProfile.objects.get(username=userName)
        perObj = Permissions.objects.get(code=perCode)
        userPerm.objects.create(user=userObj,permission=perObj)
        return JsonResponse({'code': 200})

    #删除用户权限
    def delete(self,request):
        json_str = request.body
        json_msg = json.loads(json_str)
        userName = json_msg['userName']
        perCode = json_msg['roleCode']
        userObj = UserProfile.objects.get(username=userName)
        perObj = Permissions.objects.get(code=perCode)
        userPerm.objects.filter(user=userObj,permission=perObj).delete()
        return JsonResponse({'code': 200})

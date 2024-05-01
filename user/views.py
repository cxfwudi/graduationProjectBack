import json
import random
from django.conf import settings
from django.http import JsonResponse
from user_perm.models import userPerm
from permissions.models import Permissions
from django.shortcuts import render
from .tasks import send_sms_celery


# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from tools.logging_dec import logging_check
from .models import UserProfile
import  hashlib
from tools.sms import YunTongXin
from django.core.cache import cache
#异常码范围 10100 - 10199

#django提供了一个装饰器 method_decorator可以装饰我们自己的函数的装饰器转化为方法的装饰器


#FBV
@logging_check
def users_views(request,username):   #修改头像

    if request.method != 'POST':
        result = {'code':10103,'error':'Please use POST'}
        return  JsonResponse(result)

    user = request.myuser  #校验器中配置的值，一定是已经登录的用户信息

    avatar = request.FILES['avatar']
    print(avatar)
    user.avatar = avatar
    user.save()
    return  JsonResponse({'code':200})



#更灵活，可继承
class UserViews(View):

    def get(self,request,username=None):  #个人信息页访问的接口
        #/v1/users
        if username:
            #/v1/users/xxxxx
            try:
                user = UserProfile.objects.get(username =username)
            except Exception as e:
                result = {'code':10102,'error':'The username is wrong'}
                return  JsonResponse(result)
            result = {'code':200,'username':username,'data':{
                'info':user.info,'sign':user.sign,'nickname':user.nickname,'avatar':str(user.avatar),
                'email':user.email
            }}
            return  JsonResponse(result)
        else:
            pass


    def post(self,request):   #注册
        json_str = request.body
        json_obj = json.loads(json_str)  #处理post请求中的数据
        print(json_obj)
        username = json_obj['username']
        email = json_obj['email']
        password_2 = json_obj['password_2']
        password_1 = json_obj['password_1']
        phone = json_obj['phone']
        identifying = json_obj['identifying']

        if password_1 != password_2:
            result = {'code':10100,'error':'the password is not same'}
            return JsonResponse(result)

        #比对验证码是否正确
        # old_identifying = cache.get('sms_%s'%(phone))
        # if not old_identifying:  #验证码过期
        #     result = {'code':'10110','error':'The code is wrong'}
        #     return JsonResponse(result)
        #
        # if int(identifying) != old_identifying:   #验证码不对
        #     result = {'code':'10111','error':'The code is wrong'}
        #     return JsonResponse(result)


        #检查用户名是否可用
        old_users = UserProfile.objects.filter(username=username)
        if old_users:
            result = {'code': 10101, 'error': 'the account has exists'}
            return JsonResponse(result)

        #处理密码
        p_m = hashlib.md5()
        p_m.update(password_1.encode())  #将字符窜转为字节串
        UserProfile.objects.create(username=username,nickname=username,password=p_m.hexdigest(),email=email,phone=phone,role = identifying)

        #赋值权限
        newUserPermList = ['0','1','2','3']
        for item in newUserPermList:
            userObj = UserProfile.objects.get(username=username)
            perObj = Permissions.objects.get(code=item)
            userPerm.objects.create(user=userObj, permission=perObj)

        #参数基本检查
        #检查用户名是否可用
        #result = {'code':10100,'error':'The username already existed'}
        #return JsonResponse(result)
        #UserProfile插入数据(密码要md5存储)
        result = {'code':200, 'username':username, 'data':{}}
        return JsonResponse(result)

    @method_decorator(logging_check)
    def put(self,request,username=None):   #put请求用于修改用户数据，post用于新建数据，get用于获取用户数据
        #更新用户数据
        json_str = request.body
        json_obj = json.loads(json_str)

        user = request.myuser   #直接从装饰器中取用户信息

        user.sign = json_obj['sign']
        user.info = json_obj['info']
        user.nickname = json_obj['nickname']
        user.email = json_obj['email']

        user.save()
        return  JsonResponse({'code':200})


def sms_view(request):  #短信验证
    if request.method != "POST":
        result={'code':10108,'error':'Please use POST'}
        return JsonResponse(result)

    json_str = request.body
    json_obj = json.loads(json_str)
    phone = json_obj['phone']

    #生成随机验证码
    code = random.randint(1000,9999)
    print(code)
    #存储随机码 pip django_redis
    cache_key = 'sms_%s'%(phone)
    #检查是否已经有发过的且未过期的验证码
    old_code = cache.get(cache_key)
    if old_code:
        return JsonResponse({'code':10111,'error':'The code is already existed'})



    cache.set(cache_key,code,60)
    #发送随机码->短信
    # send_sms(phone,code)  #加判定，正常码是000000

    #celery版
    send_sms_celery.delay(phone,code)
    return JsonResponse({'code':200})

def send_sms(phone,code):
    config = {
        "accountSid": settings.ACCOUNTSID,
        "accountToken": settings.ACCOUNTTOKEN,
        "appId": settings.APPID,
        "templateId": settings.TEMPLATEID
    }
    yun = YunTongXin(**config)  # **变为关键字传参
    res = yun.run(phone,code)
    return res
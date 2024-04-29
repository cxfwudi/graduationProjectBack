import jwt
from django.http import JsonResponse

from django.conf import settings

from user.models import UserProfile


def logging_check(func):   #校验token
    def wrap(request,*args,**kwargs):
        #获取token request.META.get('HTTP_AUTHORIZATION')
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code':403,'error':'Please login'}
            return  JsonResponse(result)

        #校验token
        try:
            res = jwt.decode(token,settings.JWT_TOKEN_KEY,algorithms='HS256') #返回的是payload部分
        except Exception as e:
            print('jwt decode error is %s'%(e))
            result = {'code':403,'error':'Please login'}
            return  JsonResponse(result)
        #获取用户登录
        username = res['username']
        user = UserProfile.objects.get(username=username)
        request.myuser = user    #通过request向视图（views）传递用户
        #失败，code 403 error :Pleasr login


        return func(request, *args, **kwargs)
    return  wrap


def get_user_by_request(request):   #为获取用户文章列表准备，判断访问者的身份
    #尝试性获取登录用户
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        res =jwt.decode(token,settings.JWT_TOKEN_KEY,algorithms='HS256')
    except Exception as e:
        return None

    username = res['username']
    user = UserProfile.objects.get(username=username)
    return user
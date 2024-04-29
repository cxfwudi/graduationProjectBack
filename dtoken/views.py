import json
from django.conf import settings
from django.http import JsonResponse
from user.models import UserProfile
from django.shortcuts import render
import hashlib
import time
import jwt
#异常码 10200-10299
# Create your views here.

def tokens(request):  #登录
    if(request.method != "POST"):
        result = {'code':10200,'error':'Please use POST'}
        return JsonResponse(result)

    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    password = json_obj['password']
    role = json_obj['role']

    #校验账户密码
    try:
        user = UserProfile.objects.get(username=username)
    except Exception as e:
        result = {'code':10201,'error':'the username is not exists'}
        return JsonResponse(result)

    # 校验用户身份是否对应
    if user.role != role:
        result = {'code': 10202, 'error': 'The user name does not correspond to the identity'}
        return JsonResponse(result)

    p_m = hashlib.md5()
    p_m.update(password.encode())
    if p_m.hexdigest() != user.password:  #比对密码
        result = {'code':10203,'error':'the username or password is wrong'}
        return  JsonResponse(result)
    #记录会话状态
    token = make_token(username)   #生成token
    result = {'code':200,'username':username,'data':{'token':token}}
    return JsonResponse(result)

def make_token(username,expire=3600*24):
    key = settings.JWT_TOKEN_KEY
    now_t = time.time()

    payload_data = {'username':username,'exp':now_t + expire}  #用户名和过期时间
    return  jwt.encode(payload_data,key,algorithm='HS256')
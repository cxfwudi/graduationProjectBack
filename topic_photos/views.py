from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from django.utils.decorators import method_decorator  #转换装饰器，视图类到函数,函数可以直接@加装饰器，类要加个转换器
from tools.logging_dec import logging_check,get_user_by_request    #token校验
from django.views import View
from topic.models import Topic
from topic_photos.models import Photos
from user.models import UserProfile
#异常码10700-10799



class TopicPhotosViews(View):

    @method_decorator(logging_check)
    def post(self,request,author_id):  #新建图片,发表文章或者修改文章时才调用这个接口
        author = request.myuser   #登录者

        visitor = get_user_by_request(request)  # 访问者身份获取，从token中获取
        visitor_username = None
        if visitor:
            visitor_username = visitor.username
            print(visitor_username)
        else:
            result = {'code': 10702, 'error': 'please login in'}
            return JsonResponse(result)

        if visitor_username != author_id:
            result = {'code':10703,'error':'permission denied'}
            return JsonResponse(result)

        files = request.FILES.getlist('files')  #获取数组
        t_id = request.GET.get('t_id')  # 取?后的参数
        if t_id:  #修改文章图片，传输formdata格式数据发put请求后端拿不到数据？？？
            t_id = int(t_id)
            topic = Topic.objects.get(id=t_id)
            Topic.objects.filter(id=t_id).update(has_photos=True)

        else:  #新建文章图片
            topic = Topic.objects.latest('id')   #获取最新的文章
            Topic.objects.filter(id=topic.id).update(has_photos = True)



        for item in files:
            print(item)
            Photos.objects.create(
                content=item,
                topic=topic
            )

        return JsonResponse({'code':200})

    @method_decorator(logging_check)
    def delete(self,request,author_id):  #删除图片
        try:
            author = UserProfile.objects.get(username=author_id)  # 博主用户名
        except Exception as e:
            result = {'code': 10709, 'error': 'The author is not existed'}
            return JsonResponse(result)

        visitor = get_user_by_request(request)  # 访问者身份获取，从token中获取
        visitor_username = None
        if visitor:
            visitor_username = visitor.username
            print(visitor_username)
        else:
            result = {'code': 10708, 'error': 'please login in'}
            return JsonResponse(result)

        photo_id = request.GET.get('photo_id')  # 取?后的参数  这个参数一定要有
        t_id = request.GET.get('t_id')
        print("*****")
        print(t_id)
        photo_id = int(photo_id)

        if author_id != visitor_username:  # 只能自己修改自己的
            result = {'code': 10707, 'error': 'permission denied'}
            return JsonResponse(result)


        Photos.objects.filter(id=photo_id).delete()


        update_topic = Topic.objects.get(id=t_id)
        topic_has_photo = Photos.objects.filter(topic=update_topic)
        if not topic_has_photo.exists():
            Topic.objects.filter(id=t_id).update(has_photos = False)


        return JsonResponse({'code':200})


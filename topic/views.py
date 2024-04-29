import json

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator  #转换装饰器，视图类到函数,函数可以直接@加装饰器，类要加个转换器
from django.views.decorators.cache import cache_page
from tools.cache_dec import cache_set
from tools.logging_dec import logging_check,get_user_by_request    #token校验
# Create your views here.
#异常码 10300-10399
from django.views import View
from message.models import Message
from topic.models import Topic
from user.models import UserProfile
from topic_photos.models import Photos


class Random_topic(View):
    #用于给主页返回一些展示的文章
    def make_topics_res(self,author_topics):  # 文章列表
        # {‘code’:200,’data’:{‘nickname’:’abc’, ’topics’:[
        #     {‘id’:1,’title’:’a’, ‘category’: ‘tec’, ‘created_time’: ‘2018 - 0
        # 9 - 03 10: 30:20’, ‘introduce’: ‘aaa’, ‘author’:’abc’}]}}
        res = {'code': 200, 'data': {}}
        topics_res = []
        for topic in author_topics:
            d = {}
            t_photo = Photos.objects.filter(topic = topic)
            photo_content = []
            for item in t_photo:
                photo_content.append(str(item.content))

            d['photos'] = photo_content
            d['id'] = topic.id
            d['title'] = topic.title
            d['category'] = topic.category
            d['created_time'] = topic.created_time.strftime("%Y-%m-%d %H:%M:%S")
            d['introduce'] = topic.introduce
            d['author'] = topic.author_id
            d['author_avatar'] = str(topic.author.avatar)

            topics_res.append(d)
        res['data']['topics'] = topics_res

        return res


    def get(self,request):
        page = request.GET.get('page')
        if not page:
            random_topic = Topic.objects.filter(has_photos=True,limit = 'public')[:10]
        else:
            page = int(page)
            print(page)
            random_topic = Topic.objects.filter(has_photos=True,limit = 'public')[page:page + 6]

        res = self.make_topics_res(random_topic)
        return JsonResponse(res)




class TopicViews(View):
    #缓存代码再看一遍！！！ （）（）（）删除博客时也要删除缓存
    def clear_topics_caches(self,request):  #清空缓存中的key，有用户来找新的（在发表文章时）
        path = request.path_info   #不带查询字符串的路由
        cache_key_p = ['topic_cache_self_','topic_cache_']  #url的前缀，前缀是在装饰器中自己加的
        cache_key_h = ['?category=all','?category=tec','?category=no-tec'] #url的后缀
        all_keys = []
        for key_p in cache_key_p:
            for key_h in cache_key_h:
                all_keys.append(key_p + path + key_h)

        cache.delete_many(all_keys)  #批量删除所有key为all_keys的数据（在缓存中）
        #用户可能使用自己的身份或者游客身份访问科技文章或非科技文章


    def make_topic_res(self,author,author_topic,is_self):  #is_self为true则博主访问自己
        '''{
            "code": 200,
            "data": {
                "nickname": "guoxiaonao",
                "title": "我的第一次",
                "category": "tec",
                "created_time": "2019-06-03 10:08:04",
                "content": "<p>我的第一次，哈哈哈哈哈<br></p>",
                "introduce": "我的第一次，哈哈哈哈哈",
                "author": "guoxiaonao",
                "next_id": 2,
                "next_title": "我的第二次",
                "last_id": null,
                "last_title": null,
                "messages": [],
                "messages_count": 0
            }
        }
        '''

        if is_self:
            #博主访问自己
            next_topic = Topic.objects.filter(id__gt=author_topic.id,author = author).first()  #id__gt意思是id大于
            last_topic = Topic.objects.filter(id__lt=author_topic.id,
                                              author=author).last() #取文章id大于当前文章id并且属于当前访问用户的文章
        else:  #游客访问
            next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author,limit='public').first()  # id__gt意思是id大于
            last_topic = Topic.objects.filter(id__lt=author_topic.id,
                                              author=author,limit='public').last()  # 取文章id大于当前文章id并且属于当前访问用户的文章

        next_id = next_topic.id if next_topic else None
        next_title = next_topic.title if next_topic else ''
        last_id = last_topic.id if last_topic else None
        last_title = last_topic.title if last_topic else ''

        #关联留言和回复
        all_messages = Message.objects.filter(topic=author_topic).order_by('-created_time')
        msg_ist = []   #留言
        rep_dic = {}    #留言的回复
        m_count  = 0
        for msg in all_messages:
            if msg.parent_message:
                #回复
                m_count += 1
                rep_dic.setdefault(msg.parent_message,[])
                rep_dic[msg.parent_message].append({'msg_id':msg.id,'publisher':msg.publisher.nickname,'publisher_avatar':str(msg.publisher.avatar),
                                                    'content':msg.content,'created_time':msg.created_time.strftime('%Y-%m-%d %H:%M:%S')})
            else:
                #留言
                m_count += 1
                msg_ist.append({'id':msg.id,'publisher':msg.publisher.nickname,'publisher_avatar':str(msg.publisher.avatar),
                                                    'content':msg.content,'created_time':msg.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                                'reply':[]})

        for m in msg_ist:   #m['id']对应msg.parent_message
            if m['id'] in rep_dic:
                m['reply'] = rep_dic[m['id']]

        photo_list = Photos.objects.filter(topic = author_topic)
        photo_data = []
        for item in photo_list:
            photo_item = {}
            photo_item['id'] = item.id
            photo_item['content'] = str(item.content)
            photo_data.append(photo_item)

        res = {'code':200,'data':{}}
        res['data']['nickname'] = author.nickname
        res['data']['title'] = author_topic.title
        res['data']['category'] = author_topic.category
        res['data']['limit'] = author_topic.limit
        res['data']['created_time'] = author_topic.created_time.strftime("%Y-%m-%d %H:%M:%S")
        res['data']['content'] = author_topic.content
        res['data']['content_text'] = author_topic.content_text  #带样式
        res['data']['introduce'] = author_topic.introduce
        res['data']['author'] = author.nickname
        res['data']['last_id'] = last_id
        res['data']['last_title'] = last_title
        res['data']['next_id'] = next_id
        res['data']['next_title'] = next_title
        res['data']['messages'] = msg_ist
        res['data']['messgaes_count'] = m_count
        res['data']['topic_photos'] = photo_data
        return res

    def make_topics_res(self,author,author_topics):   #文章列表
        # {‘code’:200,’data’:{‘nickname’:’abc’, ’topics’:[
        #     {‘id’:1,’title’:’a’, ‘category’: ‘tec’, ‘created_time’: ‘2018 - 0
        # 9 - 03 10: 30:20’, ‘introduce’: ‘aaa’, ‘author’:’abc’}]}}
        res = {'code':200,'data':{}}
        topics_res = []
        for topic in author_topics:
            d={}
            t_photo = Photos.objects.filter(topic=topic)
            photo_content = []
            for item in t_photo:
                photo_content.append(str(item.content))
            d['photos'] = photo_content
            d['id'] = topic.id
            d['title'] = topic.title
            d['category'] = topic.category
            d['created_time'] = topic.created_time.strftime("%Y-%m-%d %H:%M:%S")
            d['introduce'] = topic.introduce
            d['author'] = author.nickname

            topics_res.append(d)

        res['data']['topics'] = topics_res
        res['data']['nickname'] = author.nickname
        return res


    @method_decorator(logging_check)
    def post(self,request,author_id):
        author = request.myuser
        #取出前端数据，创建topic数据
        json_str = request.body
        json_obj = json.loads(json_str)   #将字典型json串转化为json字典
        title = json_obj['title']
        content = json_obj['content']  #带样式
        content_text = json_obj['content_text']  #纯内容
        introduce = content_text[:30]   #列表页展示（文章的简略描述）
        limit = json_obj['limit']
        category = json_obj['category']
        if limit not in ['public','private']:  #limit必须为这两种之一，哪两种可自己设置
            result = {'code':10300,'error':'The limit error'}
            return JsonResponse(result)
         #创建topic数据
        Topic.objects.create(title=title,content = content_text,content_text=content,
                             limit = limit,category = category,introduce = introduce,
                             author=author
                             )

        self.clear_topics_caches(request)  #发表文章时删除缓存
        return JsonResponse({'code':200})

    @method_decorator(logging_check)
    def put(self,request,author_id):
        #修改文章
        #异常吗10501-10600
        try:
            author = UserProfile.objects.get(username=author_id)  #博主用户名
            # print("author"+author)
        except Exception as e:
            result = {'code':10501,'error':'The author is not existed'}
            return JsonResponse(result)

        visitor = get_user_by_request(request)   #访问者身份获取，从token中获取
        visitor_username = None
        if visitor:
            visitor_username = visitor.username
            print(visitor_username)
        else:
            result = {'code':10502,'error':'please login in'}
            return JsonResponse(result)

        t_id = request.GET.get('t_id')   #取?后的参数  这个参数一定要有
        t_id = int(t_id)

        if author_id != visitor_username:  #只能自己修改自己的
            print("here")
            result = {'code':10602,'error':'permission denied'}
            return JsonResponse(result)

        # 取出前端数据，创建topic数据
        json_str = request.body
        json_obj = json.loads(json_str)  # 将字典型json串转化为json字典
        title = json_obj['title']
        content = json_obj['content']
        content_text = json_obj['content_text']   #不带html标签的
        introduce = content_text[:30]  # 列表页展示（文章的简略描述）
        limit = json_obj['limit']
        category = json_obj['category']
        if limit not in ['public', 'private']:  # limit必须为这两种之一，哪两种可自己设置
            result = {'code': 10300, 'error': 'The limit error'}
            return JsonResponse(result)

        Topic.objects.filter(id = t_id).update(
            title = title,
            category = category,
            limit = limit,
            introduce = introduce,
            content = content_text,
            content_text = content
        )
        return JsonResponse({'code':200})


    @method_decorator(logging_check)
    def delete(self,request,author_id): #author_id是用户名
        #删除文章
        #异常码 10400-10500
        try:
            author = UserProfile.objects.get(username=author_id)
            # print("author"+author)
        except Exception as e:
            result = {'code':10402,'error':'The author is not existed'}
            return JsonResponse(result)

        visitor = get_user_by_request(request)   #访问者身份获取，从token中获取
        visitor_username = None
        if visitor:
            visitor_username = visitor.username
            print(visitor_username)
        else:
            result = {'code':10402,'error':'please login in'}
            return JsonResponse(result)

        t_id = request.GET.get('t_id')   #取?后的参数  这个参数一定要有
        t_id = int(t_id)
        print(t_id)
        if visitor_username == author_id:  #判断是否是自己
            Topic.objects.filter(id=t_id).delete()
        else:
            result = {'code':10403,'error':'permission denied'} #没有权限
            return result
        self.clear_topics_caches(request)  #删除缓存
        return JsonResponse({'code':200})

    @method_decorator(cache_set(2))
    def get(self,request,author_id):   #不需要装饰器，谁都能访问,request可取？后面的值，author_id是路径中的值
        #author_id当前登录的用户名
        #访问者 visitor
        #当前被访问博主的博客 author

        print(author_id)
        try:
            author = UserProfile.objects.get(username=author_id)
            # print("author"+author)
        except Exception as e:
            result = {'code':10301,'error':'The author is not existed'}
            return JsonResponse(result)

        visitor = get_user_by_request(request)   #访问者身份获取，从token中获取
        visitor_username = None
        if visitor:
            visitor_username = visitor.username
            print(visitor_username)


        t_id = request.GET.get('t_id')   #取?后的参数
        if t_id:
            #获取指定文章数据
            t_id = int(t_id)
            is_self = False
            if visitor_username == author_id:  #博主访问自己的文章详情页
                is_self = True
                try:
                    author_topic = Topic.objects.get(id=t_id,author_id=author_id)
                except Exception as e:
                    result = {'code':10302,'error':'NO topic'}
                    return JsonResponse(result)
            else:  #其他人访问自己的文章详细信息，只能访问公开的
                try:
                    author_topic = Topic.objects.get(id=t_id,author_id=author_id,limit = 'public')
                except Exception as e:
                    result = {'code':10303,'error':'NO topic'}
                    return JsonResponse(result)
            res = self.make_topic_res(author,author_topic,is_self)
            return JsonResponse(res)
        else:
            #获取文章列表页数据
            # /v1/topics/xby?page=1
            # /v1/topics/xby?page=1&category=[tec|no-tec]
            print("111")
            category = request.GET.get('category')
            page = request.GET.get('page')

            if page:

                page = int(page)
                author_topics_all = Topic.objects.filter(author_id=author_id)
                print(author_topics_all[0])
                print(category)
                if category in ['tec','no-tec']: #按照文章类型分类
                    if visitor_username == author_id:
                        #博主访问自己的博客
                        author_topics = Topic.objects.filter(author_id=author_id,category=category).order_by('-updated_time')[(page-1)*10:(page-1)*10+10]
                    else:
                        author_topics = Topic.objects.filter(author_id=author_id,limit='public',category=category).order_by('-updated_time')[(page-1)*10:(page-1)*10+10]
                else:  #没有按照文章类型分类，获取全部类型
                    if visitor_username == author_id:   #visitor_username 获取问题 注意：author与author_id不一样
                        #博主访问自己的博客
                        print("访问自己")
                        author_topics = Topic.objects.filter(author_id=author_id).order_by('-updated_time')[(page-1)*10:(page-1)*10+10]
                    else:
                        print("访问他人")
                        print(visitor_username,author)
                        author_topics = Topic.objects.filter(author_id=author_id,limit='public').order_by('-updated_time')[(page-1)*10:(page-1)*10+10]

                print("xxxxxx",author_topics)
                res = self.make_topics_res(author,author_topics)
                print(len(author_topics_all))
                res['data']['total'] = len(author_topics_all)
                return JsonResponse(res)
            else:
                if category in ['tec', 'no-tec']:  # 按照文章类型分类
                    if visitor_username == author_id:
                        # 博主访问自己的博客
                        author_topics = Topic.objects.filter(author_id=author_id, category=category)
                    else:
                        author_topics = Topic.objects.filter(author_id=author_id, limit='public', category=category)
                else:  # 没有按照文章类型分类，获取全部类型
                    if visitor_username == author_id:  # visitor_username 获取问题 注意：author与author_id不一样
                        # 博主访问自己的博客
                        author_topics = Topic.objects.filter(author_id=author_id)
                    else:
                        print(visitor_username, author)
                        author_topics = Topic.objects.filter(author_id=author_id, limit='public')

                res = self.make_topics_res(author, author_topics)
                return JsonResponse(res)
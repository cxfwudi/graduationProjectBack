from .logging_dec import get_user_by_request
from django.core.cache import cache
#文章列表缓存的装饰器
#传参的装饰器需要三层def
def cache_set(expire):
    def _cache_set(func):
        #func背装饰的函数
        def wrapper(request, *args, **kwargs):  #这个参数就是视图的参数
            #区分场景，只做列表页
            print("args",args,"kwargs",kwargs)
            if 't_id' in request.GET:
                #当前请求是获取文章列表页
                return func(request, *args, **kwargs)
            #生成出正确的 cache_key [访客访问 和 博主访问]
            visitor_user = get_user_by_request(request)   #拿出访问者
            visitor_username = None
            if visitor_user:
                visitor_username = visitor_user.username
            author_usernmae = kwargs['author_id']
            print('visitor is %s'%(visitor_username))
            print('author is %s'%(author_usernmae))

            full_path = request.get_full_path()   #返回带有查询字符串的url
            if visitor_username == author_usernmae:
                cache_key = 'topic_cache_self_%s'%(full_path)
            else:
                cache_key = 'topic_cache_%s' %(full_path)   #游客访问
            print('cache_key is %s'%(cache_key))
            #判断是否有缓存，有缓存则直接返回
            res = cache.get(cache_key)
            if res:
                print('----cache in----')
                return res
            #执行视图
            res = func(request, *args, **kwargs)   #拿到视图的返回
            #存储缓存  cache对象/set/get
            cache.set(cache_key,res,expire)   #向redis中存储key为cache_key，值为res的键值对
            #返回响应

            return res
        return wrapper
    return _cache_set
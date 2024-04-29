
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import topic
from . import views
from django.conf import settings
from user import views as user_views
from dtoken import views as dtoken_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test_cors/',views.test_cors),
    path('v1/users',user_views.UserViews.as_view()),  #path方法第二个参数只能为函数，.UserViews.as_view()可以将类中的方法转为函数
    path('v1/users/',include('user.urls')),
    path('v1/tokens',dtoken_views.tokens),
    path('v1/topics/',include('topic.urls')),
    path('v1/messages/',include('message.urls')),
    path('v1/topicPhotos/',include('topic_photos.urls')),
    path('v1/permission/',include('user_perm.urls'))
]
#解决头像上传的问题，MEDIA_URL相当于一个文件路由，
#请求过来之后会在MEDIA_ROOT下找相应的文件资源
urlpatterns += static(settings.MEDIA_URL,document_root = settings
                      .MEDIA_ROOT)
from django.urls import path
from . import views
urlpatterns = [
    #v1/users/sms  注册时用户名为sms的用户不可用
    path('sms',views.sms_view),
    path('<str:username>',views.UserViews.as_view()),  #视图类
    path('<str:username>/avatar',views.users_views),  #视图函数
]
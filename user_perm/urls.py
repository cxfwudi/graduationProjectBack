from django.urls import path
from . import views

urlpatterns = [
    path('',views.PermissionManage.as_view())
]
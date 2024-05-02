from django.urls import path
from . import views

urlpatterns = [
    path('',views.UserCollect.as_view())
]
from django.urls import path
from . import views

urlpatterns = [
    path('',views.UserFavorite.as_view())
]
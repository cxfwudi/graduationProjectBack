from django.urls import path

from topic import views

urlpatterns = [
    path('<str:author_id>',views.TopicViews.as_view()),
    path('',views.Random_topic.as_view())
]
from django.urls import path

from topic_photos import views

urlpatterns = [
    path('<str:author_id>',views.TopicPhotosViews.as_view())
]
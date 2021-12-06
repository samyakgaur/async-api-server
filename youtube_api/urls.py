from django.urls import path
from youtube_api.views import (youtube_topic,
                               youtube_api_key,
                               select_topic,
                               youtube_video_list,
                               youtube_video_list_api)

app_name = 'youtube_api'

urlpatterns = [
    path('topic/', youtube_topic, name='topic'),
    path('topic/<int:topic_id>', select_topic, name='select-topic'),
    path('key/', youtube_api_key, name='key'),
    path('video/', youtube_video_list, name='video-list'),
    path('api/video/', youtube_video_list_api, name='video-list-api'),
]

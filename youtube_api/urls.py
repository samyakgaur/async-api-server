from django.urls import path
from youtube_api.views import (test,
                               youtube_topic,
                               youtube_api_key,
                               select_topic,
                               youtube_video_list)

app_name = 'youtube_api'

urlpatterns = [
    path('', test, name='test'),
    path('topic/', youtube_topic, name='topic'),
    path('topic/<int:topic_id>', select_topic, name='select-topic'),
    path('key/', youtube_api_key, name='key'),
    path('video/', youtube_video_list, name='video-list'),

]

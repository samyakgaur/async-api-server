from django.urls import path
from youtube_api.views import test

app_name = 'youtube_api'

urlpatterns = [
    path('', test, name='test')
]

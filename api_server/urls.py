from django.contrib import admin
from django.urls import path, include
from youtube_api.views import youtube_topic

urlpatterns = [
    path('admin/', admin.site.urls),
    path('youtube/', include('youtube_api.urls')),
    path('', youtube_topic, name='home'),
]

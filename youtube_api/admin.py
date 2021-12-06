from django.contrib import admin
from youtube_api.models import (YoutubeAPI,
                                YoutubeTopic,
                                YoutubeData)

admin.site.register(YoutubeAPI)
admin.site.register(YoutubeTopic)
admin.site.register(YoutubeData)

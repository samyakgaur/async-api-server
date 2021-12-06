from rest_framework import serializers
from youtube_api.models import YoutubeData


class YoutubeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeData
        fields = '__all__'

from django.db import models


class YoutubeAPI(models.Model):
    ''' This will store users
        API key for making requests
        to the youtube api server
    '''

    key = models.CharField(max_length=120)

    def __str__(self):
        return self.key


class YoutubeTopic(models.Model):
    ''' Topics for youtube api
    '''
    topic = models.CharField(max_length=128)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "%s : %s" % (self.topic, self.active)


class YoutubeData(models.Model):
    ''' This will store data
        fetched by the youtube api.
    '''

    topic = models.ForeignKey(YoutubeTopic, on_delete=models.PROTECT)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    published_at = models.DateTimeField()
    thumbnail_url = models.CharField(max_length=1000)
    video_id = models.CharField(max_length=64, unique=True)
    channel_title = models.CharField(max_length=64)

    def __str__(self):
        return self.title

    @property
    def get_video_url(self):
        return ("https://www.youtube.com/watch?v=%s" % (self.video_id))

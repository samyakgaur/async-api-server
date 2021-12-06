from youtube_api.models import YoutubeAPI, YoutubeData, YoutubeTopic
import requests
from datetime import datetime, timedelta
import urllib.parse
from pytz import timezone
from celery import shared_task


@shared_task(bind=True)
def sync_data(self):
    '''Purpose: Celery-Beat task to keep syncing data
    every 30 mins.
    '''
    fetch_data_wrapper()
    return


def get_start_time():
    '''Purpose: Calculate time for api calls
    start time = Time(now) - 30 mins
    '''
    local_timezone = timezone('Asia/Kolkata')
    lt_past_hour = datetime.now(local_timezone) + timedelta(minutes=-30)
    start_time = str(lt_past_hour.replace(tzinfo=local_timezone)).split(' ')
    return f"{start_time[0]}T{start_time[1][:-6]}Z"


def save_data(response_data, topic_obj):
    '''Purpose: Saves response data into YoutubeData
    Model making sure there is no duplicate entry.
    '''
    for item in response_data:
        try:
            YoutubeData(
                topic=topic_obj,
                title=item["snippet"]["title"],
                description=item["snippet"]["description"],
                published_at=item["snippet"]["publishedAt"],
                thumbnail_url=item["snippet"]["thumbnails"]["high"]["url"],
                video_id=item["id"]["videoId"],
                channel_title=item["snippet"]["channelTitle"],
            ).save()
        except Exception as e:
            '''As video_id is a unique field,
            we will skip any duplicate entry.
            '''
            print(e)
            continue


def fetch_data_wrapper():
    '''Purpose: Wrapper class with the main purpose of rotating
    API Keys if one starts getting error due to hit rate.
    '''
    keys = YoutubeAPI.objects.all()
    order = "date"
    max_results = 50
    topic_obj = YoutubeTopic.objects.filter(active=True).first()
    topic = urllib.parse.quote_plus(topic_obj.topic)
    published_after = get_start_time()
    try:
        '''Iterating over the saved api_keys for a safe fallback
        mechanism if api call with one api_key is unsuccessfull
        '''
        for key in keys:
            response = fetch_data(key,
                                  order,
                                  topic,
                                  max_results,
                                  published_after)
            if response.status_code == 400:
                '''Request failed, retry with a new API Key'''
                print("Key has expired, trying new key")
                continue
            if response.status_code == 200:
                '''Request was successfull, save the response'''
                save_data(response.json()["items"], topic_obj)
                break
    except Exception as e:
        print(e)


def fetch_data(key, order, topic, maxResults, publishedAfter):
    '''Purpose: API call to youtube.
    '''
    url = f"https://youtube.googleapis.com/youtube/v3/search?" \
          f"part=snippet&" \
          f"maxResults={maxResults}&" \
          f"order={order}&" \
          f"publishedAfter={publishedAfter}&" \
          f"q={topic}&" \
          f"type=video&" \
          f"key={key}"
    return requests.get(url=url)

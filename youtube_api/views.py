from django.shortcuts import render, HttpResponseRedirect
from datetime import datetime, timezone, timedelta
from youtube_api.models import YoutubeAPI, YoutubeData, YoutubeTopic
from youtube_api.api_call import fetch_data


def test(request):
    publishedAfter = get_start_time()
    print(publishedAfter)
    topic = YoutubeTopic.objects.filter(active=True).first()
    key = YoutubeAPI.objects.first()
    max_results = 50
    order = "date"
    data = fetch_data(key, order, topic, max_results, publishedAfter)
    print(data.json())
    return render(request, 'youtube_api/video_list.html', context={})


def get_start_time():
    utc_past_hour = datetime.utcnow() + timedelta(minutes=-3000000)
    my_time = str(utc_past_hour.replace(tzinfo=timezone.utc)).split(' ')
    return f"{my_time[0]}T{my_time[1][:-6]}Z"


def youtube_topic(request):
    if request.method == 'POST':
        topic = request.POST.get("youtube_topic", "")
        if topic != "":
            YoutubeTopic.objects.create(topic=topic, active=False)
    topics = YoutubeTopic.objects.all()
    context = {
        'topics': topics,
    }
    return render(request, 'youtube_api/topic_list.html', context)


def select_topic(request, topic_id):
    selected_topic = YoutubeTopic.objects.filter(active=True)
    for topic in selected_topic:
        topic.active = False
        topic.save()
    topic = YoutubeTopic.objects.get(id=topic_id)
    topic.active = True
    topic.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def youtube_api_key(request):
    if request.method == 'POST':
        key = request.POST.get("api_key", "")
        if key != "":
            YoutubeAPI.objects.create(key=key)
    keys = YoutubeAPI.objects.all()
    context = {
        'keys': keys,
    }
    return render(request, 'youtube_api/api_key_list.html', context)


def youtube_video_list(request):
    topic = YoutubeTopic.objects.filter(active=True).first()
    videos = YoutubeData.objects.filter(topic=topic)
    context = {
        'videos': videos
    }
    return render(request, 'youtube_api/video_list.html', context)
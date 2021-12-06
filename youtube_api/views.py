from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Q
from youtube_api.models import YoutubeAPI, YoutubeData, YoutubeTopic
from youtube_api.api_call import fetch_data_wrapper
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from youtube_api.serailizer import YoutubeDataSerializer
from django.core.paginator import Paginator


def youtube_topic(request):
    '''Purpose: List view for saved topics.
    It also handles creation of new topic.
    '''
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
    '''Purpose: It selects a particular topic for feed.
    It enables support for multiple topics for the user.
    Cron Job: If there are no topics initially, we also start a async
    job to keep updating the active topic feed.
    '''
    selected_topic = YoutubeTopic.objects.filter(active=True)
    for topic in selected_topic:
        topic.active = False
        topic.save()
    topic = YoutubeTopic.objects.get(id=topic_id)
    topic.active = True
    topic.save()
    if not selected_topic:
        # start sync because this is the first time any topic is selected
        schedule, _ = IntervalSchedule.objects.get_or_create(
                            every=1800, period=IntervalSchedule.SECONDS)
        PeriodicTask.objects.create(
            interval=schedule,
            name='Sync Data',
            task='youtube_api.api_call.sync_data')
    fetch_data_wrapper()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def youtube_api_key(request):
    '''Purpose: API Key create and view.
    '''
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
    ''' Purpose: This is a list view for the user youtube data.
    It also has a search feature so that user can search a particular
    video of his choice.
    '''
    topic = YoutubeTopic.objects.filter(active=True).first()
    search_q = request.GET.get('search_q')
    if search_q is not None:
        lookup = Q(topic=topic) and (
            Q(title__icontains=search_q) | Q(description__icontains=search_q))
        videos = YoutubeData.objects.filter(lookup)
    else:
        videos = YoutubeData.objects.filter(topic=topic)
    context = {
        'videos': videos
    }
    return render(request, 'youtube_api/video_list.html', context)


def youtube_video_list_api(request):
    ''' Purpose: API endpoint for api services.
    It gives user to search based on title/ description.
    It supports pagination.
    '''
    topic = YoutubeTopic.objects.filter(active=True).first()
    title_q = request.GET.get('title')
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    else:
        page_number = int(page_number)
    try:
        # Queryset building
        if title_q is not None:
            lookup = Q(topic=topic) and (
                Q(title__icontains=title_q) | Q(
                    description__icontains=title_q))
        else:
            lookup = Q(topic=topic)
        search_results = YoutubeData.objects.filter(
                            lookup).order_by('-published_at')

        # Pagination
        paginator = Paginator(search_results, 25)
        page_obj = paginator.get_page(page_number)
        if page_number > paginator.num_pages:
            page_number = paginator.num_pages

        # Serializer
        serialized_results = YoutubeDataSerializer(
                                page_obj.object_list, many=True)

        return JsonResponse(
            {"total pages": paginator.num_pages,
             "page": page_number,
             "response": serialized_results.data
             })
    except Exception as e:
        print(e)
        return JsonResponse({"success": "failed", "result": e})

from django.shortcuts import render


def test(request):
    return render(request, 'youtube_api/video_list.html', context={})

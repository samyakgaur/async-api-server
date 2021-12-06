import requests


def fetch_data(key, order, topic, maxResults, publishedAfter):
    url = f"https://youtube.googleapis.com/youtube/v3/search?" \
          f"part=snippet&" \
          f"maxResults={maxResults}&" \
          f"order={order}&" \
          f"publishedAfter={publishedAfter}&" \
          f"q={topic}&" \
          f"key={key}"

    return requests.get(url=url)

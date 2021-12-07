# 📦 Youtube Lite
## Follow what you like without getting distracted!

Youtube Lite is a unique service enabling you to follow topics you like on youtube and get updated about the latest video on that topic, so that you can watch it in peace.

- Simple and basic ✨
- No more distractions 🧘🏼‍♂️

## Features

- 🚀 Get and search Paginated API Support.
- 💡 Rotating API Keys for uninterrupted update!
- 📝 Follow multiple topics.
- 🏆 Robust search support

What do people have to say about youtube?

> Opening up YouTube can be a risky business. While YouTube can help you learn, it's also a site where clicking on one video can send you down a rabbit hole filled with screaming goats, mad music videos, and one extremely grumpy cat.


## Tech

- [Django] - Webserver.
- [Django Rest Framework] - API Building.
- [Celery] - Syncing data.
- [Docker] - Deployment.
- [Bootstrap] - Frontend.


## Installation

Clone the github repository.

Run the following commands.

```
docker-compose build
docker-compose up -d
```
All the required services will be up by now!

After running the above commands:
- Visit `http://127.0.0.1:8000/youtube/key/`
        Add youtube API Keys. Make sure you add 2-3 API Keys to ensure uninterrupted feed.
![Screenshot 2021-12-07 at 1 54 59 PM](https://user-images.githubusercontent.com/13183316/144993132-0b67db03-72ae-45b9-8ed7-c4e0903ab030.png)

- Visit `http://127.0.0.1:8000/youtube/topic/`
        Add a topic by clicking on `Add Topic` button. Then click on the `select` button to select the topic
![Screenshot 2021-12-07 at 1 56 19 PM](https://user-images.githubusercontent.com/13183316/144993355-1cdb0638-fde2-4c61-a8ad-aa7071a561c4.png)

- Visit `http://127.0.0.1:8000/youtube/video/`
   You should see the data flowing in!
![Screenshot 2021-12-07 at 1 56 51 PM](https://user-images.githubusercontent.com/13183316/144993443-cc16bd11-3957-4db3-8306-1dcdd6d8e959.png)


## API Support

Youtube Lite also provides you with on-the-go API for Get and Search purpose.

URL : `http://127.0.0.1:8000/youtube/api/video`
Method: `GET`

| Parameters | description |
| ------ | ------ |
| `page` | Jump to specific page |
| `title` | Provide a search query |

Note: Make sure you send in url encoded search query for accurate results.

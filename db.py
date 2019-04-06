import pymongo
import os
from linebot.models import (
    BubbleContainer, CarouselContainer, ImageComponent,
    BoxComponent, TextComponent, SpacerComponent, ButtonComponent, URIAction)

#  Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname

uri = os.getenv('DB_URL', None)
client = pymongo.MongoClient(uri)
db = client.get_default_database()


def get_video():
    Video = db['Video']
    video_list = list(Video.aggregate([{"$sample": {'size': 7}}]))
    template = CarouselContainer(
        contents=[]
    )
    for x in range(0, 7):
        title = video_list[x]['title']
        url = video_list[x]['url']
        thumbnails = video_list[x]['thumbnails']
        template = add_video(template, title, url, thumbnails)

    print(template.contents[2])
    return template


def add_video(template, title, url, thumbnails):
    bubble = BubbleContainer(
        direction='ltr',
        hero=ImageComponent(
            url=thumbnails,
            size='full',
            aspect_ratio='20:13',
            aspect_mode='cover',
            gravity='center'
        ),
        body=BoxComponent(
            layout='vertical',
            contents=[
                # title
                TextComponent(
                    text=title,
                    wrap=True,
                    weight='bold',
                    size='xxl',
                    align='center'
                )

            ]
        ),
        footer=BoxComponent(
            layout='vertical',
            spacing='sm',
            contents=[
                SpacerComponent(size='sm'),
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(
                        label='點擊查看',
                        uri=url
                    ),
                )
            ]
        ),
    )
    template.contents.append(bubble)
    return template

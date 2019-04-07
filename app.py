from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    MessageAction, URIAction,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton, CarouselContainer
)

from db import get_video
import os

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)

app = Flask(__name__)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    print(request)
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    user_id = event.source.user_id
    print(user_id)
    print(text)
    if text == '自我介紹':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://i.imgur.com/RXQnxHs.jpg',
                size='3xl',
                aspect_mode='cover',
                gravity='center',
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    SeparatorComponent(margin='xxl'),
                    # title
                    TextComponent(
                        text='張書維 Vicharm Chang',
                        weight='bold',
                        size='xl',
                        align='center',
                        margin='lg'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='程式語言',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=2
                                    ),
                                    TextComponent(
                                        text='Python, C, C++',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='學籍',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=2
                                    ),
                                    TextComponent(
                                        text="台大電機所計算機組,碩一",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='畢業學校',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=2
                                    ),
                                    TextComponent(
                                        text="成功大學資訊工程學系",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),

                        ],
                    ),
                    TextComponent(
                        text='學習軟體程式8年 對軟體開發有極大興趣',
                        color='#666666',
                        size='sm',
                        margin='lg'
                    ),

                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    SpacerComponent(size='sm'),
                    ButtonComponent(
                        style='primary',
                        color='#6D5546',
                        height='sm',
                        action=MessageAction(label='查看專案', text='開發專案經驗'),
                    ),
                    ButtonComponent(
                        style='primary',
                        color='#6D5546',
                        height='sm',
                        action=MessageAction(label='自我推薦', text='自我推薦'),
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="自我介紹", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif text == '開發專案經驗':
        carousel = CarouselContainer(
            contents=[
                BubbleContainer(
                    direction='ltr',
                    hero=ImageComponent(
                        url='https://i.imgur.com/kj7UJcl.jpg',
                        size='full',
                        aspect_ratio='20:13',
                        aspect_mode='cover',
                        gravity='center'
                    ),
                    body=BoxComponent(
                        margin='lg',
                        layout='vertical',
                        contents=[
                            # title
                            TextComponent(text='Konma Bot', wrap=True,
                                          weight='bold', size='xxl', align='center'),
                            # info
                            BoxComponent(
                                margin='lg',
                                layout='vertical',
                                spacing='sm',
                                contents=[
                                    BoxComponent(
                                        layout='baseline',
                                        spacing='sm',
                                        contents=[
                                            IconComponent(
                                                url='https://i.imgur.com/YMxsgqo.png'),
                                            TextComponent(
                                                text='毛孩影片推播',
                                                color='#666666',
                                                size='sm',
                                            ),
                                        ]
                                    ),
                                    BoxComponent(
                                        layout='baseline',
                                        spacing='sm',
                                        contents=[
                                            IconComponent(
                                                url='https://i.imgur.com/gtkZuKm.png'),
                                            TextComponent(
                                                text='領養送養查詢',
                                                color='#666666',
                                                size='sm',
                                            ),
                                        ]
                                    ),
                                    BoxComponent(
                                        layout='baseline',
                                        spacing='sm',
                                        contents=[
                                            IconComponent(
                                                url='https://i.imgur.com/zALcrA5.png'),
                                            TextComponent(
                                                text='寵物知識問答',
                                                color='#666666',
                                                size='sm',
                                            ),
                                        ]
                                    ),
                                    BoxComponent(
                                        layout='baseline',
                                        spacing='sm',
                                        contents=[
                                            IconComponent(
                                                url='https://i.imgur.com/0lRYfH6.png'),
                                            TextComponent(
                                                text='飼主交友分享',
                                                color='#666666',
                                                size='sm',
                                            ),
                                        ]
                                    ),
                                ]
                            )
                        ],
                    ),
                    footer=BoxComponent(
                        layout='vertical',
                        spacing='sm',
                        contents=[
                            SpacerComponent(size='sm'),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='試玩影片推播功能', text='試玩Konma Bot'),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=URIAction(
                                    label='查看github專案',
                                    uri='https://github.com/changsuwi/Konma-Chatbot'),
                            )
                        ]
                    ),
                ),
                BubbleContainer(
                    direction='ltr',
                    hero=ImageComponent(
                        url='https://live.staticflickr.com/949/27294712367_63f3db8890_z_d.jpg',
                        size='full',
                        aspect_ratio='20:13',
                        aspect_mode='cover',
                        gravity='center'
                    ),
                    body=BoxComponent(
                        layout='vertical',
                        contents=[
                            # title
                            TextComponent(text='Bon Voyage', wrap=True,
                                          weight='bold', size='xxl', align='center'),
                            # info
                            BoxComponent(
                                margin='lg',
                                layout='vertical',
                                spacing='sm',
                                contents=[
                                    BoxComponent(
                                        layout='baseline',
                                        spacing='sm',
                                        contents=[
                                            IconComponent(
                                                url='https://i.imgur.com/syxg5cD.png'),
                                            TextComponent(
                                                text='串接google map api 做資料視覺化',
                                                color='#666666',
                                                size='sm',
                                                flex=1
                                            ),
                                        ]
                                    ),
                                    BoxComponent(
                                        layout='baseline',
                                        spacing='sm',
                                        contents=[
                                            IconComponent(
                                                url='https://i.imgur.com/Ye12a4V.png'),
                                            TextComponent(
                                                text='直觀查看熱門景點動態',
                                                color='#666666',
                                                size='sm',
                                                flex=1
                                            ),
                                        ]
                                    ),
                                    BoxComponent(
                                        layout='baseline',
                                        spacing='sm',
                                        contents=[
                                            IconComponent(
                                                url='https://i.imgur.com/spcJLhA.png'),
                                            TextComponent(
                                                text="上傳圖片，與其他使用者分享",
                                                wrap=True,
                                                color='#666666',
                                                size='sm',
                                                flex=1,
                                            ),
                                        ]
                                    ),

                                ]
                            ),
                        ],
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
                                    label='查看專案github',
                                    uri='https://github.com/changsuwi/Travel-Photography'
                                ),
                            ),
                        ]
                    ),
                ),
                BubbleContainer(
                    direction='ltr',
                    hero=ImageComponent(
                        url='https://i.imgur.com/kj7UJcl.jpg',
                        size='full',
                        aspect_ratio='20:13',
                        aspect_mode='cover',
                        gravity='center'
                    ),
                    footer=BoxComponent(
                        layout='vertical',
                        spacing='sm',
                        contents=[
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=URIAction(
                                    label='查看其他github專案',
                                    uri='https://github.com/changsuwi'),
                            )
                        ]
                    ),
                ),


            ]
        )
        message = FlexSendMessage(alt_text="開發專案經驗", contents=carousel)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif text == '自我推薦':
        bubble = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='選擇我的原因',
                        weight='bold',
                        size='xxl',
                        margin='md',
                        align='center'
                    ),
                    SeparatorComponent(margin='xxl'),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=[
                            TextComponent(
                                text='1. Chatbot與其他軟體開發經驗豐富',
                                margin='md',
                                size='sm'
                            ),
                            TextComponent(
                                text='2. 對於computer science學科相當熟悉',
                                margin='md',
                                size='sm'
                            ),
                            TextComponent(
                                text='3. 學習速度快，可以快速進入狀況',
                                margin='md',
                                size='sm'
                            ),
                            TextComponent(
                                text='4. 有團隊開發經驗，縮小溝通成本',
                                margin='md',
                                size='sm'
                            ),
                        ]
                    )

                ]
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    SpacerComponent(size='sm'),
                    ButtonComponent(
                        style='primary',
                        color='#6D5546',
                        height='sm',
                        action=MessageAction(
                            label='查看自我介紹',
                            text='自我介紹'
                        ),
                    ),
                    ButtonComponent(
                        style='primary',
                        color='#6D5546',
                        height='sm',
                        action=MessageAction(
                            label='查看開發專案',
                            text='開發專案經驗'
                        ),
                    ),
                ]
            ),
        )
        message = FlexSendMessage(alt_text="自我推薦", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message)
    elif text == '試玩Konma Bot':
        message = FlexSendMessage(alt_text="試玩Konma Bot", contents=get_video())

        line_bot_api.reply_message(
            event.reply_token,
            message
        )

        message = TextSendMessage(
            text='想看更多',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(
                            label='更多寵物影片',
                            text='試玩Konma Bot'
                        )
                    ),
                    QuickReplyButton(
                        action=MessageAction(
                            label='自我推薦',
                            text='自我推薦'
                        )
                    ),
                    QuickReplyButton(
                        action=MessageAction(
                            label='開發專案經驗',
                            text='開發專案經驗'
                        )
                    ),
                ]

            )
        )

        line_bot_api.push_message(
            user_id,
            message
        )


if __name__ == "__main__":
    app.run()

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('sW9cP4130kybxXUWVKrLnp06v7rhzY2V0pNWs8Pmo0LF5J/C1hAn1Y7XgWX6+luddR7U3OQE614Hhr6zmzVI1mpvIIQMljeFFqplIDl8TVe4QKxNyHUOz8+1MCQZSObHMOF31TK6dvQ1iZiu5MwnXwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('145c6a9fb6eb012167e855eded6e7545')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
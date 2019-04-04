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

line_bot_api = LineBotApi('7XdV+zWeK2sqgmM1abJTy8Y2U/fF2UZlm8DErSwkogmmqQtGMH8SchzRpXICf7MmdR7U3OQE614Hhr6zmzVI1mpvIIQMljeFFqplIDl8TVcf1d0lqUqfIg8uB3y2u4qZUB0biEIKAHHYggJbN1NDhwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('06683b6bdb33cb015066b5a5017142bd')


@app.route("/callback", methods=['POST'])
def callback():
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
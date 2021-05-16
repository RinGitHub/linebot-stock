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

line_bot_api = LineBotApi('kK3nS0J1mu0oDHuFs+W+CFjYLYhDmKOxK2tIaE4YdN7lw4lzhhEEuSqNUvjXimGjc+QW20XzcU+Xy8OID2CLN1AmpnkF6+wIgTN2DokyzpodhyYVMgAK/i2BGvxH+u+iS/hWBqeLIbqBGLzseGdY0QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('77fdb87ee576fcbee74ebebb7c4d416b')


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

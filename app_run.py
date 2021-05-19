# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta, datetime
from pymongo import MongoClient

# ref: http://twstock.readthedocs.io/zh_TW/latest/quickstart.html#id2
import twstock

import matplotlib

matplotlib.use('Agg')  # ref: https://matplotlib.org/faq/howto_faq.html

import matplotlib.pyplot as plt
import pandas as pd

from imgurpython import ImgurClient

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi(
    'kK3nS0J1mu0oDHuFs+W+CFjYLYhDmKOxK2tIaE4YdN7lw4lzhhEEuSqNUvjXimGjc+QW20XzcU+Xy8OID2CLN1AmpnkF6'
    '+wIgTN2DokyzpodhyYVMgAK/i2BGvxH+u+iS/hWBqeLIbqBGLzseGdY0QdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('77fdb87ee576fcbee74ebebb7c4d416b')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        eve = parser.parse(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    for event in eve:
        if isinstance(event, MessageEvent):
            text = event.message.text
            if text.startswith('#'):
                text = text[1:]
                content = ''

                stock_rt = twstock.realtime.get(text)
                my_datetime = datetime.fromtimestamp(stock_rt['timestamp'] + 8 * 60 * 60)
                my_time = my_datetime.strftime('%H:%M:%S')

                content += '%s (%s) %s\n' % (
                    stock_rt['info']['name'],
                    stock_rt['info']['code'],
                    my_time)
                content += '現價: %s / 開盤: %s\n' % (
                    stock_rt['realtime']['latest_trade_price'],
                    stock_rt['realtime']['open'])
                content += '最高: %s / 最低: %s\n' % (
                    stock_rt['realtime']['high'],
                    stock_rt['realtime']['low'])
                content += '量: %s\n' % (stock_rt['realtime']['accumulate_trade_volume'])

                stock = twstock.Stock(text)  # twstock.Stock('2330')
                content += '-----\n'
                content += '最近五日價格: \n'
                price5 = stock.price[-5:][::-1]
                date5 = stock.date[-5:][::-1]
                for i in range(len(price5)):
                    # content += '[%s] %s\n' %(date5[i].strftime("%Y-%m-%d %H:%M:%S"), price5[i])
                    content += '[%s] %s\n' % (date5[i].strftime("%Y-%m-%d"), price5[i])
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=content)
                )

            elif text.startswith('/'):
                text = text[1:]
                fn = '%s.png' % text
                stock = twstock.Stock(text)
                my_data = {'close': stock.close, 'date': stock.date, 'open': stock.open}
                df1 = pd.DataFrame.from_dict(my_data)

                df1.plot(x='date', y='close')
                plt.title('[%s]' % stock.sid)
                plt.savefig(fn)
                plt.close()

            # -- upload
            # imgur with account: your.mail@gmail.com
            client_id = '219e4677b4d2110'
            client_secret = '69f161c63fe23108f9f77498f72dd3c50c7adedd'

            client = ImgurClient(client_id, client_secret)
            print("Uploading image... ")
            image = client.upload_from_path(fn, anon=True)
            print("Done")

            url = image['link']
            image_message = ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )

            line_bot_api.reply_message(
                event.reply_token,
                image_message
            )

    return 'OK'


'''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
'''

if __name__ == "__main__":
    app.run()

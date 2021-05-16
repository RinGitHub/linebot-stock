# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# import configparser

from flask import Flask, render_template
from linebot import (
    LineBotApi, WebhookHandler
)

app = Flask(__name__)
# config = configparser.ConfigParser()
# config.read("config.ini")

'''
line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])
client_id = config['imgur_api']['Client_ID']
client_secret = config['imgur_api']['Client_Secret']
album_id = config['imgur_api']['Album_ID']
API_Get_Image = config['other_api']['API_Get_Image']


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def index():
    return render_template('index.html', data=" Deploying a Flask App To Heroku");'''


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # app.run(debug=True)
    print("hello")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

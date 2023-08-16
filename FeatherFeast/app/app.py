# -*- coding: utf-8 -*-
'''
Create Date: 2023/08/13
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.2
'''

import json
from pyimgur import Imgur
from datetime import datetime
from flask import Flask, request, abort
from flasgger import Swagger
from flasgger import LazyString
from flasgger import LazyJSONEncoder
from flasgger import swag_from
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.models import TextMessage
from linebot.models import ImageMessage
from linebot.models import VideoMessage
from linebot.models import AudioMessage
from linebot.models.events import FollowEvent
from linebot.models.events import MessageEvent
from linebot.exceptions import LineBotApiError
from linebot.exceptions import InvalidSignatureError
from os.path import join
from os.path import dirname
from os.path import abspath

app = Flask(__name__)
swagger = Swagger(app)

config_dir = join(dirname(abspath(__file__)), '..', '..', 'config')
line_bot_config_path = join(config_dir, 'linebot.conf')
line_bot_config = json.load(open(line_bot_config_path, 'r', encoding='utf8'))
imgur_config_path = join(config_dir, 'imgur.conf')
imgur_config = json.load(open(imgur_config_path, 'r', encoding='utf8'))

CURRENT_DATE = datetime.today().strftime('%Y%m%d')
LINE_BOT_API = LineBotApi(line_bot_config['CHANNEL_ACCESS_TOKEN'])
HANDLER = WebhookHandler(line_bot_config['CHANNEL_SECRET'])
IMGUR_CLIENT = Imgur(imgur_config["client_id"], imgur_config["client_secret"])
USER_LOG_PATH = join(dirname(abspath(__file__)), '..', '..', 'log', CURRENT_DATE)

def start_flask() -> None:
    app.run(port=6006, debug=True)

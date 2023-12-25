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
from FeatherFeast.config.config import get_config

app = Flask(__name__)
swagger = Swagger(app)

line_bot_api, handler, imgur_client = get_config()
print(line_bot_api)
print(handler)
print(imgur_client)

current_date = datetime.today().strftime('%Y%m%d')
user_log_path = join(dirname(abspath(__file__)), '..', '..', 'log', current_date)

def start_flask() -> None:
    app.run(
        port=6006, 
        # debug=True,
    )

# -*- coding: utf-8 -*-
'''
Create Date: 2023/08/16
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.2
'''

import json
from typing import Tuple
from pyimgur import Imgur
from os.path import join
from os.path import dirname
from os.path import abspath
from linebot import LineBotApi
from linebot import WebhookHandler

def get_config() -> Tuple[LineBotApi, WebhookHandler, Imgur]:
    config_dir = join(dirname(abspath(__file__)), '..', '..', 'config')
    line_bot_config_path = join(config_dir, 'linebot.conf')
    line_bot_config = json.load(open(line_bot_config_path, 'r', encoding='utf8'))
    imgur_config_path = join(config_dir, 'imgur.conf')
    imgur_config = json.load(open(imgur_config_path, 'r', encoding='utf8'))

    line_bot_api = LineBotApi(line_bot_config['CHANNEL_ACCESS_TOKEN'])
    handler = WebhookHandler(line_bot_config['CHANNEL_SECRET'])
    imgur_client = Imgur(imgur_config["client_id"], imgur_config["client_secret"])

    return line_bot_api, handler, imgur_client
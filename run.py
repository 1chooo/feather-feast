# -*- coding: utf-8 -*-
'''
Create Date: 2023/07/26
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.2
'''

import os
import json
from flask import Flask, request, abort
from FeatherFeast import Drama
from linebot import LineBotApi
from linebot import WebhookHandler

app = Flask(__name__)

config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.', 'config')
config_path = os.path.join(config_dir, 'linebot.conf')
line_bot_config = json.load(open(config_path, 'r', encoding='utf8'))

LINE_BOT_API = LineBotApi(line_bot_config['CHANNEL_ACCESS_TOKEN'])
HANDLER = WebhookHandler(line_bot_config['CHANNEL_SECRET'])

def start_flask() -> None:
    app.run(port=5002)

def main() -> None:
    start_flask()

if __name__ == '__main__':
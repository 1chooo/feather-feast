from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    ImagemapSendMessage, TextSendMessage,
    ImageSendMessage, LocationSendMessage,
    FlexSendMessage, VideoSendMessage,
    StickerSendMessage, AudioSendMessage,
    ImageMessage, VideoMessage,
    AudioMessage, TextMessage,
    TemplateSendMessage, MessageTemplateAction
)
from linebot.models.template import (
    ButtonsTemplate, CarouselTemplate,
    ConfirmTemplate, ImageCarouselTemplate
)
from linebot.models.template import *
from linebot.models.events import (
    FollowEvent, MessageEvent
)
import os
import pandas as pd
from numpy import NaN
import math
from flask import Flask, request, abort, jsonify
import datetime
import json

def TestFunc() -> None:

    print('Hello template generator')

def buttons_template_generator() -> 'TemplateSendMessage':
    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            title='Menu',
            text='請選擇地區',
            actions=[
                MessageTemplateAction(
                    label='選項一',
                    text='option one',
                ),
                MessageTemplateAction(
                    label='option two',
                    text='選項二',
                )
            ]
        )
    )
    return buttons_template_message

# def buttons_template_generator(alt_text, title, text, label1, text1) -> 'TemplateSendMessage':

#     return

# alt_text, title, text, label1, text1, label2, text2

# buttons_template_message = TemplateSendMessage(
#     alt_text='Buttons template',
#     template=ButtonsTemplate(
#         title='Menu',
#         text='請選擇地區',
#         actions=[
#             MessageTemplateAction(
#                 label='選項一',
#                 text='option one',
#             ),
#             MessageTemplateAction(
#                 label='option two',
#                 text='選項二',
#             )
#         ]
#     )
# )

# print(buttons_template_message)
# -*- coding: utf-8 -*-
'''
Create Date: 2023/07/26
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.2
'''

import os
import json
from datetime import datetime
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.models import TextSendMessage
from linebot.models import ImageCarouselTemplate
from linebot.models import ImageCarouselColumn
from linebot.models import TemplateSendMessage
from linebot.models import ImageSendMessage
from linebot.models import ImagemapSendMessage
from linebot.models import StickerSendMessage
from linebot.models import AudioSendMessage
from linebot.models import LocationSendMessage
from linebot.models import FlexSendMessage
from linebot.models import VideoSendMessage
from linebot.models import MessageTemplateAction
from linebot.models import PostbackAction
from linebot.models import MessageAction
from linebot.models import URIAction
from linebot.models import QuickReplyButton
from linebot.models import LocationAction
from linebot.models import DatetimePickerAction
from linebot.models import RichMenuSwitchAction
from linebot.models import CarouselColumn
from linebot.models.template import CarouselTemplate
from linebot.models.template import ButtonsTemplate
from linebot.models.template import ConfirmTemplate
from linebot.models.events import MessageEvent
import pymysql

def json_to_line_messages(json_object_array) -> list:
    
    return_array = []

    for json_object in json_object_array:
        try:
            message_type = json_object['type']
        except KeyError:
            print('JSON object does not contain "type" attribute:', json_object)
            continue
          
        
        try:
            if message_type == 'text':
                return_array.append(
                    TextSendMessage.new_from_json_dict(json_object))
            elif message_type == 'imagemap':
                return_array.append(
                    ImagemapSendMessage.new_from_json_dict(json_object))
            elif message_type == 'template':
                return_array.append(
                    TemplateSendMessage.new_from_json_dict(json_object))
            elif message_type == 'image':
                return_array.append(
                    ImageSendMessage.new_from_json_dict(json_object))
            elif message_type == 'sticker':
                return_array.append(
                    StickerSendMessage.new_from_json_dict(json_object))  
            elif message_type == 'audio':
                return_array.append(
                    AudioSendMessage.new_from_json_dict(json_object))  
            elif message_type == 'location':
                return_array.append(
                    LocationSendMessage.new_from_json_dict(json_object))
            elif message_type == 'flex':
                return_array.append(
                    FlexSendMessage.new_from_json_dict(json_object))  
            elif message_type == 'video':
                return_array.append(
                    VideoSendMessage.new_from_json_dict(json_object)) 
            else:
                print('Unknown message type:', message_type)
        except:
            print('Failed to create Line message from JSON object:', json_object)
          
    return return_array


""" Find the repliance from the Excel, then turn them into the message."""

def find_drama_by_keyword(user_input_keyword) -> list:

    result = plot_content[plot_content['keyword'] == user_input_keyword]
    result_dict=result.to_dict()

    for field in result_dict.keys():
        for key in result_dict[field].keys():
            result_dict[field]= result_dict[field][key]
    
    reply_json_array=[]
    combin_json_array=[
        'reply_message1',
        'reply_message2',
        'reply_message3',
        'reply_message4',
        'reply_message5'
    ]

    for ele in combin_json_array:
        if pd.isna(result_dict[ele]) is False:
            print(result_dict[ele])
            reply_json_array.append(json.loads(result_dict[ele]))
            print(reply_json_array)

    if pd.isna(result_dict['choice_button']) is False:
        reply_json_array[len(reply_json_array)-1].update(json.loads(result_dict['choice_button']))

    reply_message_array = json_to_line_messages(reply_json_array)
    # print(reply_message_array)

    return reply_message_array
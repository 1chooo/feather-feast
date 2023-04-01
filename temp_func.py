from flask import Flask, request, abort, jsonify
import datetime
import json
import config
import os
import pandas as pd
from numpy import NaN
import math
import json
import sys
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
# Import the message type of the line bot
from linebot.models import (
    ImagemapSendMessage, TextSendMessage,
    ImageSendMessage, LocationSendMessage,
    FlexSendMessage, VideoSendMessage,
    StickerSendMessage, AudioSendMessage,
    ImageMessage, VideoMessage,
    AudioMessage, TextMessage,
    TemplateSendMessage, QuickReply
)

# Import the action type of the line bot
from linebot.models import (
    MessageTemplateAction, PostbackAction,
    MessageAction, URIAction, QuickReplyButton
)
from linebot.models.template import (
    ButtonsTemplate, CarouselTemplate,
    ConfirmTemplate, ImageCarouselTemplate
)
from linebot.models.template import *
from linebot.models.events import (
    FollowEvent, MessageEvent
)



def json_to_line_messages(json_object_array) -> list:
    
    # json_object = json.loads(json_objectString)
    return_array = []


    # 讀取其用來判斷的元件
    for json_object in json_object_array:
        json_object_type = json_object.get('type')
          
        # 轉換
        if json_object_type == 'text':
            return_array.append(
                TextSendMessage.new_from_json_dict(json_object))
        elif json_object_type == 'imagemap':
            return_array.append(
                ImagemapSendMessage.new_from_json_dict(json_object))
        elif json_object_type == 'template':
            return_array.append(
                TemplateSendMessage.new_from_json_dict(json_object))
        elif json_object_type == 'image':
            return_array.append(
                ImageSendMessage.new_from_json_dict(json_object))
        elif json_object_type == 'sticker':
            return_array.append(
                StickerSendMessage.new_from_json_dict(json_object))  
        elif json_object_type == 'audio':
            return_array.append(
                AudioSendMessage.new_from_json_dict(json_object))  
        elif json_object_type == 'location':
            return_array.append(
                LocationSendMessage.new_from_json_dict(json_object))
        elif json_object_type == 'flex':
            return_array.append(
                FlexSendMessage.new_from_json_dict(json_object))  
        elif json_object_type == 'video':
            return_array.append(
                VideoSendMessage.new_from_json_dict(json_object))   

    """__list comprehension__
    return_array = [TextSendMessage.new_from_json_dict(o) 
                    if o.get('type') == 'text'     else ImagemapSendMessage.new_from_json_dict(o) 
                    if o.get('type') == 'imagemap' else TemplateSendMessage.new_from_json_dict(o) 
                    if o.get('type') == 'template' else ImageSendMessage.new_from_json_dict(o) 
                    if o.get('type') == 'image'    else StickerSendMessage.new_from_json_dict(o) 
                    if o.get('type') == 'sticker'  else AudioSendMessage.new_from_json_dict(o) 
                    if o.get('type') == 'audio'    else LocationSendMessage.new_from_json_dict(o) 
                    if o.get('type') == 'location' else FlexSendMessage.new_from_json_dict(o) 
                    if o.get('type') == 'flex'     else VideoSendMessage.new_from_json_dict(o)
                    for o in json_object_array]
    """
 
          
    return return_array

def detect_json_array_to_new_message_array(jsonObjectArray) -> list:
    
    returnArray = []

    # 使用列表生成式快速轉換JSON物件
    messageObjects = [getattr(sys.modules[__name__], f"{j['type'].capitalize()}SendMessage").new_from_json_dict(j) for j in jsonObjectArray if j.get('type')]

    # 將轉換後的訊息陣列加入returnArray
    returnArray.extend(messageObjects)

    return returnArray

plot_content = pd.read_excel("./bearbear.xlsx")

def drama_execl_to_json(user_input_keyword) -> list:

    result = plot_content[plot_content['keyword'] == user_input_keyword]
    result_dict = {field: result[field].iloc[0] for field in result.columns}

    reply_json_array = []
    combin_json_array = [
        'reply_message1',
        'reply_message2',
        'reply_message3',
        'reply_message4',
        'reply_message5'
    ]

    for ele in combin_json_array:
        if pd.notna(result_dict[ele]):
            reply_json_array.append(json.loads(result_dict[ele]))

    if pd.notna(result_dict['choice_button']):
        reply_json_array[-1].update(json.loads(result_dict['choice_button']))

    reply_message_array = json_to_line_messages(reply_json_array)

    return reply_message_array

app = Flask(__name__)

@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event) -> None:
    
    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)
        
    # 將用戶資訊存在檔案內
    file_path = user_log_path + '/users-info.txt'
    with open(file_path, "a") as myfile:
        print(json.dumps(vars(user_profile)))
        myfile.write(json.dumps(vars(user_profile),sort_keys=True))
        myfile.write('\n')
    
    # # 回覆文字消息與圖片消息
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage('安安，我們成功成為好友了！')
    # )


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event) -> None:

    if len(drama_execl_to_json(event.message.text)) != 0 :
        line_bot_api.reply_message(
            event.reply_token,
            drama_execl_to_json(event.message.text)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage('此物件沒有劇情設計')
        )

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event) -> None:

    """
        inform the handler when the message event is
        image message do the below things.
    """

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Image has Upload'+ ' ' + event.message.id+'\n'+'你好啊！你的照片被我拿走了')
    )
    
    message_content = line_bot_api.get_message_content(event.message.id)

    file_path = user_log_path + '/img/'
    check_dir(file_path)
    output_path = get_output_path(file_path, current_date, event.message.id, '.jpg')

    with open(output_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)




@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event) -> None:

    """
        inform the handler when the message event is
        audio message do the below things.
    """

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Audio has Upload'+ ' ' + event.message.id))
    
    message_content = line_bot_api.get_message_content(event.message.id)

    file_path = user_log_path + '/audio/'
    check_dir(file_path)
    output_path = get_output_path(file_path, current_date, event.message.id, '.mp3')
    with open(output_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)



def handle_video_message(event) -> None:

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Video has Upload'+ ' ' + event.message.id))

    message_content = line_bot_api.get_message_content(event.message.id)

    file_path = user_log_path + '/video/'
    check_dir(file_path)

    output_path = get_output_path(file_path, current_date, event.message.id, '.mp4')

    with open(output_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)



@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event) -> None:

    try:

        messages = find_drama_by_keyword(event.message.text)
        if messages:
            line_bot_api.reply_message(
                event.reply_token, 
                messages)
        else:
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage('此物件沒有劇情設計'))
            
    except Exception as e:

        print(f"Error occurred: {e}")
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage('我們目前還不能辨識您的這則訊息\n或許可以試試看別的內容哦～'))
# -*- coding: utf-8 -*-

""" 
Import the package we need. 
"""

from flask import Flask, request, abort, jsonify
import datetime
import json
import config
import os
import pandas as pd
from numpy import NaN
import math
import json
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
    AudioMessage, TextMessage
)
from linebot.models.template import (
    ButtonsTemplate, CarouselTemplate,
    ConfirmTemplate, ImageCarouselTemplate
)
from linebot.models.template import *
from linebot.models.events import (
    FollowEvent, MessageEvent
)


# connect to the line bot api and the handler
line_bot_api = LineBotApi(config.line_bot_api)
handler = WebhookHandler(config.handler)

"""
    load the drama story with the Excel
"""

plot_content = pd.read_excel("./bearbear.xlsx")

"""
    Get the current date to record the behaviors
    of users.
"""
def check_dir(file_path) -> None:

    if not os.path.isdir(file_path):
        os.mkdir(file_path, mode=0o777)
        print(file_path, 'has been created successfully.')

    return None

def get_output_path(file_path, current_date, id, type) -> str:

    output_path = file_path + current_date + '_' + id + type

    return output_path


current_date = datetime.datetime.today().strftime('%Y%m%d')
user_log_path = "./log/" + current_date


check_dir(user_log_path)

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


""" start the server """

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback() -> str:

    """__start server__
        start the sever and open the route
        callback that we can get request.
    """

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)

    # record users' log
    file_path = user_log_path + '/user-event.log'
    with open(file_path, 'a') as output_file:
      output_file.write(body)
      output_file.write('\n')

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

"""
    撰寫用戶關注時，我們要處理的商業邏輯

    1. 取得用戶個資，並存回伺服器
    2. 回應用戶，歡迎用的文字消息
"""



# inform the handler when the message event is
# follow event do the below things.
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event) -> None:
    
    # 取出消息內User的資料
    try:
        user_profile = line_bot_api.get_profile(event.source.user_id)
    except LineBotApiError as e:
        # 處理取得 user profile 失敗的情況
        print(f"LineBotApiError: {e}")
        return
    
    # 將用戶資訊存在檔案內
    file_path = user_log_path + '/users-info.txt'
    with open(file_path, "a") as myfile:
        try:
            print(json.dumps(vars(user_profile)))
            myfile.write(json.dumps(vars(user_profile),sort_keys=True))
            myfile.write('\n')
        except Exception as e:
            # 處理寫檔失敗的情況
            print(f"Error: {e}")
            return
    
    # # 回覆文字消息與圖片消息
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage('安安，我們成功成為好友了！')
    # )





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


"""
    Get the image message from the user 
    when they send to the bot; also, send 
    the tips to alert them we get the 
    image message.
"""

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):

    """
        inform the handler when the message event is
        image message do the below things.
    """
    # 回覆訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Image has been Uploaded ' + 
            event.message.id + 
            '\non ' + 
            str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
    )

    # 下載照片
    try:
        message_content = line_bot_api.get_message_content(event.message.id)

        file_path = user_log_path + '/img/'
        check_dir(file_path)

        output_path = get_output_path(file_path, current_date, event.message.id, '.jpg')

        with open(output_path, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)

    except LineBotApiError as e:
        # 如果發生例外，記錄錯誤訊息
        print('Unable to get message content: ' + str(e))


"""
    Get the audio message from the user 
    when they send to the bot; also, send 
    the tips to alert them we get the 
    audio message.
"""

@handler.add(MessageEvent, message=AudioMessage)
def handle_image_message(event):

    """
        inform the handler when the message event is
        audio message do the below things.
    """
    # 回覆訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Audio has been Uploaded ' + 
            event.message.id + 
            '\non ' +
            str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
    )

    # 下載照片
    try:
        message_content = line_bot_api.get_message_content(event.message.id)

        file_path = user_log_path + '/audio/'
        check_dir(file_path)

        output_path = get_output_path(file_path, current_date, event.message.id, '.mp3')

        with open(output_path, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)

    except LineBotApiError as e:
        # 如果發生例外，記錄錯誤訊息
        print('Unable to get message content: ' + str(e))

"""
    Get the video message from the user 
    when they send to the bot; also, send 
    the tips to alert them we get the 
    video message.
"""

# inform the handler when the message event is
# video message do the below things.
@handler.add(MessageEvent, message=VideoMessage)
def handle_image_message(event):

    """
        inform the handler when the message event is
        video message do the below things.
    """
    # 回覆訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Video has been Uploaded ' + 
            event.message.id + 
            '\non ' +
            str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
    )

    # 下載照片
    try:
        message_content = line_bot_api.get_message_content(event.message.id)

        file_path = user_log_path + '/video/'
        check_dir(file_path)

        output_path = get_output_path(file_path, current_date, event.message.id, '.mp3')

        with open(output_path, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)

    except LineBotApiError as e:
        # 如果發生例外，記錄錯誤訊息
        print('Unable to get message content: ' + str(e))

def main() -> None: 

    # Web server.
    if __name__ == '__main__':
        app.run(port=5002)

main()
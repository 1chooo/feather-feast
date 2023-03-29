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
    LineBotApi, 
    WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    ImagemapSendMessage,
    TextSendMessage,
    ImageSendMessage,
    LocationSendMessage,
    FlexSendMessage,
    VideoSendMessage,
    StickerSendMessage,
    AudioSendMessage,
    ImageMessage,
    VideoMessage,
    AudioMessage,
    TextMessage
)
from linebot.models.template import (
    ButtonsTemplate,
    CarouselTemplate,
    ConfirmTemplate,
    ImageCarouselTemplate
)
from linebot.models.template import *
from linebot.models.events import (
    FollowEvent,
    MessageEvent
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
current_date = datetime.datetime.today().strftime('%Y%m%d')
user_log_path = "./log/" + current_date

if not os.path.isdir(user_log_path):
    os.mkdir(user_log_path, mode=0o777)
    print(user_log_path, 'has been created successfully.')

def detect_json_array_to_new_message_array(jsonObjectArray) -> list:
    
    # jsonObject = json.loads(jsonObjectString)
    returnArray = []


    # 讀取其用來判斷的元件
    for jsonObject in jsonObjectArray:
        message_type = jsonObject.get('type')
          
        # 轉換
        if message_type == 'text':
            returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'imagemap':
            returnArray.append(ImagemapSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'template':
            returnArray.append(TemplateSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'image':
            returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'sticker':
            returnArray.append(StickerSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'audio':
            returnArray.append(AudioSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'location':
            returnArray.append(LocationSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'flex':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'video':
            returnArray.append(VideoSendMessage.new_from_json_dict(jsonObject))    
          
    return returnArray

"""### Find the repliance from the Excel, then turn them into the message."""



def drama_execl_to_json(user_input_keyword) -> list:

    result = plot_content[plot_content['keyword']==user_input_keyword]
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

    reply_message_array = detect_json_array_to_new_message_array(reply_json_array)

    return reply_message_array

"""### start the server"""

app = Flask(__name__)

# start the sever and open the route
# that we can get request.
@app.route("/callback", methods=['POST'])
def callback() -> str:

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)

    # record users' log
    file_path = user_log_path + '/user-event.log'
    with open(file_path, 'a') as testwritefile:
      testwritefile.write(body)
      testwritefile.write('\n')

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

"""
    Get the image message from the user 
    when they send to the bot; also, send 
    the tips to alert them we get the 
    image message.
"""


# inform the handler when the message event is
# image message do the below things.
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Image has Upload'+ ' ' + event.message.id+'\n'+'你好啊！你的照片被我拿走了')
    )
    
    message_content = line_bot_api.get_message_content(event.message.id)

    file_path = user_log_path + '/'
    with open(file_path + current_date + event.message.id + '.jpg', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

"""
    Get the audio message from the user 
    when they send to the bot; also, send 
    the tips to alert them we get the 
    audio message.
"""

# inform the handler when the message event is
# audio message do the below things.
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Audio has Upload'+ ' ' + event.message.id))
    
    message_content = line_bot_api.get_message_content(event.message.id)

    file_path = user_log_path + '/'
    with open(file_path + current_date + event.message.id + '.mp3', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

"""
    Get the video message from the user 
    when they send to the bot; also, send 
    the tips to alert them we get the 
    video message.
"""

# inform the handler when the message event is
# video message do the below things.
@handler.add(MessageEvent, message=VideoMessage)
def handle_video_message(event):

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Video has Upload'+ ' ' + event.message.id))

    message_content = line_bot_api.get_message_content(event.message.id)

    file_path = user_log_path + '/'
    with open(file_path + current_date + event.message.id + '.mp4', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)



# Web server.
if __name__ == '__main__':
    app.run(port=5002)

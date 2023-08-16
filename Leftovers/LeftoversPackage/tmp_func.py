# -*- coding: utf-8 -*-
'''
Create Date: 2023/07/26
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.2
'''

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


def carousel_template_generator_one(
        alt_text, image_url, title, description, 
        label1, label1_info, label2, label2_info,
        label3, label3_info, label4, label4_info,) -> 'TemplateSendMessage':
    
    carousel_template_message = TemplateSendMessage(
        alt_text=alt_text,
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=image_url,
                    title=title,
                    text=description,
                    actions=[
                        MessageAction(
                            label=label1,
                            text=label1_info,
                        ),
                        MessageAction(
                            label=label2,
                            text=label2_info,
                        ),
                        MessageAction(
                            label=label3,
                            text=label3_info,
                        ),
                        MessageAction(
                            label=label4,
                            text=label4_info,
                        ),
                    ]
                ),
            ]
        )
    )
    return carousel_template_message


READY_TO_GET_STORE_NAME = False
STORE_USER_ID = ''
STORE_NAME = ''
READY_TO_GET_STORE_ADDRESS = False
STORE_ADDRESS = ''
STORE_INFO_NUM = 0  # to judge how many info user input.
READY_TO_GET_PRODUCT_TYPE_AMOUNT = False
PRODUCT_TYPE_AMOUNT = 0
READY_TO_GET_PRODUCT_NAME = False
PRODUCT_NAME = ''
READY_TO_GET_PRODUCT_AMOUNT = False
PRODUCT_AMOUNT = 0
READY_TO_GET_PRODUCT_PRICE = False
PRODUCT_PRICE = 0
PRODUCT_INFO_NUM = 0


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event) -> None:

    global STORE_INFO_NUM
    global READY_TO_GET_STORE_NAME, STORE_NAME
    global READY_TO_GET_STORE_ADDRESS, STORE_ADDRESS
    global READY_TO_GET_PRODUCT_TYPE_AMOUNT, PRODUCT_TYPE_AMOUNT

    global PRODUCT_INFO_NUM
    global READY_TO_GET_PRODUCT_NAME, PRODUCT_NAME
    global READY_TO_GET_PRODUCT_AMOUNT, PRODUCT_AMOUNT
    global READY_TO_GET_PRODUCT_PRICE

    try:

        if (event.message.text) == '來認識「一食二鳥」吧！':

            reply_message = []
            message1 = TextSendMessage(
                text='歡迎來到\n「一食二鳥-剩食媒合平台」\n有你來惜食 永續新開始🌱')
            reply_message.append(message1)
            message2 = TextMessage(
                text='我們幫助店家\n上架每日剩食\n並讓消費者可自由選購\n' +
                '好康划算的剩食媒合平台\n完成一筆交易\n滿足雙方需求的同時\n' +
                '也是愛惜食物\n為地球盡一份心力🌍')
            reply_message.append(message2)
            message3 = TextSendMessage(
                text='你的加入\n將會是我們的一大步🦶\n讓我們一起把試營運的\n剩食平台落地吧！')
            reply_message.append(message3)
            
            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '我要成為商家（測試用）' \
            or (event.message.text) == '我想查詢今日商品（測試用）'\
            or (event.message.text) == '我想評論（測試用）'\
            or (event.message.text) == '我要成為食客（測試用）':

            reply_message = []
            message1 = TextSendMessage(
                text='此功能仍在測試中，近請期待～ ')
            reply_message.append(message1)
            reply_message.append(Generator.known_us_quick_reply)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)

            
        elif (event.message.text) == '我要成為商家':

            reply_message = []

            message1 = TextSendMessage(
                text='在成為商家前，需要確認您是否同意遵守我們的使用者條款呢？')
            reply_message.append(message1)
            reply_message.append(
                Generator.policy_buttons_template_message)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '我還不太清楚使用者條款，可以給我看看使用者條款嗎？':

            reply_message = []

            message1 = TextSendMessage(
                text='來看看我們的使用者條款吧！')
            reply_message.append(message1)
            message2 = TextSendMessage(
                text='使用者條款\n使用者條款使用者條款')
            reply_message.append(message2)
            reply_message.append(
                Generator.policy_buttons_template_message)
            
            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '我已詳閱使用者條款並且願意遵守':

            reply_message = []

            message1 = TextSendMessage(
                text='請開始依序點擊下方按鈕：\n' + 
                '「商品名稱、店家地址、商品數量種類」\n' + 
                '以「完整」填寫商家資訊，\n' + 
                '這樣我們才能正確登陸商店資訊哦～')
            reply_message.append(message1)
            reply_message.append(Generator.products_info1)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '我想要輸入店家名稱':

            READY_TO_GET_STORE_NAME = True

            reply_message = []

            message1 = TextSendMessage(
                text='請問您的店家名稱是？')
            reply_message.append(message1)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
        
        elif READY_TO_GET_STORE_NAME == True:

            print('準備搜集用戶商店名稱')
            STORE_NAME = ''
            STORE_NAME = event.message.text
            READY_TO_GET_STORE_NAME = False
            print('已將用戶商店名稱存入`STORE_NAME`，可以準備送進資料庫')
            STORE_INFO_NUM += 1

            reply_message = []
            message1 = TextSendMessage(
                '已成功收到商家名稱，\n您的商店名稱是「' + STORE_NAME + '」！')
            reply_message.append(message1)
            message2 = TextSendMessage(
                '請繼續點擊「店家地址」以填寫完整資！')
            reply_message.append(message2)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '我想要輸入店家地址':

            READY_TO_GET_STORE_ADDRESS = True

            reply_message = []

            message1 = TextSendMessage(
                text='請問您的店家地址是？')
            reply_message.append(message1)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif READY_TO_GET_STORE_ADDRESS == True:

            print('準備搜集用戶商店地址')
            STORE_ADDRESS = ''
            STORE_ADDRESS = event.message.text
            READY_TO_GET_STORE_ADDRESS = False
            print('已將用戶商店地址存入`STORE_ADDRESS`，可以準備送進資料庫')
            STORE_INFO_NUM += 1

            reply_message = []
            message1 = TextSendMessage(
                '已成功收到商家地址，\n您的商店地址是「' + STORE_ADDRESS + '」！')
            reply_message.append(message1)
            message2 = TextSendMessage(
                '請繼續點擊「商品種類數量」以填寫完整資！')
            reply_message.append(message2)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '我想要輸入今天欲上架商品種類數量':

            READY_TO_GET_PRODUCT_TYPE_AMOUNT = True

            reply_message = []

            message1 = TextSendMessage(
                text='請問今日欲上架的商品種類為多少種？')
            reply_message.append(message1)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif READY_TO_GET_PRODUCT_TYPE_AMOUNT == True:

            """__Still need to research__
                === Need to change the type of `event.message.text` ===
                This will occur the error that cannot be printed in `TextSendMessage()`
                PRODUCT_TYPE_AMOUNT = int(PRODUCT_TYPE_AMOUNT)      
            """
            
            print('準備搜集用戶今日欲上架的商品種類數量')
            PRODUCT_TYPE_AMOUNT = ''
            PRODUCT_TYPE_AMOUNT = event.message.text
            READY_TO_GET_PRODUCT_TYPE_AMOUNT = False
            print('已將用戶用戶今日欲上架的商品種類數量存入`PRODUCT_TYPE_AMOUNT`，可以準備送進資料庫')
            STORE_INFO_NUM += 1
            

            reply_message = []
            message1 = TextSendMessage(
                '已成功收到商家地址，\n您今日欲上架的商品種類數量是「' + PRODUCT_TYPE_AMOUNT + '」！')
            reply_message.append(message1)
            message2 = TextSendMessage(
                '最後與您確認已收到的店家資訊為如下：\n' +
                '店家名稱：\n' +
                STORE_NAME + '\n' +
                '店家地址：\n' +
                STORE_ADDRESS + '\n' +
                '商品種類數量：' + 
                PRODUCT_TYPE_AMOUNT)
            reply_message.append(message2)
            reply_message.append(Generator.check_store_info_buttons_template_message)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '我還有細節要調整':

            STORE_INFO_NUM = 0
            reply_message = []

            message1 = TextSendMessage(
                text='請重新依序依序點擊下方按鈕：\n' + 
                '「店家名稱、店家地址、商品數量種類」\n' + 
                '以「完整」填寫商家資訊，\n' + 
                '這樣我們才能正確登陸商店資訊哦～')
            reply_message.append(message1)
            reply_message.append(Generator.products_info1)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '以上資訊商家完全正確':

            """__Still need to research__
                === if the carousel_template action equal to 4 ===
                This will occur the error that cannot send the 
                message to the user. (500)

               __How to Solve in the current method__
               Ask the user whether they want to upload the Image.
               Therefore, judge the statement independently.  
            """

            reply_message = []

            message1 = TextSendMessage(
                text='請開始依序依序點擊下方按鈕：\n' + 
                '「商品名稱、商品數量、商品單價」\n' + 
                '以「完整」填寫商品資訊，\n' + 
                '這樣我們才能正確登陸商品資訊哦～')
            reply_message.append(message1)
            reply_message.append(Generator.products_info2)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '我想要輸入商品名稱':

            reply_message = []

            message1 = TextSendMessage(
                text='請問您的商品名稱是？')
            reply_message.append(message1)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
        
            
        else :

            reply_message = []

            message1 = TextSendMessage(
                text='這句話我們還不認識，或許有一天我們會學起來！')
            reply_message.append(message1)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        
            
    except Exception as e:

        print(f"Error occurred: {e}")
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage('我們目前還不能辨識您的這則訊息\n或許可以試試看別的內容哦～'))
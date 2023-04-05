# -*- coding: utf-8 -*-

""" 
Import the package we need. 
"""

import sys
import os
from numpy import NaN
import json
import pandas as pd
import math
from flask import Flask, request, abort, jsonify, render_template, url_for
import datetime
import tornado.web
import tornado.ioloop
import asyncio
import threading
import DatabaseService
import config

""" Import the self-definite function """
from LeftoversPackage import (
    Generator, Tools, 
)

""" Below is the package with Line Bot"""

from linebot import (
    LineBotApi, WebhookHandler,
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError,
)
# Import the message type of the line bot
from linebot.models import (
    ImagemapSendMessage, TextSendMessage,
    ImageSendMessage, LocationSendMessage,
    FlexSendMessage, VideoSendMessage,
    StickerSendMessage, AudioSendMessage,
    ImageMessage, VideoMessage,
    AudioMessage, TextMessage,
    TemplateSendMessage, QuickReply,
)

# Import the action type of the line bot
from linebot.models import (
    MessageTemplateAction, PostbackAction,
    MessageAction, URIAction, QuickReplyButton
)
from linebot.models.template import (
    ButtonsTemplate, CarouselTemplate,
    ConfirmTemplate, ImageCarouselTemplate,
)
from linebot.models.template import *
from linebot.models.events import (
    FollowEvent, MessageEvent,
)


# connect to the line bot api and the handler
line_bot_api = LineBotApi(config.line_bot_api)
handler = WebhookHandler(config.handler)

"""
    Get the current date to record the behaviors
    of users.
"""

current_date = datetime.datetime.today().strftime('%Y%m%d')
user_log_path = "./log/" + current_date


Tools.check_dir(user_log_path)



# modelPretrained = joblib.load("./Precipitation_Predict.pkl")
""" start the server """

app = Flask(__name__)

@app.route('/launch_products')
def formPage():
    return render_template("form.html")


# YES = False
# NO = False
YES = ''
NO = ''
CHECK_POLICY = False
STORE_NAME = ''
STORE_ADDRESS = ''
PRODUCT_TYPE_AMOUNT = 0
FIRST_PRODUCT_NAME = ''
FIRST_PRODUCT_AMOUNT = 0
FIRST_PRODUCT_PRICE = 0
SECOND_PRODUCT_NAME = ''
SECOND_PRODUCT_AMOUNT = 0
SECOND_PRODUCT_PRICE = 0
THIRD_PRODUCT_NAME = ''
THIRD_PRODUCT_AMOUNT = 0
THIRD_PRODUCT_PRICE = 0
EXPIRY_DATE = ''
PICKUP_TIME = ''
STATUS = ''

@app.route("/submit", methods = ['POST'])
def submit() -> str:

    global YES
    global NO
    global CHECK_POLICY

    global STORE_NAME
    global STORE_ADDRESS

    global PRODUCT_TYPE_AMOUNT

    global FIRST_PRODUCT_NAME, FIRST_PRODUCT_AMOUNT, FIRST_PRODUCT_PRICE
    global SECOND_PRODUCT_NAME, SECOND_PRODUCT_AMOUNT, SECOND_PRODUCT_PRICE
    global THIRD_PRODUCT_NAME, THIRD_PRODUCT_AMOUNT, THIRD_PRODUCT_PRICE

    global EXPIRY_DATE
    global PICKUP_TIME

    global STATUS

    if request.method == 'POST':

        """__TypeError Checking__
            Add try except to alert the users.
        """
        form_data = request.form

        print(form_data)

        """__Data Type__
        ImmutableMultiDict([
            ('CHECK_POLICY', '1'), 
            ('STORE_NAME', '苦苦'), 
            ('STORE_ADDRESS', '苦苦'), 
            ('productTypeAmount', '3'), 
            ('FIRST_PRODUCT_NAME', '苦苦'), 
            ('FIRST_PRODUCT_AMOUNT', '12'), 
            ('FIRST_PRODUCT_PRICE', '123'), 
            ('SECOND_PRODUCT_NAME', '苦苦'), 
            ('SECOND_PRODUCT_AMOUNT', '11'), 
            ('SECOND_PRODUCT_PRICE', '2736'), 
            ('THIRD_PRODUCT_NAME', '苦苦'), 
            ('THIRD_PRODUCT_AMOUNT', '236'), 
            ('THIRD_PRODUCT_PRICE', '737'), 
            ('EXPIRY_DATE', '2023-04-04T16:46'), 
            ('PICKUP_TIME', '2023-04-04T16:46')]
        )
        """

        # Policy
        YES = ''
        NO = ''
        if int(form_data['CHECK_POLICY'])== 1:
            YES = 'checked'
        else:
            NO = 'checked'

        STORE_NAME = str(form_data['STORE_NAME'])
        STORE_ADDRESS = str(form_data['STORE_ADDRESS'])

        PRODUCT_TYPE_AMOUNT = int(form_data['productTypeAmount'])

        FIRST_PRODUCT_NAME = str(form_data['FIRST_PRODUCT_NAME'])
        FIRST_PRODUCT_AMOUNT = int(form_data['FIRST_PRODUCT_AMOUNT'])
        FIRST_PRODUCT_PRICE = int(form_data['FIRST_PRODUCT_PRICE'])

        SECOND_PRODUCT_NAME = str(form_data['SECOND_PRODUCT_NAME'])
        SECOND_PRODUCT_AMOUNT = int(form_data['SECOND_PRODUCT_AMOUNT'])
        SECOND_PRODUCT_PRICE = int(form_data['SECOND_PRODUCT_PRICE'])

        THIRD_PRODUCT_NAME = str(form_data['THIRD_PRODUCT_NAME'])
        THIRD_PRODUCT_AMOUNT = int(form_data['THIRD_PRODUCT_AMOUNT'])
        THIRD_PRODUCT_PRICE = int(form_data['THIRD_PRODUCT_PRICE'])

        EXPIRY_DATE = str(form_data['EXPIRY_DATE'])
        PICKUP_TIME = str(form_data['PICKUP_TIME'])

        if NO == 'checked':

            STATUS = f'請先同意使用者條款' 

        if YES == 'checked':

            STATUS = ''
            STATUS = f'商家名稱：{STORE_NAME}\n\
                       商家地址：{STORE_ADDRESS}\n\
                       商品種類數量：{PRODUCT_TYPE_AMOUNT}\n\
                       第一項商品資訊：\n\
                       第一項商品名稱：{FIRST_PRODUCT_NAME}\n\
                       第一項商品數量：{FIRST_PRODUCT_AMOUNT}\n\
                       第一項商品售價：{FIRST_PRODUCT_PRICE}\n\
                       第二項商品資訊：\n\
                       第二項商品名稱：{SECOND_PRODUCT_NAME}\n\
                       第二項商品數量：{SECOND_PRODUCT_AMOUNT}\n\
                       第二項商品售價：{SECOND_PRODUCT_PRICE}\n\
                       第三項商品資訊：\n\
                       第三項商品名稱：{THIRD_PRODUCT_NAME}\n\
                       第三項商品數量：{THIRD_PRODUCT_AMOUNT}\n\
                       第三項商品售價：{THIRD_PRODUCT_PRICE}\n\
                       最佳食用期限：{EXPIRY_DATE}\n\
                       最後取餐時間：{PICKUP_TIME}\n'
            

        # STATUS = ''
        # STATUS = '商家名稱：' + STORE_NAME + '\n'
        # STATUS += '商家地址：' + STORE_ADDRESS + '\n'
        # STATUS += '商品種類數量：' + PRODUCT_TYPE_AMOUNT + '\n'
        # STATUS += '第一項商品資訊：\n'
        # STATUS += '第一項商品名稱：' + FIRST_PRODUCT_NAME + '\n'
        # STATUS += '第一項商品數量：' + FIRST_PRODUCT_AMOUNT + '\n'
        # STATUS += '第一項商品售價：' + FIRST_PRODUCT_PRICE + '\n'
        # STATUS += '第二項商品資訊：\n'
        # STATUS += '第二項商品名稱：' + SECOND_PRODUCT_NAME + '\n'
        # STATUS += '第二項商品數量：' + SECOND_PRODUCT_AMOUNT + '\n'
        # STATUS += '第二項商品售價：' + SECOND_PRODUCT_PRICE + '\n'
        # STATUS += '第三項商品資訊：\n'
        # STATUS += '第三項商品名稱：' + THIRD_PRODUCT_NAME + '\n'
        # STATUS += '第三項商品數量：' + THIRD_PRODUCT_AMOUNT + '\n'
        # STATUS += '第三項商品售價：' + THIRD_PRODUCT_PRICE + '\n'
        # STATUS += '最佳食用期限：' + EXPIRY_DATE + '\n'
        # STATUS += '最後取餐時間：' + PICKUP_TIME + '\n'
        # print(STATUS)
        
        return render_template(
            'form.html',
            YES = YES, 
            NO = NO, 
            STORE_NAME = STORE_NAME,
            STORE_ADDRESS = STORE_ADDRESS,
            FIRST_PRODUCT_NAME = FIRST_PRODUCT_NAME,
            FIRST_PRODUCT_AMOUNT = FIRST_PRODUCT_AMOUNT,
            FIRST_PRODUCT_PRICE = FIRST_PRODUCT_PRICE,
            SECOND_PRODUCT_NAME = SECOND_PRODUCT_NAME,
            SECOND_PRODUCT_AMOUNT = SECOND_PRODUCT_AMOUNT,
            SECOND_PRODUCT_PRICE = SECOND_PRODUCT_PRICE,
            THIRD_PRODUCT_NAME = THIRD_PRODUCT_NAME,
            THIRD_PRODUCT_AMOUNT = THIRD_PRODUCT_AMOUNT,
            THIRD_PRODUCT_PRICE = THIRD_PRODUCT_PRICE,
            EXPIRY_DATE = EXPIRY_DATE,
            PICKUP_TIME = PICKUP_TIME,
            STATUS = STATUS,
        )


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

SERVER_DOMAIN_URL = ''
IMAGE_SERVER_DOMAIN_URL = ''


def getDomainUrl(SERVER_DOMAIN_URL) -> str:

    SERVER_DOMAIN_URL = str(input('Please input your current server domain: '))

    return SERVER_DOMAIN_URL


def getImageDomainUrl(IMAGE_SERVER_DOMAIN_URL) -> str:

    IMAGE_SERVER_DOMAIN_URL = str(input('Please input your current IMAGE server domain: '))

    return IMAGE_SERVER_DOMAIN_URL

SERVER_DOMAIN_URL = getDomainUrl(SERVER_DOMAIN_URL)

FORMS_URL = SERVER_DOMAIN_URL + '/launch_products'

STORE_USER_ID = ''
UPDATE_STORE_INFO_TO_DB = False

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event) -> None:

    global FORMS_URL
    global CHECK_POLICY
    global STORE_NAME
    global STORE_ADDRESS

    global PRODUCT_TYPE_AMOUNT
    global PRODUCT_TYPE_AMOUNT_1
    global PRODUCT_TYPE_AMOUNT_2
    global PRODUCT_TYPE_AMOUNT_3

    global FIRST_PRODUCT_NAME, FIRST_PRODUCT_AMOUNT, FIRST_PRODUCT_PRICE
    global SECOND_PRODUCT_NAME, SECOND_PRODUCT_AMOUNT, SECOND_PRODUCT_PRICE
    global THIRD_PRODUCT_NAME, THIRD_PRODUCT_AMOUNT, THIRD_PRODUCT_PRICE

    global EXPIRY_DATE
    global PICKUP_TIME

    global STORE_USER_ID
    global UPDATE_STORE_INFO_TO_DB

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

            
        elif (event.message.text) == '我要成為商家上架商品':

            reply_message = []

            message1 = TextSendMessage(
                text='在成為商家上架商品前，需要確認您是否同意遵守我們的使用者條款呢？')
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
                text='請點選「以下連結」，' + 
                '進入連結後點選「藍色按鈕——Visit Site」' + 
                '，以填寫詳細商家資訊與商品資訊！')
            reply_message.append(message1)
            message2 = TextSendMessage(FORMS_URL)
            reply_message.append(message2)
            reply_message.append(
                Generator.check_launch_buttons_template_message)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '我已完成填寫商品登錄連結！':

            reply_message = []

            message1 = TextSendMessage(
                text='您的商家名稱是：' + 
                STORE_NAME +
                '\n您的商家地址是：' +
                STORE_ADDRESS +
                '\n您今日欲上架商品種類數量：' +
                str(PRODUCT_TYPE_AMOUNT))
            reply_message.append(message1)
            message2 = TextSendMessage(
                text='第一項商品資訊：\n---\n' +
                '第一項商品名稱：' + FIRST_PRODUCT_NAME + '\n' +
                '第一項商品數量：' + str(FIRST_PRODUCT_AMOUNT) + '\n' +
                '第一項商品售價：' + str(FIRST_PRODUCT_PRICE) + '\n' +
                '第二項商品資訊：\n---\n' +
                '第二項商品名稱：' + SECOND_PRODUCT_NAME + '\n' +
                '第二項商品數量：' + str(SECOND_PRODUCT_AMOUNT) + '\n' +
                '第二項商品售價：' + str(SECOND_PRODUCT_PRICE) + '\n' +
                '第三項商品資訊：\n---\n' +
                '第三項商品名稱：' + THIRD_PRODUCT_NAME + '\n' +
                '第三項商品數量：' + str(THIRD_PRODUCT_AMOUNT) + '\n' +
                '第三項商品售價：' + str(THIRD_PRODUCT_PRICE))
            reply_message.append(message2)

            """ __message words limits__
                if happened, use the below comment code.
            """
            # message2 = TextSendMessage(
            #     text='第一項商品資訊：\n' +
            #     '第一項商品名稱：' + FIRST_PRODUCT_NAME + '\n' +
            #     '第一項商品數量：' + str(FIRST_PRODUCT_AMOUNT) + '\n' +
            #     '第一項商品售價：' + str(FIRST_PRODUCT_PRICE))
            # reply_message.append(message2)
            # message3 = TextSendMessage(
            #     text='第二項商品資訊：\n' +
            #     '第二項商品名稱' + SECOND_PRODUCT_NAME + '\n' +
            #     '第二項商品數量' + str(SECOND_PRODUCT_AMOUNT) + '\n' +
            #     '第二項商品售價' + str(SECOND_PRODUCT_PRICE))
            # reply_message.append(message3)
            # message4 = TextSendMessage(
            #     text='第三項商品資訊：\n' +
            #     '第三項商品名稱' + THIRD_PRODUCT_NAME + '\n' +
            #     '第三項商品數量' + str(THIRD_PRODUCT_AMOUNT) + '\n' +
            #     '第三項商品售價' + str(THIRD_PRODUCT_PRICE) + '\n')
            # reply_message.append(message4)
            message5 = TextSendMessage(
                text='最佳食用期限：' +
                EXPIRY_DATE + '\n' +
                '最後取餐時間：' +
                PICKUP_TIME)
            reply_message.append(message5)

            reply_message.append(
                Generator.check_store_info_buttons_template_message)
            
            line_bot_api.reply_message(
                event.reply_token,
                reply_message)


        elif (event.message.text) == '我馬上就會填完連結！':

            reply_message = []

            message1 = TextSendMessage(
                text='請點選「以下連結」，' + 
                '進入連結後點選「藍色按鈕——Visit Site」' + 
                '，以填寫詳細商家資訊與商品資訊！')
            reply_message.append(message1)
            message2 = TextSendMessage(FORMS_URL)
            reply_message.append(message2)
            reply_message.append(
                Generator.check_launch_buttons_template_message)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '我還有細節要調整':

            reply_message = []

            message1 = TextSendMessage(
                text='請重新點選「以下連結」，' + 
                '進入連結後點選「藍色按鈕——Visit Site」' + 
                '，以修改商家資訊與商品資訊！')
            reply_message.append(message1)
            message2 = TextSendMessage(FORMS_URL)
            reply_message.append(message2)
            reply_message.append(
                Generator.check_launch_buttons_template_message)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '以上商家資訊完全正確，請將資料登錄資料庫':

            UPDATE_STORE_INFO_TO_DB = True

            # Get complete store info to fulfill the format of data
            # in our database.
            STORE_USER_ID = (event.source.user_id)
            # profile = line_bot_api.get_profile(STORE_USER_ID)
            # print(profile)

            reply_message = []
            message1 = TextSendMessage(
                text='您的商家資訊已成功註冊於資料庫中，祝您商品販售順利！')
            reply_message.append(message1)
            reply_message.append(
                Generator.products_list_quick_reply)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '我想查詢今日商家':
            
            reply_message = []

            reply_message.append(Generator.get_all_store_template_message)

            line_bot_api.reply_message(
                event.reply_token,
                reply_message)
            
        elif (event.message.text) == '查看今日有上架商品的商家':

            products_info1 = Generator.carousel_template_generator_three(
                alt_text='Carousel template',
                image_url='https://i.imgur.com/vG4FgDX.png',
                title=STORE_NAME,
                description=f'商家地址：{STORE_ADDRESS}',
                label1=FIRST_PRODUCT_NAME,
                label1_info=f'我想要了解{FIRST_PRODUCT_NAME}',
                label2=SECOND_PRODUCT_NAME,
                label2_info=f'我想要了解{SECOND_PRODUCT_NAME}',
                label3=THIRD_PRODUCT_NAME,
                label3_info=f'我想要了解{THIRD_PRODUCT_NAME}',
            )
            
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
        Tools.check_dir(file_path)

        output_path = Tools.get_output_path(file_path, current_date, event.message.id, '.jpg')

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
        Tools.check_dir(file_path)

        output_path = Tools.get_output_path(file_path, current_date, event.message.id, '.mp3')

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
        Tools.check_dir(file_path)

        output_path = Tools.get_output_path(file_path, current_date, event.message.id, '.mp3')

        with open(output_path, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)

    except LineBotApiError as e:
        # 如果發生例外，記錄錯誤訊息
        print('Unable to get message content: ' + str(e))


# Start Tornado server
def start_tornado():

    asyncio.set_event_loop(asyncio.new_event_loop())
    # Initialize Tornado app
    tornado_app = tornado.web.Application([
        ("/"+ config.image_folder +"/(.*)", 
         tornado.web.StaticFileHandler, 
         {"path": config.image_folder}),
    ])
    tornado_app.listen(5012)
    tornado.ioloop.IOLoop.instance().start()

def start_flask() -> None:

    # Start Flask server
    app.run(port=5002)


def main() -> None: 

    # Web server.
    if __name__ == '__main__':

        # Start Tornado server in a separate thread
        tornado_thread = threading.Thread(target=start_tornado)
        tornado_thread.start()

        # Start Flask server in the main thread
        start_flask()

main()

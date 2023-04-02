# -*- coding: utf-8 -*-

""" 
Import the package we need. 
"""

import sys
import os
from numpy import NaN
import json
import pandas as pd
from numpy import NaN
import math
from flask import Flask, request, abort, jsonify, render_template, url_for
import datetime
import tornado.web
import tornado.ioloop
import asyncio
import threading
import DatabaseService
import config
import joblib

""" Import the self-definite function """
from LeftoversPackage import (
    Generator, Tools, 
)

""" Below is the package with Line Bot"""

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



modelPretrained = joblib.load("./Precipitation_Predict.pkl")
""" start the server """

app = Flask(__name__)

@app.route('/forms')
def formPage():
    return render_template("form.html")

@app.route("/submit", methods = ['POST'])
def submit():

    if request.method == 'POST':
        form_data = request.form
        # print(form_data)


        inputPressure = ""
        relativeHumidity = ""
        wind = ""
        gustWind = ""
        inputTemerature = ""

        
        result = modelPretrained.predict([[
        int(form_data["currentPressure"]), 
        int(form_data["todayMaximumPressure"]), 
        int(form_data["todayMinimumPressure"]), 
        int(form_data["currentTemperature"]), 
        int(form_data["todayMaximumTemperature"]),
        int(form_data["todayMinimumTemperature"]),
        int(form_data["currentRelativeHumidity"]), 
        int(form_data["todayMinimumRelativeHumidity"]), 
        int(form_data["currentWindSpeed"]), 
        int(form_data["currentWindDirection"]), 
        int(form_data["currentGustWindSpeed"]), 
        int(form_data["currentGustWindDirection"])
        ]])

        resultProba = modelPretrained.predict_proba([[
        int(form_data["currentPressure"]), 
        int(form_data["todayMaximumPressure"]), 
        int(form_data["todayMinimumPressure"]), 
        int(form_data["currentTemperature"]), 
        int(form_data["todayMaximumTemperature"]),
        int(form_data["todayMinimumTemperature"]),
        int(form_data["currentRelativeHumidity"]), 
        int(form_data["todayMinimumRelativeHumidity"]), 
        int(form_data["currentWindSpeed"]), 
        int(form_data["currentWindDirection"]), 
        int(form_data["currentGustWindSpeed"]), 
        int(form_data["currentGustWindDirection"])
        ]])

        print(f'Result:{result}')
        print(f'Result_Proba:{resultProba}')

        if result[0] == 1.:
            prediction = f'會下雨哦！ - 系統信心 {resultProba[0][1]:.10f}'
        else:
            prediction = f'不會下雨哦！ - 系統信心 {resultProba[0][0]:.10f}'
        
        
        return render_template('form.html',
        inputPressure = inputPressure,
        currentPressure = form_data["currentPressure"],
        todayMaximumPressure = form_data["todayMaximumPressure"],
        todayMinimumPressure = form_data["todayMinimumPressure"],
        inputTemerature = inputTemerature,
        currentTemperature = form_data["currentTemperature"],
        todayMaximumTemperature = form_data["todayMaximumTemperature"],
        todayMinimumTemperature = form_data["todayMinimumTemperature"],
        relativeHumidity = relativeHumidity, 
        currentRelativeHumidity = form_data["currentRelativeHumidity"],
        todayMinimumRelativeHumidity = form_data["todayMinimumRelativeHumidity"],
        wind = wind,
        currentWindSpeed = form_data["currentWindDirection"],
        currentWindDirection = form_data["currentWindDirection"],
        gustWind = gustWind,
        currentGustWindSpeed = form_data["currentGustWindSpeed"],
        currentGustWindDirection = form_data["currentGustWindDirection"],
        prediction = prediction)

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
        ("/"+ config.image_folder +"/(.*)", tornado.web.StaticFileHandler, {"path": config.image_folder}),
    ])
    tornado_app.listen(5012)
    tornado.ioloop.IOLoop.instance().start()

# Start Flask server
def start_flask():
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

# -*- coding: utf-8 -*-
'''
Create Date: 2023/07/26
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.2
'''

from flask import Flask, request, abort, jsonify
import json
from flask_ngrok import run_with_ngrok
from linebot import (
    LineBotApi, 
    WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
import config


# 生成實體物件
line_bot_api = LineBotApi(config.line_bot_api)
handler = WebhookHandler(config.handler)

# 
'''
建置主程序app

建置handler與 line_bot_api
'''

# 設定Server啟用細節
app = Flask(__name__)
# run_with_ngrok(app)

# 
'''
建置主程序的API入口
  接受Line傳過來的消息
  並取出消息內容
  將消息內容存在google drive的檔案內
  並請handler 進行消息驗證與轉發
'''

# 啟動server對外接口，使Line能丟消息進來
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)

    with open('./ai-event.txt', 'a') as testwritefile:
        testwritefile.write(body)
        testwritefile.write('\n')
    # 記錄用戶log
    with open('./ai-event.log', 'a') as writefile:
        writefile.write(body)
        writefile.write('\n')

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 
'''

撰寫用戶關注時，我們要處理的商業邏輯

1. 取得用戶個資，並存回伺服器
2. 回應用戶，歡迎用的文字消息

'''

# 載入Follow事件
from linebot.models.events import (
    FollowEvent,MessageEvent
)

# 引入套件
from linebot.models import(
    TextSendMessage, 
    ImageSendMessage,
    ImageMessage,
    VideoMessage,
    AudioMessage,
    AudioSendMessage
)

# 告知handler，如果收到FollowEvent，則做下面的方法處理
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    
    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)
        
     # 將用戶資訊存在檔案內
    with open("./users.txt", "a") as myfile:
        myfile.write(json.dumps(vars(user_profile),sort_keys=True))
        myfile.write('\n')
    
    # 回覆文字消息與圖片消息
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     [TextSendMessage('安安，你的個資已被我紀錄了')]
    # )

# 
'''

若收到圖片消息時，

先回覆用戶文字消息，並從Line上將照片拿回。

'''

# 引入套件
from linebot.models import(
    TextSendMessage, ImageMessage,VideoMessage,AudioMessage,AudioSendMessage
)

# 告知handler，當收到消息事件，且消息為圖片消息時，作下列的方法
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):

    # 麻煩line_bot_api回應用戶消息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Image has Upload'+ ' ' + event.message.id))
    
    # 麻煩line_bot_api跟line索取該消息的多媒體訊息
    # 存回Colab的臨時電腦內
    message_content = line_bot_api.get_message_content(event.message.id)
    with open(event.message.id+'.jpg', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

# 
'''

若收到圖片消息時，

先回覆用戶文字消息，並從Line上將照片拿回。

'''

# 引入套件
from linebot.models import(
    TextSendMessage, ImageMessage,VideoMessage,AudioMessage,AudioSendMessage
)

# 告知handler，當收到消息事件，且消息為圖片消息時，作下列的方法
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):

    # 麻煩line_bot_api回應用戶消息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Audio has Upload'+ ' ' + event.message.id))
    
    # 麻煩line_bot_api跟line索取該消息的多媒體訊息
    # 存回Colab的臨時電腦內
    message_content = line_bot_api.get_message_content(event.message.id)
    with open(event.message.id+'.mp3', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

# 
'''

若收到圖片消息時，

先回覆用戶文字消息，並從Line上將影片拿回。

'''

# 引入套件
from linebot.models import(
    TextSendMessage, ImageMessage,VideoMessage,AudioMessage,AudioSendMessage
)

# 告知handler，當收到消息事件，且消息為圖片消息時，作下列的方法
@handler.add(MessageEvent, message=VideoMessage)
def handle_video_message(event):

    # 麻煩line_bot_api回應用戶消息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Video has Upload'+ ' ' + event.message.id))
    
    # 麻煩line_bot_api跟line索取該消息的多媒體訊息
    # 存回Colab的臨時電腦內
    message_content = line_bot_api.get_message_content(event.message.id)
    with open(event.message.id+'.mp4', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

# 
# 運行主程序
if __name__ == "__main__":
    app.run(port=5002)
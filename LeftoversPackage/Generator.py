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
    MessageAction, URIAction, 
    QuickReplyButton, LocationAction,
    DatetimePickerAction, RichMenuSwitchAction
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


def text_message_generator(reply_text) :

    text_message = '{\"type\": \"text\", \"text\": \"' + reply_text + '\"}'

    return text_message

def buttons_template_generator_two(
    alt_text, title, title_info, 
    label1, label1_reply, 
    label2, label2_reply
    ) -> 'TemplateSendMessage':
    
    buttons_template_message = TemplateSendMessage(
        alt_text=alt_text,
        template=ButtonsTemplate(
            title=title,
            text=title_info,
            actions=[
                MessageTemplateAction(
                    label=label1,
                    text=label1_reply,
                ),
                MessageTemplateAction(
                    label=label2,
                    text=label2_reply,
                )
            ]
        )
    )

    return buttons_template_message


def quick_reply_generator(
        text, label, reply_content) -> 'TextSendMessage':

    quick_reply = TextSendMessage(
        text=text,
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(
                        label=label, 
                        text=reply_content,
                    )
                )
            ]
        )
    )

    return quick_reply

known_us_quick_reply = quick_reply_generator(
    text='請選擇要顯示的買賣超資訊',
    label='來認識我們吧', 
    reply_content='來認識「一食二鳥」吧！',
)

products_list_quick_reply = quick_reply_generator(
    text='歡迎點選主選單「商品」功能，以查看商品上架成果',
    label='點我使用查詢商家功能', 
    reply_content='我想查詢今日商家',
)

no_more_image_quick_reply = quick_reply_generator(
    text='',
    label='我已上傳完成', 
    reply_content='最後確認商品資訊',
)

check_image_quick_reply = quick_reply_generator(
    text='',
    label='我已上傳完成', 
    reply_content='最後確認商品資訊',
)

def buttons_template_generator_one(alt_text, 
    title, title_info, label1, label1_reply,
    ) -> 'TemplateSendMessage':
    
    buttons_template_message = TemplateSendMessage(
        alt_text=alt_text,
        template=ButtonsTemplate(
            title=title,
            text=title_info,
            actions=[
                MessageTemplateAction(
                    label=label1,
                    text=label1_reply,
                ),
            ]
        )
    )

    return buttons_template_message

def carousel_template_generator_three(
        alt_text, image_url, title, description, 
        label1, label1_info, label2, label2_info,
        label3, label3_info,
    ) -> 'TemplateSendMessage':
    
    carousel_template_message = TemplateSendMessage(
        alt_text=alt_text,
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=image_url,
                    image_aspect_ratio='square',
                    image_size='cover',
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
                    ]
                ),
            ]
        )
    )
    return carousel_template_message

def carousel_template_generator_four(
        alt_text, image_url, title, description, 
        label1, label1_info, label2, label2_info,
        label3, label3_info, label4, label4_info,
    ) -> 'TemplateSendMessage':
    
    carousel_template_message = TemplateSendMessage(
        alt_text=alt_text,
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=image_url,
                    image_aspect_ratio='square',
                    image_size='cover',
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


products_info1 = carousel_template_generator_three(
    alt_text='Carousel template',
    image_url='https://i.imgur.com/vG4FgDX.png',
    title='店家名稱、店家地址、商品數量種類',
    description='請輸入店家詳細資訊',
    label1='店家名稱',
    label1_info='我想要輸入店家名稱',
    label2='店家地址',
    label2_info='我想要輸入店家地址',
    label3='商品種類數量',
    label3_info='我想要輸入今天欲上架商品種類數量',
)


get_all_store_template_message = TemplateSendMessage(
    alt_text='All Store Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/vG4FgDX.png',
                image_aspect_ratio='square',
                image_size='cover',
                title='查詢今日所有商家',
                text='展示今日有供應商品商家',
                actions=[
                    MessageAction(
                        label='所有商家',
                        text='查看今日有上架商品的商家',
                    ),
                ]
            ),
        ]
    )
)

"""

"""
products_info2 = carousel_template_generator_three(
    alt_text='Carousel template',
    image_url='https://i.imgur.com/vG4FgDX.png',
    title='商品名稱、商品數量、商品售價',
    description='請輸入商品詳細資訊（商品照片仍在測試階段）',
    label1='商品名稱',
    label1_info='我想要輸入商品名稱',
    label2='商品數量',
    label2_info='我想要輸入商品數量',
    label3='商品售價',
    label3_info='我想要輸入商品售價',
    # label4='商品售價',
    # label4_info='我想要輸入商品售價',
)

products_info1 = carousel_template_generator_three(
    alt_text='Carousel template',
    image_url='https://i.imgur.com/vG4FgDX.png',
    title='商品名稱',
    description='請輸入商品詳細資訊（商品照片仍在測試階段）',
    label1='商品名稱',
    label1_info='我想要輸入商品名稱',
    label2='商品數量',
    label2_info='我想要輸入商品數量',
    label3='商品售價',
    label3_info='我想要輸入商品售價',
)

image_upload_carousel = carousel_template_generator_three(
    alt_text='Image Carousel template',
    image_url='https://i.imgur.com/vG4FgDX.png',
    title='照片上傳',
    description='！！！一種商品限一張！！！',
    label1='第一種商品照片',
    label1_info='我想要上傳第一種商品照片',
    label2='第二種商品照片',
    label2_info='我想要上傳第二種商品照片',
    label3='第三種商品照片',
    label3_info='我想要上傳第三種商品照片',
)


policy_buttons_template_message = buttons_template_generator_two(
    alt_text='policy button',
    title='我願意遵守使用者條款',
    title_info='願意遵守使用者條款',
    label1='願意',
    label1_reply='我已詳閱使用者條款並且願意遵守',
    label2='再看看',
    label2_reply='我還不太清楚使用者條款，可以給我看看使用者條款嗎？',
)

image_check_2_buttons_template_message = buttons_template_generator_two(
    alt_text='policy button',
    title='我已完成照片上傳',
    title_info='願意遵守使用者條款',
    label1='完成',
    label1_reply='最後確認商品資訊',
    label2='繼續',
    label2_reply='我想要上傳第二種商品照片',
)

image_check_3_buttons_template_message = buttons_template_generator_two(
    alt_text='policy button',
    title='我已完成照片上傳',
    title_info='願意遵守使用者條款',
    label1='完成',
    label1_reply='最後確認商品資訊',
    label2='繼續',
    label2_reply='我想要上傳第三種商品照片',
)

final_image_check_buttons_template_message = buttons_template_generator_two(
    alt_text='policy button',
    title='我已完成照片上傳',
    title_info='願意遵守使用者條款',
    label1='完成',
    label1_reply='最後確認商品資訊',
    label2='再修改',
    label2_reply='我想要修改商品的照片！',
)

check_launch_buttons_template_message = buttons_template_generator_two(
    alt_text='check launch button',
    title='商品登陸確認',
    title_info='確認連結是否填寫完成',
    label1='完成',
    label1_reply='我已完成填寫商品登錄連結！',
    label2='晚點完成',
    label2_reply='我馬上就會填完連結！',
)

check_store_info_buttons_template_message = buttons_template_generator_two(
    alt_text='policy button',
    title='請問內容是否皆正確',
    title_info='若資料無誤將登陸資料庫中',
    label1='正確',
    label1_reply='以上商家資訊完全正確，請將資料登錄資料庫',
    label2='再調整',
    label2_reply='我還有細節要調整',
)

check_product_image_buttons_template_message = buttons_template_generator_two(
    alt_text='image button',
    title='請問需要上傳商品圖片？',
    title_info='一種商品限一張！！！',
    label1='需要',
    label1_reply='我想要幫我的商品加上美照！',
    label2='正在拍',
    label2_reply='我還在幫我的商品們拍照！',
)

check_again_product_image_buttons_template_message = buttons_template_generator_two(
    alt_text='image button',
    title='請問還需要上傳商品圖片？',
    title_info='一種商品限一張！！！',
    label1='需要',
    label1_reply='我想要幫我的商品加上美照！',
    label2='沒關係',
    label2_reply='今天先不傳照片，我要直接上架商品',
)

carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://example.com/item1.jpg',
                title='this is menu1',
                text='description1',
                actions=[
                    PostbackAction(
                        label='postback1',
                        display_text='postback text1',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label='message1',
                        text='message text1'
                    ),
                    URIAction(
                        label='uri1',
                        uri='http://example.com/1'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/item2.jpg',
                title='this is menu2',
                text='description2',
                actions=[
                    PostbackAction(
                        label='postback2',
                        display_text='postback text2',
                        data='action=buy&itemid=2'
                    ),
                    MessageAction(
                        label='message2',
                        text='message text2'
                    ),
                    URIAction(
                        label='uri2',
                        uri='http://example.com/2'
                    )
                ]
            )
        ]
    )
)

flex_message = TextSendMessage(
    text="請選擇要顯示的買賣超資訊",
    quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=MessageAction(
                    label="最新法人", 
                    text="最新法人買賣超 "
                )
            ),
            QuickReplyButton(
                action=MessageAction(
                    label="歷年法人", 
                    text="歷年法人買賣超 "
                )
            ),
            QuickReplyButton(
                action=MessageAction(
                    label="外資", 
                    text="外資買賣超 "
                )
            ),
            QuickReplyButton(
                action=MessageAction(
                    label="投信", 
                    text="投信買賣超 "
                )
            ),
            QuickReplyButton(
                action=MessageAction(
                    label="自營商", 
                    text="自營商買賣超 "
                )
            ),
            QuickReplyButton(
                action=MessageAction(
                    label="三大法人", 
                    text="三大法人買賣超 "
                )
            )
        ]
    )
)
# -*- coding: utf-8 -*-
'''
Create Date: 2023/07/26
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.1
'''

# 生成實體物件
line_bot_api = ''
handler = ''

# AWS要知道大家是誰，需要類似身份帳號密碼的亂數
client_aws_access_key_id = ""
client_aws_secret_access_key = ""
client_aws_session_token=""

# 模型在AWS的位置
model_arn=''

# 存放消費者上傳照片的桶子名
client_bucket_name=''
client_region_name=''

# database settings
database_host=''
database_port=''
database_user=''
database_passwd=''
database_db=''
database_charset=''

# Domain Settings
SERVER_DOMAIN_URL = ''
IMAGE_SERVER_DOMAIN_URL = ''

# image server host
image_server_host=''
image_folder=''

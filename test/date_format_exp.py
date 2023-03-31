# -*- coding: utf-8 -*-

""" https://ithelp.ithome.com.tw/articles/10250334 """

import datetime
import os

current_date = datetime.datetime.today().strftime('%Y%m%d')


path = './log/' + current_date

if not os.path.isdir(path):
    os.mkdir(path, mode=0o777)
    print(path, 'has been created successfully.')

print(datetime.datetime.today().strftime('%Y%m%d'))

user_log_path = "./log/" + current_date
print(user_log_path)
file_path = user_log_path + '/user-event.log'
print(file_path)
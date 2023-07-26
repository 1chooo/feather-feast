# -*- coding: utf-8 -*-
'''
Create Date: 2023/07/26
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.2
'''

import config
import pymysql

def initDataBase():
    db = pymysql.connect(
        host=config.database_host, 
        port=config.database_port, 
        user=config.database_user, 
        passwd=config.database_passwd, 
        db=config.database_db, 
        charset=config.database_charset
    )
    cursor = db.cursor()
    return db, cursor
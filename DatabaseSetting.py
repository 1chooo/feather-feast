import config
import pymysql

db = pymysql.connect(
    host=config.database_host, 
    port=config.database_port, 
    user=config.database_user, 
    passwd=config.database_passwd, 
    db=config.database_db, 
    charset=config.database_charset
)

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
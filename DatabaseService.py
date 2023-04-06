from datetime import datetime
import pytz
import DatabaseSetting as database
import pymysql
import config

# get store id by store name
def getStore(item, hasUserId = False):
    db, cursor = database.initDataBase()
    if hasUserId:
        sql = "SELECT id FROM stores WHERE user_id = '%s'" % (item)
    else:
        sql = "SELECT id FROM stores WHERE name = '%s'" % (item)
    cursor.execute(sql)
    results = cursor.fetchmany(1)
    db.close()
    if results:
        return results[0][0]
    else:
        raise ValueError("查無此商店")

# get product by product id and store id
def getProduct(productId, storeId):
    db, cursor = database.initDataBase()
    sql = "SELECT id FROM products WHERE id = %d AND store_id = %d" % (productId, storeId)
    cursor.execute(sql)
    data = cursor.fetchall()
    if data:
        return True
    else:
        raise ValueError("查無此商品")

# create store
def createStore(storeName, userId, storeAddress):
    try:
        db, cursor = database.initDataBase()
        sql = "INSERT INTO stores (name, user_id, address) VALUES ('%s', '%s', '%s')" % (storeName, userId, storeAddress)
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except pymysql.err.IntegrityError:
        raise ValueError("該使用者已建立商店")
        
# create product
def createProduct(userId, productName, productPrice, productNumber, imageFileName, expiredDate, lastPickUpDate):
    storeId = getStore(userId, True)
    imageUrl = config.image_folder + "/" + imageFileName
    dateTimeToday = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')
    db, cursor = database.initDataBase()
    sql = "INSERT INTO products (store_id, name, price, number, image_url, create_at, expired_date, last_pick_up_date) VALUES (%d, '%s', %d, %d, '%s', '%s', '%s', '%s')" % (storeId, productName, productPrice, productNumber, imageUrl, dateTimeToday, datetime.strptime(expiredDate, '%Y-%m-%dT%H:%M'), datetime.strptime(lastPickUpDate, '%Y-%m-%dT%H:%M'))
    cursor.execute(sql)
    db.commit()
    db.close()
    return True

# update product
def updateProduct(userId, productId, productName, productPrice, productNumber, imageFileName, productExpiredDate, productLastPickUpDate):
    storeId = getStore(userId, True)
    if (getProduct(productId, storeId)):
        imageUrl = config.image_folder + "/" + imageFileName
        db, cursor = database.initDataBase()
        sql = "UPDATE products SET name = '%s', price = %d, number = %d, image_url = '%s', expired_date = '%s', last_pick_up_date = '%s' WHERE id = %d" % (productName, productPrice, productNumber, imageUrl, datetime.strptime(productExpiredDate, '%Y-%m-%dT%H:%M'), datetime.strptime(productLastPickUpDate, '%Y-%m-%dT%H:%M'), productId)
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    else:
        raise ValueError("查無此商品")

# delete product
def deleteProduct(userId, productId):
    storeId = getStore(userId, True)
    if (getProduct(productId, storeId)):
        db, cursor = database.initDataBase()
        sql = "DELETE FROM products WHERE id = %d" % (productId)
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    else:
        raise ValueError("查無此商品")

# place order
def placeOrder(userId, storeId, productId, userName, description):
    db, cursor = database.initDataBase()
    try:
        cursor.execute("SELECT name, price, expired_date, last_pick_up_date FROM products WHERE id = %d AND number != 0 AND store_id = %d FOR UPDATE" % (productId, storeId))
        product = cursor.fetchmany(1)
        if product:
            productName = product[0][0]
            productPrice = product[0][1]
            productExpiredDate = product[0][2]
            productLastPickUpDate = product[0][3]
            sql = "UPDATE products SET number = number - 1 WHERE id = %d" % (productId)
            cursor.execute(sql)
            sql = "INSERT INTO orders (user_id, store_id, product_name, product_price, product_expired_date, product_last_pick_up_date, user_name, total, description) VALUES ('%s', %d, '%s', %d, '%s', '%s', '%s', %d, '%s')" % (userId, storeId, productName, productPrice, productExpiredDate, productLastPickUpDate, userName, productPrice, description)
            cursor.execute(sql)
            db.commit()
            db.close()
            return True
        else:
            raise ValueError("商品已售完")
    except pymysql.err.OperationalError as error:
        cursor.execute("ROLLBACK")
        db.close()
        raise ValueError("系統忙碌中，目前無法建立訂單，請稍後再試")

# cancel order
def cancelOrder(orderId, userId):
    db, cursor = database.initDataBase()
    sql = "SELECT id FROM orders WHERE id = %d AND user_id = '%s'" % (orderId, userId)
    cursor.execute(sql)
    data = cursor.fetchmany(1)
    if data:
        sql = "DELETE FROM orders WHERE id = %d AND user_id = '%s'" % (orderId, userId)
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    else:
        raise ValueError("查無訂單")

# get product details by product name
def getProductByName(productName):
    db, cursor = database.initDataBase()
    sql = "SELECT id, name, price, number, image_url, expired_date, last_pick_up_date FROM products WHERE name = '%s' AND DATE(created_at) = CURDATE()" % (productName)
    cursor.execute(sql)
    data = cursor.fetchmany(1)
    db.close()
    if data:
        headers = ("id", "name", "price", "number", "image_url", "expired_date", "last_pick_up_date")
        datum = dict(zip(headers, data[0]))
        datum['image_url'] = config.image_server_host + "/" + datum['image_url']
        datum['expired_date'] = datum['expired_date'].strftime('%Y-%m-%d %H:%M')
        datum['last_pick_up_date'] = datum['last_pick_up_date'].strftime('%Y-%m-%d %H:%M')
        return datum
    else:
        raise ValueError("查無此商品")

# get product name by store name
def getProductsName(storeName):
    result = []
    storeId = getStore(storeName)
    db, cursor = database.initDataBase()
    sql = "SELECT id, name FROM products WHERE store_id = %d AND DATE(created_at) = CURDATE()" % (storeId)
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    if data:
        for i in data:
            headers = ("id", "name")
            result.append(dict(zip(headers, data[0])))
        return result
    else:
        raise ValueError("查無商品")

def getStoreNameByOnlineProduct():
    storeId = []
    result = []
    db, cursor = database.initDataBase()
    sql = "SELECT store_id, COUNT(store_id) FROM products WHERE DATE(created_at) = CURDATE() GROUP BY store_id"
    cursor.execute(sql)
    data = cursor.fetchall()
    if data:
        for i in data:
            storeId.append(i[0])
        storeIdString = ', '.join(str(item) for item in storeId)
        sql = "SELECT name FROM stores WHERE id IN ({})".format(storeIdString)
        cursor.execute(sql)
        data = cursor.fetchall()
        db.close()
        if data:
            for i in data:
                result.append(i[0])
            return result
    else:
        db.close()
        raise ValueError("今日無任何商店有上架商品")

# get order details by store id
def getStoreDetails(storeId):
    db, cursor = database.initDataBase()
    sql = "SELECT * FROM stores WHERE id = %d" % (storeId)
    cursor.execute(sql)
    data = cursor.fetchmany(1)
    db.close()
    if data:
        headers = ("id", "name", "address")
        result = dict(zip(headers, data[0]))
        return result
    else:
        raise ValueError("查無此商店")

# get order detail
def getOrderDetails(itemId, isStoreOrder = False, isUserOrder = False):    
    db, cursor = database.initDataBase()
    if isStoreOrder:
        sql = "SELECT * FROM orders WHERE store_id = %d" % (itemId)
    elif isUserOrder:
        sql = "SELECT * FROM orders WHERE user_id = '%s'" % (itemId)
    else:
        sql = "SELECT * FROM orders WHERE id = %d" % (itemId)
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    if data:
        results = [];
        for i in data:
            store = getStoreDetails(i[2])
            headers = ("id", "user_id", "store","user_name", "product_name", "product_price", "product_expired_date", "product_last_pick_up_date", "total", "description")
            result = dict(zip(headers, i))
            result['store'] = store
            result['product_expired_date'] = result['product_expired_date'].strftime('%Y-%m-%d %H:%M')
            result['product_last_pick_up_date'] = result['product_last_pick_up_date'].strftime('%Y-%m-%d %H:%M')
            results.append(result)
        return results
    else:
        raise ValueError("查無訂單")

# get orders by store name
def getOrdersByStore(userId):
    storeId = getStore(userId, True)
    order = getOrderDetails(storeId, True, False)
    return order

# get orders by user id
def getOrdersByUser(userId):
    order = getOrderDetails(userId, False, True)
    return order


print(getStoreNameByOnlineProduct())
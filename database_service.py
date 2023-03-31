import database_setting as database
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
    db, cursor = database.initDataBase()
    sql = "INSERT INTO stores (name, user_id, address) VALUES ('%s', '%s', '%s')" % (storeName, userId, storeAddress)
    cursor.execute(sql)
    db.commit()
    db.close()
    return True
        
# create product
def createProduct(userId, productName, productPrice, productNumber, imageFileName):
    storeId = getStore(userId)
    imageUrl = config.image_server_host + "/" + config.image_folder + "/" + imageFileName
    db, cursor = database.initDataBase()
    sql = "INSERT INTO products (store_id, name, price, number, image_url) VALUES (%d, '%s', %d, %d, '%s')" % (storeId, productName, productPrice, productNumber, imageUrl)
    cursor.execute(sql)
    db.commit()
    db.close()
    return True

# update product
def updateProduct(userId, productId, productName, productPrice, productNumber, imageFileName):
    storeId = getStore(userId, True)
    if (getProduct(productId, storeId)):
        imageUrl = config.image_server_host + "/" + config.image_folder + "/" + imageFileName
        db, cursor = database.initDataBase()
        sql = "UPDATE products SET name = '%s', price = %d, number = %d, image_url = '%s' WHERE id = %d" % (productName, productPrice, productNumber, imageUrl, productId)
        cursor.execute(sql)
        db.commit()
        db.close()
        return True

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

# place order
def placeOrder(userId, storeId, productId, userName, description):
    db, cursor = database.initDataBase()
    try:
        cursor.execute("SELECT name, price FROM products WHERE id = %d AND number != 0 AND store_id = %d FOR UPDATE" % (productId, storeId))
        product = cursor.fetchmany(1)
        if product:
            productName = product[0][0]
            productPrice = product[0][1]
            sql = "UPDATE products SET number = number - 1 WHERE id = %d" % (productId)
            cursor.execute(sql)
            sql = "INSERT INTO orders (user_id, store_id, product_name, product_price, user_name, total, description) VALUES ('%s', %d, '%s', %d, '%s', %d, '%s')" % (userId, storeId, productName, productPrice, userName, productPrice, description)
            cursor.execute(sql)
            db.commit()
            db.close()
            return True
        else:
            raise ValueError("商品已售完")
    except pymysql.err.OperationalError as error:
        cursor.execute("ROLLBACK")
        db.close()
        raise DeadLockError("系統忙碌中，目前無法建立訂單，請稍後再試")
        # raise DeadLockError("Failed to place order, error: {}".format(error))

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

# get products by store name
def getProducts(storeName):
    result = []
    storeId = getStore(storeName)
    db, cursor = database.initDataBase()
    sql = "SELECT id, name, price, number, image_url FROM products WHERE store_id = %d" % (storeId)
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    if data:
        for i in data:
            headers = ("id", "name", "price", "number", "image_url")
            result.append(dict(zip(headers, data[0])))
        return result
    else:
        raise ValueError("查無此商品")

# get order details by store id
def getStoreDetails(storeId):
    db, cursor = database.initDataBase()
    sql = "SELECT * FROM stores WHERE id = '%s'" % (storeId)
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
        sql = "SELECT * FROM orders WHERE user_id = %d" % (itemId)
    else:
        sql = "SELECT * FROM orders WHERE id = %d" % (itemId)
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    if data:
        results = [];
        for i in data:
            store = getStoreDetails(i[2])
            headers = ("id", "user_id", "store","user_name", "product_name", 'product_price', "total", "description")
            result = dict(zip(headers, i))
            result['store'] = store
            results.append(result)
        return results
    else:
        raise ValueError("查無此訂單")

# get orders by store name
def getOrdersByStore(userId):
    storeId = getStore(userId)
    order = getOrderDetails(storeId, True, False)
    return order

# get orders by user id
def getOrdersByUser(userId):
    order = getOrderDetails(userId, False, True)
    return order
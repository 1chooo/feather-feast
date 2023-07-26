# -*- coding: utf-8 -*-
'''
Create Date: 2023/07/26
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.2
'''

import DatabaseSetting as database
import threading
import DatabaseService as transaction
import time

def run_transactions():
    db, cursor = database.initDataBase()
    for i in range(2):
        transaction.placeOrder("1", 2, 2, "ABC", "TEST")
    db.close()

threads = []
for i in range(2):
    thread = threading.Thread(target=run_transactions)
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("All transactions completed successfully.")
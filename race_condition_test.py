import database_setting as database
import threading
import database_service as transaction
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
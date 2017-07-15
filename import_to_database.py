import MySQLdb as SQL
import dictionary as cos_dict
import import_to_DB_class as idb
#-------------------------variable
db_password = "tl3n3xk7"
db_name = "cosmetic"

search_brand = '202'

pid = '202343'
p_name = 'asdsdsd'
bid = '202'
p_price = 2400
p_attri = '0011G'
timestamp ='1483286400'
sell_amount = 2


db = SQL.connect("localhost", "root", db_password, db_name, charset='utf8')
cursor = db.cursor()
try:
    try:
        cursor.execute(idb.search_product(search_brand, p_name))
        data = cursor.fetchone()
        #insert selling amount
        cursor.execute(idb.insert_selling(pid, timestamp, sell_amount))
        db.commit()
        print("'%s' selling amount '%d' 新增成功！" % (data[0], sell_amount))
    except:
    #互動視窗選定attribute
    #處理pid = bid後2+attribute+序號
        cursor.execute(idb.insert_product(pid, p_name, bid, p_price, p_attri))
        db.commit()
        print('新增成功!')
except:
    db.rollback()
    print('failed')
'''
for row in data:
    if row[0] == p_name:

        print('true')
    print(row[0])
'''
#cursor.execute(insert_selling) #insert銷售日期銷售數量

db.close()

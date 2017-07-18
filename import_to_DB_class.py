import csv
def search_product(search_brand, p_name):
    return "SELECT * FROM product \
                   WHERE product_brand_code = '%s' AND product_name = '%s'" % (search_brand, p_name)

def search_product_id(product_id):
    return "SELECT * FROM product WHERE pid = '%s'" % product_id

def insert_product( pid, bid, p_name, p_price, p_attri, p_parcel):
    return "INSERT INTO product(pid, bid, product_name, product_price, product_attribute, product_parcel)  \
           VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" \
                     % (pid, bid, p_name, p_price, p_attri, p_parcel)

def insert_attribute( attr_code, attr_class, attr_subclass, attr_function, attr_type):
    return "INSERT INTO product_attribute(attribute_code, attribute_class, attribute_subclass, attribute_function, \
           attribute_type) VALUES ('%s', '%s', '%s', '%s', '%s')" \
                     % (attr_code, attr_class, attr_subclass, attr_function, attr_type)

def insert_selling(pid, timestamp, sell_amount):
    return "INSERT INTO selling(pid, sell_date, sell_amount) VALUES  \
                     ('%s', '%s','%s')" % (pid, timestamp, sell_amount)

def insert_selling_set(pid, timestamp, sell_amount):
    return "INSERT INTO selling(pid, sell_date, sell_amount) VALUES  \
                     ('%s', '%s','%s')" % (pid, timestamp, sell_amount)

def insert_restore(file_name, prod_name):
    return "INSERT INTO restore_table(file_name, prod_name) VALUE ('%s','%s')" % (file_name, prod_name)

def search_restore(file_name):
    return "SELECT prod_name FROM restore_table WHERE file_name = '%s'" % file_name

def search_restore_id(file_name):
    return "SELECT pid FROM restore_table WHERE file_name = '%s'" % file_name

def search_brand(bid):
    return "SELECT name_brand FROM brandlist WHERE brand_code = '%s'" % bid
'''
def pid_generate(bid, attr):
    try:

    except:
    return pid
'''

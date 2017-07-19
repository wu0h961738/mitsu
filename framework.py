from tkinter import *
from tkinter import ttk
import csv
import MySQLdb as SQL
import dictionary as dict
import import_to_DB_class as idb
import structure as st
import windows_frame as main_lo

from tkinter import filedialog
db = SQL.connect("192.168.1.108", "wu0h961738", 'tl3n3xk7', 'cosmetic', charset='utf8')
cursor = db.cursor()


class insert_product_fr():
    def __init__(self, frame, gyd, data_list, last_data, condition, p_name):
        self.frame = frame
        self.gyd = gyd
        self.p_name = p_name
        self.data_list = data_list
        self.last_data = last_data
        self.condition = condition
        # 擷取資料代表欄位
        self.x2 = 0
        self.name = 1
        self.amount = 2
        self.date = 3
        self.price = 4
        self.widget_opt = {'fill': BOTH, 'expand': Y, 'padx': 5, 'pady': 5}

        cursor.execute(idb.search_brand(self.data_list[self.x2][:3]))
        bid = cursor.fetchone()

        self.roasted_name_title = Label(self.frame, text='產品名稱')
        self.brand_name = Label(self.frame, text=bid[0])
        #self.roasted_name = Label(self.frame, textvariable=self.p_name)
        self.roasted_name = Text(self.frame, height=1, borderwidth=0)
        self.roasted_name.insert(1.0, self.data_list[self.x2]+self.p_name.get())
        self.attribute_title = Label(self.frame, text="產品屬性")
        self.attr_subclass_title = Label(self.frame, text="產品種類")
        self.attr_subclass = ttk.Combobox(self.frame, width=10, values=self.return_subclass())
        self.attr_function_title = Label(self.frame, text="產品功效")
        self.attr_function = ttk.Combobox(self.frame, width=10, values=self.return_function())
        self.attr_type_title = Label(self.frame, text="產品顏色")
        self.attr_type = ttk.Combobox(self.frame, width=10, values=self.return_type())
        self.attr_parcel_title = Label(self.frame, text="產品包裝")
        self.attr_parcel = ttk.Combobox(self.frame, width=10, values=self.return_parcel())

        #set insert newproduct需改寫

        self.add_event = Button(self.frame, text="新增項目", command=lambda: self.add_product(p_name))
        self.insert_product_fr_pack()

    def insert_product_fr_pack(self):
        self.frame.pack(**self.widget_opt)
        self.brand_name.pack(**self.widget_opt)
        self.roasted_name_title.pack(**self.widget_opt)
        self.roasted_name.pack(**self.widget_opt)
        self.attribute_title.pack(**self.widget_opt)
        self.attr_subclass_title.pack(side=LEFT)
        self.attr_subclass.pack(**self.widget_opt)  # subclass menu
        self.attr_subclass.pack(side=LEFT)
        self.attr_function_title.pack(side=LEFT)
        self.attr_function.pack(**self.widget_opt)
        self.attr_function.pack(side=LEFT)  # subclass menu
        self.attr_type_title.pack(side=LEFT)
        self.attr_type.pack(**self.widget_opt)  # type menu
        self.attr_type.pack(side=LEFT)
        self.attr_parcel_title.pack(side=LEFT)
        self.attr_parcel.pack(**self.widget_opt)  # type menu
        self.attr_parcel.pack(side=LEFT)
        self.add_event.pack(**self.widget_opt)  # XXXXXXXXXXXXXXXXXXXXXXX新增產品

    def insert_product_fr_forget(self):
        self.frame.pack_forget()
        self.brand_name.pack_forget()
        self.roasted_name_title.pack_forget()
        self.roasted_name.pack_forget()
        self.attribute_title.pack_forget()
        self.attr_subclass_title.pack_forget()
        self.attr_subclass.pack_forget()  # subclass menu
        self.attr_function_title.pack_forget()
        self.attr_function.pack_forget()  # subclass menu
        self.attr_type_title.pack_forget()
        self.attr_type.pack_forget() # type menu
        self.attr_parcel_title.pack_forget()
        self.attr_parcel.pack_forget()  # type menu
        self.add_event.pack_forget()  # XXXXXXXXXXXXXXXXXXXXXXX新增產品

    def add_product(self, p_name): # XXXXXXXXXXXXXXXXXXXXXXX新增產品後顯示下一個商品名稱
        #防止DB timeout
        db = SQL.connect("localhost", "root", 'tl3n3xk7', 'cosmetic', charset='utf8')
        cursor = db.cursor()

        #product attribute擷取
        p_attr = self.attr_fetch()
        cursor.execute("SELECT parcel_id FROM attr_parcel WHERE parcel_name= '%s'" % self.attr_parcel.get())
        id_parcel = cursor.fetchone()

        if self.condition =='set':
            #新增產品到DB-product
            pid = self.data_list[self.x2][:3] + p_attr
            p_search = pid + '%'
            #確認重複ｐｉｄ
            if cursor.execute("SELECT pid FROM product WHERE pid LIKE '%s' ORDER BY pid DESC " % p_search):
                code_temp = cursor.fetchone
                code = self.code_rule(code_temp[0][-2:])
            else:
                code = '00'
            pid += code
            cursor.execute(idb.insert_product(pid, pid[:3], self.data_list[self.name], '0', p_attr, id_parcel[0]))#p_name = prod.get_name()
            db.commit()
            return pid

        else:
            # insert product
            cursor.execute(idb.insert_product(self.data_list[self.x2], self.data_list[self.x2][:3],
                                              self.data_list[self.name], self.data_list[self.price][:-2],
                                              p_attr, id_parcel[0]))
            db.commit()
            #insert selling
            cursor.execute(idb.insert_selling(self.data_list[self.x2], self.data_list[self.date][:10], self.data_list[self.amount]))
            db.commit()

            #重置combobox
            #self.frame.pack_forget()
            self.insert_product_fr_forget()
            #新增下一個品項名稱到label
            self.yield_data_wrap()  #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXfunction有問題


    def attr_fetch(self):
        # fetch attribute data from db      fetchone資料形式 (data,):擷取資料方法= id[0]
        cursor.execute("SELECT subclass_id FROM attr_subclass WHERE subclass_name= '%s'" % self.attr_subclass.get())
        id_subclass = cursor.fetchone()
        cursor.execute("SELECT function_id FROM attr_function WHERE function_name= '%s'" % self.attr_function.get())
        id_function = cursor.fetchone()
        cursor.execute("SELECT type_id FROM attr_type WHERE type_name= '%s'" % self.attr_type.get())
        id_type = cursor.fetchone()
        subclass_get = self.attr_subclass.get()

        cursor.execute(
            "SELECT class_id FROM attr_class WHERE class_name= '%s'" % dict.subclass_class[subclass_get])
        id_class = cursor.fetchone()
        p_attr = id_class[0] + id_subclass[0] + id_function[0] + id_type[0]
        # commit to attr_class
        # attribute table找是否有相同的attribute code 沒有則新增
        if cursor.execute("SELECT attribute_code FROM product_attribute WHERE attribute_code = '%s'" % p_attr):
            pass
        else:
            cursor.execute(idb.insert_attribute(p_attr, id_class[0], id_subclass[0], id_function[0], id_type[0]))
            db.commit()

        return p_attr

    def code_rule(self, code):
        if int(code) < 9:
            return '0' + str(int(code) + 1)
        else:
            return str(int(code) + 1)

    def yield_data_wrap(self):
        self.data_list = next(self.gyd)
        #檢查是否跟上一個品名相同
        #while self.data_list:
        self.p_name.set(self.data_list[self.name])

        while self.data_list[self.x2] == self.last_data[self.x2]:
            self.either_proorset1()
        self.either_proorset2()

    def either_proorset1(self):
        if '組' in self.data_list[self.name]:
            '''
            cursor.execute(idb.insert_selling_set(
                self.data_list[self.x2], self.data_list[self.date][:10], self.data_list[self.amount]))
            db.commit()
            '''
            pass
        else:
            cursor.execute(idb.insert_selling(
                self.data_list[self.x2], self.data_list[self.date][:10], self.data_list[self.amount]))
            db.commit()
        self.data_list = next(self.gyd)
        self.p_name.set(self.data_list[self.name])

    def either_proorset2(self):
        del self.last_data[:]
        self.last_data.append(self.data_list[self.x2])
        self.last_data.append(self.data_list[self.name])  # 儲存當前產品名稱比較下個產品

        if '組' in self.data_list[self.name]:
            # 執行insert set模組
            '''
            if cursor.execute("SELECT pid FROM special_set WHERE pid= '%s'" % self.data_list[self.x2]):
                cursor.execute(idb.insert_selling_set(
                    self.data_list[self.x2], self.data_list[self.date], self.data_list[self.amount]))
                db.commit()
                self.yield_data_wrap()
            else:
                self.frame.pack_forget()
                insert_set_fr(self.frame, self.gyd, self.data_list, self.last_data, 'set', self.p_name)
            '''
            self.yield_data_wrap()
        else:
            # 執行insert product模組
            if cursor.execute("SELECT pid FROM product WHERE pid = '%s'" % self.data_list[self.x2]):
                cursor.execute(idb.insert_selling(
                    self.data_list[self.x2], self.data_list[self.date][:10], self.data_list[self.amount]))
                db.commit()
                self.yield_data_wrap()
            else:
                self.frame.pack_forget()
                insert_product_fr(self.frame, self.gyd, self.data_list, self.last_data, 'prod', self.p_name)  # 包含新增單品健

    def return_subclass(self):
        cursor.execute("SELECT subclass_name FROM attr_subclass")
        data = cursor.fetchall()
        return data

    def return_type(self):
        cursor.execute("SELECT type_name FROM attr_type")
        data = cursor.fetchall()
        return data

    def return_function(self):
        cursor.execute("SELECT function_name FROM attr_function")
        data = cursor.fetchall()
        return data

    def return_parcel(self):
        cursor.execute("SELECT parcel_name FROM attr_parcel")
        data = cursor.fetchall()
        return data



class insert_set_fr(insert_product_fr):
    def __init__(self, frame, gyd, data_list, last_data, p_name):
        self.frame = frame
        self.p_name = p_name
        self.gyd = gyd
        self.data_list = data_list
        self.last_data = last_data
        self.prod_list = [] #單品陣列
        self.set_prodlist = []
        #new_frame variable
        self.new_item_list = [] # 要新增單品的儲存陣列

        self.widget_opt = {'fill': BOTH, 'expand': Y, 'padx': 5, 'pady': 5}
        set_product_count = IntVar()

        self.set_entry_frame = Frame(self.frame)
        self.bottom_frame = Frame(self.frame)

        self.new_single(set_product_count)
        self.new_product_btn = Button(self.bottom_frame, text="+新增單品", command=lambda count=set_product_count:
            self.new_single(count), underline=0)

        self.set_new_btn = Button(self.bottom_frame, text="新增特惠組", command=lambda count=set_product_count:
            self.add_set(count))
        self.insert_set_fr_pack()

    def insert_set_fr_pack(self):
        self.frame.pack(**self.widget_opt)
        self.set_entry_frame.pack(**self.widget_opt)
        self.bottom_frame.pack(**self.widget_opt)
        self.bottom_frame.pack(side=BOTTOM)
        self.new_product_btn.pack()
        Label(self.bottom_frame, text='').pack(**self.widget_opt)
        self.set_new_btn.pack(**self.widget_opt)

    def add_set(self, count): #frame= set_entry_frame
        p_index=0

        for prod in self.prod_list:
            # 檢查上一個單品是否存在DB，沒有則跳出單品新增視窗 (若輸入為空值則跳message說為空值)
            check_name = '%'+prod.get_name()+'%'
            if cursor.execute("SELECT pid, product_name FROM product WHERE product_name LIKE '%s'" %check_name):
                self.prod_list.remove(prod)
                namo= cursor.fetchall()
                if self.check_num(namo) == 1:
                    cursor.execute("INSERT INTO special_set(pid, bid, set_id, set_name, set_price, amount_of_set) \
                                     VALUE ('%s', '%s', '%s', '%s', '%s', '%d')"
                                   % (namo[p_index], self.data_list[self.x2][:3], self.data_list[self.x2],
                                      self.data_list[self.name], self.data_list[self.price][:-2], prod.get_num()))
                else:
                    temp = []
                    for item_cont in namo:
                        tempo = st.item(item_cont[0],item_cont[1])
                        temp.append(tempo)
                    set_prod = st.add_set_item(prod.get_name(), prod.get_num, temp)
                    self.set_prodlist.append(set_prod)

        if self.set_prodlist or self.prod_list:  #找到但是很多項 或是 在DB沒找到的，則另外開窗
            self.pos_new()

            #super().yield_data_wrap(self.p_name)
        count.set(0)

    def pos_new(self):
        new = Tk()
        new_frame = Frame(new)
        new_frame_prod = Frame(new)
        multi_item_frame = Frame(new_frame_prod)
        not_in_db_frame = Frame(new_frame_prod)
        for prod in self.set_prodlist:
            self.pos_new_mult(multi_item_frame,prod) #prod: add_set_item的struct

        for prod in self.prod_list: #沒有在ＤＢ的情況開一個新增產品frame的 function
            self.pos_new_not(not_in_db_frame, prod)

        new_btn = Button(new_frame, text='新增產品群', command=self.new_set_item())

        new_frame.pack(expand=Y, fill=BOTH)
        new_frame_prod.pack(expand=Y, fill=BOTH)
        multi_item_frame.pack(**self.widget_opt)
        multi_item_frame.pack(side=LEFT)
        not_in_db_frame.pack(**self.widget_opt)
        not_in_db_frame.pack(side=LEFT)
        new_btn.pack(side=BOTTOM)

    def new_set_item(self):
        #self.multi_item_list, self.new_item_list
        for prod in self.set_prodlist: #prod = add_set_item()
            #choose one to update to DB好幾個item 的 checkbutton
            for item in prod.list:
                if item.checkbtn.get():
                    # insert into DB-special_set
                    cursor.execute("INSERT INTO special_set(pid, bid, set_id, set_name, set_price, amount_of_pid) \
                                   VALUES ('%s', '%s', '%s', '%s', '%s', '%d')"
                                   % (item.pid, self.data_list[self.x2][:3], self.data_list[self.x2],
                                      self.data_list[self.name], self.data_list[self.price][:-2], prod.get_num()))
                    #insert into DB-selling
                    cursor.execute(idb.insert_selling(
                        item.pid, self.data_list[self.x2][:3], self.data_list[self.date][:10],
                        self.data_list[self.amount]*prod.amount))
        for prod in self.new_item_list: #prod = new_prod_struct()
            #新增產品到DB-product
            pid = prod.prod_attr.add_product(self.p_name)
            # 新增set到DB-special_set
            cursor.execute("INSERT INTO special_set(pid, bid, set_id, set_name, set_price, amount_of_pid) \
                                                           VALUES ('%s', '%s', '%s', '%s', '%s', '%d')"
                           % (pid, self.data_list[self.x2][:3], self.data_list[self.x2], self.data_list[self.name],
                              self.data_list[self.price], prod.get_num()))
            # insert into DB-selling
            cursor.execute(idb.insert_selling(pid, self.data_list[self.date][:10], self.data_list[self.amount] * prod.amount))

        #insert into special_set_selling
        cursor.execute(idb.insert_selling_set(self.data_list[self.x2],
                                              self.data_list[self.date][:10], self.data_list[self.amount]))
        #下一個
        self.yield_data_wrap()

    def pos_new_mult(self, frame, prod): #新增一個多重選擇的set_frame
        mult_pro_frame = Frame(frame)
        prod_name = Label(mult_pro_frame, text=prod.name)
        for item in prod.list:
            var=BooleanVar()
            check_item = Checkbutton(mult_pro_frame, text=item.name, onvalue=1, offvalue=0, variable=var)
            check_item.pack(**self.widget_opt)
            item.checkbtn = var #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXcheckbutton變數

        mult_pro_frame.pack(**self.widget_opt)
        prod_name.pack(**self.widget_opt)

    def pos_new_not(self, frame, prod):
        prod_name = Label(frame, textvariable=prod.get_name(), name='roasted_name').pack(
            **self.widget_opt)
        new_prod = insert_product_fr(frame, self.gyd, self.data_list, self.last_data, 'set', prod.get_name)
        new_prod.add_event.pack_forget()
        new_prod_struct = st.add_set_newprod(prod.get_name, prod.get_num, new_prod)
        self.new_item_list.append(new_prod_struct)

    def check_num(self, data_list):
        data_count = 0
        for data in data_list:
            data_count += 1
        return data_count


    def new_single(self, count):
        prod = set_frame_new_single(count, self.set_entry_frame)
        self.prod_list.append(prod)  # 單品物件塞入陣列

class set_frame_new_single():
    def __init__(self, count, frame):
        self.frame = frame
        self.count = count
        self.c = count.get()
        count.set(self.c + 1)
        set_frame = Frame(self.frame)
        set_title = Label(set_frame, textvariable='產品' + str(self.c + 1), width=10)
        self.set_input = Entry(set_frame, width=20)
        item_num_title = Label(set_frame, text='數量')
        self.item_num = Entry(set_frame, width=5)
        self.widget_opt = {'fill': BOTH, 'expand': Y, 'padx': 5, 'pady': 5}
        set_frame.pack(**self.widget_opt)
        set_title.pack(**self.widget_opt)
        set_title.pack(side=LEFT)
        self.set_input.pack(**self.widget_opt)
        self.set_input.pack(side=LEFT)
        item_num_title.pack(**self.widget_opt)
        item_num_title.pack(side=LEFT)
        self.item_num.pack(**self.widget_opt)
        self.item_num.pack(side=LEFT)

    def get_name(self):
        return self.set_input.get()

    def get_num(self):
       return self.item_num.get()


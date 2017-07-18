'''
from tkinter import *
from tkinter.ttk import *


win.title('新增資料庫')
win.mainloop()
'''
import MySQLdb as SQL
import dictionary as dict
import os
import import_to_DB_class as idb
import framework as fw
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import csv
import cosdata as cosd

db_password = "tl3n3xk7"
db_name = "cosmetic"


class NotebookDemo(Frame):

    def __init__(self, name='notebookdemo'):
        Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('楊副理')
        self.p_name = StringVar()
        self._create_widgets()


    def _create_widgets(self):
        self._create_demo_panel()

    def _create_demo_panel(self):
        demoPanel = Frame(self, name='demo')
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)

        # create the notebook
        nb = ttk.Notebook(demoPanel, name='notebook')

        # extend bindings to top level window allowing
        #   CTRL+TAB - cycles thru tabs
        #   SHIFT+CTRL+TAB - previous tab
        #   ALT+K - select tab using mnemonic (K = underlined letter)
        #nb.enable_traversal()

        nb.pack(fill=BOTH, expand=Y)
        self._create_filewalker_tab(nb)
        self._create_product_tab(nb)
        #self._create_text_tab(nb)

    def _create_filewalker_tab(self, nb):
        # frame to hold contentx
        self.row_file_name = StringVar()
        frame = Frame(nb, name='descrip')
        file_cook_btn = Button(frame, text='選擇要煮的檔案', command=lambda fn=self.row_file_name: self.aof(fn))
        file_name_text = Label(frame, textvariable=self.row_file_name)
        file_roast_btn = Button(frame, text='煮一煮', command=lambda: self.roast_row_file())
        self.file_mention_text = Label(frame, text='煮完了!')
        file_cook_btn.pack()
        file_name_text.pack()
        file_roast_btn.pack()


        nb.add(frame, text='煮sap資料', underline=0, padding=2)

    def roast_row_file(self):
            cosd.roast_the_data(self.row_file_name.get())
            self.file_mention_text.pack()

    def callback(event):
        print("say something")
    # =============================================================================
    def _create_product_tab(self, nb):
        # Populate the second pane. Note that the content doesn't really matter
        frame = Frame(nb)

        self.generator_yield_data = object
        testo = StringVar()

        file_pointer = StringVar() #絕對路徑

        self.data_list = list  #yield當前資料串列
        self.last_data = ['x','x'] #前一筆資料陣列，加速新增selling速度
        self.widget_opt = {'fill': BOTH, 'expand': Y, 'padx': 5, 'pady': 5}
        #擷取資料代表欄位
        self.x2 = 0
        self.name = 1
        self.amount = 2
        self.date = 3
        self.price = 4
        self.tess = StringVar()
        self.file_name = StringVar()  # 乾淨的檔案名稱
        select_file = Button(frame, text='選擇檔案', command=lambda f_pointer=file_pointer, p_name=self.p_name:
            self.askopenfilename(f_pointer, p_name)).pack(**self.widget_opt)

        file_name = Label(frame, textvariable=self.file_name)
        file_name.pack(**self.widget_opt)
        self.update2restore = Button(frame, text='上傳檔案資料', command=self.to_restore)

        #tester = Label(frame, textvariable=self.p_name).pack()
        #get_start = Button(frame, text='get start', command=lambda p_name=product_name:
        #self.yield_data_wrap(p_name), name='yd') # test yield_data_wrap function
        #get_start.pack(**self.widget_opt)

        #-----------------------------------------------特惠組frame
        self.set_frame = Frame(frame)

        #-----------------------------------------------單品frame
        self.attr_frame = Frame(frame)

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure((0, 1), weight=1, uniform=1)
        nb.add(frame, text='新增產品項目', underline=0)

        # test = Label(frame, textvariable=testo).pack(side=LEFT)

    def to_restore(self):


        #print(type(prod_temp))
        if cursor.execute(idb.search_restore(self.file_name.get())):
            prod_temp = cursor.fetchone()
            if prod_temp[0] == self.p_name.get():
                messagebox.showinfo('資料庫提示', '資料庫已更新為最新!勿拍打餵食!')
            else:
                cursor.execute("UPDATE restore_table SET prod_name= '%s' WHERE file_name='%s'"
                               % (self.p_name.get(), self.file_name.get()))
                db.commit()
                messagebox.showinfo('資料庫提示', '資料庫更新成功!')
        else:
            cursor.execute("INSERT INTO restore_table(file_name, prod_name) VALUE ('%s','%s')"
                           % (self.file_name.get(), self.p_name.get()))
            db.commit()
            messagebox.showinfo('資料庫提示', '資料上傳成功!')

    def askopenfilename(self, file, p_name):
        self.file_opt = options = {}
        options['defaultextension'] = '.csv'
        options['filetypes'] = [('all files', '.*'), ('csv files', '.csv')]
        options['initialdir'] = os.getcwd()
        options['initialfile'] = 'myfile.csv'
        options['title'] = '選擇要餵的資料'
        # get filename
        filename = filedialog.askopenfilename(**self.file_opt)
        file.set(filename)
        file_temp = filename.split('/')
        self.file_name.set(file_temp[-1])
        self.generator_yield_data = self.yield_data(filename)
        self.update2restore.pack(**self.widget_opt)
        self.yield_data_wrap()
        self.update()

    def aof(self, file_n):
        self.file_opt = options = {}
        options['defaultextension'] = '.csv'
        options['filetypes'] = [('all files', '.*'), ('csv files', '.csv')]
        options['initialdir'] = os.getcwd()
        options['initialfile'] = 'myfile.csv'
        options['title'] = '選擇要餵的資料'
        # get filename
        filename = filedialog.askopenfilename(**self.file_opt)
        file_n.set(filename)

    def yield_data(self, filename):  # yield 批次讀取資料
        data = open(filename, 'r')
        #偵測是否有處理過資料

        if cursor.execute(idb.search_restore(self.file_name.get())):
            prod_name = cursor.fetchone()
            for emp in csv.reader(data):
                if prod_name[0] in emp[1]:
                    yield emp
                    break

        for row in csv.reader(data):
            yield row

    def yield_data_wrap(self):
        self.data_list = next(self.generator_yield_data)
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
                self.data_list[self.x2], self.data_list[self.date], self.data_list[self.amount]))
            db.commit()
            '''
            pass
        else:
            cursor.execute(idb.insert_selling(
                self.data_list[self.x2], self.data_list[self.date][:10], self.data_list[self.amount]))
            db.commit()
        self.data_list = next(self.generator_yield_data)
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
                self.attr_frame.pack_forget()
                self.set_frame.pack(**self.widget_opt)
                fw.insert_set_fr(self.set_frame, self.generator_yield_data,
                                 self.data_list, self.last_data, self.roasted_name, self.p_name)
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
                self.set_frame.pack_forget()
                self.attr_frame.pack(**self.widget_opt)
                fw.insert_product_fr(self.attr_frame, self.generator_yield_data, self.data_list,
                                     self.last_data, 'prod', self.p_name)  # 包含新增單品健
                #self.tess.set(self.data_list[1])



    # =============================================================================
    def _create_text_tab(self, nb):
        # populate the third frame with a text widget
        frame = Frame(nb)

        txt = Text(frame, wrap=WORD, width=40, height=10)
        vscroll = Scrollbar(frame, orient=VERTICAL, command=txt.yview)
        txt['yscroll'] = vscroll.set
        vscroll.pack(side=RIGHT, fill=Y)
        txt.pack(fill=BOTH, expand=Y)

        # add to notebook (underline = index for short-cut character)
        nb.add(frame, text='Text Editor', underline=0)


def on_closing():
    if messagebox.askokcancel("Quit", "是否已經按下'上傳檔案資料'鍵?"):
        win.destroy()

if __name__ == '__main__':
    db = SQL.connect("192.168.1.108", "wu0h961738", db_password, db_name, charset='utf8')
    cursor = db.cursor()
    win = Tk()
    win.protocol("WM_DELETE_WINDOW", on_closing)
    NotebookDemo().mainloop()




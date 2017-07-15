'''
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
import dictionary as di

root = Tk()
frame = Frame(root)
frame.pack(expand=Y, fill=BOTH)
combotext = StringVar()

class new_single_G():
    def __init__(self, count, frame):
        self.frame = frame
        self.count = count
        self.set_input = Entry(self.frame, width=20)
        self.set_input.pack(expand=Y)
    def get_name(self):
        return self.set_input.get()

def _say_neat(v,r):
    if r.get()==attr_subclass.get():
        v.set(r.get())
    if r.get()=='3':

        bottomframe.pack()
    if r.get()=='2':
        bottomframe.pack_forget()
        checkframe.pack()
    attr_subclass.set('')

def neww():
    new = Tk()
    new_frame =Frame(new)
    new_frame.pack(expand=Y, fill=BOTH,side=LEFT)
    Label(new_frame,text='ahah').pack()

def new_single(count):
    c=count.get()
    count.set(c+1)


attr_subclass = ttk.Combobox(frame, width=10, values=(0,1,2,3,4,5))
attr_subclass.pack()
roasted_name = Label(frame, textvariable=combotext)
roasted_name.pack()


neatVar = StringVar()
btn = Button(frame, text='Neat!', underline=0,
             command=lambda v=combotext:_say_neat(v, attr_subclass))
btn.pack()

bottomframe = Frame(root)
redbutton = Button(bottomframe, text="Red", fg="red", command=neww)
greenbutton = Button(bottomframe, text="Brown", fg="brown")
bluebutton = Button(bottomframe, text="Blue", fg="blue")
blackbutton = Button(bottomframe, text="Black", fg="black")
set_product_count = IntVar()
new_product_btn = Button(frame, text="新增單品", command=lambda count=set_product_count: new_single(count))
new_product_text = Label(frame, textvariable=str(set_product_count))
new_product_btn.pack()
new_product_text.pack()
redbutton.pack(side=LEFT)
greenbutton.pack(side=LEFT)
bluebutton.pack(side=LEFT)
blackbutton.pack()

class new():
    def __init__(self):
        c= StringVar()
        list_out = StringVar()
        listp=[]
        self.var1 = BooleanVar()
        check_la = StringVar()
        self.checkframe = Frame(root)
        self.checkframe.pack()
        self.testo = 'DDDDDDDDtest'
        fuck = new_single_G(2, self.checkframe)
        btnn= Button(frame, text="self?", command=lambda: self.dealing_re(listp,self.checkframe))
        listp.append(fuck)
        texx = Label(self.checkframe, textvariable=list_out)
        bt = Button(self.checkframe, text="done", command=lambda: self.deal_end(list_out,listp))
        self.check_test = Checkbutton(frame, text='areuready', onvalue=1, offvalue=0, variable=self.var1, name='areuready',command=lambda v=self.var1: self.stat_cha(v))
        self.check_test.pack()
        check_btn = Button(frame, text="areche?", command=lambda label=check_la: self.check_fun(label))
        check_btn.pack()
        checl_label = Label(frame, textvariable=check_la)
        checl_label.pack()
        texx.pack()
        bt.pack(side=BOTTOM)
        btnn.pack(side=BOTTOM)

    def stat_cha(self, var):
        pass
        #var.set(not var)

    def check_fun(self, text):
        if self.var1.get()==FALSE:
            text.set('no')
        elif self.var1.get()==TRUE:
            text.set('eys')

    def dealing_re(self, listo, frame):
        a8 = new_single_G(2, self.checkframe)
        self.testo = 'haha'
        listo.append(a8)
        # last_d = Button(frame, text="self?", command=lambda: dealing_re(last_d, listo, pl))
        # last_d.pack(side=BOTTOM)
        # listo.insert(0, a8.get_name())

    def deal_end(self, list_out, list_in):
        te = []
        for i in list_in:
            te.append(i.get_name())

        te.append(self.testo)
        list_out.set(te)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        print('gg')
        root.destroy()
new()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
'''


#DB搜尋字串
import MySQLdb as ms

db = ms.connect("localhost", "root", "tl3n3xk7", "cosmetic", charset='utf8')
cursor = db.cursor()
ss='%'+'唇'+'%'

if cursor.execute("SELECT subclass_id, subclass_name FROM attr_subclass WHERE subclass_name LIKE '%s'ORDER BY subclass_name DESC" %ss):
    data = cursor.fetchone()
    if data[1][:1].find('唇')==0:
        print(data[1][:1])
    print('---------------------------------')
    #for row in data:
     #   print(row[0])

cursor.execute("SELECT subclass_name FROM attr_subclass WHERE subclass_name LIKE '%s'" %ss)
data = cursor.fetchall()
print('uuuuuuuuuuuuuunordered list:')
for row in data:
    print(row[0])

db.close()
#取值= row[0]

'''
import csv


filename = "C:\\Users\\jimmy\\PycharmProjects\\untitled\\data\\ggc_roast.csv"
def test(filename):
    data = open(filename, 'r')
    for x in csv.reader(data):
        if '62' in x[1]:
            break
    for row in csv.reader(data):
       yield row

a = test(filename)
print(next(a))
'''
x = 'asdfasdfasdsssssss'
print(x[:-3])
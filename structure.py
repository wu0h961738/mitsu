class add_set_item(): #1-1
    def __init__(self, name, amount, i_list): #list = item()s
        self.name = name
        self.amount =amount
        self.list = i_list # DB資料 好多個item


class item(): #從DB上找到的項目 #1-2
    def __init__(self, pid, name):
        self.name = name
        self.pid = pid
        self.checkbtn = int #checkbutton 資料

class add_set_newprod(): #未在ＤＢ上　＃２－１
    def __init__(self, name, amount, attr):
        self.name = name
        self.amount = amount
        self.prod_attr = attr


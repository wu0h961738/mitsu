from tkinter import *
import os
from tkinter import filedialog

master = Tk()

file_opt = options = {}
options['defaultextension'] = '.csv'
options['filetypes'] = [('all files', '.*'), ('csv files', '.csv')]
options['initialdir'] = os.getcwd()
options['initialfile'] = 'myfile.csv'
options['title'] = '選擇要餵的資料'
# get filename
filename = filedialog.askopenfilename(**file_opt)
print(filename)
#w.configure(state="disabled")

# if tkinter is 8.5 or above you'll want the selection background
# to appear like it does when the widget is activated
# comment this out for older versions of Tkinter
#w.configure(inactiveselectbackground=w.cget("selectbackground"))

mainloop()
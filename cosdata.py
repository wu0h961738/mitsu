import csv
import datetime
import os
import codecs
import sys
'''
說明:
1.find_unroasted_file: 再根目錄以下的資料夾找副檔名為.csv且尚未處理過之資料
    return 變數'DATA_file'=未加上路徑之乾淨檔名
'''

def find_unroasted_file():
    directory = os.getcwd()+'\\data'
    finder = '_roast'
    del_temp = []
    try:
        for (dirpath, dirnames, file_names) in os.walk(directory):
            pass
        for file_name in file_names:
            if file_name.find(finder) != -1:
                del_temp.append(file_name)
                del_temp.append(file_name.replace(finder, ''))
        for temp in del_temp:
            file_names.remove(temp)
        going_roast = file_names[0]
        file_names.remove(file_names[0])
        return (going_roast, file_names)
    except:
        print('done with roasting')
        sys.exit()


def roast_the_data(RTD_file_name):
    row_data = codecs.open(RTD_file_name, 'r', encoding='utf-8')
    roast_data = open(RTD_file_name.replace('.csv', '_roast.csv'), 'w', newline='', encoding='utf-8')
    w = csv.writer(roast_data)
    line = 0

    for row in csv.reader(row_data):
        line += 1
        del row[0:3], row[1], row[3:6], row[5:9]
        if (line != 1) & (row[0] != ''):
            row[0] = row[0][3:] #brand_code+pid
            date_temp = datetime.datetime.strptime(row[3], '%Y/%m/%d').timestamp() #convert to timestamp
            row[3] = date_temp
            row[4] = str(int(row[4])/int(row[2])) #convert sell_price into positive num
            row[2] = str(0-int(row[2])) #convert sell_amount into positive num
            w.writerow(row)
    roast_data.close()
    row_data.close()

def check_data_set(data_set):
    try:
        data=data_set[0]
        data_set.remove(data)
        return (data, data_set)
    except:
        print('done with roasting!')
        sys.exit()


'''
while 1:
    (DATA_file, DATA_set) = find_unroasted_file()
    print(DATA_file)
    print(DATA_set)
    roast_the_data('data/' + DATA_file) #name = data_directory + data_file_name
    #doing insert stuff
    (DATA_file, DATA_set) =check_data_set(DATA_set)
'''
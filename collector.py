# -*- coding: utf-8 -*-
from netmiko import ConnectHandler
import threading
import xlrd
import os

wb=xlrd.open_workbook('book.xlsx')
sheet=wb.sheet_by_index(0)
list_device=[]
path=str(os.getcwd())+'/results'

if 'results' not in os.listdir():
    os.mkdir(path)

nrows=sheet.nrows
ncols=sheet.ncols
n=0

for x in range(nrows):
    arr = []
    for i in range (ncols):
        arr.append(sheet.cell_value(x,i))
    list_device.append(arr)


print(list_device)

lst = [];die=[];diel=open('die.txt','w')


def try_connect(ipadx):
    try:
        connect_ssh=ConnectHandler(device_type='cisco_ios_telnet',username=ipadx[1],password=ipadx[2],secret=ipadx[3],ip=ipadx[0])
        connect_ssh.enable()
        find_hostname = connect_ssh.find_prompt()
        connect_ssh.send_command("terminal len 0")
        connect_ssh.open_session_log('results/'+ find_hostname  +'.txt', 'w')
        connect_ssh.send_command('sh run') # you can edit this command
        connect_ssh.close_session_log()


    except:
        die.append(ipadx);diel.write(ipadx+'\n')

for i in list_device:
    t = threading.Thread(target=try_connect, args=(i,))
    lst.append(t)

for t in lst:
    t.start()

for t in lst:
    t.join()
del t

if not die:
    print('\nSUCCESS')
else :
    print ('\nSUCCESS\n### list device down ###');diel.close()

    for i in range (len(die)):
        print (die[i])

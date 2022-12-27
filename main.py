import datetime
import os
from tkinter import ttk
import tkinter as tk
import sqlite3


ql = tk.Tk()
title = ttk.Label(ql,text="Quản Lý Thống Kê").grid(row=0,column=1)
tab_ctr = ttk.Notebook(ql)
tab1 = ttk.Frame(tab_ctr)
tab2 = ttk.Frame(tab_ctr)
#
day = ttk.Label(tab1,text=datetime.datetime.now())
day.grid(row=1)


namedatabase =str( datetime.date.today())
def connect(name):
    con1 = sqlite3.connect(name+".db")
    con2 = sqlite3.connect("data.db")
    cur1 = con1.cursor()
    cur2 = con2.cursor()
    # cur2.execute("CREATE TABLE IF NOT EXISTS emp(id,  name TEXT, status TEXT)")
    #
    #
    # cur2.execute("INSERT INTO emp VALUES (?, ?, ?)", (1, "Tien Dat", ""))
    # cur2.execute("INSERT INTO emp VALUES (?, ?, ?)", (2, "Hai Dang", ""))
    # cur2.execute("INSERT INTO emp VALUES (?, ?, ?)", (3, "Bao Huu", ""))
    # cur2.execute("INSERT INTO emp VALUES (?, ?, ?)", (4, "Hong Thai", ""))
    # cur2.execute("INSERT INTO emp VALUES (?, ?, ?)", (5, "Xuan Thuong", ""))
    # cur2.execute("INSERT INTO emp VALUES (?, ?, ?)", (6, "Chu An", ""))
    # cur2.execute("INSERT INTO emp VALUES (?, ?, ?)", (7, "Tra My", ""))
    try:
        cur1.execute("SELECT * FROM emp")
        # storing the data in a list
        data_list = cur1.fetchall()
        for item in data_list:
            print(item)
    except sqlite3.OperationalError:
        cur1.execute("CREATE TABLE IF NOT EXISTS emp(id,  name TEXT, status TEXT)")
        cur2.execute("SELECT * FROM emp")
        # storing the data in a list
        data_list = cur2.fetchall()
        for i in data_list:
            cur1.execute("INSERT INTO emp VALUES (?, ?, ?)", (i[0], i[1], i[2]))

    con1.commit()
    con2.commit()
    con1.close()
    con2.close()

def View():
    con2 = sqlite3.connect(namedatabase + ".db")
    cur2 = con2.cursor()
    cur2.execute("SELECT * FROM emp")
    rows = cur2.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    con2.close()

def SecondWD(id):
    sc=tk.Tk()
    var = tk.IntVar(sc,2)
    def sel():
        selection = "You selected the option " + str(var.get())
        print(selection)
        if (var.get() == 1):
            tt = "Vang"
        else:
            tt = "Dung Gio"
        con1 = sqlite3.connect(namedatabase + ".db")
        con1.execute(f'UPDATE emp SET status="{tt}" WHERE id={id}')
        for i in tree.get_children():
            tree.delete(i)
        cur2 = con1.cursor()
        cur2.execute("SELECT * FROM emp")
        rows = cur2.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)
        con1.commit()
        con1.close()
        sc.destroy()
    ttk.Radiobutton(sc,text="Vang",variable=var,value=1,command=sel).grid(row=0,column=1)
    ttk.Radiobutton(sc, text="Dung Gio", variable=var, value=2,command=sel).grid(row=2,column=1)
    sc.mainloop()


def selectItem(a):
    trv = tree.selection()[0]
    curItem = tree.focus()
    SecondWD(tree.item(curItem)['values'][0])

def timkiem():
    a=int(findbox.get())
    print(a)
    con2 = sqlite3.connect(namedatabase + ".db")
    cur2 = con2.cursor()
    for i in tree.get_children():
        tree.delete(i)
    cur2.execute("SELECT * FROM emp WHERE id=?", (a,))
    rows = cur2.fetchall()
    for row in rows:
        print(row)
        tree.insert("", tk.END, values=row)
    con2.close()
lst = []
def HTtuan():
    path = "/home/judai/PycharmProjects/thongke"
    lst_db = []
    for item in os.listdir(path):
        if item.endswith('.db') and item != "data.db":
            lst_db.append(item)
    lst_nv = dict()
    lst_vang = dict()
    lst_all = []
    for item in lst_db:
        con2 = sqlite3.connect(item)
        cur2 = con2.cursor()
        cur2.execute("SELECT * FROM emp")
        rows = cur2.fetchall()
        for r in rows:
            if str(r[0]) not in lst_nv:
                lst_nv[str(r[0])] = r[1]
        lst_all.append(rows)
    for id in lst_nv:
        lst_vang[id] = 0
    for row in lst_all:
        for item in row:
            if item[2] == "Vang" or item[2] == '':
                lst_vang[str(item[0])] = lst_vang[str(item[0])] + 1
    for id in lst_nv:
        print(str(id) + "\t" + lst_nv[id] + "\t" + str(lst_vang[id]) + "\n")
        t = tuple((str(id), str(lst_nv[id]), str(lst_vang[id])))
        lst.append(t)
    for row in lst:
        print(row)
        week.insert("", tk.END, values=row)
def reloadBT():
    for i in week.get_children():
        week.delete(i)
    lst.clear()
    HTtuan()



connect(namedatabase)
tree = ttk.Treeview(tab1, column=("c1", "c2", "c3"), show='headings')
tree.column("#1", anchor=tk.CENTER)
tree.heading("#1", text="Mã Nhân Viên")
tree.column("#2", anchor=tk.CENTER)
tree.heading( "#2", text="Tên Nhân Viên")
tree.column("#3", anchor=tk.CENTER)
tree.heading("#3", text="Tình trạng")
tree.grid(row=4)
View()
findbox = ttk.Entry(tab1)
findbox.grid(row=2,column=0)
btfind = ttk.Button(tab1,text="Tim",command=timkiem)
btfind.grid(row=3,column=0)
button =ttk.Button(tab1,text="Sửa thông tin",command=View)
button.grid(row=5)
week = ttk.Treeview(tab2, column=("c1", "c2", "c3"), show='headings')
week.column("#1", anchor=tk.CENTER)
week.heading("#1", text="Mã Nhân Viên")
week.column("#2", anchor=tk.CENTER)
week.heading( "#2", text="Tên Nhân Viên")
week.column("#3", anchor=tk.CENTER)
week.heading("#3", text="So Buoi Nghi")
week.grid(row=1)
HTtuan()
reloadbt = ttk.Button(tab2,text="Reload",command=reloadBT)
reloadbt.grid(row=2)
tab_ctr.add(tab1,text='Ngày')
tab_ctr.add(tab2,text='Tuần')
tab_ctr.grid(row=1,column=1)
tree.bind('<ButtonRelease-1>', selectItem)
ql.mainloop()






# coding:utf-8
import sqlite3

con = None

def connect_db():
    global con
    try:
        con = sqlite3.connect('lianjia.db')
        con.text_factory = str
    except Exception:
        print 'connect_db error'

def close_db():
    global con
    try:
        con.close()
    except Exception:
        print 'close_db error'

def dongchengjiaoshui_create_table():
    global con
    try:
        con.execute('drop table if exists dongchengjiaoshui')
        con.execute('create table dongchengjiaoshui (id integer primary key not null, hetonghao varchar(100) not null,'
                    'kehuxingming varchar(100) not null, kehushenfenzheng varchar(100) not null, guohuzhuanyuan varchar(100) not null,'
                    'yuyueshijian varchar(100) not null, dateType varchar(100),'
                    'status varchar(10) not null)')
    except Exception:
        print 'dongchengjiaoshui_create_table error'
        connect_db()

def dongchengjiaoshui_insert(info):
    global con
    try:
        con.execute('insert into dongchengjiaoshui (hetonghao, kehuxingming, kehushenfenzheng,'
                    'guohuzhuanyuan, yuyueshijian, dateType, status)'
                    'values (?, ?, ?, ?, ?)', info)
        con.commit()
    except Exception:
        print 'dongchengjiaoshui_insert error'
        connect_db()
def dongchengjiaoshui_update(info):
    try:
        con.execute('update dongchengjiaoshui set '
                    'hetonghao = ?,'
                    'kehuxingming = ?,'
                    'kehushenfenzheng = ?,'
                    'guohuzhuanyuan = ?,'
                    'yuyueshijian = ?,'
                    'dateType = ?,'
                    'status = ? where id = ?', info)
        con.commit()
    except Exception:
        print 'dongchengjiaoshui_update error'
        connect_db()

def dongchengjiaoshui_select():
    cur = con.cursor()
    cur.execute('select * from dongchengjiaoshui')
    return cur.fetchall()
    try:
        con.execute('select hetonghao, kehuxingming, kehushenfenzheng,'
                    'guohuzhuanyuan, yuyueshijian, dateType, status from dongchengjiaoshui')
        return con.fetchall()
    except Exception:
        print 'dongchengjiaoshui_select error'
        connect_db()

def foo():
    return 1, 2

if __name__ == '__main__':
    a = '1'
    if a is '1':
        print 'dengyu 1'
    else:
        print 'budeng'
    #connect_db()
    #dongchengjiaoshui_create_table()
    #a = ('123', 'ss', '456', 'mm', '0')
    #for i in a:
    #    print type(i)
    #    dongchengjiaoshui_insert(a)
    #    #dongchengjiaoshui_insert(['323', 'ss', '456', 'mm', '0'])
    #    #dongchengjiaoshui_insert(('223', 'ss', '456', 'mm', '0'))
    #    #dongchengjiaoshui_update(('897', 'hh', '234', 'll', '1', 2))
    #    for item in dongchengjiaoshui_select():
    #        for i in item:
    #            print type(i)
    #            close_db()

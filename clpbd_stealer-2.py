#coding:utf-8

import win32clipboard
import time

def get_clipboard(old_data):
    try:
        win32clipboard.OpenClipboard()
        clipboardData = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        if clipboardData == old_data:
            return None
        else:
            return clipboardData
    except:
        return None

old_data = ''

while True:
    data = get_clipboard(old_data)
    if data:
        old_data = data
        print data
    time.sleep(1)
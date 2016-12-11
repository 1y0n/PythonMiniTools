#coding:utf-8

from PyQt4.QtGui import *

app = QApplication([])
clipboard = QApplication.clipboard()

def on_clipboard_change():
    data = clipboard.mimeData()
    if data.hasFormat('text/uri-list'):
        for path in data.urls():
            print path
    if data.hasText():
        print data.text()

clipboard.dataChanged.connect(on_clipboard_change)

app.exec_()
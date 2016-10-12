#coding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import requests
import re
import Queue


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.request_edit = QTextEdit()
        self.dir1_label = QLabel('dir1')
        self.dir2_label = QLabel('dir2')
        self.dir1_edit = QLineEdit()
        self.dir2_edit = QLineEdit()
        self.start_btn = QPushButton('Start Crack')
        grid = QGridLayout()
        grid.addWidget(self.request_edit, 1, 0, 10, 2)
        grid.addWidget(self.dir1_label, 11, 0)
        grid.addWidget(self.dir1_edit, 11, 1)
        grid.addWidget(self.dir2_label, 12, 0)
        grid.addWidget(self.dir2_edit, 12, 1)
        grid.addWidget(self.start_btn, 13, 0, 1, 2)
        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)
        self.resize(900, 400)
        self.method = ''
        self.headers = {}
        self.dir1_queue = Queue.Queue()
        self.dir2_queue = Queue.Queue()

    def bruter(self):
        pass


    def start(self):
        header = self.request_edit.toPlainText()
        for line in header:
            if line.count(':') != 0:
                tmp_list = line.rstrip.split(':')
                self.headers[tmp_list[0]] = tmp_list[1:]
            if line.count('=') != 0:
                pass
            if line.startswith('POST'):
                self.method = 'POST'
            elif line.startswith('GET'):
                self.method = 'GET'
        if self.dir1_edit.text() == '':
            pass
        else:
            dir1 = open(self.dir1_edit.text())
            for line in dir1.readlines():
                self.dir1_queue.put(line.rstrip())
            dir1.close()
            if self.dir2_edit.text() != '':
                dir2 = open(self.dir2_edit.text())
                for line in dir2.readlines():
                    self.dir2_queue.put(line.rstrip())
                dir1.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
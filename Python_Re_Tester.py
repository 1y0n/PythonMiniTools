#coding:utf-8

import re
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        self.reg_edit = QTextEdit()
        self.i_checkbox = QCheckBox('Re.I')
        self.m_checkbox = QCheckBox('Re.M')
        self.s_checkbox = QCheckBox('Re.S')
        self.string_edit = QTextEdit()
        self.result_edit = QTextEdit()
        self.ok_btn = QPushButton('OK')
        self.clear_btn = QPushButton('Clear All')
        self.highlighter = highlighter(self.string_edit)
        grid = QGridLayout()
        grid.addWidget(QLabel('Input your reg exp here:'), 0, 0, 1, 2)
        grid.addWidget(self.reg_edit, 1, 0, 3, 5)
        grid.addWidget(self.i_checkbox, 4, 0)
        grid.addWidget(self.m_checkbox, 4, 1)
        grid.addWidget(self.s_checkbox, 4, 2)
        grid.addWidget(self.ok_btn, 4, 3)
        grid.addWidget(self.clear_btn, 4, 4)
        grid.addWidget(QLabel('Paste your string here:'), 5, 0, 1, 2)
        grid.addWidget(QLabel('Result:'), 5, 3, 1, 2)
        grid.addWidget(self.string_edit, 6, 0, 1, 3)
        grid.addWidget(self.result_edit, 6, 3, 1, 2)
        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)
        self.resize(900, 600)
        self.setWindowTitle('Regex Tester for Python')
        self.statusBar().showMessage('Ready!')
        self.clear_btn.clicked.connect(lambda: self.clear_all())
        self.ok_btn.clicked.connect(lambda: self.reg())

    def reg(self):
        self.result_edit.setText('')
        rei = self.i_checkbox.isChecked()
        rem = self.m_checkbox.isChecked()
        res = self.s_checkbox.isChecked()
        string = unicode(self.reg_edit.toPlainText()).rstrip()
        if not (rei or rem or res):
            self.pattern = re.compile(string)
        elif (rei and (not rem) and (not res)):
            self.pattern = re.compile(string, re.I)
        elif (rei and rem and (not res)):
            self.pattern = re.compile(string, re.I|re.M)
        elif (rei and (not rem) and res):
            self.pattern = re.compile(string, re.I|re.S)
        elif (rei and rem and res):
            self.pattern = re.compile(string, re.I|re.M|re.S)
        elif ((not rei) and rem and (not res)):
            self.pattern = re.compile(string, re.M)
        elif ((not rei) and rem and res):
            self.pattern = re.compile(string, re.M|re.S)
        elif ((not rei) and (not rem) and res):
            self.pattern = re.compile(string, re.S)

        self.result_list = re.findall(self.pattern, unicode(self.string_edit.toPlainText()))
        for result in self.result_list:
            self.result_edit.setText(unicode(self.result_edit.toPlainText()) + result + '\n')
        self.statusBar().showMessage('Complete!  ' + unicode(len(self.result_list)) + '  result(s) found!')
        self.highlighter.setHighlightData(self.result_list)
        self.highlighter.rehighlight()

    def clear_all(self):
        self.reg_edit.setText('')
        self.string_edit.setText('')
        self.result_edit.setText('')
        self.statusBar().showMessage('Clear complete!')


class highlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        self.highlightdata = []
        self.matched_format = QTextCharFormat()
        brush = QBrush(Qt.green, Qt.SolidPattern)
        self.matched_format.setBackground(brush)

    def highlightBlock(self, text):
        index = 0
        length = 0
        for item in self.highlightdata:
            if item.count('\n') != 0:
                itemList = item.split('\n')
                for part in itemList:
                    index = text.indexOf(part, index + length)
                    if index == -1:
                        index = 0
                    else:
                        length = len(part)
                        self.setFormat(index, length, self.matched_format)
            else:
                index = text.indexOf(item, index + length)
                length = len(item)
                self.setFormat(index, length, self.matched_format)

    def setHighlightData(self, highlightdata):
        self.highlightdata = highlightdata

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
# -*- coding: iso-8859-15 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
import os

#imagePath = "/home/Josep/programacio/progs/rahisi/images/add.png"
ficheros=os.listdir("/usr/share/icons/default.kde/48x48/apps/")

class ImgWidget1(QtGui.QLabel):

    def __init__(self, imagen, parent=None):
        super(ImgWidget1, self).__init__(parent)
        pic = QtGui.QPixmap(imagen)
        self.setPixmap(pic)

class ImgWidget2(QtGui.QWidget):

    def __init__(self, parent=None):
        super(ImgWidget2, self).__init__(parent)
        self.pic = QtGui.QPixmap(imagePath)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.pic)


class Widget(QtGui.QWidget):

    def __init__(self):
        super(Widget, self).__init__()
        num=len(ficheros)
        tableWidget = QtGui.QTableWidget(40, 10, self)
        for x in range(num):
            tableWidget.setCellWidget(x, 1, ImgWidget1(self,ficheros[x]))

if __name__ == "__main__":
    app = QtGui.QApplication([])

    wnd = Widget()
    wnd.setGeometry(5,30,1020,700)
    wnd.show()
    sys.exit(app.exec_())

#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Function to warn if you have desconnected a USB Device Incorrectly
#

from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from PyQt4 import uic

from ui_usbtray_warn import Ui_Form_Usbtray_Warn as Ui_Form

class usbtray_warning(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        global tipus
        #uic.loadUi("ui/action.ui", self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

#usbtray_warn = usbtray_warn()
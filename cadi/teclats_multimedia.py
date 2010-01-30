#!/usr/bin/python
#-*- coding: iso-8859-15 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from commands import getoutput
from os import path, system

#import funcions_k

from ui_teclats_multimedia import Ui_FormTeclatsMultimedia as Ui_Form

class panelTeclatsMultimedia(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        global tipus
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.a=QProcess()
        self.a.start("keytouch")

#####  SIGNAL & SLOTS  #####
        self.connect(self.ui.b_sortir, SIGNAL("clicked()"), self.boto_sortir)
        #self.connect(self.ui.b_SaX, SIGNAL("clicked()"), self.SaveAndExit)
        self.connect(self.ui.b_keyboard, SIGNAL("clicked()"), self.boto_keyboard)


#### END SIGNAL & SLOTS ####

    def boto_sortir(self):
        self.close()

    def boto_keyboard(self):
        self.a=QProcess()
        self.a.start("keytouch")

    #def SaveAndExit(self):
        #self.close()


#app = QApplication(sys.argv)
#preferencies = preferencies()
#preferencies.show()
#app.exec_()
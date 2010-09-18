#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from commands import getoutput
from os import path, system

#import funcions_k

from ui_bluetooth import Ui_FormBluetooth as Ui_Form

class panelBluetooth(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        global tipus
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.b_SaX.setEnabled(False)

#####  SIGNAL & SLOTS  #####
        self.connect(self.ui.b_sortir, SIGNAL("clicked()"), self.boto_sortir)
        self.connect(self.ui.b_SaX, SIGNAL("clicked()"), self.SaveAndExit)
        self.connect(self.ui.le_pin, SIGNAL("textEdited (const QString&)"), self.enableSaX)

#### END SIGNAL & SLOTS ####

        self.pin=""
        f=open('/etc/bluetooth/hcid.conf','r')
        self.linea=f.readlines()
        f.close()
        for i in self.linea:
            if i.find("passkey")>0:
                self.pin=i.split('"')[1]
                break
        self.ui.le_pin.setText(self.pin)


    def enableSaX(self):
        self.ui.b_SaX.setEnabled(True)
        
    def boto_sortir(self):
        self.close()

    def SaveAndExit(self):
        f=open('/etc/bluetooth/hcid.conf','r')
        linea=f.readlines()
        f.close()
	
        f=open('/etc/bluetooth/hcid.conf','w')

        for i in linea:
            if i.find("passkey")>0:
                f.write('    passkey "'+self.ui.le_pin.text()+'"; \n')
            else:
                f.write(i)
        f.close()
        self.close()


#app = QApplication(sys.argv)
#preferencies = preferencies()
#preferencies.show()
#app.exec_()
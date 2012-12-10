#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
#import unicodedata
#from subprocess import getoutput
#from os import path

#import funcions_k
#from threadCopyfiles import *

import common
import nano

import dbus, dbus.glib


class instalador(nano.instalador, common.instalador, QMainWindow):
  def __init__(self):
    QMainWindow.__init__(self)
    self.ui = uic.loadUi("instalador.ui", self)
    #self.ui = Ui_Form()
    #self.ui.setupUi(self)
    self.defineCommons()
    self.prepareGui()
    self.setIconVars()
    self.setConnections()
    
    self.prepareNanoPath()
     # Should print 'foo'
     
app = QApplication(sys.argv)
instalador = instalador()
instalador.show()
	#global args
	#args=sys.argv
	#print args
app.exec_()

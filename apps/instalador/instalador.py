#!/usr/bin/python
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
import mainPage
import nanoPage

import dbus, dbus.glib


class instalador(mainPage.instalador, nanoPage.instalador, common.instalador, QMainWindow):
  def __init__(self):
    QMainWindow.__init__(self)
    self.ui = uic.loadUi("instalador.ui", self)
    #self.ui = Ui_Form()
    #self.ui.setupUi(self)
    self.defineCommons()
    self.prepareMainPage()
    self.setIconVars()
    self.setConnections()
    
    self.prepareNanoPath()
     
app = QApplication(sys.argv)

locale = QLocale.system().name()   #ca_ES
qtTranslator = QTranslator()
if qtTranslator.load("/usr/share/kademar/utils/instalador/tr/"+locale.split("_")[0]+".qm"):
    app.installTranslator(qtTranslator)
    #print "Loaded "+locale
elif qtTranslator.load("/usr/share/kademar/utils/instalador/tr/en.qm"):
    app.installTranslator(qtTranslator)
    #print "Loaded "+locale

qtTranslatorQT = QTranslator()
qtTranslatorQT.load("qt_"+locale, "/usr/share/qt4/translations")
app.installTranslator(qtTranslatorQT)

instalador = instalador()
instalador.show()
	#global args
	#args=sys.argv
	#print args
app.exec_()

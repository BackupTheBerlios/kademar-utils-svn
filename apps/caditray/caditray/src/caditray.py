#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from caditray.caditray import cadiTray

#from pacupdate.tray import PacupdateTrayIcon
#from pacupdate.confpacupdate import ConfPacupdate
#from pacupdate.updatechecker import UpdateChecker
#from gtk import main
#from gobject import timeout_add

#def call_updates(data=None):
    #'''
    #Call the update method
    #'''
    
    #pacupdate.on_updates(PacupdateTrayIcon)
    #return True

## Create a instance of PacupdateTrayIcon
#pacupdate = PacupdateTrayIcon()

## Create the trayicon
#pacupdate.create_tray()

## Get the time of interval
#update_time = int(ConfPacupdate().readConf().get('global', 'update_interval')) * 60000

## Run updates periodically
#call = timeout_add(int(update_time), call_updates, pacupdate)

#try:
    #main()
#except KeyboardInterrupt:
    #pass




app = QApplication(sys.argv)
locale = QLocale.system().name()
qtTranslator = QTranslator()
data="/usr/share/caditray/tr/"
if qtTranslator.load(data+locale+".qm"):
    app.installTranslator(qtTranslator)
    print ("Loaded "+locale)
    
elif qtTranslator.load(data+locale.split("_")[0]+".qm"):
    app.installTranslator(qtTranslator)
    print ("Loaded "+locale.split("_")[0])
    
elif qtTranslator.load(data+"en.qm"):
    app.installTranslator(qtTranslator)
    print ("Loaded en.qm")

widget = cadiTray( app)

#settings=QSettings("Kademar","cadiTray")

#if str(settings.value("startOnTray")).lower() != "true":
    #widget.show()
    #print("show")

#else:
    #print("not show")
#print(settings.value("startOnTray"))

app.exec_()


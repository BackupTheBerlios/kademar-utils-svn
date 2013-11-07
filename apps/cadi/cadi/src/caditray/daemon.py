#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow
import dbus.mainloop.qt
from time import sleep
class cadiTray(QMainWindow):

#############
### CONNECTION WITH CADI DAEMON
#############
    def initDaemon(self):
        try:
            #dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
            self.session_bus = dbus.SystemBus()
            self.objDaemon =  self.session_bus.get_object("org.freedesktop.CADI","/Daemon")
            self.interfaceDaemon = dbus.Interface(self.objDaemon, "org.freedesktop.CADI")

        except Exception:
            print(self.tr("Seems daemon isn't running. Let's execute"))
            self.daemon=QProcess()
            self.daemon.start("pkexec /usr/lib/cadi/cadidaemon")
            #self.daemon.waitForFinished()

            
            
    def connectToDaemon(self):
        connection=False
        for i in [ 1,2,3,4,5,6,7,8,9,10]:
            try:
                self.session_bus = dbus.SystemBus()
                self.objDaemon =  self.session_bus.get_object("org.freedesktop.CADI","/Daemon")
                self.interfaceDaemon = dbus.Interface(self.objDaemon, "org.freedesktop.CADI")
                print("Daemon is running")
                connection=True
                break
                

            except Exception:
                connection=False
            print ("Retrying connection in 1 second")
            sleep(1)

        if not connection:
            print ("Fatal daemon error: Daemon is not running")
            self.deleteLater()
            
#############
### END CONNECTION WITH CADI DAEMON
#############

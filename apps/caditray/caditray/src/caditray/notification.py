#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow
import dbus.mainloop.qt

class cadiTray(QMainWindow):

#############
### NOTIFYCATION PART
#############
    def initNotify(self):
        try:
            dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
            self.session_bus = dbus.SessionBus()
            self.obj =  self.session_bus.get_object("org.freedesktop.Notifications","/org/freedesktop/Notifications")
            self.interface = dbus.Interface(self.obj, "org.freedesktop.Notifications")
            self.notifySystem=True

        except Exception:
            self.interface = None
            self.notifySystem=False
            print(self.tr("unable to create DBUS connecton to notify"))
        #print("hola")
#############
### END NOTIFYCATION PART
#############

    def sendNotify(self, title, body):
        if self.notifySystem:
            self.app_name="CADI Tray"
            #self.summary="Starting Server"
            #self.body="sdf"
            self.app_icon=self.imagepath+"caditray.png"
            self.expire_timeout=5000
            self.actions = [] #["update", "\nUpdate\n"]
            self.hints = {}
            self.interface.Notify(self.app_name, 0, self.app_icon, title, body, self.actions, self.hints, self.expire_timeout)
 
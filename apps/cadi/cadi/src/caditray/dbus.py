#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow
from os import path
#import dbus
#import dbus.service
#import dbus.mainloop.glib

class cadiTray(QMainWindow):

    def initDbus(self):
        #http://qt-project.org/wiki/PySide_DBus_Integration

        pass
        #self.connect(self.dbus, SIGNAL('hola'), self.holas)
        #self.connect(self.action_exit, SIGNAL("triggered()"), self.askForExit)
        #dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        #self.session_bus = dbus.SessionBus()

        #self.name = dbus.service.BusName("org.freedesktop.CADI", self.session_bus)
        #self.widget = DBusWidget(self.session_bus, '/CadiTray')
        
    def holas(self):
        print("ye")
#class DBusWidget(dbus.service.Object):
    #def __init__(self, name, session):
        ## export this object to dbus
        #dbus.service.Object.__init__(self, name, session)

    #@dbus.service.method("org.freedesktop.CADI", signature='')
    #def hello(self):
        ##Gtk.main_quit()   # Terminate after running. Daemons don't use this.
        #return "Hello,World!"  

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from caditray.caditray import cadiTray
import dbus
import dbus.service
import dbus.mainloop.glib


#class DBusWidget(dbus.service.Object):
    #def __init__(self, name, session):
        ## export this object to dbus
        #dbus.service.Object.__init__(self, name, session)

    #@dbus.service.method("org.freedesktop.CADI", signature='')
    #def hello(self):
        #return "Hello,World!"

        ##app.connect(app, QtCore.SIGNAL('messageAvailable'), window.handleMessage)


#not start if KDE session autoload
if len(sys.argv) > 1:
    if sys.argv[1] == "-session":
        print ("Not starting, it's a KDE session autoload")
        sys.exit()


app = QApplication(sys.argv)
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
session_bus = dbus.SessionBus()



try:
    #Try to connect. Find other CadiTray instance
    objDaemon =  session_bus.get_object("org.freedesktop.CADI","/CadiTray")
    interfaceDaemon = dbus.Interface(objDaemon, "org.freedesktop.CADI")
    print ("CadiTray Already Executing")

except Exception:
    #Single instance
    
    # Export the service
    name = dbus.service.BusName("org.freedesktop.CADI", session_bus)
   
    #Allow external connections
    #widget = DBusWidget(session_bus, '/CadiTray')
    
    
    window = cadiTray(app)
    sys.exit(app.exec_())
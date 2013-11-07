#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow

class cadiTray(QMainWindow):

    def initTray(self):
#############
####  TRAY MODULE & ACTIONS
#############
        #### TRAY ####
        self.tray = QSystemTrayIcon(self)
        self.trayMenu = QMenu()
     # Menu items
        self.action_exit = QAction(QIcon(self.imagepath+"exit.png"), self.tr('Exit CADI Tray  '+self.kademarType), self)

     # Append items to menu
        #self.trayMenu.addAction(self.action_browseFile)
        #self.trayMenu.addSeparator()
        #self.trayMenu.addMenu(self.appsMenu)
        #self.trayMenu.addSeparator()
        self.trayMenu.addAction(self.action_exit)

     # Tray icon definitions
        self.trayIcon = QIcon(self.imagepath+"caditray.png")
        self.tray.setContextMenu(self.trayMenu)
        self.tray.setIcon(self.trayIcon)
        self.tray.setToolTip("CADI Tray "+self.kademarType)
        self.tray.show()
#############
####  END  TRAY MODULE & ACTIONS
#############

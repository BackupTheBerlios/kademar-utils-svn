#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow

class cadiTray(QMainWindow):

    def initConnects(self):
        ###Connectar Accions al fer click a un del menu, la function que executa
        #self.connect(self.action_start, SIGNAL("triggered()"), self.startServer)
        #self.connect(self.actionStart_Server, SIGNAL("triggered()"), self.startServer)
        
        #self.connect(self.action_stop, SIGNAL("triggered()"), self.stopServer)
        #self.connect(self.actionStop_Server, SIGNAL("triggered()"), self.stopServer)
     
        #self.connect(self.action_restart, SIGNAL("triggered()"), self.restartServer)
        #self.connect(self.actionRestart_Server, SIGNAL("triggered()"), self.restartServer)
        
        #self.connect(self.action_manage, SIGNAL("triggered()"), self.openStackManager)
        #self.connect(self.actionManage_Stacks, SIGNAL("triggered()"), self.openStackManager)
        
        #self.connect(self.action_exit, SIGNAL("triggered()"), self.askForExit)
        #self.connect(self.actionExit, SIGNAL("triggered()"), self.askForExit)

        #self.connect(self.action_browse, SIGNAL("triggered()"), self.openBrowser)
        #self.connect(self.actionOpen_Browser, SIGNAL("triggered()"), self.openBrowser)
        
        #self.connect(self.actionOpen_Cache_Stack, SIGNAL("triggered()"), self.openCacheStack)

        #self.connect(self.actionOpen_File_Manger, SIGNAL("triggered()"), self.openFileManager)
        #self.connect(self.action_browseFile, SIGNAL("triggered()"), self.openFileManager)

        #Quan fas clic al tray executa eventsdeltray (function)
        self.tray.connect( self.tray, SIGNAL( "activated(QSystemTrayIcon::ActivationReason)" ), self.eventsdeltray )
        
        #self.sendNotify(self.tr("Bitnami Control Updated"),self.tr("It has been updated, you should reboot the Kademar Bitnami Control Panel to get the new features."))
        self.connect(self.action_exit, SIGNAL("triggered()"), self.askForExit)

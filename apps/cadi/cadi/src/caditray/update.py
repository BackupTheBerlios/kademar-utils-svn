#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow


#
#  VARIABLES
# 
#     self.upgradeType
#       VALUES 
#        0=auto install
#        1=download and warn
#        2=only warn
#        3=no update

#     self.update3G
#       VALUES
#        True = Update when in a 3G Connection
#        False = NO Update when in a 3G Connection

class cadiTray(QMainWindow):
    def initUpdate(self):
        self.updatingSystem=False
        self.timer=QTimer()
        self.fistTimer=QTimer()
        self.prepareUpdateTimer()
            
    def prepareUpdateTimer(self):
        #print ("updatetype",self.upgradeType)
        #print ("update3G",        self.upgrade3G)
        if not self.upgradeType == 3:
            self.timerCheckUpdates(3600)  #3600 = one hour
        else:
            self.timer.stop()
            self.fistTimer.stop()
            print("Not setting update timer. Set on config")
        
    #Check updates fist time if it's 5 minutes opened computer
    def firstCheckUpdates(self):
        if not self.upgradeType == 3:
            self.fistTimer.singleShot(300 *1000, self.checkUpdates)
        else:
            print("Not updating. Set on config")
        
    def timerCheckUpdates(self, milliseconds):
        self.timer.setInterval(milliseconds*1000)
        self.timer.start()
        #self.timer.timeout,self.connect(self.hello)
        #connect(self.timer, SIGNAL(timeout()), this, SLOT(update()))
        self.connect(self.timer, SIGNAL("timeout()"), self.checkUpdates)

        
    def checkUpdates(self, force=False):
        #Update If isn't on liveCD   or we force it
        if not self.isLiveCd() or force == True:
            #If we aren't updating system already
            if not self.updatingSystem:
               #And if we have internet
               if self.checkInternetConnection():
                   #Really do system update
                   self.interfaceDaemon.updateDBPackages() #Update pacman DB
                   packagesToUpdate=self.interfaceDaemon.queryPackagesToUpdate() #Check if there are some packages to update
                   #Continue if there are more than 0 == nothing
                   if packagesToUpdate != "0":
                       #If we aren't on  Warn-only mode, or we are forcing (user pressed the update button),  real update
                       if self.upgradeType != 2 or force == True:
                           #Notify about how many packages to update there are
                           self.sendNotify("CADI", packagesToUpdate+" "+self.tr('packages available to update'))
                           self.updatingSystem=True
                           #If in Download Only mode, say it to daemon
                           if self.upgradeType == 1:
                               self.interfaceDaemon.updateSystemPackages("download-only")
                           else:
                               #Real update system
                               print("Updating System")
                               result=self.interfaceDaemon.updateSystemPackages()
                               self.updatingSystem=False
                               #If after update, there isn't more packages to update, means all OK
                               if self.interfaceDaemon.queryPackagesToUpdate() == "0":
                                   #Say that system is successfully updated.
                                   print("System Updated")
                                   self.sendNotify("CADI", packagesToUpdate+" "+self.tr('Packages where updated successfully!'), "ok")
                       else:
                           #If we are on Warn-only mode, arrived here by automatic update, warn only :)
                           self.sendNotify("CADI", packagesToUpdate+" "+self.tr('packages available to update\nClick here to update now'), "info")
                             
                    elif force==True:
                        #if there's no packages to update, and we arribe here automatically don't say nothing:
                        # if user pressed the button fo update, say that is already updated
                        self.sendNotify("CADI", self.tr('System already updated!'), "ok")
               else:
                   #don't do nothing if isn't internet
                   print("No internet Connection")
                   if force==True:
                       #if he pressed the update button, say it that we cannot do nothing
                       self.sendNotify("CADI", self.tr('No internet Connection'), "error")
            else:
                #Don't do nothing if already updating
                print("Already Updating System")
        else:
            #Don't do nothing if we are on livecd. Could be a disaster.
            print("Not updating. Is in LiveCD")
            
        

    def checkUpdatesNowFunction(self):
        if not self.isLiveCd():
            self.checkUpdates(force=True)
        else:
            preg = self.showWarningMessage("infopreg", self.tr('Update System'), self.tr("You are on LiveCD session. Isn't recommended to update.\nDo you want to update anyway?"))
            if preg == QMessageBox.Yes:
                #self.stopServer()
                self.checkUpdates(force=True)
 
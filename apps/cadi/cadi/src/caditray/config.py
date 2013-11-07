#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *

class cadiTray(QMainWindow):
    def prepareConfig(self):
        self.settings=QSettings("Kademar", "CADI")


    def loadConfig(self):
        self.upgradeType = int(self.settings.value("Upgrade/upgradeType", 0))
        self.upgrade3G=bool(self.settings.value("Upgrade/upgrade3G", 0))
        self.ui.CBUpgrade.setCurrentIndex(self.upgradeType)
        self.ui.CHUpgrade3G.setChecked(self.upgrade3G)


    def saveConfig(self):
        self.settings.setValue("Upgrade/upgradeType", self.ui.CBUpgrade.currentIndex())
        self.settings.setValue("Upgrade/upgrade3G", self.ui.CHUpgrade3G.isChecked())
        self.loadConfig() #read again all


        #Prepare system update with actual configuration
        self.prepareUpdateTimer()
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow

class instalador(QMainWindow):

      #Inst. rapida: PMain -> PInfo -> PQuickInstall -> PInstalling -> PEnd
      #Inst. Avanç: PMain -> PInfo -> PTime -> PDisk -> PUsers -> PSystem ->
      #PNet -> PSoft -> PInstalling -> PEnd
      #Inst. Nano: PMain -> PNano -> PInstalling -> PEnd
      
    def prepareMainPage(self):
        self.ui.BBack.setVisible(False)
        self.ui.BNext.setVisible(False)
        self.ui.scrollArea_2.setVisible(False)
        self.ui.stackedPages.setCurrentWidget(self.ui.PMain) #go to fist main page
        #Show buttons of available installation paths
        self.showYourPaths()


    def showYourPaths(self):
            
       #Function to show your available installation paths

        #Define Main page buttons
        self.ui.BQuickInstall.setVisible(False)
        self.ui.LQuickInstall.setVisible(False)
        self.ui.BAdvancedInstall.setVisible(False)
        self.ui.LAdvancedInstall.setVisible(False)
        self.ui.BRemoteInstall.setVisible(False)
        self.ui.LRemoteInstall.setVisible(False)
        
        #Detect Removable Devices
        self.removableDevicesDetected=self.listBlockDevices(removable=True)
        #print(self.removableDevicesDetected)
        
        #Enable/Disable nano path
        if len(self.removableDevicesDetected) == 0:
            self.ui.BNanoInstall.setEnabled(False)
            self.ui.LNanoInstall.setEnabled(False)
        else:
            self.ui.BNanoInstall.setEnabled(True)
            self.ui.LNanoInstall.setEnabled(True)
        
        
        self.staticDevicesDetected=self.listBlockDevices(removable=False)
        #print(self.staticDevicesDetected)
        if len(self.staticDevicesDetected) == 0:
            self.ui.BAdvancedInstall.setEnabled(False)
            self.ui.LAdvancedInstall.setEnabled(False)
        else:
            self.ui.BAdvancedInstall.setEnabled(True)
            self.ui.LAdvancedInstall.setEnabled(True)
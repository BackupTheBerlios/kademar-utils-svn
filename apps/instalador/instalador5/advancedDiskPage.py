#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow


class instalador(QMainWindow):

    def prepareAdvancedPath(self):
        #prepare combobox devices
        self.modelRoot = QStandardItemModel()
        self.viewRoot = QTreeView()
        self.viewRoot.setModel(self.modelRoot)
        self.viewRoot.setIconSize(QSize(40,30))
        self.ui.CBPartRoot.setView(self.viewRoot)
        self.ui.CBPartRoot.setModel(self.modelRoot)
        self.itemListRoot=[]
        
        self.modelSwap = QStandardItemModel()
        self.viewSwap = QTreeView()
        self.viewSwap.setModel(self.modelSwap)
        self.viewSwap.setIconSize(QSize(40,30))
        self.ui.CBPartSwap.setView(self.viewSwap)
        self.ui.CBPartSwap.setModel(self.modelSwap)
        self.itemListSwap=[]

        self.modelOther = QStandardItemModel()
        self.viewOther = QTreeView()
        self.viewOther.setModel(self.modelOther)
        self.viewOther.setIconSize(QSize(40,30))
        self.ui.CBPartOther.setView(self.viewOther)
        self.ui.CBPartOther.setModel(self.modelOther)
        self.itemListOther=[]
        
        self.prepareAdvancedDiskConnections()

        #Hide from kademar Installer 
        for i in [self.ui.LTime, self.ui.LUsers, self.ui.LSystem, self.ui.LNetwork, self.ui.LSoftware, self.ui.LSystemInfo]:
            i.setVisible(True)

        for i in [self.ui.iTime, self.ui.iUsers, self.ui.iSystem, self.ui.iNetwork, self.ui.iSoftware, self.ui.iSystemInfo]:
            i.setVisible(True)

        #hide from installation process
        for i in [self.ui.LRoot, self.ui.LCreatingUsers, self.ui.LNetConfig, self.ui.LInstallingProgress, self.ui.LFinishedProgress]:
            i.setVisible(True)

        for i in [self.ui.iRoot, self.ui.iCreatingUsers, self.ui.iNetConfig, self.ui.iInstallingProgress, self.ui.iFinishedProgress]:
            i.setVisible(True)
            
        #Show from all
        for i in [self.ui.iPersistentChangesFile]:
            i.setVisible(False)
            
        for i in [self.ui.LPersistentChangesFile]:
            i.setVisible(False)
      
        self.ui.CHSamePart.setChecked(True)
        
        #while we don't have auto-partitioner
        for i in [self.ui.RBPartitionN, self.ui.RBPartitionA, self.ui.RBPartitionY]:
            i.setVisible(False)
        self.choosedPath=[self.ui.PMain, self.ui.PDisk]
        
        self.fillListOfDevicesOnCombobox()
        self.ui.BBack.setVisible(True)
        self.ui.BNext.setVisible(True)
        self.ui.scrollArea_2.setVisible(True)
        self.nextButton() #go to first nano page


    def prepareAdvancedDiskConnections(self):
        self.connect(self.ui.CHSamePart, SIGNAL("stateChanged(int)"), self.installationWithinSamePartitionCheckboxChanged)
        self.connect(self.ui.BGparted, SIGNAL("clicked()"), self.openGparted)
        self.connect(self.ui.CBPartSwap, SIGNAL("currentIndexChanged(int)"), self.checkPartitionsAdvancedInstaller)
        self.connect(self.ui.CBPartRoot, SIGNAL("currentIndexChanged(int)"), self.checkPartitionsAdvancedInstaller)
        self.connect(self.ui.CBPartOther, SIGNAL("currentIndexChanged(int)"), self.checkPartitionsAdvancedInstaller)

        
    def checkPartitionsAdvancedInstaller(self):
        if self.ui.CHSamePart.isChecked():
            if self.ui.CBPartSwap.currentIndex() == self.ui.CBPartRoot.currentIndex():
                print("hola")

    def installationWithinSamePartitionCheckboxChanged(self, state):
        for i in [self.ui.LPartOther, self.ui.CBPartDir,self.ui.CBPartOther,self.ui.CBDiskFormatOther,self.ui.LVMountPointList,self.ui.BAddPartition,self.ui.BRemovePartition]:
            i.setVisible(not(state))

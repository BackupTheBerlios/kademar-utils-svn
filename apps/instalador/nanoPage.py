#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow
from random import randint 
class instalador(QMainWindow):

      #Inst. rapida: PMain . PInfo . PQuickInstall . PInstalling . PEnd
      #Inst. Avanç: PMain . PInfo . PTime . PDisk . PUsers . PSystem .
      #PNet . PSoft . PInstalling . PEnd
      #Inst. Nano: PMain . PNano . PInstalling . PEnd
      
    def prepareNanoPath(self):    
        #Hide from kademar Installer 
        for i in [self.ui.LTime, self.ui.LUsers, self.ui.LSystem, self.ui.LNetwork, self.ui.LSoftware]:
            i.setVisible(False)
        
        for i in [self.ui.iTime, self.ui.iUsers, self.ui.iSystem, self.ui.iNetwork, self.ui.iSoftware]:
            i.setVisible(False)
            
        #hide from installation process
        for i in [self.ui.LPartitioning, self.ui.LRoot, self.ui.LCreatingUsers, self.ui.LNetConfig]:
            i.setVisible(False)
            
        for i in [self.ui.iPartitioning, self.ui.iRoot, self.ui.iCreatingUsers, self.ui.iNetConfig]:
            i.setVisible(False)
        
        
        
        #labelList=[self.ui.LBoot,self.ui.LCopy,self.ui.LCreatingUsers,self.ui.LDisk,self.ui.LFinishedProgress,self.ui.LInstallingProgress,self.ui.LNetConfig,self.ui.LNetwork,self.ui.LPartitioning,self.ui.LProcess,self.ui.LRoot,self.ui.LSoftware,self.ui.LSystem,self.ui.LSystemInfo,self.ui.LTime,self.ui.LUsers]
        #for i in labelList:
            #i.setVisible(False)
        #stateList=[self.ui.FBoot,self.ui.FCopy,self.ui.FCreatingUsers,self.ui.FDisk,self.ui.FFinished,self.ui.FFinished,self.ui.FInstalling,self.ui.FNetConfig,self.ui.FNetwork,self.ui.FPartitioning,self.ui.FRoot,self.ui.FSoft,self.ui.FSystem,self.ui.FSystemInfo,self.ui.FTime,self.ui.FUsers]
        #for i in stateList:
            #i.setVisible(False)
            
        self.choosedPath=[self.ui.PMain, self.ui.PNano, self.ui.PInstalling, self.ui.PEnd]
        self.ui.CHChangesFile.setChecked(False)
        self.permanentChangesFileCheckboxChanged()
        self.ui.BBack.setVisible(True)
        self.ui.BNext.setVisible(True)
        self.ui.scrollArea_2.setVisible(True)
        #self.ui.prepareNanoPath.setChecked(False)
        #self.ui.CHChangesFile.setChecked(False)
        self.prepareNanoConnections()


        self.completeListDevices=[]
        self.itemList=[]
        self.model = QStandardItemModel()
        self.view = QTreeView()
        #self.model.setHeaderData(0, Qt.Horizontal, "Unit");
        #self.model.setHeaderData(1, Qt.Horizontal, "Size");
        #self.model.setHeaderData(2, Qt.Horizontal, "Information");
        #self.model.setHeaderData(3, Qt.Horizontal, "Fs");
        
        self.view.setModel(self.model)
        parent = self.model.invisibleRootItem()
        self.view.setIconSize(QSize(40,30))
	
	##Empty Partition&Device ComboBox 
       #self.ui.CBNanoDevice.clear()
        #Fill the Removable devices list
        #print(self.removableDevicesDetected)
        for i in range(len(self.removableDevicesDetected)):
            #print(self.removableDevicesDetected[i])
            hdd=self.removableDevicesDetected[i][0]
            hddsize=float(self.removableDevicesDetected[i][1])  # 20450
            hddsize1=str(hddsize).split(".")[0]
            hddsize2=str(hddsize).split(".")[1]
            model=self.removableDevicesDetected[i][2]
            vendor=self.removableDevicesDetected[i][3]

            if len(str(hddsize).split(".")[0])<=3:
                #print(str(hddsize).split(".")[0][:-3])#hddsize=int(self.removableDevicesDetected[i].split("-")[1])  #J
                #hddsize1
                hddsize=hddsize1+","+hddsize2[:2]
                unitat="Mb"
            else:
                #hddsize=str(hddsize)[:-3]+","+str(hddsize)[-3]
                hddsize1process=str(hddsize1)[:-3]
                hddsize=hddsize1process+","+hddsize1[-3:-1]
                unitat="Gb"
            #self.ui.CBNanoDevice.addItem(QIcon(self.icon_device_pendrive),hdd+" "+hddsize+" "+unitat+" "+model+" "+vendor)
            self.completeListDevices.append([hdd,hddsize,unitat,model,vendor])
            self.itemList.append(QStandardItem(QIcon(self.icon_device_pendrive), self.tr("Disk")+" "+hdd))
            self.itemList.append(QStandardItem(hddsize+" "+unitat))
            self.itemList.append(QStandardItem(str(model+" "+vendor)))
            self.itemList.append(QStandardItem(" "))
            self.itemList[len(self.itemList)-4].setSelectable(False)
            self.itemList[len(self.itemList)-3].setSelectable(False)
            self.itemList[len(self.itemList)-2].setSelectable(False)
            self.itemList[len(self.itemList)-1].setSelectable(False)

            parent.appendRow([
                self.itemList[len(self.itemList)-4],
                self.itemList[len(self.itemList)-3],
                self.itemList[len(self.itemList)-2],
                self.itemList[len(self.itemList)-1],
                #it3,
                ])


            actualparent=self.itemList[len(self.itemList)-4]
            parts=self.listPartitionsOfDevice(hdd)
            for i in range(len(parts)):
                #print(self.removableDevicesDetected[i])
                part=parts[i][0]
                partsize=float(parts[i][1])  # 20450
                partsize1=str(partsize).split(".")[0]
                partsize2=str(partsize).split(".")[1]
                fs=parts[i][2]
                label=parts[i][3]
                #swaptype=parts[i][4]

                if len(str(partsize).split(".")[0])<=3:
                    #print(str(hddsize).split(".")[0][:-3])#hddsize=int(self.parts[i].split("-")[1])  #J
                    #hddsize1
                    partsize=partsize1+","+partsize2[:2]
                    unitat="Mb"
                else:
                    #hddsize=str(hddsize)[:-3]+","+str(hddsize)[-3]
                    partsize1process=str(partsize1)[:-3]
                    partsize=partsize1process+","+partsize1[-3:-1]
                    unitat="Gb"

                self.completeListDevices.append([part,partsize,unitat,fs,label])
                self.itemList.append(QStandardItem(QIcon(self.icon_partition),  self.tr("Partition")+"  "+part))
                self.itemList.append(QStandardItem(partsize+" "+unitat))
                self.itemList.append(QStandardItem(str(label)))
                self.itemList.append(QStandardItem(str(fs)))
                

                actualparent.appendRow([
                    self.itemList[len(self.itemList)-4],
                    self.itemList[len(self.itemList)-3],
                    self.itemList[len(self.itemList)-2],
                    self.itemList[len(self.itemList)-1],
                    #it3,
                    ])
            #self.ui.CBNanoDevice.addItem(QIcon(self.icon_partition),part+" "+partsize+" "+fs+" "+unitat+" "+label)
                #print(hd)
                
        self.view.adjustSize()
        self.view.setAutoExpandDelay(0)
        self.view.header().hide()
        #self.model.child(1).appendRow([
                #QStandardItem("besa"),
                #QStandardItem("hola"),
                #QStandardItem(),
                #])
                
        self.ui.CBNanoDevice.setView(self.view)
        self.ui.CBNanoDevice.setModel(self.model)
        self.ui.CBNanoDevice.setCurrentIndex(-1)
        self.ui.CHChangesFile.setEnabled(False)
        self.ui.CHFormatNano.setEnabled(False)

        self.view.expandAll()
        combo = QComboBox()
        self.view.setIndexWidget(self.model.indexFromItem(parent), combo )
        self.view.resizeColumnToContents(0)
        self.view.resizeColumnToContents(1)
        self.view.resizeColumnToContents(2)
        self.view.resizeColumnToContents(3)
        self.nextButton() #go to first nano page

        
    def prepareNanoConnections(self):
        self.connect(self.ui.BGpartedNano, SIGNAL("clicked()"), self.openGparted)
        self.connect(self.ui.SChangeFile, SIGNAL("valueChanged(int)"), self.permanentChangesFileSliderValueChanged)
        self.connect(self.ui.CHChangesFile, SIGNAL("stateChanged(int)"), self.permanentChangesFileCheckboxChanged)
        self.connect(self.ui.CBNanoDevice, SIGNAL("currentIndexChanged(int)"), self.activateOptionsBeforeDeviceIsSelected)
        
    def processNanoPageBeforeNext(self):
        if self.workingList == []:
            self.showWarningMessage("critical", self.tr("Error: No partition selected"), self.tr("You should select a a partition to install"))
            return False
            
        if self.ui.CHFormatNano.isChecked() == True:
            reply = self.showWarningMessage("infopreg", self.tr("Begin of installation process"), self.tr("Will be erased ALL data of the selected partition!!!\n\nFor more security, it's recommended to have a backup of data of your drive."))
            if reply != QMessageBox.Yes:
                return False
        
        return True

    def permanentChangesFileSliderValueChanged(self, int):
        self.ui.LChangeFilePercent.setText(str(int)+"%")
        
    def permanentChangesFileCheckboxChanged(self):
        state=self.ui.CHChangesFile.isChecked()
        self.ui.LChangeFilePercent.setVisible(state)
        self.ui.SChangeFile.setVisible(state)
        self.ui.LChangesFileSize.setVisible(state)
        self.ui.FChangesFileInfo.setVisible(state)

    def activateOptionsBeforeDeviceIsSelected(self,int):
        if int!=-1:
            self.ui.CHChangesFile.setEnabled(True)
            self.ui.CHFormatNano.setEnabled(True)
            
            #Select the working sublist of device (contains all partition selected information)
            #print(self.completeListDevices)
            self.workingList=[]
            search = self.ui.CBNanoDevice.currentText()
            if search != "":
                search=search.split()[1]
                #print(search)
                for sublist in self.completeListDevices:
                    if sublist[0] == search:
                        #print("Found it!", sublist)
                        #Found it! ['sdc1', '3,96', 'Gb', 'vfat', 'V7']
                        self.workingList=sublist
                        break

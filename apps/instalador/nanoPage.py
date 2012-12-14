#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow
from random import randint 
from os import system
from subprocess import check_call

class instalador(QMainWindow):

      #Inst. rapida: PMain . PInfo . PQuickInstall . PInstalling . PEnd
      #Inst. Avanç: PMain . PInfo . PTime . PDisk . PUsers . PSystem .
      #PNet . PSoft . PInstalling . PEnd
      #Inst. Nano: PMain . PNano . PInstalling . PEnd

    def prepareNanoPath(self):    
        self.selectedDeviceToInstall=[]

        self.totalSizeOfKademar=self.getSizeOfMountedDevice("/media/f96f9953-8ea6-4a13-995d-6e7baccf8535/archlive/releng64/out/a")
        #self.totalSizeOfKademar=self.getSizeOfMountedDevice("/media/Isos")
        #self.totalSizeOfKademar=self.getSizeOfMountedDevice("/run/archiso/bootmnt")
        #self.totalSizeOfKademar=self.getUsedSpaceOfMountedDevice("/run/archiso/bootmnt")

        #Hide from kademar Installer 
        for i in [self.ui.LTime, self.ui.LUsers, self.ui.LSystem, self.ui.LNetwork, self.ui.LSoftware]:
            i.setVisible(False)

        for i in [self.ui.iTime, self.ui.iUsers, self.ui.iSystem, self.ui.iNetwork, self.ui.iSoftware]:
            i.setVisible(False)

        #hide from installation process
        for i in [self.ui.LPartitioning, self.ui.LRoot, self.ui.LCreatingUsers, self.ui.LNetConfig, self.ui.LInstallingProgress, self.ui.LFinishedProgress]:
            i.setVisible(False)

        for i in [self.ui.iPartitioning, self.ui.iRoot, self.ui.iCreatingUsers, self.ui.iNetConfig, self.ui.iInstallingProgress, self.ui.iFinishedProgress]:
            i.setVisible(False)
            
        for i in [self.ui.LFinishedLogo, self.ui.PBLogo, self.ui.LInstallFinished]:
            i.setVisible(False)
            
        #Show from all
        for i in [self.ui.iPersistentChangesFile]:
            i.setVisible(True)
            
        for i in [self.ui.LPersistentChangesFile]:
            i.setVisible(True)


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
        self.fillListOfDevicesOnCombobox()
        self.ui.CHChangesFile.setEnabled(False)
        self.ui.CHFormatNano.setEnabled(False)
        self.nextButton() #go to first nano page


    def fillListOfDevicesOnCombobox(self,dev_path=None):
        if not self.copying:
            #print("refill devices") 
            self.ui.CBNanoDevice.blockSignals(True)
            try:
                destroy(self.completeListDevices)
                destroy(self.itemList)
            except:
                self.completeListDevices=[]
                self.itemList=[]
            self.completeListDevices=[]
            self.itemList=[]
            self.model = QStandardItemModel()
            self.view = QTreeView()
            self.model.clear()
            #self.model.setHeaderData(0, Qt.Horizontal, "Unit");
            #self.model.setHeaderData(1, Qt.Horizontal, "Size");
            #self.model.setHeaderData(2, Qt.Horizontal, "Information");
            #self.model.setHeaderData(3, Qt.Horizontal, "Fs");

            self.view.setModel(self.model)
            parent = self.model.invisibleRootItem()
            self.view.setIconSize(QSize(40,30))

        ##Empty Partition&Device ComboBox 
            self.ui.CBNanoDevice.clear()
            #Fill the Removable devices list
            #print(self.removableDevicesDetected)
            for i in range(len(self.removableDevicesDetected)):
                #print(self.removableDevicesDetected[i])
                hdd=self.removableDevicesDetected[i][0]
                parts=[]
                parts=self.listPartitionsOfDevice(hdd)
                #print(parts)
                #Only append all HDD if has partitions (failed show when desconnecting pendrives)
                if parts != [] and parts != None:
                    hddsize=float(self.removableDevicesDetected[i][1])  # 20450
                    model=self.removableDevicesDetected[i][2]
                    vendor=self.removableDevicesDetected[i][3]

                    size,unit=self.convertSizeAndUnits(hddsize)

                    #self.ui.CBNanoDevice.addItem(QIcon(self.icon_device_pendrive),hdd+" "+hddsize+" "+unitat+" "+model+" "+vendor)
                    self.completeListDevices.append([hdd,hddsize,unit,model,vendor])
                    self.itemList.append(QStandardItem(QIcon(self.icon_device_pendrive), self.tr("Disk")+" "+hdd))
                    self.itemList.append(QStandardItem(size+" "+unit))
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
                    for i in range(len(parts)):
                        #print(self.removableDevicesDetected[i])
                        part=parts[i][0]
                        partsize=float(parts[i][1])  # 20450
                        fs=parts[i][2]
                        label=parts[i][3]
                        #swaptype=parts[i][4]

                        size,unit=self.convertSizeAndUnits(partsize)

                        self.completeListDevices.append([part,partsize,unit,fs,label])
                        self.itemList.append(QStandardItem(QIcon(self.icon_partition),  self.tr("Partition")+"  "+part))
                        self.itemList.append(QStandardItem(size+" "+unit))
                        self.itemList.append(QStandardItem(str(label)))
                        self.itemList.append(QStandardItem(str(fs)))

                        actualparent.appendRow([
                            self.itemList[len(self.itemList)-4],
                            self.itemList[len(self.itemList)-3],
                            self.itemList[len(self.itemList)-2],
                            self.itemList[len(self.itemList)-1],
                            ])
                    #self.ui.CBNanoDevice.addItem(QIcon(self.icon_partition),part+" "+partsize+" "+fs+" "+unitat+" "+label)
                        #print(hd)

            self.view.adjustSize()
            self.view.setAutoExpandDelay(0)
            self.view.header().hide()

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
            self.ui.CBNanoDevice.blockSignals(False)
            
            self.showYourPaths() #could be changed


    def prepareNanoConnections(self):
        self.connect(self.ui.BGpartedNano, SIGNAL("clicked()"), self.openGparted)
        self.connect(self.ui.SChangeFile, SIGNAL("valueChanged(int)"), self.permanentChangesFileSliderValueChanged)
        self.connect(self.ui.CHChangesFile, SIGNAL("stateChanged(int)"), self.permanentChangesFileCheckboxChanged)
        self.connect(self.ui.CBNanoDevice, SIGNAL("currentIndexChanged(int)"), self.activateOptionsBeforeDeviceIsSelected)

    def processNanoPageBeforeNext(self):
        if self.selectedDeviceToInstall == []:
            self.showWarningMessage("critical", self.tr("Error: No partition selected"), self.tr("You should select a a partition to install"))
            return False

        if self.ui.CHFormatNano.isChecked() == True:
            reply = self.showWarningMessage("infopreg", self.tr("Begin of installation process!"), self.tr("Caution: Lose data is possible!!!\n\n\nWill be erased ALL data of the selected partition!!!\n\nFor more security, it's recommended to have a backup of your device."))
            if reply != QMessageBox.Yes:
                return False
        else:
            reply = self.showWarningMessage("infopreg", self.tr("Begin of installation process!"), self.tr("Your data from your USB device will remain.\n\nTo be more sure, it's recommended to have a backup of your device."))
            
            #Folders with name 'kademar' and '_persistent' will be permanently deleted and overwrite if exists
            
            #Les dades del dispositiu USB es CONSERVARAN\n\nDurant el procés d'instal·lació no podrà accedir al seu dispositiu USB,\n  Es BORRARA el contingut de les carpetes 'boot', 'kademar' i 'html' en cas d'existir. Vagi en compte.\n\nPer a més seguretat, es recomana tenir una còpia de seguretat de les dades."))
        
            if reply != QMessageBox.Yes:
                return False
        
        #self.preparaUsb()
        while True:
            system("for i in `cat /proc/mounts | grep '"+self.selectedDeviceToInstall[0]+"' | awk ' { print $2 } ' | sort -r`; do umount $i; done")
            system("umount /dev/"+self.selectedDeviceToInstall[0][:-1]+"* 2>/dev/null")
            if not self.execShellProcess("/bin/sh","-c","mount | grep -i /dev/"+self.selectedDeviceToInstall[0]+"* 2>/dev/null")=="":
            ##system("echo mandonguilla")
            #try:
            #if not self.execShellProcess("/bin/sh","-c","echo mandonguilla | grep -i dong"):     
                return True
                ##a=subprocess.check_call("mount | grep -i /dev/"+self.selectedDeviceToInstall[0]+"* 2>/dev/null", shell=True)
            #except:
            else:
                reply = self.showWarningMessage("infopreg", self.tr("Close all applications"), self.tr("You must close all applications that have disk access, to be able to continue the installation.\n\nIf you want to stop the process, press 'NO'"))
                if reply==QMessageBox.No:
                    break
                

    def permanentChangesFileSliderValueChanged(self, int):
        self.totalSizeOfDevice=self.selectedDeviceToInstall[1]
        #print(self.totalSizeOfDevice)
        #print(self.totalSizeOfKademar)
        #print(self.totalSizeOfDevice-self.totalSizeOfKademar)
        #print(str(self.totalSizeOfDevice-self.totalSizeOfKademar)[0]) #if it's "-" means device it's too small for install kademar
        self.realChangeFileSize=int*self.totalFreeSizeAfterInstallation/100
        #print(self.realChangeFileSize)
        size,unit=self.convertSizeAndUnits(self.realChangeFileSize)
        self.ui.LChangeFilePercent.setText(str(int)+"%  ("+str(size)+" "+str(unit)+")")

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
            search = self.ui.CBNanoDevice.currentText()
            if search != "":
                search=search.split()[1]
                #print(search)
                for sublist in self.completeListDevices:
                    if sublist[0] == search:
                        #print("Found it!", sublist)
                        #Found it! ['sdc1', '3,96', 'Gb', 'vfat', 'V7']
                        self.selectedDeviceToInstall=sublist
                        break
                self.totalSizeOfDevice=self.selectedDeviceToInstall[1]
                #print(self.totalSizeOfDevice)
                #print(self.totalSizeOfDevice-self.totalSizeOfKademar)
                self.totalFreeSizeAfterInstallation=self.totalSizeOfDevice-self.totalSizeOfKademar

                if str(self.totalFreeSizeAfterInstallation)[0] == "-": #if it's "-" means device it's too small for install kademar
                    self.showWarningMessage("critical", "Error: The selected partition it's too small", "The selectted partition to install it's too small, choose other.")
                    self.ui.CBNanoDevice.setCurrentIndex(-1)
                    self.ui.CHChangesFile.setEnabled(False)
                    self.ui.CHFormatNano.setEnabled(False)
                else:
                    #self.permanentChangesFileSliderValueChanged(30)
                    self.ui.SChangeFile.setValue(0)
                    self.ui.SChangeFile.setValue(30)

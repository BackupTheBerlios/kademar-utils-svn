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
        #Prepare device list combobox
        self.modelNano = QStandardItemModel()
        self.viewNano = QTreeView()
        self.viewNano.setModel(self.modelNano)
        self.viewNano.setIconSize(QSize(40,30))
        self.ui.CBNanoDevice.setView(self.viewNano)
        self.ui.CBNanoDevice.setModel(self.modelNano)
        self.itemListNano=[]
        
        self.selectedDeviceToInstall=[]

        #self.totalSizeOfKademar=self.getSizeOfMountedDevice("/media/f96f9953-8ea6-4a13-995d-6e7baccf8535/archlive/releng64/out/a")
        #self.totalSizeOfKademar=self.getSizeOfMountedDevice("/media/Isos")
        self.totalSizeOfKademar=self.getUsedSpaceOfMountedDevice("/run/archiso/bootmnt") #get size of kademar to check it later if fits on the drvive

        #Hide from kademar Installer 
        for i in [self.ui.LTime, self.ui.LUsers, self.ui.LSystem, self.ui.LNetwork, self.ui.LSoftware, self.ui.LSystemInfo]:
            i.setVisible(False)

        for i in [self.ui.iTime, self.ui.iUsers, self.ui.iSystem, self.ui.iNetwork, self.ui.iSoftware, self.ui.iSystemInfo]:
            i.setVisible(False)

        #hide from installation process
        for i in [self.ui.LRoot, self.ui.LCreatingUsers, self.ui.LNetConfig, self.ui.LInstallingProgress, self.ui.LFinishedProgress]:
            i.setVisible(False)

        for i in [self.ui.iRoot, self.ui.iCreatingUsers, self.ui.iNetConfig, self.ui.iInstallingProgress, self.ui.iFinishedProgress]:
            i.setVisible(False)
            
        #Show from all
        for i in [self.ui.iPersistentChangesFile]:
            i.setVisible(True)
            
        for i in [self.ui.LPersistentChangesFile]:
            i.setVisible(True)


        #labelList=[self.ui.LBoot,self.ui.LCopy,self.ui.LCreatingUsers,self.ui.LDisk,self.ui.LFinishedProgress,self.ui.LInstallingProgress,self.ui.LNetConfig,self.ui.LNetwork,self.ui.LFormating,self.ui.LProcess,self.ui.LRoot,self.ui.LSoftware,self.ui.LSystem,self.ui.LSystemInfo,self.ui.LTime,self.ui.LUsers]
        #for i in labelList:
            #i.setVisible(False)
        #stateList=[self.ui.FBoot,self.ui.FCopy,self.ui.FCreatingUsers,self.ui.FDisk,self.ui.FFinished,self.ui.FFinished,self.ui.FInstalling,self.ui.FNetConfig,self.ui.FNetwork,self.ui.FFormating,self.ui.FRoot,self.ui.FSoft,self.ui.FSystem,self.ui.FSystemInfo,self.ui.FTime,self.ui.FUsers]
        #for i in stateList:
            #i.setVisible(False)

        self.choosedPath=[self.ui.PMain, self.ui.PNano, self.ui.PInstalling, self.ui.PEnd]
        self.ui.CHChangesFile.setChecked(False)
        self.permanentChangesFileCheckboxChanged()
        self.ui.BBack.setVisible(True)
        self.ui.BNext.setVisible(True)
        self.ui.scrollArea_2.setVisible(True)
        self.ui.iDisk.setPixmap(QPixmap(self.icon_state_blue))
        #self.ui.prepareNanoPath.setChecked(False)
        #self.ui.CHChangesFile.setChecked(False)
        self.prepareNanoConnections()
        self.fillListOfDevicesOnCombobox(removable=True)
        self.ui.CHChangesFile.setEnabled(False)
        self.ui.CHFormatNano.setEnabled(False)
        self.nextButton() #go to first nano page
        #self.makeFitsRemovableDevicesComboBoxData()

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
            if not str(self.execShellProcess("/bin/sh","-c","mount | grep -i /dev/"+self.selectedDeviceToInstall[0]+"* 2>/dev/null"))=="":
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
        #self.logMessage(self.totalSizeOfDevice)
        #self.logMessage(self.totalSizeOfKademar)
        #self.logMessage(self.totalSizeOfDevice-self.totalSizeOfKademar)
        #self.logMessage(str(self.totalSizeOfDevice-self.totalSizeOfKademar)[0]) #if it's "-" means device it's too small for install kademar
        self.realChangeFileSize=int*self.totalFreeSizeAfterInstallation/100
        #self.logMessage(self.realChangeFileSize)
        size,unit=self.convertSizeAndUnits(self.realChangeFileSize)
        self.ui.LChangeFilePercent.setText(str(int)+"%  ("+str(size)+" "+str(unit)+")")

    def permanentChangesFileCheckboxChanged(self):
        state=self.ui.CHChangesFile.isChecked()
        self.ui.LChangeFilePercent.setVisible(state)
        self.ui.SChangeFile.setVisible(state)
        self.ui.LChangesFileSize.setVisible(state)
        #self.ui.FChangesFileInfo.setVisible(state)

    def activateOptionsBeforeDeviceIsSelected(self,int):
        #self.logMessage("holad")
        if int!=-1:
            self.ui.CHChangesFile.setEnabled(True)
            self.ui.CHFormatNano.setEnabled(True)
            self.ui.BNext.setEnabled(True)

            #Select the working sublist of device (contains all partition selected information)
            #self.logMessage(self.completeListOfDevices)
            search = self.ui.CBNanoDevice.currentText()
            if search != "":
                search=search.split()[1]
                #self.logMessage(search)
                for sublist in self.completeListOfDevices:
                    if sublist[0] == search:
                        #self.logMessage("Found it!", sublist)
                        #Found it! ['sdc1', '3,96', 'Gb', 'vfat', 'V7']
                        self.selectedDeviceToInstall=sublist
                        break
                self.totalSizeOfDevice=self.selectedDeviceToInstall[1]
                #self.logMessage(self.totalSizeOfDevice)
                #self.logMessage(self.totalSizeOfDevice-self.totalSizeOfKademar)
                self.totalFreeSizeAfterInstallation=self.totalSizeOfDevice-self.totalSizeOfKademar

                if str(self.totalFreeSizeAfterInstallation)[0] == "-": #if it's "-" means device it's too small for install kademar
                    self.showWarningMessage("critical", self.tr("Error: The selected partition it's too small"), self.tr("The selectted partition to install it's too small, choose other."))
                    self.ui.CBNanoDevice.setCurrentIndex(-1)
                    self.ui.CHChangesFile.setEnabled(False)
                    self.ui.CHFormatNano.setEnabled(False)
                else:
                    #self.permanentChangesFileSliderValueChanged(30)
                    self.ui.SChangeFile.setValue(0)
                    self.ui.SChangeFile.setValue(30)
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow
from os import system

#list partitions
import dbus

class instalador(QMainWindow):
    #def __init__(self):
      #print("juas")

      #Inst. rapida: PMain -> PInfo -> PQuickInstall -> PInstalling -> PEnd
      #Inst. Avanç: PMain -> PInfo -> PTime -> PDisk -> PUsers -> PSystem ->
      #PNet -> PSoft -> PInstalling -> PEnd
      #Inst. Nano: PMain -> PNano -> PInstalling -> PEnd
      
    def defineCommons(self):
        #Define to Zero
        self.choosedPath=[]
        self.pagePosition=0
      
        #self.pagePathNano=[self.ui.PMain]
        self.ui.stackedPages.setCurrentWidget(self.ui.PMain) #go to fist main page
      
        self.showYourPaths()
        
    def showYourPaths(self):
        self.ui.BQuickInstall.setVisible(False)
        self.ui.LQuickInstall.setVisible(False)
        self.ui.BAdvancedInstall.setVisible(False)
        self.ui.LAdvancedInstall.setVisible(False)
        self.ui.BRemoteInstall.setVisible(False)
        self.ui.LRemoteInstall.setVisible(False)
        
        #Detect Removable Devices
        self.removableDevicesDetected=self.listRemovableDevices()
        if len(self.removableDevicesDetected) == 0:
            self.ui.BNanoInstall.setVisible(False)
            self.ui.LNanoInstall.setVisible(False)
        
    def setConnections(self):
        self.connect(self.ui.BExit, SIGNAL("clicked()"), self.close)
        self.connect(self.ui.BBack, SIGNAL("clicked()"), self.backButton)
        self.connect(self.ui.BNext, SIGNAL("clicked()"), self.nextButton)

        self.connect(self.ui.BNanoInstall, SIGNAL("clicked()"), self.prepareNanoPath)

        
    def setIconVars(self):
        self.pathinstaller="."
        self.icon_partition=self.pathinstaller+"/img/partition.png"
        self.icon_device_pendrive=self.pathinstaller+"/img/device-pendrive.png"

    def openGparted(self):
        system("gparted-pkexec")
        
    def listRemovableDevices(self):
        bus = dbus.SystemBus()
        ud_manager_obj = bus.get_object("org.freedesktop.UDisks", "/org/freedesktop/UDisks")
        ud_manager = dbus.Interface(ud_manager_obj, 'org.freedesktop.UDisks')
        varReturn=[]
        
        for dev in ud_manager.EnumerateDevices():
            varActual=[]
            device_obj = bus.get_object("org.freedesktop.UDisks", dev)
            #print dev
            device_props = dbus.Interface(device_obj, dbus.PROPERTIES_IFACE)
            isDrive=device_props.Get('org.freedesktop.UDisks.Device', "DeviceIsDrive")
            devicefile=device_props.Get('org.freedesktop.UDisks.Device', "DeviceFile")
            size=device_props.Get('org.freedesktop.UDisks.Device', "PartitionSize")
            isEjectable=device_props.Get('org.freedesktop.UDisks.Device', "DriveIsMediaEjectable")
            isDetachable=device_props.Get('org.freedesktop.UDisks.Device', "DriveCanDetach")
            model=device_props.Get('org.freedesktop.UDisks.Device', "DriveModel")
            vendor=device_props.Get('org.freedesktop.UDisks.Device', "DriveVendor")
            
            rootimage=str(device_props.Get('org.freedesktop.UDisks.Device', "DeviceFileById"))
            #print device_props.Get('org.freedesktop.UDisks.Device', "PartitionSize")
            if isDrive == 1 and isEjectable==0:
                devicefile=devicefile.replace("/dev/","")
                if devicefile.find("loop") == -1 and rootimage.find("root-image") == -1 and devicefile.find("zram") == -1 and isDetachable == 1:
                        #print isDrive
                    #print(size)
                    size=size/1000000
                    varActual.append(devicefile)
                    varActual.append(str(size))
                    varActual.append(model)
                    varActual.append(vendor)
                    varReturn.append(varActual)
                    
        #varActual=["sdz","403701.76","label"]
        #varReturn.append(varActual)
        #varActual=["sdx","4037.0176","label"]
        #varReturn.append(varActual)
        #varActual=["sdw","403.70176","label"]
        #varReturn.append(varActual)
        return(varReturn)
        
    def listPartitionsOfDevice(self,device):
        result=""
        bus = dbus.SystemBus()
        ud_manager_obj = bus.get_object("org.freedesktop.UDisks", "/org/freedesktop/UDisks")
        ud_manager = dbus.Interface(ud_manager_obj, 'org.freedesktop.UDisks')
        varReturn=[]

        #Get thre Real name (sometimes detected like sr0 -> device real name  /dev/scd0)
        for dev in ud_manager.EnumerateDevices():
            device_obj = bus.get_object("org.freedesktop.UDisks", dev)
            device_props = dbus.Interface(device_obj, dbus.PROPERTIES_IFACE)
            devicefile=device_props.Get('org.freedesktop.UDisks.Device', "DeviceFile")
            if str(device).replace("/dev/","")==devicefile.replace("/dev/",""):
                #print devicefile
                disk=dev
                break
                
        for dev in ud_manager.EnumerateDevices():
            varActual=[]
            device_obj = bus.get_object("org.freedesktop.UDisks", dev)
            device_props = dbus.Interface(device_obj, dbus.PROPERTIES_IFACE)
            isDrive=device_props.Get('org.freedesktop.UDisks.Device', "DeviceIsDrive")
            iduuid=device_props.Get('org.freedesktop.UDisks.Device', "IdUuid")
            label=device_props.Get('org.freedesktop.UDisks.Device', "IdLabel")

            if str(dev).find(disk) != -1 and isDrive==0 and iduuid != "":
                devicefile=device_props.Get('org.freedesktop.UDisks.Device', "DeviceFile")
                devicefile=devicefile.strip("/dev/")
                fs=device_props.Get('org.freedesktop.UDisks.Device', "IdType")
                size=device_props.Get('org.freedesktop.UDisks.Device', "PartitionSize")
                size=size/1000000
                #if str(fs).find("swap") != -1:
                    #result=result+" "+str(devicefile)+"-"+str(fs)+"-"+str(size)+"-82"
                #else:
                #result=result+" "+str(devicefile)+"-"+str(fs)+"-"+str(size)

                varActual.append(devicefile)
                varActual.append(str(size))
                varActual.append(str(fs))
                varActual.append(str(label))
                #if str(fs).find("swap") != -1:
                    #varActual.append("82")
                #else:
                    #varActual.append("")

                varReturn.append(varActual)

        #a=sorted(result.split())
        #print(" ".join(a))
        return(varReturn)
        
        
    def backButton(self):
        if self.pagePosition>0:
            self.pagePosition=self.pagePosition-1
            self.ui.stackedPages.setCurrentWidget(self.choosedPath[self.pagePosition])
            self.processPageOnEnter()
        #print(self.choosedPath.indexOf(self.ui.stackedPages.currentWidget()))
        
    def nextButton(self):
        if len(self.choosedPath)-1>self.pagePosition:
            if self.processPageBeforeNext() == True:
                self.pagePosition=self.pagePosition+1
                self.ui.stackedPages.setCurrentWidget(self.choosedPath[self.pagePosition])
        #print(self.choosedPath.indexOf(self.ui.stackedPages.currentWidget()))
        
    def processPageOnEnter(self):
        if self.choosedPath[self.pagePosition]== self.ui.PMain:
            self.prepareMainPage()
    
    def processPageBeforeNext(self):
        if self.choosedPath[self.pagePosition]== self.ui.PNano:
            return self.processNanoPageBeforeNext()
        else:
            return True
    
    ##  FUNCIONS DE WARNING
    def showWarningMessage(self, tipu, miss1, miss2):
        if tipu=="critical":
            QMessageBox.critical(self, miss1, miss2, QMessageBox.Ok)
        if tipu=="warning":
            return QMessageBox.critical(self, miss1, miss2, QMessageBox.Retry, QMessageBox.Ignore)
        if tipu=="infopreg":
            return QMessageBox.critical(self, miss1, miss2, QMessageBox.Yes| QMessageBox.No,  QMessageBox.No)
        if tipu=="info":
            QMessageBox.critical(self, miss1, miss2, QMessageBox.Ok)    
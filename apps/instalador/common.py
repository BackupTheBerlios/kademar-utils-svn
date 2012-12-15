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
      #Inst. rapida: PMain -> PInfo -> PQuickInstall -> PInstalling -> PEnd
      #Inst. Avanç: PMain -> PInfo -> PTime -> PDisk -> PUsers -> PSystem -> PNet -> PSoft -> PInstalling -> PEnd
      #Inst. Nano: PMain -> PNano -> PInstalling -> PEnd
      
    def defineCommons(self):
        #Define to Zero
        self.choosedPath=[]
        self.pagePosition=0
        self.copying=0
        self.endedCopy=0
        self.kademarType="Kademar"
        self.pathInstaller="."        
        self.bus = dbus.SystemBus()
        self.ud_manager_obj = self.bus.get_object("org.freedesktop.UDisks", "/org/freedesktop/UDisks")
        self.ud_manager = dbus.Interface(self.ud_manager_obj, 'org.freedesktop.UDisks')
      
        self.lookDeviceUdisksChangesReloadList()
      
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
        #print("ara", self.removableDevicesDetected)
        if len(self.removableDevicesDetected) == 0:
            self.ui.BNanoInstall.setVisible(False)
            self.ui.LNanoInstall.setVisible(False)
        else:
            self.ui.BNanoInstall.setVisible(True)
            self.ui.LNanoInstall.setVisible(True)
        
    def setConnections(self):
        self.connect(self.ui.BExit, SIGNAL("clicked()"), self.close)
        self.connect(self.ui.BBack, SIGNAL("clicked()"), self.backButton)
        self.connect(self.ui.BNext, SIGNAL("clicked()"), self.nextButton)

        self.connect(self.ui.BNanoInstall, SIGNAL("clicked()"), self.prepareNanoPath)

    def closeEvent(self, event):
        if self.copying:
            self.showWarningMessage("critical", self.tr("Installer cannot be closed"), self.tr("Installer is working and it cannot be closed until it finish."),)
            event.ignore()
            
    def setIconVars(self):
        self.icon_partition=":/img/img/partition.png"
        self.icon_device_pendrive=":/img/img/device-pendrive.png"

    def openGparted(self):
        system("gparted-pkexec")
        
    def listRemovableDevices(self):

        varReturn=[]
        
        for dev in self.ud_manager.EnumerateDevices():
            varActual=[]
            device_obj = self.bus.get_object("org.freedesktop.UDisks", dev)
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
        
    def getDeviceKademarIsBootingFrom(self,var):
        for dev in self.ud_manager.EnumerateDevices():
            device_obj = self.bus.get_object("org.freedesktop.UDisks", dev)
            device_props = dbus.Interface(device_obj, dbus.PROPERTIES_IFACE)
            mount=device_props.Get('org.freedesktop.UDisks.Device', "DeviceMountPaths")
            matching = [s for s in mount if var in s]
            if matching:
                devicefile=str(device_props.Get('org.freedesktop.UDisks.Device', "DeviceFile"))
                devicefile=devicefile.replace("/dev/","")
                return devicefile
            
            
            
    def listPartitionsOfDevice(self,device):
        result=""
        varReturn=[]
        #print (device)
        disk=""

        #Get thre Real name (sometimes detected like sr0 -> device real name  /dev/scd0)
        for dev in self.ud_manager.EnumerateDevices():
            device_obj = self.bus.get_object("org.freedesktop.UDisks", dev)
            device_props = dbus.Interface(device_obj, dbus.PROPERTIES_IFACE)
            devicefile=device_props.Get('org.freedesktop.UDisks.Device', "DeviceFile")
            if str(device).replace("/dev/","")==devicefile.replace("/dev/",""):
                #print devicefile
                disk=dev
        #print(disk)
        if disk !="":
            for dev in self.ud_manager.EnumerateDevices():
                varActual=[]
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
        
    def getUsedSpaceOfMountedDevice(self,var):
        size=self.execShellProcess("/bin/sh", "-c", "df "+var+" | grep -i "+var+" | awk ' { print $3 } '")
        size=float(size)/1000
        return size
        
    def getSizeOfMountedDevice(self,var):
        
        for dev in ud_manager.EnumerateDevices():
            varActual=[]
            device_obj = self.bus.get_object("org.freedesktop.UDisks", dev)
            #print dev
            device_props = dbus.Interface(device_obj, dbus.PROPERTIES_IFACE)
            mount=device_props.Get('org.freedesktop.UDisks.Device', "DeviceMountPaths")
            matching = [s for s in mount if var in s]
            if matching:
                size=device_props.Get('org.freedesktop.UDisks.Device', "PartitionSize")
                size=size/1000000
                return size
        
        
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
                QApplication.processEvents()
                self.processPageOnEnter()
                QApplication.processEvents()
        #print(self.choosedPath.indexOf(self.ui.stackedPages.currentWidget()))
        
    def processPageOnEnter(self):
        actualPage=self.choosedPath[self.pagePosition]
        if actualPage== self.ui.PMain:
            self.prepareMainPage()
        elif actualPage == self.ui.PInstalling:
            if [x for x in range(len(self.choosedPath)) if self.choosedPath[x]==self.ui.PNano]:
                self.prepareInstallNanoCopy()
        elif actualPage== self.ui.PEnd:
            self.prepareEndPage()
        QApplication.processEvents()


            #self.prepareCopy()
    
    def processPageBeforeNext(self):
        if self.choosedPath[self.pagePosition]== self.ui.PNano:
            return self.processNanoPageBeforeNext()
        else:
            return True
    
    def convertSizeAndUnits(self,size):

        size1=str(size).split(".")[0]
        size2=str(size).split(".")[1]
        #print(size1)
        #print(size2)
        if len(str(size).split(".")[0])<=3:
            #print(str(hddsize).split(".")[0][:-3])#hddsize=int(self.parts[i].split("-")[1])  #J
            #hddsize1
            size=size1+","+size2[:2]
            unit="Mb"
        else:
            #hddsize=str(hddsize)[:-3]+","+str(hddsize)[-3]
            size1process=str(size1)[:-3]
            size=size1process+","+size1[-3:-1]
            unit="Gb"
    
        return size,unit
    
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
            
            
    def execShellProcess(self, idCommand, idParam = "", idParam2 = ""):
        param=[]
        if idParam:
            param.append(idParam)
        if idParam2:
            param.append(idParam2)
        proc = QProcess()
        proc.start(idCommand, param)
        proc.waitForFinished()
        result = proc.readAll()
        #print(str(result))
        proc.close()
        return result

####
## HARDWARE CHANGES DETECTOR - RELOAD DEVICE LIST
####

    def lookDeviceUdisksChangesReloadList(self):
        self.ud_manager.connect_to_signal('DeviceAdded', self.fillListOfDevicesOnCombobox)
        self.ud_manager.connect_to_signal('DeviceRemoved', self.fillListOfDevicesOnCombobox)

#####
##  END HARDWARE CHANGES DETECTOR - RELOAD DEVICE LIST
#####
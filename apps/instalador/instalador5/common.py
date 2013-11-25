#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow
from os import system
from socket import socket, AF_INET, SOCK_STREAM

#list partitions
import dbus
import platform

class instalador(QMainWindow):
    #def __init__(self):
      #Inst. rapida: PMain -> PInfo -> PQuickInstall -> PInstalling -> PEnd
      #Inst. Avanç: PMain -> PInfo -> PDisk -> PTime -> PUsers -> PSystem -> PNet -> PSoft -> PInstalling -> PEnd
      #Inst. Nano: PMain -> PNano -> PInstalling -> PEnd
      
    def defineCommons(self):
        #Define to Zero
        self.choosedPath=[]
        self.actualPage=""

        self.pagePosition=0
        self.copying=0
        self.endedCopy=0
        self.kademarType="Kademar"
        self.pathInstaller="/usr/share/instalador" 
        self.logFile = "/tmp/kademar5-install.log"
        self.checkInternetConnection()
        
        self.putDistroNameOnGui()
        
        locale = QLocale.system().name()   #ca_ES
        
        #Define variables for any dbus connection
        self.bus = dbus.SystemBus()
        self.ud_manager_obj = self.bus.get_object("org.freedesktop.UDisks", "/org/freedesktop/UDisks")
        self.ud_manager = dbus.Interface(self.ud_manager_obj, 'org.freedesktop.UDisks')
        
        self.deviceKademarIsBootingFrom=self.getDeviceKademarIsBootingFrom("/run/archiso/bootmnt") #know from where kademar is booting
      
        self.lookDeviceUdisksChangesReloadList()
      
        self.ui.stackedPages.setCurrentWidget(self.ui.PMain) #go to fist main page
      
        self.ui.FDebug.setVisible(False)  #Hide debug frame
        self.prepareDebugLogFile() #initializate debug vars
        
        #Hide finished components of status frame
        for i in [self.ui.LFinishedLogo, self.ui.PBLogo, self.ui.LInstallFinished]:
            i.setVisible(False)
        
    def setConnections(self):
        #Control GUI connections
        self.connect(self.ui.BExit, SIGNAL("clicked()"), self.close)
        self.connect(self.ui.BBack, SIGNAL("clicked()"), self.backButton)
        self.connect(self.ui.BNext, SIGNAL("clicked()"), self.nextButton)

        #Installation Path Connections
        self.connect(self.ui.BNanoInstall, SIGNAL("clicked()"), self.prepareNanoPath)
        self.connect(self.ui.BAdvancedInstall, SIGNAL("clicked()"), self.prepareAdvancedPath)

    def closeEvent(self, event):
        if self.copying:
            self.showWarningMessage("critical", self.tr("Installer cannot be closed"), self.tr("Installer is working and it cannot be closed until it finish."),)
            event.ignore()
        else:
            if self.ui.CBReboot.isChecked():
                system("reboot")
            
    def setIconVars(self):
        self.icon_partition=":/img/img/partition.png"
        self.icon_device_pendrive=":/img/img/device-pendrive.png"
        self.icon_device_hdd=":/img/img/device-hdd.png"
        self.icon_greenTick=":/img/img/finish.png"
        self.icon_waitGrey=":/img/img/waitGrey.gif"
        self.icon_state_blue=":/img/img/state_blue.png"

    def openGparted(self):
        system("gparted")
        
    def listBlockDevices(self,removable):
        #if removable:
            #detachable=1
        #else:
            #detachable=0

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
            if devicefile.find("loop") == -1 and rootimage.find("root-image") == -1 and devicefile.find("zram") == -1 and isDetachable == removable and devicefile != self.deviceKademarIsBootingFrom:
                devicefile=devicefile.replace("/dev/","")
                if isDrive == 1 and isEjectable==0:
                        #print isDrive
                    #self.logMessage(size)
                    size=size/1024 #to MiB
                    size=size/1024 #to GiB
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
        
        

    def fillListOfDevicesOnCombobox(self,removable=None):
        #Function to fill on combobox device block and partitions on each combobox
        model=[]
        #self.logMessage("refill devices") 
        try:
            destroy(self.completeListOfDevices)
            destroy(self.itemListNano)
            destroy(self.itemListSwap)
            destroy(self.itemListRoot)
            destroy(self.itemListOther)
        except:
            self.completeListOfDevices=[]
            self.itemListNano=[]
            self.itemListSwap=[]
            self.itemListRoot=[]
            self.itemListOther=[]
                
        #Check if we want removable deveces or not, and prepare to use them comboboxes
        #if [x for x in range(len(self.choosedPath)) if self.choosedPath[x]==self.ui.PNano]:
        if self.ui.PNano in self.choosedPath:
            #For the nano installer
            #print("Nano Detected")
            desiredDeviceList=self.removableDevicesDetected
            iconDevice=self.icon_device_pendrive
            comboBox=[self.ui.CBNanoDevice]
            model=[self.modelNano]
            view=[self.viewNano]
            itemList=[self.itemListNano]
            
        else:
            #print("Advanced Detected")
            #for the advanced installer
            desiredDeviceList=self.staticDevicesDetected
            iconDevice=self.icon_device_hdd
            comboBox=[ self.ui.CBPartSwap,self.ui.CBPartRoot, self.ui.CBPartOther]
            model=[ self.modelSwap, self.modelRoot,self.modelOther]
            view=[ self.viewSwap,self.viewRoot, self.viewOther]
            itemList=[self.itemListSwap,self.itemListRoot,self.itemListOther]
            
        #Block signals and clean combobox. To not have strange signals and duplicated entries
        for i in comboBox:
            i.blockSignals(True)
            #Empty Partition&Device ComboBox 
            i.clear()
        
        self.completeListOfDevices=[] #Store a real copy of devices to use later
        
        for i in itemList:
            i=[]
            
        for i in model:
            i.clear()
        
        for i in range(len(view)):
            view[i].setModel(model[i])
            view[i].setIconSize(QSize(40,30))

        #Fill the Removable devices list
        #self.logMessage(desiredDeviceList)
        
        for i in range(len(desiredDeviceList)):
            #self.logMessage(desiredDeviceList[i])
            hdd=desiredDeviceList[i][0]
            parts=[]
            parts=self.listPartitionsOfDevice(hdd)
            #self.logMessage(parts)
            #Only append all HDD if has partitions (failed show when desconnecting pendrives)
            if self.deviceKademarIsBootingFrom != hdd: #hide from where is booting from
                if parts != [] and parts != None:  #put partitions if there are. If not, don't put any thing
                    hddsize=float(desiredDeviceList[i][1])  # 20450
                    hddmodel=desiredDeviceList[i][2]
                    vendor=desiredDeviceList[i][3]
                    health=self.getSmartHealthOfDevice(hdd)
                    size,unit=self.convertSizeAndUnits(hddsize)

                    #comboBox.addItem(QIcon(iconDevice),hdd+" "+hddsize+" "+unitat+" "+model+" "+vendor)
                    self.completeListOfDevices.append([hdd,hddsize,unit,hddmodel,vendor,health])
                    
                    for i in itemList:
                        i.append(QStandardItem(QIcon(iconDevice), self.tr("Disk")+" "+hdd))
                        i.append(QStandardItem(size+" "+unit))
                        i.append(QStandardItem(str(hddmodel+" "+vendor)))
                        if str(health) != "":
                            i.append(QStandardItem(self.tr("SMART HEALTH:")+health))
                        else:
                            i.append(QStandardItem(" "))
                    
                    #Set to non-selectable 4 fields of block device (name,size,vendor+model,smart)
                    for i in [1, 2, 3, 4]:
                        #Of each itemList
                        for j in itemList:
                            j[len(j)-i].setSelectable(False)
                    
                    for i in range(len(model)):
                        parent = model[i].invisibleRootItem()
                        parent.appendRow([
                            itemList[i][len(itemList[i])-4],
                            itemList[i][len(itemList[i])-3],
                            itemList[i][len(itemList[i])-2],
                            itemList[i][len(itemList[i])-1],
                            #it3,
                            ])

                    for j in itemList:
                        actualparent=j[len(j)-4]
                        for i in range(len(parts)):
                            #self.logMessage(desiredDeviceList[i])
                            part=parts[i][0]
                            partsize=float(parts[i][1])  # 20450
                            fs=parts[i][2]
                            label=parts[i][3]
                            #swaptype=parts[i][4]

                            size,unit=self.convertSizeAndUnits(partsize)

                            self.completeListOfDevices.append([part,partsize,unit,fs,label])
                            j.append(QStandardItem(QIcon(self.icon_partition),  self.tr("Partition")+"  "+part))
                            j.append(QStandardItem(size+" "+unit))
                            j.append(QStandardItem(str(label)))
                            j.append(QStandardItem(str(fs)))

                            actualparent.appendRow([
                                j[len(j)-4],
                                j[len(j)-3],
                                j[len(j)-2],
                                j[len(j)-1],
                                ])
                    #comboBox.addItem(QIcon(self.icon_partition),part+" "+partsize+" "+fs+" "+unitat+" "+label)
                        #self.logMessage(hd)

        #Restore again non selected nothing on GUI
        for i in comboBox:
            i.setCurrentIndex(-1)
            
        if removable:
            #From the nano path
            self.ui.CHChangesFile.setEnabled(False)
            self.ui.CHFormatNano.setEnabled(False)
            self.ui.LChangeFilePercent.setVisible(False)
            self.ui.SChangeFile.setVisible(False)
            self.ui.LChangesFileSize.setVisible(False)
            #self.ui.FChangesFileInfo.setVisible(False)
            self.ui.CHChangesFile.setChecked(False)
            self.ui.CHFormatNano.setChecked(False)
        self.ui.BNext.setEnabled(False)

        combo = QComboBox()

        for i in view:
            i.adjustSize()
            i.setAutoExpandDelay(0)
            i.header().hide()
            i.expandAll()
        #for i in range(len(comboBox)):
            #comboBox[i].setView(view[i])
            #comboBox[i].setModel(model[i])
        #self.ui.CBNanoDevice.setView(self.viewNano)
        #self.ui.CBNanoDevice.setModel(self.modelNano)        

        #self.viewNano.expandAll()
        self.makeFitsRemovableDevicesComboBoxData()
        
        for i in comboBox:
            i.blockSignals(False)
            

    def makeFitsRemovableDevicesComboBoxData(self):
        #print("hola", comboBox, model, view)
        if self.ui.PNano in self.choosedPath:
            #print("Nano Detected")
            comboBox=[self.ui.CBNanoDevice]
            view=[self.viewNano]
        else:
            #for the advanced installer
            #print("Advanced Detected")
            comboBox=[ self.ui.CBPartSwap,self.ui.CBPartRoot, self.ui.CBPartOther]
            view=[ self.viewSwap,self.viewRoot, self.viewOther]
        
        for i in range(len(view)):
            value=int(str(int(comboBox[i].width())/8).split(".")[0])
            #print(comboBox[i].width())
            #view[i].header().resizeSection(0, value*3) #name
            view[i].header().resizeSection(0, value*3) #name
            view[i].header().resizeSection(1, value) #size
            view[i].header().resizeSection(2, value*2) #model+vendor / label
            view[i].header().resizeSection(3, value*2) #fs / smart info

    def getDeviceKademarIsBootingFrom(self,var):
        for dev in self.ud_manager.EnumerateDevices():
            device_obj = self.bus.get_object("org.freedesktop.UDisks", dev)
            device_props = dbus.Interface(device_obj, dbus.PROPERTIES_IFACE)
            mount=device_props.Get('org.freedesktop.UDisks.Device', "DeviceMountPaths")
            matching = [s for s in mount if var in s]
            if matching:
                devicefile=str(device_props.Get('org.freedesktop.UDisks.Device', "DeviceFile"))
                devicefile=devicefile.replace("/dev/","")
                return devicefile[:-1]
            
            
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
        #self.logMessage(disk)
        if disk !="":
            for dev in self.ud_manager.EnumerateDevices():
                varActual=[]
                device_obj = self.bus.get_object("org.freedesktop.UDisks", dev)
                device_props = dbus.Interface(device_obj, dbus.PROPERTIES_IFACE)
                isDrive=device_props.Get('org.freedesktop.UDisks.Device', "DeviceIsDrive")
                iduuid=device_props.Get('org.freedesktop.UDisks.Device', "IdUuid")
                label=device_props.Get('org.freedesktop.UDisks.Device', "IdLabel")

                if str(dev).find(disk) != -1 and isDrive==0 and iduuid != "":
                    devicefile=device_props.Get('org.freedesktop.UDisks.Device', "DeviceFile")
                    devicefile=devicefile.strip("/dev/")
                    fs=device_props.Get('org.freedesktop.UDisks.Device', "IdType")
                    size=device_props.Get('org.freedesktop.UDisks.Device', "PartitionSize")
                    size=size/1024  #to MiB
                    size=size/1024  #to GiB
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
            #self.logMessage(" ".join(a))
            return(varReturn)
        
    def getSmartHealthOfDevice(self,device):
        health=str(self.execShellProcess("/bin/sh", "-c", "LANG=C smartctl -H /dev/"+device+" 2>/dev/null | grep -i overall-health | cut -d: -f2"))
        health=str(health).replace("\\n","").replace("'","")[1:]
        return health
        
        
    def getUsedSpaceOfMountedDevice(self,var):
        size=self.execShellProcess("/bin/sh", "-c", "df "+var+" | grep -i "+var+" | awk ' { print $3 } '")
        size=float(size)/1024
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
                size=size/1024 #to MiB
                size=size/1024 #to GiB
                return size
        
        
    def backButton(self):
        if self.pagePosition>0:
            self.pagePosition=self.pagePosition-1
            self.ui.stackedPages.setCurrentWidget(self.choosedPath[self.pagePosition])
            self.processPageOnEnter()
        #self.logMessage(self.choosedPath.indexOf(self.ui.stackedPages.currentWidget()))
        
    def nextButton(self):
        if len(self.choosedPath)-1>self.pagePosition:
            if self.processPageBeforeNext() == True:
                self.pagePosition=self.pagePosition+1
                self.ui.stackedPages.setCurrentWidget(self.choosedPath[self.pagePosition])
                QApplication.processEvents()
                self.processPageOnEnter()
                QApplication.processEvents()
        #self.logMessage(self.choosedPath.indexOf(self.ui.stackedPages.currentWidget()))
        
    def processPageOnEnter(self):
        self.actualPage=self.choosedPath[self.pagePosition]
        if self.actualPage== self.ui.PMain:
            self.prepareMainPage()
        elif self.actualPage == self.ui.PInstalling:
            #if [x for x in range(len(self.choosedPath)) if self.choosedPath[x]==self.ui.PNano]:
            if self.ui.PNano in self.choosedPath:
                self.prepareInstallNanoCopy()
        elif self.actualPage== self.ui.PEnd:
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
        #self.logMessage(size1)
        #self.logMessage(size2)
        if len(str(size).split(".")[0])<=3:
            #self.logMessage(str(hddsize).split(".")[0][:-3])#hddsize=int(self.parts[i].split("-")[1])  #J
            #hddsize1
            size=size1+","+size2[:2]
            unit="MiB"
        else:
            #hddsize=str(hddsize)[:-3]+","+str(hddsize)[-3]
            size1process=str(size1)[:-3]
            size=size1process+","+size1[-3:-1]
            unit="GiB"
    
        return size,unit
    
    def showWarningMessage(self, wantedType, miss1, miss2):
        #Show dialog function
        if wantedType=="critical":
            QMessageBox.critical(self, miss1, miss2, QMessageBox.Ok)
        if wantedType=="warning":
            return QMessageBox.critical(self, miss1, miss2, QMessageBox.Retry, QMessageBox.Ignore)
        if wantedType=="infopreg":
            return QMessageBox.critical(self, miss1, miss2, QMessageBox.Yes| QMessageBox.No,  QMessageBox.No)
        if wantedType=="info":
            QMessageBox.critical(self, miss1, miss2, QMessageBox.Ok)    


    def execShellProcess(self, idCommand, idParam = "", idParam2 = ""):
        #Execute a shell order and return the result
        # for pipe commands use idCommand="/bin/bash" idParam="-c" idParam2="shell | piped command"
        param=[]
        if idParam:
            param.append(idParam)
        if idParam2:
            param.append(idParam2)
        proc = QProcess()
        proc.start(idCommand, param)
        proc.waitForFinished()
        result = proc.readAll()
        #self.logMessage(str(result))
        proc.close()
        return result

####
## HARDWARE CHANGES DETECTOR - RELOAD DEVICE LIST
####

    def lookDeviceUdisksChangesReloadList(self):
        #If a device is added or removed, refill the combobox again
        self.ud_manager.connect_to_signal('DeviceAdded', self.reloadDeviceList)
        self.ud_manager.connect_to_signal('DeviceRemoved', self.reloadDeviceList)

    def reloadDeviceList(self, changes=None):
        if not self.copying:
            #Reload static and removable devices and update wich paths are available
            self.staticDevicesDetected=self.listBlockDevices(removable=0)
            self.removableDevicesDetected=self.listBlockDevices(removable=1)
            self.showYourPaths()
            #print(self.choosedPath)
            #if you are in a path, fill devices combobox
            if not len(self.choosedPath)==0: #if we entered on a path
                self.fillListOfDevicesOnCombobox()
#####
##  END HARDWARE CHANGES DETECTOR - RELOAD DEVICE LIST
#####

    def resizeEvent(self, event):
        #print ("resized")
        #if self.choosedPath==[]:
            #event.ignore()
        if not len(self.choosedPath)==0:
            if  self.actualPage==self.ui.PNano or self.actualPage==self.ui.PDisk:
                #event.accept
                self.makeFitsRemovableDevicesComboBoxData()
            
    def keyPressEvent(self, event):
        #Change visivility of Debug frame with F12
        if event.key() == Qt.Key_F12:
            self.toggleDebugVisibility()
            
    def putDistroNameOnGui(self):
        #if not, kademar is already defined
        if platform.node() == "heliox":
            self.kademarType="Heliox"
        else:
            self.kademarType="Kademar"
 

#        if QFile("/etc/kademar/config-livecd.heliox").exists():
#            self.kademarType="Heliox"

        #Put distro name in all parts that are parepared to recibe distro name
        for i in [ self.ui.LInstaller, self.ui.LHelp, self.ui.LWelcomeTitle, self.ui.LQuickInstall, self.ui.LAdvancedInstall, self.ui.LNanoInstall, self.ui.LRemoteInstall, self.ui.LWelcome, self.ui.LInformation, self.ui.RBLicenseQuickN, self.ui.RBLicenseN, self.ui.LFinished, self.ui.LThanks ]:
            text=i.text()
            i.setText(text.replace("%1", self.kademarType))
        
        self.ui.LEPcName.setText(self.kademarType) #line hostname
        
        #logos
        self.ILogo.setPixmap(QPixmap(":/img/img/"+self.kademarType+"Logo.png"))
        self.ILogo_2.setPixmap(QPixmap(":/img/img/"+self.kademarType+"Logo.png"))
        
        #Window Title
        self.ui.setWindowTitle(self.tr("%1 Installer").replace("%1", self.kademarType))
        
        self.ui.setWindowIcon(QIcon(":/img/img/instalador-"+str(self.kademarType).lower()+".png"))


    def logMessage(self, var, var1="", var2="", var3="", var4="", var5=""):
        #log function, to logfile and print it, compatible with debug frame
        print(var, var1, var2, var3, var4, var5)
        with open(self.logFile, "a") as f:
            f.write(var+"\n")
            if var1:
                f.write(var+"\n")
            if var2:
                f.write(var+"\n")
            if var3:
                f.write(var+"\n")
            if var4:
                f.write(var+"\n")
            if var5:
                f.write(var+"\n")
                
    def checkInternetConnection(self):
        self.internet=0
        testConn=socket(AF_INET,SOCK_STREAM)
        try:
            testConn.connect(('www.kademar.org',80))
            testConn.close()
            self.internet=1
            #self.setWindowTitle('Gestion Freetec - Conexión al Servidor - Internet')
        except:
            testConn.close()
            self.internet=0

#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow
from platform import architecture
from platform import node

class cadiTray(QMainWindow):
    def prepareGui(self):
        self.ui.tabWidget.setCurrentWidget(self.ui.General)
        self.putDistroNameOnGui()
        self.loadConfig()

    def putDistroNameOnGui(self):
        #if not, kademar is already defined
        if node() == "heliox":
            self.kademarType="Heliox"
        else:
            self.kademarType="Kademar"

        #Put distro name in all parts that are parepared to recibe distro name
        for i in [ self.ui.L_distName ]:
            text=i.text()
            i.setText(text.replace("%1", self.kademarType))
        
        #logos
        self.ILogoDistro.setPixmap(QPixmap(self.imagepath+self.kademarType+"Logo.png"))
        
        #Window Title
        #self.ui.setWindowTitle(self.tr("%1 Installer").replace("%1", self.kademarType))
        
        #self.ui.setWindowIcon(QIcon(":/img/img/instalador-"+str(self.kademarType).lower()+".png"))


    def putInformationOnGui(self):
    
        text=self.ui.LRam.text()
        self.ui.LRam.setText(text.replace("%1", self.getRam()))
        
        text=self.ui.LKernel.text()
        self.ui.LKernel.setText(text.replace("%1", self.getKernel()))
        
        text=self.ui.LHostname.text()
        self.ui.LHostname.setText(text.replace("%1", self.getHostname()))

        text=self.ui.LCpu.text()
        self.ui.LCpu.setText(text.replace("%1", self.getCpu()))
        
        text=self.ui.LCpuCores.text()
        self.ui.LCpuCores.setText(text.replace("%1", self.getCpuCores()))

        text=self.ui.LCpuArch.text()
        self.ui.LCpuArch.setText(text.replace("%1", self.getArchitecture()))
        
        #self.ui.LCpuInfo.setText(self.getCpuInfo())

    def getRam(self):
        ram=str(self.execShellProcess("/bin/sh", "-c", "LANG=C grep 'MemTotal' /proc/meminfo  | awk '{ print $2 }' "))
        ram=str(ram).replace("\\n","").replace("'","")[1:]
        return ram+" Mb"

    def getKernel(self):
        kernel=str(self.execShellProcess("/bin/sh", "-c", "LANG=C uname -r "))
        kernel=str(kernel).replace("\\n","").replace("'","")[1:]
        return kernel
      
    def getHostname(self):
        hostname=str(self.execShellProcess("/bin/sh", "-c", "LANG=C hostname")) #hostname -f
        hostname=str(hostname).replace("\\n","").replace("'","")[1:]
        return hostname
      
    def getCpu(self):
        cpu=str(self.execShellProcess("/bin/sh", "-c", "LANG=C grep 'model name' /proc/cpuinfo | sed s.'model name'..g | sed s.:..g"))
        cpu=str(cpu).split("\\n")[0]
        cpu=str(cpu).replace("\\n","").replace("\\t","").replace("'","").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ")[1:]
        return cpu

    def getCpuInfo(self):
        cpuinfo=str(self.execShellProcess("/bin/sh", "-c", "LANG=C grep 'cpu MHz' /proc/cpuinfo | awk '{ print $4 }'"))
        cpuinfo=str(cpuinfo).split("\\n")[0]
        cpuinfo=str(cpuinfo).replace("\\n","").replace("'","")[1:]
        return cpuinfo
    
    def getCpuCores(self):
        cpucore=str(self.execShellProcess("/bin/sh", "-c", "LANG=C grep 'cpu MHz' /proc/cpuinfo | awk '{ print $4 }' | wc -l"))
        cpucore=str(cpucore).replace("\\n","").replace("'","")[1:]
        return cpucore
        
        
    def getArchitecture(self):
        if architecture()[0] == "64bit":
            arch="64bit"
        else:
            arch="32bit"
         
        return arch
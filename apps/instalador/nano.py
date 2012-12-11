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
      
    def prepareNanoPath(self):
        #labelList=[self.ui.LBoot,self.ui.LCopy,self.ui.LCreatingUsers,self.ui.LDisk,self.ui.LFinishedProgress,self.ui.LInstallingProgress,self.ui.LNetConfig,self.ui.LNetwork,self.ui.LPartitioning,self.ui.LProcess,self.ui.LRoot,self.ui.LSoftware,self.ui.LSystem,self.ui.LSystemInfo,self.ui.LTime,self.ui.LUsers]
        #for i in labelList:
            #i.setVisible(False)
        
        #stateList=[self.ui.FBoot,self.ui.FCopy,self.ui.FCreatingUsers,self.ui.FDisk,self.ui.FFinished,self.ui.FFinished,self.ui.FInstalling,self.ui.FNetConfig,self.ui.FNetwork,self.ui.FPartitioning,self.ui.FRoot,self.ui.FSoft,self.ui.FSystem,self.ui.FSystemInfo,self.ui.FTime,self.ui.FUsers]
        #for i in stateList:
            #i.setVisible(False)
            
        self.choosedPath=[self.ui.PMain, self.ui.PNano, self.ui.PInstalling, self.ui.PEnd]
        self.ui.BBack.setVisible(True)
        self.ui.BNext.setVisible(True)
        self.ui.scrollArea_2.setVisible(True)
        self.ui.stackedPages.setCurrentWidget(self.ui.PNano) #go to first nano page
        self.prepareNanoConnections()

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
            self.ui.CBNanoDevice.addItem(QIcon(self.icon_device_pendrive),hdd+" "+hddsize+" "+unitat+" "+model+" "+vendor)
            #print(hdd, hddsize,unitat,model,vendor)
            #hddsize=str(hddsize).rjust(7)
            #hd=[]                  #Juntem tota la info del hd en una llista
            #hd.append(hdd)         #Juntem tota la info del hd en una llista
            #hd.append(hddsize)     #Juntem tota la info del hd en una llista
            #self.ui.CBNanoDevice.append(hd)    #Fem llista total de llistes de HD

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
            self.ui.CBNanoDevice.addItem(QIcon(self.icon_partition),part+" "+partsize+" "+fs+" "+unitat+" "+label)
                #print(hd)
        
        #disk (sda) samsung bla bla 500,1gb
	  #part1 sda1 ext4 20,9 gb
        
    def prepareNanoConnections(self):
        self.connect(self.ui.BGpartedNano, SIGNAL("clicked()"), self.openGparted)

        
    #def setConnections(self):
        
        
        
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow
from subprocess import check_call
from os import system
from time import sleep

class instalador(QMainWindow):

      #Inst. rapida: PMain . PInfo . PQuickInstall . PInstalling . PEnd
      #Inst. Avanç: PMain . PInfo . PTime . PDisk . PUsers . PSystem . PNet . PSoft . PInstalling . PEnd
      #Inst. Nano: PMain . PNano . PInstalling . PEnd

    def prepareInstallNanoCopy(self):
        #print("installing")
        self.target="/instalador/nano"
        self.copying=True
        self.ui.WButons_2.setVisible(False)
        
        self.movieGreyIcon=QMovie(self.ui.icon_waitGrey)

        
        wantFormat=0
        if self.ui.CHFormatNano.isChecked():
            wantFormat=1
                
                
        arch=str(self.execShellProcess("uname", "-m").replace("\n","").replace("b",""))[1:]
        persistentFilePath=str(self.target+"/persistent_/"+arch)
        if self.ui.CHChangesFile.isChecked():
            persistentFileSize=str(self.realChangeFileSize).split(".")[0]
        else:
            persistentFileSize=0
            
        self.installNanoKademarProcess=installNanoKademarProcess(self.target, self.selectedDeviceToInstall[0], wantFormat, self.pathInstaller, self.kademarType, persistentFilePath,persistentFileSize, self.totalSizeOfKademar)
        # FUNCIO COPIA
        self.connect(self.installNanoKademarProcess, SIGNAL("formated"), self.nanoEndedFormat)
        self.connect(self.installNanoKademarProcess, SIGNAL("endedCopy"), self.nanoEndedCopyProcess)
        self.connect(self.installNanoKademarProcess, SIGNAL("persistentFileCreated"), self.persistentFileCreated)
        self.connect(self.installNanoKademarProcess, SIGNAL("bootManagerInstalled"), self.bootManagerInstalled)
        #self.connect(self.installNanoKademarProcess, SIGNAL("progress"), self.updateProgressBar)
        self.installNanoKademarProcess.start()
        self.ui.iDisk.setPixmap(QPixmap(self.icon_greenTick))
        
        self.movieGreyIcon.start()
        self.ui.iFormating.setMovie(self.movieGreyIcon)
   
    def nanoEndedFormat(self):
        self.ui.iFormating.setPixmap(QPixmap(self.icon_greenTick))
        self.ui.iCopy.setMovie(self.movieGreyIcon)
        
        #Starting second Thread to check process (ProgressBar)
        self.checkSpace=checkSpace(self.target, self.selectedDeviceToInstall[0], self.totalSizeOfKademar)
        self.connect(self.checkSpace, SIGNAL("progressFromCopyThread"), self.updateProgressBar)
        self.checkSpace.start()

    def nanoEndedCopyProcess(self):
        #global varcopiaacabada, copiant, led_order, icona_verda, icona_taronja, icona_vermella, currentpage, idioma, autologin, mbr, particioarrel, particioswap, particiohome, filesystems, target, pathinstaller
        self.ui.PBInstalling.setVisible(0)
        self.ui.LInstallFinished.setVisible(1)
        self.ui.LFinishedLogo.setVisible(1)
        
        #self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/kademar.png")) #posa al 100% el logo de kademar
        #QApplication.processEvents()  # python QT Yield
        #self.endedCopy=1
        self.ui.iCopy.setPixmap(QPixmap(self.icon_greenTick))
        self.ui.iPersistentChangesFile.setMovie(self.movieGreyIcon)
        
        self.checkSpace.terminate()
        print("Terminated CheckSpace Thread")

 
        #global espaidisc
        #from os import path
        #self.espaidisc.stop()   #Parem el thread de controla el espai en disc

        #self.ui.led_copia.setPixmap(QPixmap(icona_verda))
        #QApplication.processEvents()  # python QT Yield
        

    def persistentFileCreated(self):
        self.ui.iPersistentChangesFile.setPixmap(QPixmap(self.icon_greenTick))
        self.ui.iBoot.setMovie(self.movieGreyIcon)
        
    def bootManagerInstalled(self):
        self.ui.iBoot.setPixmap(QPixmap(self.icon_greenTick))
        self.movieGreyIcon.stop() #we will not use more
        self.copying=False
        QApplication.processEvents()
        #desmunta els directoris si existeixen per una fallida de l'instalador
        system("for i in `cat /proc/mounts | grep '"+self.target+"' | awk ' { print $2 } ' | sort -r`; do umount $i; done")
        #Muntem sistemes de fitxers virtuals
        system("umount "+self.target+"/dev "+self.target+"/proc $DESTI/proc 2>/dev/null")

        #desmunta els directoris si existeixen per una fallida de l'instalador - FORÇAT
        system("for i in `cat /proc/mounts | grep '"+self.target+"' | awk ' { print $2 } ' | sort -r`; do umount -l $i; done")
        #Tornem a desmuntaro x tal d'assegurar-nos - FORÇAT
        system("umount -l "+self.target+"/dev "+self.target+"/proc "+self.target+"/proc 2>/dev/null")
        
    
        #Go to END page
        self.nextButton()

    def updateProgressBar(self, value):
        #print("updating",num)
        self.ui.PBInstalling.setValue(value)
        self.ui.PBLogo.setValue(value)
        

#Funcio de Format i Còpia de fitxers
class installNanoKademarProcess(QThread):
    def __init__(self, target, device, wantFormat, pathInstaller, kademarType, persistentFilePath, persistentFileSize,  totalSizeOfKademar):
        QThread.__init__(self)
        self.target=target
        self.wantFormat=wantFormat
        self.device=device
        self.pathInstaller=pathInstaller
        self.persistentFilePath=persistentFilePath
        self.persistentFileSize=persistentFileSize
        self.kademarType=kademarType
        self.totalSizeOfKademar=totalSizeOfKademar

    def run(self):
        #desmunta els directoris si existeixen per una fallida de l'instalador

        #QApplication.processEvents()
        # es creen els directoris home i es munten a les particions seleccionades
        # Si s'ha definit el HOME
        #copiant=1
        #borrem per si estem actualitzant un USB
        system("for i in `cat /proc/mounts | grep '"+self.target+"' | awk ' { print $2 } ' | sort -r`; do umount $i; done")

        system("mkdir -p "+self.target)
        if self.wantFormat:
            print("Formating ", self.device)
            system("mkfs.vfat -n '"+self.kademarType+"' /dev/"+self.device)
            #system('dosfslabel /dev/'+self.device+' "'+self.kademarType+'"')
        else:
            system('rm -fr '+self.target+'/kademar')
            
        print("mounting /dev/"+self.device, "on",self.target)
        system("mount -rw /dev/"+self.device+" "+self.target)

        self.emit(SIGNAL("formated"))
        #global espaidisc
        #self.checkSpace=checkSpace(self.target, self.device)
        ##self.connect(self.checkSpace, SIGNAL("progressFromCopyThread"), self.sendProgress)
        #self.checkSpace.start()

        #QApplication.processEvents()
        print("Begining Copy")
        system('cp -u -a /run/archiso/bootmnt/kademar '+self.target+' ; echo $? > /tmp/instalador-copia')
        #system("sleep 5")
        
        self.emit(SIGNAL("endedCopy"))


        #PERSISTENT
        if int(self.persistentFileSize) != 0:
            print("Creating Persistent File")
            system("rm -fr "+self.target+"/persistent_") #deleting old persistent
            system("mkdir -p "+self.persistentFilePath)
            system("dd if=/dev/zero of="+self.persistentFilePath+"/root-image.cow bs=1M count="+self.persistentFileSize)
            system("mkfs.ext3 -F "+self.persistentFilePath+"/root-image.cow")
        self.emit(SIGNAL("persistentFileCreated"))



        ##############
        # BOOTLOADER #
        ##############
        print("Installing Bootmanager")
        system("rm -f "+self.target+"/kademar/boot/syslinux/usb-bootinst.sh")
        #system("sleep 5")
        system('cp '+self.pathInstaller+'/scripts/nano/usb-bootinst.sh "'+self.target+'/kademar/boot/syslinux/"') #without cp -a to be sure that don't copy a link
        system('sh '+self.target+'/kademar/boot/syslinux/usb-bootinst.sh')
        #system('rm -f '+self.target+'/install-nano-bootinst.sh')
        self.emit(SIGNAL("bootManagerInstalled"))


        #print("emit acabat")

    #Envia al thread principal el progress
    #def sendProgress(self, num):
        #self.emit(SIGNAL("progressToGauge"), int(num))

#Comprobació de el progrés de la còpia
class checkSpace(QThread):
    def __init__(self, target, device, totalSizeOfKademar):
        QThread.__init__(self)
        print ("Initializing Check Space Class")
        self.target=target
        self.device=device
        self.totalSizeOfKademar=totalSizeOfKademar

    def getUsedSpaceOfMountedDevice(self,var):
        #print("/bin/sh", "-c", "df "+var+" | grep -i "+var+" | awk ' { print $3 } '")
        size=self.execShellProcess("/bin/sh", "-c", "df "+var+" 2>/dev/null | grep -i "+var+" | awk ' { print $3 } '")
        if str(size) != "" and size != None:
            size=int(size)/1000
            return size
    
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
        #print(str(result))
        proc.close()
        #result=str(str(result).replace("b","").replace("\n","").replace("'",""))
        return result

    def run(self):
        print ("starting Check Space")
        #QApplication.processEvents()
        sleep(2)
        #QApplication.processEvents()
        
        #self.totalSizeOfKademar=self.getUsedSpaceOfMountedDevice(self.target)
        #if self.totalSizeOfKademar == None:
            #sleep(5)
            #self.totalSizeOfKademar=self.getUsedSpaceOfMountedDevice(self.target)
        #if self.totalSizeOfKademar == None:
            #sleep(5)
            #self.totalSizeOfKademar=self.getUsedSpaceOfMountedDevice(self.target)
        #print(self.totalSizeOfKademar,"ok")

        #from os import path
        #global target, varcopiaacabada, particioarrel, particioswap, particiohome

        #from os import system
        #from commands import getoutput
        

        #print("check")

        ##print "Check Space Function"

        #self.percent=0
        ##self.totalSizeOfKademar conté el tamany dels fitxers que s'han de copiar
        ##self.totalSizeOfKademar=getoutput("df /run/archiso/bootmnt | grep -i kademar.lzm | awk ' { print $3 } ' ")  #busquem quan ocupa el live-cd

        ###ocupainicial conté el tamany de les particions, per si no s'han formatat
        ### pero per si s'ha seleccionat home separats... es comprova cada un d'ells
        ##ocupaarrel=int(getoutput("df /dev/"+self.device+" | grep /dev/"+self.device+"  | awk ' { print $3 } ' "))
        self.initialSizeOfDevice=self.getUsedSpaceOfMountedDevice("/dev/"+self.device)
        self.actualSizeOfDevice=self.initialSizeOfDevice

        
        if self.initialSizeOfDevice == None or self.actualSizeOfDevice == None:
            sleep(5)
            self.initialSizeOfDevice=self.getUsedSpaceOfMountedDevice(self.target)
            self.actualSizeOfDevice=self.getUsedSpaceOfMountedDevice(self.target)
            
        #print(self.initialSizeOfDevice,self.actualSizeOfDevice)
        ##ocupainicial=ocupaarrel
        ##ocupaactual=ocupainicial

        ##TEMP
        while True:
            sleep(5)  #Comproba cada 10 segons
            #QApplication.processEvents()
            #print("check")
            #QApplication.processEvents()

            ##if not varcopiaacabada:
            ###print "comproba la situacio actual de la copia"
            ##ocupaarrelactual=int(getoutput("df "+target+" | grep "+target+" | awk ' { print $3 } ' "))
            self.actualSizeOfDevice=self.getUsedSpaceOfMountedDevice("/dev/"+self.device)
            ##ocupaactual=ocupaarrelactual

            size=self.actualSizeOfDevice-self.initialSizeOfDevice
            #print(size)
            actualpercentage=float(size)*100
            actualpercentage=actualpercentage/self.totalSizeOfKademar
            #/float(self.totalSizeOfKademar))
            #print(percent)
            
            percent=int(str(actualpercentage).split(".")[0])
            #print(percent)
            #print("initialSizeOfDevice",self.initialSizeOfDevice)
            #print("actualSizeOfDevice",self.actualSizeOfDevice)
            #print("totalSizeOfKademar",self.totalSizeOfKademar)
            #print("size",size)
            #print("percent", percent)
            
###DEBUG
            ###print "PERCENT"
            ###QApplication.processEvents()  # python QT Yield

            if percent<100 and percent>0:
                self.emit(SIGNAL("progressFromCopyThread"), int(percent))
                ##QApplication.processEvents()  # python QT Yield

        ##else:
            ###self.stop()
            ##QApplication.processEvents()  # python QT Yield

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow
from subprocess import check_call
from os import system

class instalador(QMainWindow):

      #Inst. rapida: PMain . PInfo . PQuickInstall . PInstalling . PEnd
      #Inst. Avanç: PMain . PInfo . PTime . PDisk . PUsers . PSystem . PNet . PSoft . PInstalling . PEnd
      #Inst. Nano: PMain . PNano . PInstalling . PEnd

    def prepareInstallNanoCopy(self):
        #print("installing")
        self.target="/instalador/nano"
        self.copying=True
        self.ui.WButons_2.setVisible(False)
        
        wantFormat=0
        if self.ui.CHFormatNano.isChecked():
            wantFormat=1
                
                
        arch=str(self.execShellProcess("uname", "-m").replace("\n",""))
        persistentFilePath=str(self.target+"/persistent_/"+arch)
        if self.ui.CHChangesFile.isChecked():
            persistemSize=str(self.realChangeFileSize).split(".")[0]
        else:
            persistemSize=0
            

        self.installNanoKademarProcess=installNanoKademarProcess(self.target, self.selectedDeviceToInstall[0], wantFormat, persistentFilePath)
        # FUNCIO COPIA
        self.connect(self.installNanoKademarProcess, SIGNAL("endedCopy"), self.nanoEndedCopyProcess)
        self.connect(self.installNanoKademarProcess, SIGNAL("formated"), self.formated)
        self.connect(self.installNanoKademarProcess, SIGNAL("persistentFileCreated"), self.persistentFileCreated)
        self.connect(self.installNanoKademarProcess, SIGNAL("bootManagerInstalled"), self.bootManagerInstalled)
        #self.connect(self.installNanoKademarProcess, SIGNAL("progress"), self.posaprogressbar)
        self.installNanoKademarProcess.start()
        self.ui.iDisk.setPixmap(QPixmap(self.icon_greenTick))
        
    def nanoEndedCopyProcess(self):
        #global varcopiaacabada, copiant, led_order, icona_verda, icona_taronja, icona_vermella, currentpage, idioma, autologin, mbr, particioarrel, particioswap, particiohome, filesystems, target, pathinstaller
        self.ui.PBInstalling.setVisible(0)
        self.ui.LInstallFinished.setVisible(1)
        self.ui.LFinishedLogo.setVisible(1)
        
        #self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/kademar.png")) #posa al 100% el logo de kademar
        #QApplication.processEvents()  # python QT Yield
        self.endedCopy=1
        print("copia acabada")
        self.ui.iCopy.setPixmap(QPixmap(self.icon_greenTick))
        
        #global espaidisc
        #from os import path
        #self.espaidisc.stop()   #Parem el thread de controla el espai en disc

        #self.ui.led_copia.setPixmap(QPixmap(icona_verda))
        #QApplication.processEvents()  # python QT Yield
        
    def formated(self):
        self.ui.iFormating.setPixmap(QPixmap(self.icon_greenTick))

    def persistentFileCreated(self):
        self.ui.iPersistentChangesFile.setPixmap(QPixmap(self.icon_greenTick))

    def bootManagerInstalled(self):
        self.ui.iBoot.setPixmap(QPixmap(self.icon_greenTick))
        self.copying=False
        
##################
# ENDING PROCESS #
##################
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


#Funcio de Format i Còpia de fitxers
class installNanoKademarProcess(QThread):
    def __init__(self, target, device, wantFormat, pathInstaller, persistentFilePath, persistemSize):
        QThread.__init__(self)
        self.target=target
        self.wantFormat=wantFormat
        self.device=device
        self.pathInstaller=pathInstaller
        self.persistentFilePath=persistentFilePath
        self.persistemSize=persistemSize

    def run(self):
        #desmunta els directoris si existeixen per una fallida de l'instalador

        #global espaidisc
        #self.espaidisc=checkspace()
        #self.connect(self.espaidisc, SIGNAL("progress2"), self.enviaprogress)
        #self.espaidisc.start()
        #QApplication.processEvents()
        # es creen els directoris home i es munten a les particions seleccionades
        # Si s'ha definit el HOME
        #copiant=1
        #borrem per si estem actualitzant un USB
        system("mkdir -p "+self.target)
        if self.wantFormat:
            system("mkfs.vfat /dev/"+self.device)
            print("Formating ", self.device)
            system('dosfslabel /dev/'+self.device+' "'+self.kademarType+'"')
        self.emit(SIGNAL("formated"))
            
        print("mounting /dev/"+self.device, "on",self.target)
        system("mount -rw /dev/"+self.device+" "+self.target)
        
        print("Begining Copy")
        system('rm -fr '+self.target+'/kademar')
        system('cp -u -a /run/archiso/bootmnt/kademar '+self.target+' ; echo $? > /tmp/instalador-copia')
        #system("sleep 10")
        #import time
        #time.sleep(15)
        self.emit(SIGNAL("endedCopy"))


        #PERSISTENT
        if self.persistemSize != 0:
            print("INSTALLING CASPER")
            system("rm -fr "+self.target+"/persistent_") #deleting old persistent
            system("mkdir -p "+self.persistentFilePath)
            system("dd if=/dev/zero of="+self.persistentFilePath+"/root-image.cow bs=1M count="+self.persistemSize)
            system("mkfs.ext3 -F "+self.persistentFilePath+"/root-image.cow")
        self.emit(SIGNAL("persistentFileCreated"))



        ##############
        # BOOTLOADER #
        ##############
        
        system("rm -f "+self.target+"/kademar/boot/syslinux/usb-bootinst.sh")
        system('cp '+self.pathInstaller+'/scripts/usb-bootinst.sh "'+self.target+'/kademar/boot/syslinux/"') #without cp -a to be sure that don't copy a link
        system('sh '+self.target+'/kademar/boot/syslinux/usb-bootinst.sh')
        #system('rm -f '+self.target+'/install-nano-bootinst.sh')
        self.emit(SIGNAL("bootManagerInstalled"))


        #print("emit acabat")

    #Envia al thread principal el progress
    #def enviaprogress(self, num):
        #self.emit(SIGNAL("progress"), int(num))

#Comprobació de el progrés de la còpia
#class checkspace(QThread):
    #def __init__(self):
        #QThread.__init__(self)
        #####
        ##  FILESYSTEMS  HD  &  PARTITIONS
        #####
        ##selected_partition[0][0]  -  ARREL  |||   mkfilesystems[particioarrel[1]]  -  particionador (mkfs.reiserfs, etc)
        ##selected_partition[1][0]  -  SWAP   |||   mkfilesystems[particioswap[1]]  -  particionador (mkfs.reiserfs, etc)
        ##selected_partition[2][0]  -  HOME   |||   mkfilesystems[particiohome[1]]  -  particionador (mkfs.reiserfs, etc)

    #def run(self):
        #from os import path
        #global target, varcopiaacabada, particioarrel, particioswap, particiohome

        #from os import system
        #from commands import getoutput
        #from time import sleep

        #sleep(10)  #Comproba cada 10 segons

        ##print "Check Space Function"

        #percent=0
        ##suma conté el tamany dels fitxers que s'han de copiar
        #suma=getoutput("df /run/archiso/bootmnt | grep -i kademar.lzm | awk ' { print $3 } ' ")  #busquem quan ocupa el live-cd

        ##ocupainicial conté el tamany de les particions, per si no s'han formatat
        ## pero per si s'ha seleccionat home separats... es comprova cada un d'ells
        #ocupaarrel=int(getoutput("df /dev/"+particioarrel[0]+" | grep /dev/"+particioarrel[0]+"  | awk ' { print $3 } ' "))

        #ocupainicial=ocupaarrel
        #ocupaactual=ocupainicial

        ##TEMP
        #while True:
            #sleep(10)  #Comproba cada 10 segons

            #if not varcopiaacabada:
                ##print "comproba la situacio actual de la copia"
                #ocupaarrelactual=int(getoutput("df "+target+" | grep "+target+" | awk ' { print $3 } ' "))
                #ocupaactual=ocupaarrelactual

                #cant=ocupaactual-ocupainicial
                #percent=int((int(cant)*100)/int(suma))

##DEBUG
                ##print "PERCENT"
                ##print percent
                ##QApplication.processEvents()  # python QT Yield

                #if percent<100 and percent>0:
                    #self.emit(SIGNAL("progress2"), percent)
                    ##QApplication.processEvents()  # python QT Yield

            #else:
                ##self.stop()
                #QApplication.processEvents()  # python QT Yield

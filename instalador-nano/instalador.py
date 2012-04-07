#!/usr/bin/python
#-*- coding: iso-8859-15 -*-


#############################################
#         -=|  INSTALADOR 5  |=-            #
#             .Main Program.                #
#  ---------------------------------------  #
#     Author: Adonay Sanz Alsina            #
#     License: GPL 2.0 or higer             #
#     First Creation Date:  09-12-08        #
#         Based on instalador 5             #
#  ---------------------------------------  #
#        The Nano (USB) Installer           #
#############################################

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from PyQt4 import uic

from commands import getoutput
#from os import getuid
from os import path
from os import system

import funcions_k

import dbus, dbus.glib

from ui_instalador import Ui_Form

class instalador(QDialog):
    def __init__(self):
        QWidget.__init__(self)
        global tipus
        #uic.loadUi("ui/instalador3.ui", self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
	
        #Get PC info & put on info labels
        kernel=funcions_k.versiokernel()
        versiokademar=funcions_k.versiokademar()
        tipuskademar=funcions_k.tipuskademar()
        self.setWindowTitle("kademar Installer "+str(tipuskademar)+" "+str(versiokademar))

        ######
        #  VARIABLES
        ######
        global led_order, page_order, icona_verda, icona_taronja, icona_vermella, icona_blava, band_cat, band_esp, band_eng, copiant, fs_detector, grephalinfo, target, inicial, icona_pen, icona_partition, mkfilesystems, filesystems, varcopiaacabada, pathinstaller, posicioprogress

        #suport a linux-live i els burnix
        if path.exists("/mnt/live/memory/images/kademar.lzm"):
            inicial="/mnt/live/memory/images/kademar.lzm"
        else:
            inicial="/initrd/rootsquash"

        target="/instalador/desti-nano"  #On es copiaran els fitxers

        pathinstaller="/usr/share/kademar/utils/instalador-nano"  #Path del instalador

        #Definicio de icones
        icona_vermella=pathinstaller+"/img/vermell_p.png"
        icona_taronja=pathinstaller+"/img/taronja_p.png"
        icona_verda=pathinstaller+"/img/verd_p.png"
        icona_blava=pathinstaller+"/img/blau_p.png"

        #Definicio de banderes
        band_cat=pathinstaller+"/img/cat.png"
        band_esp=pathinstaller+"/img/esp.png"
        band_eng=pathinstaller+"/img/eng.png"

        icona_pen=pathinstaller+"/img/pen.png"
        icona_partition=pathinstaller+"/img/partition.png"

        #Ordre de fer aparèixer els leds i les pagines
        led_order=[self.ui.led_disc]
        page_order=["principal", "disc", "mbr", "final"]

        copiant=0       #Estat de si està copiant o no
        varcopiaacabada=0  #Estat de copia finalitzada

        grephalinfo="sh scripts/grephalinfo.sh"  #Script to grep info from hal
        fs_detector="sh scripts/fs-detector"         #Script to get hd & partition info

        mkfilesystems=["mkfs.vfat"]
        filesystems=["vfat"]

        posicioprogress=0

        ####
        ##  INITIAL PREPARATION
        ###

        ###Principal
        #Botons
        #self.ui.img.setPixmap(QPixmap(pathinstaller+self.tr("/img/fons_benvinguda_ca.png")))
        self.ui.l_finished.setVisible(0)

        #Show Principal Page
        self.ui.pages.setCurrentIndex(0)
        #self.ui.pages.setGeometry(150,0,520,420)

        ### Particions i disc dur
        self.llista_particions()

        ###  FINAL
        self.ui.f_final.setVisible(0)


        #####################
        # Signals & Slots Buttons
        #####################

        # Principal
        self.connect(self.ui.boto_next, SIGNAL("clicked()"), self.botonext)
        self.connect(self.ui.boto_exit, SIGNAL("clicked()"), self.botoexit)

        # Particions i disc dur
        #self.connect(self.ui.ch_adv, SIGNAL("clicked()"), self.discs_adv) 

        #####################
        # END  Signals & Slots Buttons
        #####################

####
## HARDWARE CHANGES DETECTOR - RELOAD DEVICE LIST
####

        self.bus = dbus.SystemBus()
        self.hal_manager_obj = self.bus.get_object("org.freedesktop.Hal", 
                                                   "/org/freedesktop/Hal/Manager")
        self.hal_manager = dbus.Interface(self.hal_manager_obj,
                                          "org.freedesktop.Hal.Manager")

        # gdl_changed will be invoked when the Global Device List is changed
        # per the hal spec
        self.hal_manager.connect_to_signal("DeviceAdded", 
                         lambda *args: self.gdl_changed("DeviceAdded", *args))
        self.hal_manager.connect_to_signal("DeviceRemoved", 
                         lambda *args: self.gdl_changed("DeviceRemoved", *args))

    def gdl_changed(self, signal_name, device_udi, *args):
        """This method is called when a HAL device is added or removed."""
        global copiant
        if not copiant:  #If not filecopy started, regenerate partition_list
            if signal_name=="DeviceAdded":
                obj = self.bus.get_object("org.freedesktop.Hal", device_udi)
                dev = dbus.Interface(obj, 'org.freedesktop.Hal.Device')
                if str(dev.GetPropertyStringList("info.capabilities")).find("volume")>=0:  #If it's a volume
                    self.llista_particions()	#Reload partition list
            if signal_name=="DeviceRemoved":
                self.llista_particions()

#####
##  END HARDWARE CHANGES DETECTOR - RELOAD DEVICE LIST
#####


#storage.bus = usb, mmc (falta fw)

    def llista_particions(self):
        global discs, particions, fs_detector, grephalinfo, icona_pen, icona_partition
        #Borrem tota la info
        self.ui.cb_hd_arrel.clear()
        hddtotal=getoutput(fs_detector+" 0 2>/dev/null").split()
        discs=[]
        particions=[]
        #print discos
        #self.ui.cb_hd_arrel.addItem("")
        contahd=contapart=1

        for i in range(len(hddtotal)):
            #print hddtotal[i]
            hdd=hddtotal[i].split("-")[0]
            hddsize=int(hddtotal[i].split("-")[1])/1000  #J
            unitat=" Gb"
            if hddsize<=0:
                hddsize=int(hddtotal[i].split("-")[1])  #J
                unitat=" Mb"
            hddsize=str(hddsize).rjust(7)
            hd=[]                  #Juntem tota la info del hd en una llista
            hd.append(hdd)         #Juntem tota la info del hd en una llista
            hd.append(hddsize)     #Juntem tota la info del hd en una llista
            discs.append(hd)    #Fem llista total de llistes de HD

            #Agafa la informacio de LSHAL del producte
            product=getoutput(grephalinfo+" /dev/"+hdd+" product")
            self.ui.cb_hd_arrel.addItem(QIcon(icona_pen), self.tr("Disc ")+str(contahd)+" ("+hdd+")   "+product+" "+hddsize+unitat)
            self.ui.cb_hd_arrel.setCurrentIndex(-1)

            contahd=contahd+1
            #print hdd
            #print hddsize
            parthdd=getoutput(fs_detector+" "+hdd+" 2>/dev/null").split()
            contapart=1  #Sempre les particions comencen de 1
            for j in parthdd:
                #print j
                part=j.split("-")[0].rjust(6)
                partfs=j.split("-")[1].rjust(15)
                partsize=int(j.split("-")[2])/1000 #Ja en GB
                unitat=" Gb"
                if partsize<=0:
                    partsize=int(j.split("-")[2])  #J
                    unitat=" Mb"
                partsize=str(partsize).rjust(7)

                #print part
                #print partfs
                #print partsize
                #print partswap
                parti=[]                     #Juntem tota la info de la particio en una llista
                parti.append(part)           #Juntem tota la info de la particio en una llista
                parti.append(partfs)         #Juntem tota la info de la particio en una llista
                parti.append(partsize)       #Juntem tota la info de la particio en una llista
                particions.append(parti) #Fem llista total de llistes de particions
                self.ui.cb_hd_arrel.addItem(QIcon(icona_partition),"  Part. "+str(contapart)+" "+part+partfs+str(partsize)+unitat)
                contapart=contapart+1


#####
##  CLOSE EVENT
#####
    def closeEvent(self, event):
        global copiant, running, varcopiaacabada
        if copiant:
            self.showwarnmsg("critical", self.tr("No pot Tencar"), self.tr("Aquest programa està funcionant i no es pot tencar fins que no hagi acabat les seves tasques.."),)
            event.ignore()
        else:
            system("rm -f "+running)
            if varcopiaacabada==1 and self.ui.cb_reboot.isChecked():  #If copy is finished and reboot checkbox is checked, reboot
                system("reboot")
            event.accept()

#####
##  FUNCIONS DEL BOTO NEXT
#####
    def botonext(self):
        global led_order, icona_verda, icona_taronja, icona_vermella, currentpage
        currentpage=self.ui.pages.currentIndex()
        #print currentpage
        if self.checkvalidform(currentpage):
            self.ui.pages.setCurrentIndex(currentpage+1)
            if len(led_order)>currentpage:  #No intentis assignar un led no existent
                led_order[currentpage].setPixmap(QPixmap(icona_taronja))

#####
##  FUNCIONS DEL BOTO EXIT
#####
    def botoexit(self):
        self.close()

    def posaprogressbar(self, num):
        global posicioprogress, pathinstaller
        value=int(num)
        self.ui.progressBar.setValue(value)
        if 20>value>=10 and not posicioprogress==10:
            self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/progres_10.png"))
            posicioprogress=10
        if 30>value>=20 and not posicioprogress==20:
            self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/progres_20.png"))
            posicioprogress=20
        if 40>value>=30 and not posicioprogress==30:
            self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/progres_30.png"))
            posicioprogress=30
        if 50>value>=40 and not posicioprogress==40:
            self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/progres_40.png"))
            posicioprogress=40
        if 60>value>=50 and not posicioprogress==50:
            self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/progres_50.png"))
            posicioprogress=50
        if 70>value>=60 and not posicioprogress==60:
            self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/progres_60.png"))
            posicioprogress=60
        if 80>value>=70 and not posicioprogress==70:
            self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/progres_70.png"))
            posicioprogress=70
        if 90>value>=80 and not posicioprogress==80:
            self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/progres_80.png"))
            posicioprogress=80
        if 100>value>=90 and not posicioprogress==90:
            self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/progres_90.png"))
            posicioprogress=90
        QApplication.processEvents()  # python QT Yield

#####
## FUNCIONS STANDARS
#####
    ## CHARACTER VALIDATOR
    def charvalidator(self, char):
        charorig=char
        if char<>"":
            char=char[-1]
            if char=="à" or char=="á" or char=="è" or char=="é" or char=="í" or char=="ì" or char=="ó" or char=="ò" or char=="ú" or char=="ù" or char=="ç" or char=="·" or char==" " or char=="$" or char=="#" or char=="(" or char==")" or char==" ":
                self.showwarnmsg("critical", self.tr("Error en el Caràcter"), self.tr("No pots escriure caràcters especials com: \n   à, è, é, í, ò, ó, ú, (, ), ' ', ç, ·, $, #, etc"))
                return charorig[:-1]  #Return modified line without invalid char

    ##  FUNCIONS DE WARNING
    def showwarnmsg(self, tipu, miss1, miss2):
        if tipu=="critical":
            QMessageBox.critical(self, miss1, miss2, QMessageBox.Ok)
        if tipu=="warning":
            return QMessageBox.critical(self, miss1, miss2, QMessageBox.Retry, QMessageBox.Ignore)
        if tipu=="infopreg":
            return QMessageBox.critical(self, miss1, miss2, QMessageBox.No, QMessageBox.Ok)
        if tipu=="info":
            QMessageBox.critical(self, miss1, miss2, QMessageBox.Ok)


    def particionar(self):
        system("gparted")
        self.llista_particions()

#####
##  FUNCTION TO BE SURE THAT THE FORM IS FILLED CORRECTLY
#####
    def checkvalidform(self, current):
        #led_order=[self.ui.led_disc, self.ui.led_sistema, self.ui.led_passwd, self.ui.led_user, self.ui.led_mbr]
        #page_order=["principal", "disc", "sistema", "passwd", "user", "mbr", "final"]

        global page_order, icona_verda, icona_taronja, icona_vermella, pathinstaller
        check=page_order[current]
        error=0
        if check=="principal":
            pass  #Nothing to check
        elif check=="disc":
            if self.ui.cb_hd_arrel.currentText()=="":
                error=1
            if str(self.ui.cb_hd_arrel.currentText()).find(self.tr("Disc"))>=0:
                self.ui.cb_hd_arrel.setCurrentIndex(-1)
                error=2

	    if error==1:
	        self.showwarnmsg("critical", self.tr("Error: Partició Buida"), self.tr("Les particions sel·leccionades no poden estar buides. S'ha de seleccionar una partició"))
	    elif error==2:
	        self.showwarnmsg("critical", self.tr("Error: Disc Escollit"), self.tr("Enlloc de triar una partició, s'ha escollit un disc i aquesta no és una entrada vàlida."))


           

    ##copia real de fitxers aquí
            #If error has warned, do not enter on the second loop of checks
            if not error:
                global particioarrel
                particioarrel=[str(self.ui.cb_hd_arrel.currentText()).split()[2]]
    
            #TEMP
                if self.ui.cb_format.isChecked():
                    reply = self.showwarnmsg("infopreg", self.tr("Inici del procés d'instal·lació!"), self.tr("Es borraran TOTES les dades de les particions sel·leccionades!!!\n\nDurant el procés d'instal·lació no podrà accedir als seus discs durs,\n  tanqui tots els programes per assegurar l'accés a tots els recursos.\n\nPer a més seguretat, es recomana tenir una còpia de seguretat de les dades."))
                    if reply==QMessageBox.Ok:
                        error=0
                    else:
                        error=5
                else:
                    reply = self.showwarnmsg("infopreg", self.tr("Inici del procés d'instal·lació!"), self.tr("Les dades del dispositiu USB es CONSERVARAN\n\nDurant el procés d'instal·lació no podrà accedir al seu dispositiu USB,\n  Es BORRARA el contingut de les carpetes 'boot', 'kademar' i 'html' en cas d'existir. Vagi en compte.\n\nPer a més seguretat, es recomana tenir una còpia de seguretat de les dades."))
                    if reply==QMessageBox.Ok:
                        error=0
                    else:
                        error=7
                if not error:
                    if not self.preparaUsb():
                        #Si hi ha un error, vol dir que no s'ha desmuntat bé i torna a fer-ho, aviant
                        while True:
                            reply = self.showwarnmsg("infopreg", self.tr("Tanqui tots els programes"), self.tr("Haurà de tancar tots els programes que tinguin accés als discs, per tal de poder realitzar la instal·lació satisfactòriament.\n\nSi vol aturar el procés, premi 'NO'"))
                            if reply==QMessageBox.No:
                                error=3
                                break
                            elif self.preparaUsb():
                                error=0
                                break
                    else:
                        #Di en despuntar no hi ha hagut error vol dir k tot està ok
                        error=0
                #si ha contestat que no vol començar el procés d'instal·lació, para-ho
                else:
                    error=3
            else:
                error=4
    
            #error=1 #debug
            if not error:
                self.ui.boto_exit.setVisible(0)  #Desactivem el boto de sortida
    
                self.ui.led_disc.setPixmap(QPixmap(icona_verda))  #Select HD completed
                self.ui.led_copia.setPixmap(QPixmap(icona_taronja))  #Begin copy files
                self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/progres_0.png"))  #Imatge kademar de progres al 0%
    
                self.ui.boto_next.setVisible(0)
                self.ui.boto_exit.setVisible(0)
    
                ##print selected_partitions
    
                self.copyfiles=copyfiles()
                # FUNCIO COPIA
                self.connect(self.copyfiles, SIGNAL("acabat"), self.copiaacabada)
                self.connect(self.copyfiles, SIGNAL("progress"), self.posaprogressbar)
                self.copyfiles.start()
    
                    #self.finaltask()  #On form 5 enter, execute finish tasks
        if not error:
            return True
        else:
            return False


    def preparaUsb(self):
        global particioarrel
        system("for i in `cat /proc/mounts | grep '"+target+"' | awk ' { print $2 } ' | sort -r`; do umount $i; done")
        

        system("mkdir -p "+target)
        system("umount /dev/"+particioarrel[0][:-1]+"* 2>/dev/null") #desmuntem totes les particions del USB
        if not getoutput("mount | grep -i /dev/"+particioarrel[0]+"* 2>/dev/null"): #comprobem que tot està desmuntat per poder continuar
            #formata si està marcat
            if self.ui.cb_format.isChecked():
                system("mkfs.vfat /dev/"+particioarrel[0])

            # munta la particio arrel on copiarem els fitxers del sistema
            system("mount -rw /dev/"+particioarrel[0]+" "+target)
            return 1
        else:
            return 0

    def copiaacabada(self):
        global varcopiaacabada, copiant, led_order, icona_verda, icona_taronja, icona_vermella, currentpage, idioma, autologin, mbr, particioarrel, particioswap, particiohome, filesystems, target, pathinstaller
        self.ui.progressBar.setVisible(0)
        self.ui.l_finished.setVisible(1)
        self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/kademar.png")) #posa al 100% el logo de kademar
        QApplication.processEvents()  # python QT Yield
        varcopiaacabada=1
        QApplication.processEvents()

        #global espaidisc
        from os import path
        #self.espaidisc.stop()   #Parem el thread de controla el espai en disc

        self.ui.led_copia.setPixmap(QPixmap(icona_verda))
        self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/kademar.png")) #posa al 100% el logo de kademar
        QApplication.processEvents()  # python QT Yield

        print "copia acabada"

        ##############
        # BOOTLOADER #
        ##############
        system('rm -f '+target+'/install-nano-bootinst.sh')
        system('cp scripts/bootinst.sh '+target+'/install-nano-bootinst.sh') #without cp -a to be sure that don't copy a link
        system('sh '+target+'/install-nano-bootinst.sh')
        system('rm -f '+target+'/install-nano-bootinst.sh')
        QApplication.processEvents()

################
# FINALITZACIO #
################
	#desmunta els directoris si existeixen per una fallida de l'instalador
	system("for i in `cat /proc/mounts | grep '"+target+"' | awk ' { print $2 } ' | sort -r`; do umount $i; done")
	#Muntem sistemes de fitxers virtuals
	system("umount "+target+"/dev "+target+"/proc $DESTI/proc 2>/dev/null")

	#desmunta els directoris si existeixen per una fallida de l'instalador - FORÇAT
	system("for i in `cat /proc/mounts | grep '"+target+"' | awk ' { print $2 } ' | sort -r`; do umount -l $i; done")
	#Tornem a desmuntaro x tal d'assegurar-nos - FORÇAT
	system("umount -l "+target+"/dev "+target+"/proc "+target+"/proc 2>/dev/null")
###################
# FI FINALITZACIO #
###################

###########3   3########
# FI FEINES FINALS !!! #
###########3   3########
        QApplication.processEvents()
	#posem l'ultima pag
        self.ui.pages.setCurrentIndex(2)
        self.ui.f_final.setVisible(1)
        self.ui.boto_exit.setGeometry(165,10,111,31)  #Posemlo al mig
        self.ui.boto_exit.setVisible(1)  # Fem visible el boto de sortir
        copiant=0

#Funcio de Format i Còpia de fitxers
class copyfiles(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global target, inicial, copiant, mkfilesystems, filesystems, particioarrel, particioswap, particiohome
        from os import system
        from commands import getoutput
        #print "Zona de Format"

        ####
        #  FILESYSTEMS  HD  &  PARTITIONS
        ####
        #particioarrel[0] -  ARREL  |||   mkfilesystems[particioarrel[1]]  -  particionador (mkfs.reiserfs, etc)
        #particioswap[0]  -  SWAP   |||   mkfilesystems[particioswap[1]]  -  particionador (mkfs.reiserfs, etc)
        #particiohome[0]  -  HOME   |||   mkfilesystems[particiohome[1]]  -  particionador (mkfs.reiserfs, etc)

        #if mkfilesystems[particioarrel[1]]<>"":
            #print "Formatant ARREL  /dev/"+particioarrel[0]+" amb "+mkfilesystems[particioarrel[1]]
            #system(mkfilesystems[particioarrel[1]]+" /dev/"+particioarrel[0])
            #print  mkfilesystems[particioarrel[1]]+" /dev/"+particioarrel[0]+" Arrel"
        #print "Comença copia de Fitxers"

        #TEMP
        from os import system
        #desmunta els directoris si existeixen per una fallida de l'instalador

        global espaidisc
        self.espaidisc=checkspace()
        self.connect(self.espaidisc, SIGNAL("progress2"), self.enviaprogress)
        self.espaidisc.start()
        QApplication.processEvents()
        # es creen els directoris home i es munten a les particions seleccionades
        # Si s'ha definit el HOME
        copiant=1
        #borrem per si estem actualitzant un USB
        system('rm -fr '+target+'/boot '+target+'/kademar '+target+'/html '+target+'/autorun.bat '+target+'/autorun.inf '+target+'/kademar.ico')
        system('cp -u -a /mnt/live/mnt/*/* '+target+' ; echo $? > /tmp/instalador-copia')
        #import time
        #time.sleep(15)
        self.emit(SIGNAL("acabat"))

        print "emit acabat"

    #Envia al thread principal el progress
    def enviaprogress(self, num):
        self.emit(SIGNAL("progress"), int(num))

#Comprobació de el progrés de la còpia
class checkspace(QThread):
    def __init__(self):
        QThread.__init__(self)
        ####
        #  FILESYSTEMS  HD  &  PARTITIONS
        ####
        #selected_partition[0][0]  -  ARREL  |||   mkfilesystems[particioarrel[1]]  -  particionador (mkfs.reiserfs, etc)
        #selected_partition[1][0]  -  SWAP   |||   mkfilesystems[particioswap[1]]  -  particionador (mkfs.reiserfs, etc)
        #selected_partition[2][0]  -  HOME   |||   mkfilesystems[particiohome[1]]  -  particionador (mkfs.reiserfs, etc)

    def run(self):
        from os import path
        global target, varcopiaacabada, particioarrel, particioswap, particiohome

        from os import system
        from commands import getoutput
        from time import sleep

        sleep(10)  #Comproba cada 10 segons

        #print "Check Space Function"

        percent=0
        #suma conté el tamany dels fitxers que s'han de copiar
        suma=getoutput("df /mnt/live/memory/images/kademar.lzm | grep -i kademar.lzm | awk ' { print $3 } ' ")  #busquem quan ocupa el live-cd

        #ocupainicial conté el tamany de les particions, per si no s'han formatat
        # pero per si s'ha seleccionat home separats... es comprova cada un d'ells
        ocupaarrel=int(getoutput("df /dev/"+particioarrel[0]+" | grep /dev/"+particioarrel[0]+"  | awk ' { print $3 } ' "))

        ocupainicial=ocupaarrel
        ocupaactual=ocupainicial

        #TEMP
        while True:
            sleep(10)  #Comproba cada 10 segons

            if not varcopiaacabada:
                #print "comproba la situacio actual de la copia"
                ocupaarrelactual=int(getoutput("df "+target+" | grep "+target+" | awk ' { print $3 } ' "))
                ocupaactual=ocupaarrelactual

                cant=ocupaactual-ocupainicial
                percent=int((int(cant)*100)/int(suma))

#DEBUG
                #print "PERCENT"
                #print percent
                #QApplication.processEvents()  # python QT Yield

                if percent<100 and percent>0:
                    self.emit(SIGNAL("progress2"), percent)
                    #QApplication.processEvents()  # python QT Yield

            else:
                #self.stop()
                QApplication.processEvents()  # python QT Yield

#TEMP
global running
running="/tmp/instalador-pyqt-running"
#if path.exists(running):
    #system("touch "+running)
app = QApplication(sys.argv)


locale = QLocale.system().name()   #ca_ES
qtTranslator = QTranslator()
if qtTranslator.load("/usr/share/kademar/utils/instalador-nano/tr/"+locale.split("_")[0]+".qm"):
    app.installTranslator(qtTranslator)
    print "Loaded "+locale
elif qtTranslator.load("/usr/share/kademar/utils/instalador-nano/tr/en.qm"):
    app.installTranslator(qtTranslator)
    print "Loaded "+locale

qtTranslatorQT = QTranslator()
qtTranslatorQT.load("qt_"+locale, "/usr/share/qt4/translations")
app.installTranslator(qtTranslatorQT)

instalador = instalador()
instalador.show()
	#global args
	#args=sys.argv
	#print args
app.exec_()

#TEMP
#else:
    #print "Already Running"

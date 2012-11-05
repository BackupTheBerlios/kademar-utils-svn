#!/usr/bin/python2
# -*- coding: utf-8 -*-

#############################################
#         -=|  INSTALADOR 5  |=-            #
#             .Main Program.                #
#  ---------------------------------------  #
#     Author: Adonay Sanz Alsina            #
#     License: GPL 2.0 or higer             #
#     First Creation Date:  03-03-08        #
#  ---------------------------------------  #
#             The Installer                 #
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
from threadCopyfiles import *

import dbus, dbus.glib

from ui_instalador import Ui_FormInstall as Ui_Form

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
        
        if path.exists("/etc/kademar/config-livecd.heliox"):
            self.setWindowTitle("Heliox Installer")
        else:
            self.setWindowTitle("Kademar Installer")
	


        ######
        #  VARIABLES
        ######
        global led_order, page_order, icona_verda, icona_taronja, icona_vermella, icona_blava, band_cat, band_esp, band_eng, copiant, fs_detector, grephalinfo, target, inicial, inicialfs, icona_hd, icona_partition, mkfilesystems, filesystems, varcopiaacabada, pathinstaller, posicioprogress, labelfilesystems

        #suport a linux-live i els burnix
        #if path.exists("/run/archiso/sfs/root-image/root-image.fs"):
        inicialfs="/run/archiso/sfs/root-image/root-image.fs"
        inicial="/run/archiso/root-image"
        #inicial="/mnt/live/memory/images/kademar.lzm"

        #else:
            #inicial="/initrd/rootsquash"

        target="/instalador/desti"  #On es copiaran els fitxers

        pathinstaller="/usr/share/kademar/utils/instalador"  #Path del instalador

        #Definicio de icones
        icona_vermella=pathinstaller+"/img/vermell_p.png"
        icona_taronja=pathinstaller+"/img/taronja_p.png"
        icona_verda=pathinstaller+"/img/verd_p.png"
        icona_blava=pathinstaller+"/img/blau_p.png"
        self.waitIcon=pathinstaller+"/img/wait.gif"
        self.clockIcon=pathinstaller+"/img/wait2.gif"

        #Definicio de banderes
        band_cat=pathinstaller+"/img/cat.png"
        band_esp=pathinstaller+"/img/esp.png"
        band_eng=pathinstaller+"/img/eng.png"

        icona_hd=pathinstaller+"/img/hdd.png"
        icona_partition=pathinstaller+"/img/partition.png"

        #Ordre de fer aparèixer els leds i les pagines
        led_order=[self.ui.led_disc, self.ui.led_disc, self.ui.led_license, self.ui.led_sistema, self.ui.led_passwd, self.ui.led_user, self.ui.led_mbr]
        page_order=["principal", "information", "disc", "license", "sistema", "passwd", "user", "mbr", "final"]

        copiant=0       #Estat de si està copiant o no
        varcopiaacabada=0  #Estat de copia finalitzada

        grephalinfo="python2 scripts/grepproductinfo"  #Script to grep info from hal
        fs_detector="python2 scripts/fs-detector"         #Script to get hd & partition info

        mkfilesystems=["mkfs.ext4","mkfs.reiserfs -q", "mkfs.ext3", "mkfs.ext2", "", "mkswap"]
        filesystems=["ext4", "reiserfs", "ext3", "ext2", "", "reiserfs"]
        labelfilesystems=["e2label $DISK$ $LABEL$","reiserfstune -l $LABEL$ $DISK$", "e2label $DISK$ $LABEL$", "e2label $DISK$ $LABEL$", "", ""]


        posicioprogress=0

        ####
        ##  INITIAL PREPARATION
        ###

        ###Principal
        #Botons
        #self.ui.img.setPixmap(QPixmap(pathinstaller+self.tr("/img/fons_benvinguda_ca.png")))
        self.ui.boto_back.setVisible(0)
        self.ui.l_finished.setVisible(0)

        #Show Principal Page
        self.ui.pages.setCurrentIndex(0)
        #self.ui.pages.setGeometry(150,0,520,420)

        ### System Information
        self.setWaitIcon(self.ui.l_mng)

        ### Particions i disc dur
        self.discs_adv()
        self.discs_tot_en_particio()
        self.llista_particions()

        ### System & Language
        #idioma=funcions_k.idioma()
        locale = QLocale.system().name()
        idioma=locale.split("_")[0]
        if idioma=="ca":
            self.idiomacat()
        elif idioma=="es":
            self.idiomaesp()
        elif idioma=="en":
            self.idiomaeng()

        ###  MBR
        self.ui.cb_mbr.setVisible(0)
        self.ui.ch_initrd.setChecked(1)
        self.ui.ch_initrd.setVisible(0)
        
        if path.exists("/etc/kademar/config-livecd.heliox"):
            self.ui.t_pc.setText("Heliox")

        ###  FINAL
        #self.ui.f_final.setVisible(0)


        #####################
        # Signals & Slots Buttons
        #####################

        # Principal
        self.connect(self.ui.boto_next, SIGNAL("clicked()"), self.botonext)
        self.connect(self.ui.boto_back, SIGNAL("clicked()"), self.botoback)
        self.connect(self.ui.boto_exit, SIGNAL("clicked()"), self.botoexit)
        self.connect(self.ui.boto_ajuda2, SIGNAL("clicked()"), self.botoajuda)
        self.connect(self.ui.boto_ajuda, SIGNAL("clicked()"), self.botoajuda)


        # Particions i disc dur
        self.connect(self.ui.ch_adv, SIGNAL("clicked()"), self.discs_adv)   #Checkbox Advanced
        self.connect(self.ui.ch_tot_en_particio, SIGNAL("clicked()"), self.discs_tot_en_particio)  #Checkbox Tot en una particio
        self.connect(self.ui.cb_hd_arrel, SIGNAL("currentIndexChanged (int)"), self.checkarrelpart)  
        self.connect(self.ui.cb_hd_swap, SIGNAL("currentIndexChanged (int)"), self.checkswappart)
        self.connect(self.ui.cb_hd_home, SIGNAL("currentIndexChanged (int)"), self.checkhomepart)
        self.connect(self.ui.boto_particionar, SIGNAL("clicked()"), self.particionar)  #Engega gparted

        # Sistema
        self.connect(self.ui.t_pc, SIGNAL("textChanged (const QString&)"), self.charvalidatorpc)
        self.connect(self.ui.b_cat, SIGNAL("clicked()"), self.idiomacat)
        self.connect(self.ui.b_esp, SIGNAL("clicked()"), self.idiomaesp)
        self.connect(self.ui.b_eng, SIGNAL("clicked()"), self.idiomaeng)

        # User
        self.connect(self.ui.t_user_account, SIGNAL("textChanged (const QString&)"), self.charvalidatoruser)
        self.connect(self.ui.t_nom, SIGNAL("textChanged (const QString&)"), self.fillaccount)

        # MBR
        self.connect(self.ui.rb_auto, SIGNAL("clicked()"), self.selecciombr)
        self.connect(self.ui.rb_man, SIGNAL("clicked()"), self.selecciombr)
        self.connect(self.ui.rb_no, SIGNAL("clicked()"), self.selecciombr)

        #####################
        # END  Signals & Slots Buttons
        #####################

####
## HARDWARE CHANGES DETECTOR - RELOAD DEVICE LIST
####

        self.bus = dbus.SystemBus()
        self.hal_manager_obj = self.bus.get_object("org.freedesktop.UDisks", 
                                                   "/org/freedesktop/UDisks/Manager")
        self.hal_manager = dbus.Interface(self.hal_manager_obj,
                                          "org.freedesktop.UDisks.Manager")

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
                obj = self.bus.get_object("org.freedesktop.UDisks", device_udi)
                dev = dbus.Interface(obj, 'org.freedesktop.UDisks.Device')
                if str(dev.GetPropertyStringList("info.capabilities")).find("volume")>=0:  #If it's a volume
                    self.llista_particions()	#Reload partition list
            if signal_name=="DeviceRemoved":
                self.llista_particions()

#####
##  END HARDWARE CHANGES DETECTOR - RELOAD DEVICE LIST
#####

    def llista_particions(self):
        global discs, particions, fs_detector, grephalinfo, icona_hd, icona_partition
        #Borrem tota la info
        for i in self.ui.cb_hd_arrel, self.ui.cb_hd_swap, self.ui.cb_hd_home, self.ui.cb_mbr:
            i.clear()
        hddtotal=getoutput(fs_detector+" 0 2>/dev/null | grep -v zram | sort").split()  #get out all rubbish
        discs=[]
        particions=[]
        #print discos
        #self.ui.cb_hd_arrel.addItem("")
        contahd=contapart=1

        for i in range(len(hddtotal)):
            #print hddtotal[i]
            hdd=hddtotal[i].split("-")[0]
            hddsize=int(hddtotal[i].split("-")[1])  # 20450
            #MB support
            if len(str(hddsize))<=3:
                hddsize=int(hddtotal[i].split("-")[1])  #J
                unitat=" Mb"
            else:
                hddsize=str(hddsize)[:-3]+","+str(hddsize)[-3]
                unitat=" Gb"

            hddsize=str(hddsize).rjust(7)
            hd=[]                  #Juntem tota la info del hd en una llista
            hd.append(hdd)         #Juntem tota la info del hd en una llista
            hd.append(hddsize)     #Juntem tota la info del hd en una llista
            discs.append(hd)    #Fem llista total de llistes de HD

            #Agafa la informacio de LSHAL del producte
            product=getoutput(grephalinfo+" /dev/"+hdd+" product")
            for i in self.ui.cb_hd_arrel, self.ui.cb_hd_swap, self.ui.cb_hd_home, self.ui.cb_mbr:
                i.addItem(QIcon(icona_hd), self.tr("Disk ")+str(contahd)+" ("+hdd+")   "+product+" "+hddsize+unitat)
                i.setCurrentIndex(-1)

            contahd=contahd+1
            #print hdd
            #print hddsize
            parthdd=getoutput(fs_detector+" "+hdd+" 2>/dev/null").split()
            contapart=1  #Sempre les particions comencen de 1
            for j in parthdd:
                #print j
                part=j.split("-")[0].rjust(6)
                partfs=j.split("-")[1].rjust(15)
                partsize=int(j.split("-")[2]) #Ja en GB
                if len(str(partsize))<=3:
                    #si te separador, treu-lo
                    if str(partsize).find("-")>0:
                        partsize=int(hddtotal[i].split("-")[1])  #J
                    #else:
                        #partsize=int(hddtotal[i])  #J
                    unitat=" Mb"
                else:
                    partsize=str(partsize)[:-3]+","+str(partsize)[-3]
                    unitat=" Gb"
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
                for i in self.ui.cb_hd_arrel, self.ui.cb_hd_swap, self.ui.cb_hd_home:
                    i.addItem(QIcon(icona_partition),"  Part. "+str(contapart)+" "+part+partfs+str(partsize)+unitat)
                contapart=contapart+1


        #Si finalment no hi ha més d'un disc dur, desactiva la possiblitat d'escollir manual al MBR
        if len(discs)==1:
            self.ui.rb_man.setVisible(0)
        #Autoseleccio de la particio swap. Si es troba, posala, sino posa -1 == RES
        tmpswap=self.ui.cb_hd_swap.findText("swap", Qt.MatchContains)
        if tmpswap<>-1:
            self.ui.cb_hd_swap.setCurrentIndex(tmpswap)

            #print particions
            #print discs

#####
##  CLOSE EVENT
#####
    def closeEvent(self, event):
        global copiant, running, varcopiaacabada
        if copiant:
            self.showwarnmsg("critical", self.tr("Installer cannot be closed"), self.tr("Installer is working and it cannot be closed until it finish."),)
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
##  FUNCIONS DEL BOTO BACK
#####
    def botoback(self):
        global led_order, icona_verda, icona_taronja, icona_vermella, currentpage
        currentpage=self.ui.pages.currentIndex()
        #Cannot back after start copy live-cd files to HD
        #Des / Activa botons de endevant o tenca als ultims panels
        if currentpage==4:
            self.ui.boto_back.setVisible(0)
        elif currentpage==8:
            self.ui.boto_next.setVisible(1)

        if currentpage>2:
            self.ui.pages.setCurrentIndex(currentpage-1)
            #Set blue led = you have been already here
            if len(led_order)>=currentpage:  #No intentis assignar un led no existent
                led_order[currentpage-1].setPixmap(QPixmap(icona_blava))

#####
##  FUNCIONS DEL BOTO EXIT
#####
    def botoexit(self):
        self.close()

#####
##  FUNCIONS DEL BOTO AJUDA
#####
    def botoajuda(self):
        for i in ['okular','kpdf','xpdf','kghostview','epdfview','evince-gtk','areader']:
            if len(getoutput('which %s' %(i))) > 0:
                reader=i
                break
        manual=[pathinstaller+"/docs/manual_es.pdf"]
        self.process = QProcess()
        self.process.start(reader, manual)

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
                self.showwarnmsg("critical", self.tr("Character error"), self.tr("You cannot write special characters as: \n   à, è, é, í, ò, ó, ú, (, ), ' ', ç, ·, $, #, mayus, etc"))
                return charorig[:-1]  #Return modified line without invalid char

            ### TODO: non capital letters for login name
            
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


#####
## FUNCIONS DE LA FORM DE DISCS & PARTICIONS
#####
    #Si esta conectat fes visible la seleccio de  /HOME
    def discs_tot_en_particio(self):  #Tot en la mateixa particio
        if not self.ui.ch_tot_en_particio.isChecked():
            visible=1
        else:
            visible=0
        for i in self.ui.l_part_home, self.ui.cb_hd_home, :
            i.setVisible(visible)

        if visible and self.ui.ch_adv.isChecked():
            self.ui.cb_hd_format_home.setVisible(1)
        else:
            self.ui.cb_hd_format_home.setVisible(0)

    #Si està activat, fes visible lo de Format
    def discs_adv(self):  #Advanced
        if self.ui.ch_adv.isChecked():
            visible=1
        else:
            visible=0
        for i in self.ui.l_format, self.ui.cb_hd_format_arrel, self.ui.cb_hd_format_swap:
            i.setVisible(visible)

        if visible and not self.ui.ch_tot_en_particio.isChecked():
           self.ui.cb_hd_format_home.setVisible(1)
        else:
           self.ui.cb_hd_format_home.setVisible(0)

    def checkparticionsiguals(self, tipus, select):
        error=0
        if tipus=="arrel":
            cur=self.ui.cb_hd_arrel.currentIndex()
            if cur==-1:
                cur=127
            if self.ui.cb_hd_swap.currentIndex()==cur:
                error=1
                self.ui.cb_hd_swap.setCurrentIndex(-1)
            if self.ui.cb_hd_home.currentIndex()==cur:
                self.ui.cb_hd_home.setCurrentIndex(-1)
                if not self.ui.ch_tot_en_particio.isChecked():
                    error=1
            if error:
                self.showwarnmsg("critical", self.tr("Same Partitions"), self.tr("Cannot have two assigned functions to the same partition."))

            #self.ui.cb_hd_arrel.currentIndex()==cur:

        elif tipus=="swap":
            cur=self.ui.cb_hd_swap.currentIndex()
            if cur==-1:
                cur=127
            if self.ui.cb_hd_arrel.currentIndex()==cur:
                error=1
                self.ui.cb_hd_arrel.setCurrentIndex(-1)
            if self.ui.cb_hd_home.currentIndex()==cur:
                self.ui.cb_hd_home.setCurrentIndex(-1)
                if not self.ui.ch_tot_en_particio.isChecked():
                    error=1
            if error:
                self.showwarnmsg("critical", self.tr("Same Partitions"), self.tr("Cannot have two assigned functions to the same partition."))

        elif tipus=="home":
            cur=self.ui.cb_hd_home.currentIndex()
            if cur==-1:
                cur=127
            if self.ui.cb_hd_arrel.currentIndex()==cur:
                error=1
                self.ui.cb_hd_arrel.setCurrentIndex(-1)
            if self.ui.cb_hd_swap.currentIndex()==cur:
                self.ui.cb_hd_swap.setCurrentIndex(-1)
                error=1
            if error:
                self.showwarnmsg("critical", self.tr("Same Partitions"), self.tr("Cannot have two assigned functions to the same partition."))

    def checkarrelpart(self, char):
        self.checkparticionsiguals("arrel", char)

    def checkswappart(self, char):
        self.checkparticionsiguals("swap", char)

    def checkhomepart(self, char):
        self.checkparticionsiguals("home", char)

    def particionar(self):
        system("gparted-pkexec")
        self.llista_particions()

#####
## FUNCIONS DE LA FORM SISTEMA
#####

    def setidioma(self, lang):
        global band_cat, band_esp, band_eng, idioma
        if lang=="ca":
            idioma="ca"
            self.ui.b_cat.setEnabled(0)
            for i in self.ui.b_esp, self.ui.b_eng:
                i.setEnabled(1)
                i.setChecked(0)
            self.ui.l_bandera.setPixmap(QPixmap(band_cat))
        elif lang=="es":
            idioma="es"
            self.ui.b_esp.setEnabled(0)
            for i in self.ui.b_cat, self.ui.b_eng:
                i.setEnabled(1)
                i.setChecked(0)
            self.ui.l_bandera.setPixmap(QPixmap(band_esp))
        elif lang=="en":
            idioma="en"
            self.ui.b_eng.setEnabled(0)
            for i in self.ui.b_cat, self.ui.b_esp:
                i.setEnabled(1)
                i.setChecked(0)
            self.ui.l_bandera.setPixmap(QPixmap(band_eng))

    def idiomacat(self):
        self.setidioma("ca")
    def idiomaesp(self):
        self.setidioma("es")
    def idiomaeng(self):
        self.setidioma("en")

    #Use the Character Validator to confirm OK of PC name
    def charvalidatorpc(self, line):
        ret = self.charvalidator(line)
        if ret or ret=="":
            self.ui.t_pc.setText(str(ret))

#####
##  FUNCTIONS OF USER FORM
#####
    def fillaccount(self, char):
        replacers=[("à","a"),("á","a"),("è","e"),("é","e"),("í","i"),("ì","i"),("ò","o"),("ó","o"),("ú","u"),("ù","u"),("ç","c")]
        nom=char.split(" ")[0]  #Agafem la primera part del nom
        for i in replacers:
            nom=nom.replace(i[0], i[1])
        self.ui.t_user_account.setText(str(nom).lower())  #Defineix el nom del compte en minuscules

    #Use the Character Validator to confirm OK of login user
    def charvalidatoruser(self, line):
        ret = self.charvalidator(line)
        if ret or ret=="":
            self.ui.t_user_account.setText(str(ret))


#####
##  FUNCTIONS OF MBR / GRUB  FORM
#####
    def selecciombr(self):
        if self.ui.rb_auto.isChecked():
            self.ui.cb_mbr.setVisible(0)
        elif self.ui.rb_man.isChecked():
            self.ui.cb_mbr.setVisible(1)
        elif self.ui.rb_no.isChecked():
            self.ui.cb_mbr.setVisible(0)

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
            #pass  #Nothing to check
            self.ui.boto_exit.setVisible(0)
            self.ui.boto_next.setVisible(0)
            #self.ui.pages.setCurrentIndex(currentpage+1)
            #QApplication.processEvents()  # python QT Yield
            self.getSystemInformation()
        elif check=="information":
            #pass  #Nothing to check
            self.ui.boto_exit.setVisible(1)
            self.ui.boto_next.setVisible(1)
            self.movie.stop()
        elif check=="disc":
            if self.ui.cb_hd_arrel.currentText()=="":
                error=1
            if self.ui.cb_hd_swap.currentText()=="":
                error=1
            if str(self.ui.cb_hd_arrel.currentText()).find(self.tr("Disk"))>=0:
                self.ui.cb_hd_arrel.setCurrentIndex(-1)
                error=2
            if str(self.ui.cb_hd_swap.currentText()).find(self.tr("Disk"))>=0:
                self.ui.cb_hd_swap.setCurrentIndex(-1)
                error=2
            if not self.ui.ch_tot_en_particio.isChecked():
                if self.ui.cb_hd_home.currentText()=="":
                    error=1
                if str(self.ui.cb_hd_home.currentText()).find(self.tr("Disk"))>=0:
                    self.ui.cb_hd_arrel.setCurrentIndex(-1)
                    error=2

	    if error==1:
	        self.showwarnmsg("critical", self.tr("Error: Empty Partition"), self.tr("Selected partition cannot be empty. You must select two paritions, for Root and Swap at least."))
	    elif error==2:
	        self.showwarnmsg("critical", self.tr("Error: Disk Choosen"), self.tr("Instead to select a partition, you have choosed a disk, and is an invalid selection."))

            #Be Sure to Format partitions
            #if not error:
                #if not cb_adv.isChecked()

             #If error has warned, do not enter on the second loop of checks
            if not error:


                global particioarrel, particioswap, particiohome
                particioarrel=particioswap=particiohome=[]
                # Set the format of partitions
                if self.ui.ch_adv.isChecked():
                    partiarrel=self.ui.cb_hd_format_arrel.currentIndex()
                    partiswap=self.ui.cb_hd_format_swap.currentIndex()
                    partihome=self.ui.cb_hd_format_home.currentIndex()
                else:
                    partiarrel=partihome=0  #defineix quin FS utilitzar en relacio a la llista   mkfilesystems. Per defecte reiserfs - EXT4 (encara no)

                partiswap=4  #Swap solament et pot formatar amb mkswap -> no comprobar res

                #selected_partitions=[,(str(self.ui.cb_hd_swap.currentText()).split()[2], partiswap)]
                particioarrel=[str(self.ui.cb_hd_arrel.currentText()).split()[2], partiarrel]
                particioswap=[str(self.ui.cb_hd_swap.currentText()).split()[2], partiswap]

                if not self.ui.ch_tot_en_particio.isChecked():
                    particiohome=[str(self.ui.cb_hd_home.currentText()).split()[2], partihome]

                #if mkfs is selected, then partition will be formated and warn to do it
                hddtoformat=""
                hddtoformat=particioswap[0]
                if mkfilesystems[particioarrel[1]]:
                    hddtoformat=hddtoformat+" "+particioarrel[0]
                if particiohome:
                    if mkfilesystems[particiohome[1]]<>"":
                        hddtoformat=hddtoformat+" "+particiohome[0]

                reply = self.showwarnmsg("infopreg", self.tr("Start Installation Process!"), self.tr("ALL data of")+" "+hddtoformat+" "+self.tr("will be erased!!!\n\nWhile installator is working, you cannot access to your hard disk,\n please, close opened programs to have full access to your resources.\n\nFor security reasons, it's recomended to have a backup of your data.\n\nIf you haven't selected a format for your partitions, it will be formated as")+" "+filesystems[0])
                
                if reply==QMessageBox.Ok:
                    if 0<>0:
                        #Si hi ha un error, vol dir que no s'ha desmuntat bé i torna a fer-ho, aviant
                        while True:
                            reply = self.showwarnmsg("infopreg", self.tr("Close all applications"), self.tr("You should close all opened applications with disk access, in order to be able to install sucessfully.\n\nIf you want to stop installation process, press 'NO'"))
                            if reply==QMessageBox.No:
                                error=3
                                break
                            elif int(getoutput("umnt-kademar 2>/dev/null; echo $?"))==0:
                                error=0
                                break
                    else:
                        #Di en despuntar no hi ha hagut error vol dir k tot està ok
                        error=0
                #si ha contestat que no vol començar el procés d'instal·lació, para-ho
                else:
                    error=3

            if not error:
                self.ui.boto_exit.setVisible(0)  #Desactivem el boto de sortida

                self.ui.led_disc.setPixmap(QPixmap(icona_verda))  #Select HD completed
                self.ui.led_copia.setPixmap(QPixmap(icona_taronja))  #Begin copy files
                self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/progres_0.png"))  #Imatge kademar de progres al 0%

                #print selected_partitions

                #mount FS on a folder to copy
		system("mkdir -p "+inicial)
                system("mount "+inicialfs+" "+inicial)
                
                self.copyfiles=copyfiles(target, inicial, mkfilesystems, filesystems, particioarrel, particioswap, particiohome, labelfilesystems)
                # FUNCIO COPIA
                self.connect(self.copyfiles, SIGNAL("acabat"), self.copiaacabada)
                self.connect(self.copyfiles, SIGNAL("progress"), self.posaprogressbar)
                self.copyfiles.start()
                copiant=1


        elif check=="license":
            if not self.ui.rb_license_yes.isChecked() and not self.ui.rb_license_no.isChecked():
                error=1
            else:
                self.ui.boto_back.setVisible(1)

            if error==1:
                self.showwarnmsg("critical", self.tr("Error: License"), self.tr("Please accept or decline non free licenses."))

        elif check=="sistema":
            if self.ui.t_pc.text()=="":   # If no pc name defined -> kademar
                self.ui.t_pc.setText("kademar")

        elif check=="passwd":
           if not self.ui.t_root_passwd1.text()==self.ui.t_root_passwd2.text():
               self.showwarnmsg("critical", self.tr("Error on Administrator Password"), self.tr("Check that two passwords are identical.",))
               error=1
           elif self.ui.t_root_passwd1.text()=="" or self.ui.t_root_passwd2.text()=="" and not error:
                self.showwarnmsg("critical", self.tr("Error on Administrator Password"), self.tr("Check that the administrator password is not empty."))
                error=1
           elif len(self.ui.t_root_passwd1.text())<=5 and not error:
               reply = self.showwarnmsg( "warning", self.tr("Security Warning on Administratror Password"),self.tr("For security reasons Administrator password should be longer than 6 characters."))
               if reply==QMessageBox.Retry:
                   error=1

        elif check=="user":
           if self.ui.t_user_account.text()=="":
               self.showwarnmsg("critical", self.tr("Error on User Account"), self.tr("User Account cannot be empty."))
               error=1
           elif not self.ui.t_user_passwd1.text()==self.ui.t_user_passwd2.text() and not error:
               self.showwarnmsg("critical", self.tr("Error on User Password"), self.tr("Check that two passwords are identical."))
               error=1
           elif self.ui.t_user_passwd1.text()=="" or self.ui.t_user_passwd2.text()=="" and not error:
               self.showwarnmsg("critical", self.tr("Error on User Password"), self.tr("Check that the user password is not empty."))
               error=1
           elif len(self.ui.t_user_passwd1.text())<=5 and not error:
               reply = self.showwarnmsg("warning", self.tr("Security Warning on User Account"), self.tr("For security reasons Administrator password should be longer than 6 characters."))
               if reply==QMessageBox.Retry:
                   error=1
           if self.ui.t_root_passwd1.text()==self.ui.t_user_passwd1.text() and not error:
               reply = self.showwarnmsg("warning", self.tr("Security Warning on User Account"), self.tr("For security reasons is recommended to have different password on User and Administrator Account"))
               if reply==QMessageBox.Retry:
                   error=1
           global autologin
           if self.ui.cb_autologin.isChecked():
               autologin="si"
           else:
               autologin="no"
        if check=="mbr":
            global mbr
            if self.ui.rb_auto.isChecked():
                mbr="auto"
            elif self.ui.rb_man.isChecked():
                mbr=str(self.ui.cb_mbr.currentText()).split()[2].replace("(","").replace(")","")  #Que quedi   sda
            elif self.ui.rb_no.isChecked():
                mbr="no"
            #print "MBR"
            #print mbr
            self.ui.boto_next.setVisible(0)

            self.ui.pages.setCurrentIndex(currentpage+1)
            QApplication.processEvents()  # python QT Yield
            self.finaltask()  #On form 5 enter, execute finish tasks
        if not error:
            return True
        else:
            return False

    def copiaacabada(self):
        global varcopiaacabada
        self.ui.progressBar.setVisible(0)
        self.ui.l_finished.setVisible(1)
        self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/kademar.png")) #posa al 100% el logo de kademar
        QApplication.processEvents()  # python QT Yield
        varcopiaacabada=1
        QApplication.processEvents()
        self.finaltask()
        QApplication.processEvents()

#Get System Information
    def getSystemInformation(self):
        self.Thread=getSystemInformationThread()
        # FUNCIO COPIA
        self.connect(self.Thread, SIGNAL("acabat"), self.botonext)
        self.Thread.start()
        #print "engegat"


    def setWaitIcon(self, label, icon="wait"):
        if icon=="wait":
            img=self.waitIcon
        elif icon=="clock":
            img=self.clockIcon
        self.movie=QMovie(img)
        label.setMovie(self.movie)
        self.movie.start()

#Funcio a executar al acabar
    def finaltask(self):
        global varcopiaacabada, copiant, led_order, icona_verda, icona_taronja, icona_vermella, currentpage, idioma, autologin, mbr, particioarrel, particioswap, particiohome, filesystems, target, pathinstaller
        #global espaidisc
        from os import path
        #self.espaidisc.stop()   #Parem el thread de controla el espai en disc

        self.ui.led_copia.setPixmap(QPixmap(icona_verda))
        #self.ui.logo_kademar.setPixmap(QPixmap(pathinstaller+"/img/kademar.png")) #posa al 100% el logo de kademar
        QApplication.processEvents()  # python QT Yield


        print "copia acabada"
        if currentpage==7 and varcopiaacabada:  #Si estem a la última pàgina, vol dir ue hem acabat
            self.ui.boto_back.setVisible(0)
            self.ui.boto_next.setVisible(0)
            
            #self.setWaitIcon(self.ui.l_clock, "clock")

            self.ui.boto_ajuda2.setVisible(0)
            self.ui.boto_ajuda.setVisible(0)

            print "tasques finals"

            led_order[1].setPixmap(QPixmap(icona_verda))


            ########
            ##   TASQUES FINALS DE L'INSTALADOR - ZONA D'SCRIPTS AMB BASH
            ########
            
            #put username in lowercase to be compatible
            self.ui.t_user_account.setText(str(self.ui.t_user_account.text()).lower())
            
            ########

            if path.exists(target+"/home/"+str(self.ui.t_user_account.text())):
                creahome="creahome_no"
            else:
                creahome="creahome_si"
            #CREACIO PLANTILLA BASH
            #TEMP
            #plantilla="/home/clawlinux/plantilla"
            plantilla="/tmp/instalador-environment"
            plantillapasswd="/tmp/instalador-environment-passwd"  #Plantilla amb les contrassenyes

            f=open(plantilla,'w')
            f.writelines('# Taula de Configuracio de la nova instal·lació \n')
            f.writelines('particioarrel=/dev/'+particioarrel[0]+' \n')
            f.writelines('fsparticioarrel='+filesystems[particioarrel[1]]+' \n')
            f.writelines('particioswap=/dev/'+particioswap[0]+' \n')
            if particiohome:
                f.writelines('particiohome=/dev/'+particiohome[0]+' \n')
                f.writelines('fsparticiohome='+filesystems[particiohome[1]]+' \n')
            f.writelines("#Desti d'instal·lacio  \n")
            f.writelines('DESTI='+target+' \n')
            f.writelines("#Nom PC i Idioma de la instal·lada \n")
            f.writelines('NOM_PC="'+self.ui.t_pc.text()+'" \n')
            f.writelines('LANGUAGE='+idioma+' \n')
            f.writelines('#Nom persona \n')
            f.writelines('nom="'+self.ui.t_nom.text()+'" \n')
            f.writelines('#Username \n')
            f.writelines('login="'+self.ui.t_user_account.text()+'" \n')
            f.writelines('#Autologin on KDM \n')
            f.writelines('AUTOLOGIN='+autologin+' \n')
            f.writelines('#Si es un nou usuari o no \n')
            f.writelines('crea_home="'+creahome+'" \n')
            f.writelines('mbr='+mbr+' \n')
            f.writelines('mbr_dev='+particioarrel[0]+' \n')
            f.writelines('#Initrd creation  \n')
            if self.ui.ch_initrd.isChecked():
                f.writelines('make_initrd="yes" \n')
            else:
                f.writelines('make_initrd="no" \n')

            if self.ui.rb_license_yes.isChecked():
                f.writelines('license="yes" \n')
            else:
                f.writelines('license="no" \n')
            f.close()

            f=open(plantillapasswd,'w')
            f.writelines("#Root Password \n")
            f.writelines('rootpasswd="'+self.ui.t_root_passwd1.text()+'" \n')
            f.writelines("#User Password \n")
            f.writelines('passwd="'+self.ui.t_user_passwd1.text()+'" \n')
            f.close()

    #########3   3#######
    # FEINES FINALS !!! #
    #########3   3#######
        #############################
        # CONFIGURACIONS DE SISTEMA #
        #############################

        #Muntem sistemes de fitxers virtuals
            system("mount --bind /dev "+target+"/dev")
            system("mount -t proc "+target+"/proc "+target+"/proc")
            system("mount -t sysfs "+target+"/sys "+target+"/sys")
            led_order[2].setPixmap(QPixmap(icona_verda))

            system("sh scripts/install-sysconfig")
            led_order[3].setPixmap(QPixmap(icona_verda)) #license

            QApplication.processEvents()  # python QT Yield

        ################################
        # FI CONFIGURACIONS DE SISTEMA #
        ################################

        ###############################
        # CANVI PASS DE ROOT          #
        ###############################

            system("sh scripts/install-root_passwd")
            led_order[4].setPixmap(QPixmap(icona_verda))
            QApplication.processEvents()  # python QT Yield


        #############################
        # CONFIGURACIO USUARI       #
        #############################
            ###################################
            # AFEGEIX USUARI, EXTRET DEL CADI #
            ###################################
            password=self.ui.t_user_passwd1.text()
            gecos=self.ui.t_nom.text()
            login=self.ui.t_user_account.text()
            
            #Delete LIVECD default user
            default_user=getoutput(". /etc/kademar/config-livecd ; echo $user")
            groups=getoutput('for i in $(grep -i '+default_user+' /etc/group | cut -d: -f1); do echo -n $i,; done')

            
            if default_user<>login:
                print "Deleting LiveCD default user"
                system("chroot "+target+" /usr/sbin/userdel "+default_user)
                system("rm -fr "+target+"/home/"+default_user)


#-m      create home
#-M      no create home
#chpass user

            #home='/home/'+login
            #bash='/bin/bash'
            if not path.exists(target+'/home'+login):
                crea_home="-m"
                print "Crea Home SI"
            else:
                crea_home="-M"
                print "Crea Home NO"

            system(str('chroot '+str(target)+' /usr/sbin/useradd '+str(crea_home)+' -p "" -c "'+str(gecos)+'" -g users -G "'+str(groups[:-1])+'" '+str(login)))
            print str('chroot '+str(target)+' /usr/sbin/useradd '+str(crea_home)+' -p "" -c "'+str(gecos)+'" -g users -G "'+str(groups[:-1])+'" '+str(login))

            system("sh scripts/install-user_passwd")
            
                    
            system("sh scripts/install-usuaris")

            led_order[5].setPixmap(QPixmap(icona_verda))
            QApplication.processEvents()  # python QT Yield

        #############################
        # FI CONFIGURACION USUARI   #
        #############################


        ##############
        # BOOTLOADER #
        ##############
        # si el checkbox2 està marcat es desitja NO instal.lar el GRUB
        # l'usuari tindrà que configurar a ma el seu sistema d'engegada
        # amb la opció marcada les passes 1 a 4 no es faràn 

            # Prepara el grub (carpeta /boot)
            print "sh scripts/install-bootloader" 
            QApplication.processEvents()  # python QT Yield
            system("sh scripts/install-bootloader")
            QApplication.processEvents()  # python QT Yield

            if mbr=="no":
                print "No s'instal·la GRUB"
            else:
                print 'mbr=',mbr

            # ENTRADA PEL LOG
                print "FERGRUB"
                #import fergrub
            # ENTRADA PEL LOG
                #crea menu.list de grub
                #print "sh scripts/make-grub_menu"
                #system("sh scripts/make-grub_menu")
                QApplication.processEvents()  # python QT Yield
            # ENTRADA PEL LOG
                print "sh scripts/install-bootloader-final"
            #Instalem el grub en el  MBR del disc.
                system("sh scripts/install-bootloader-final")

                led_order[6].setPixmap(QPixmap(icona_verda))
                QApplication.processEvents()  # python QT Yield
        #################
        # FI BOOTLOADER #
        #################

	################
        # FINALITZACIO #
        ################
            #Copiem el log de l'instal.lador i tots els fitxers que poden haver tingut a veure i borrem anteriors logs
            if path.exists(target+"/usr/share/kademar/install.log.tar.gz"):
                system("rm -f "+target+"/usr/share/kademar/install.log.tar.gz")
            system("tar cfz "+target+"/usr/share/kademar/install.log.tar.gz /tmp/kademar* /tmp/particions* /tmp/instalador-environment /tmp/particio_swap /var/tmp/xserver /var/xsession* /var/es /var/en /var/ca /etc/default/locale /etc/kademar-release /etc/kademar/config* /etc/kademar* "+target+"/boot/grub/menu.lst 2>/dev/null")
            system("chmod 400 "+target+"/usr/share/kademar/install.log.tar.gz")
            system("chown root:root "+target+"/usr/share/kademar/install.log.tar.gz")
            #desmunta els directoris si existeixen per una fallida de l'instalador
            system("for i in `cat /proc/mounts | grep '"+target+"' | awk ' { print $2 } ' | sort -r`; do umount $i; done")
            #Muntem sistemes de fitxers virtuals
            system("umount "+target+"/dev "+target+"/proc $DESTI/proc 2>/dev/null")

            #desmunta els directoris si existeixen per una fallida de l'instalador - FORÇAT
            system("for i in `cat /proc/mounts | grep '"+target+"' | awk ' { print $2 } ' | sort -r`; do umount -l $i; done")
            #Tornem a desmuntaro x tal d'assegurar-nos - FORÇAT
            system("umount -l "+target+"/dev "+target+"/proc "+target+"/proc 2>/dev/null")



            ########
            ##   FI TASQUES FINALS DE L'INSTALADOR - ZONA D'SCRIPTS AMB BASH
            ########

        ###################
        # FI FINALITZACIO #
        ###################
    ###########3   3########
    # FI FEINES FINALS !!! #
    ###########3   3########
            #QApplication.processEvents()
            #self.ui.pages.setCurrentWidget(self.ui.p_end) #go to end page

            QApplication.processEvents()
            #self.movie.stop()

            #self.ui.p_end.setVisible(1) #go to end page
            #self.ui.p_final.setVisible(0)

            self.ui.pages.setCurrentWidget(self.ui.p_end) #go to end page


            self.ui.boto_exit.setGeometry(230, 10, 111, 31)  #Posemlo al mig
            self.ui.boto_exit.setVisible(1)  # Fem visible el boto de sortir
            self.ui.l_finished.setVisible(0) #set hidden label "finished copy"
            copiant=0


class getSystemInformationThread(QThread):
    def __init__(self):	
        QThread.__init__(self)

    def run(self):
        global pathinstaller
        #self.engega=QProcess()
        system("sh "+pathinstaller+"/scripts/get_system_information.sh")
        #if not self.engega.waitForFinished(2 * 60 * 1000): #wait for 2 hours
            #print "the end"
        self.emit(SIGNAL("acabat"))

#TEMP
global running
running="/tmp/instalador-pyqt-running"
#if path.exists(running):
    #system("touch "+running)
app = QApplication(sys.argv)


locale = QLocale.system().name()   #ca_ES
qtTranslator = QTranslator()
if qtTranslator.load("/usr/share/kademar/utils/instalador/tr/"+locale.split("_")[0]+".qm"):
    app.installTranslator(qtTranslator)
    print "Loaded "+locale
elif qtTranslator.load("/usr/share/kademar/utils/instalador/tr/en.qm"):
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

#!/usr/bin/python
#-*- coding: iso-8859-15 -*-

#
# Function to manage Recent Hotplugged Hardware
#  Shows Window with options to execute and process
#  It's called by detecta_hardware.py
#

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from PyQt4 import uic
from commands import getoutput
#from os import getuid
import funcions_k
from os import path
from os import system
#from hotplugactions_variables import HotplugactionsVariables #Possible variables a fer per cada medi
from ui_hotplugactions import Ui_Form_hotplugactions as Ui_Form


class hotplugaction(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        #uic.loadUi("ui/action.ui", self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.hpvar=[]
	
        #checkbox no visible
        self.ui.ch_save.setVisible(False)
	
	#Define icon size
        self.ui.listWidget.setIconSize(QSize(48,48))

	#####################
        #Signals & Slots Buttons
	#####################
        self.connect(self.ui.boto_sortir, SIGNAL("clicked()"), self.sortir)
        self.connect(self.ui.boto_fesaccio, SIGNAL("clicked()"), self.fesaccio)

        self.connect(self.ui.listWidget, SIGNAL("itemSelectionChanged()"), self.enableboto)
#Si se li fa dos clics al item, procesal com si apretes el boto de desconnecta
        self.connect(self.ui.listWidget, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.fesaccio)
#GLOBAL VARIABLES
        #print "ACCTION"
        #print self.tipus
        #for i in cdrom:
            #print i[1]
        self.ui.boto_fesaccio.setEnabled(0)

        #print dir()
        #self.self.program()
        #self.programns = accions_possibles()
        #self.programns.start()
        #print dir(self.self.program)

    def accio(self, medi, block, mount="", name=""):
        self.media=medi

        self.icona=self.descr=self.program=self.nom=""

        #Transfer local variables to global
        self.blk=block
        self.mnt=mount
        self.label=name
        
        #self.hpvar.append(HotplugactionsVariables())
        self.defineix_variables(self.blk, self.mnt, self.label, self.blk.replace("/dev/",""))
        continua=True
        self.load_config() #Search for preconfigured programs to run
        #print dir(hotplugactionsconfig)
        if medi=="cdrom": #CD normal
            self.icona=self.cdromicon
            self.descr=self.cdromprop
            self.program=self.cdrom
            self.nom=self.cdromname
            prog=hotplugactionsconfig.cdrom_prog
        elif medi=="dvddata": #DVD normal
            self.icona=self.dvddataicon
            self.descr=self.dvddataprop
            self.program=self.dvddata
            self.nom=self.dvddataname
            prog=hotplugactionsconfig.dvddata_prog
        elif medi=="dvd" or medi=="vcd": #PELI DVD
            self.icona=self.dvdicon
            self.descr=self.dvdprop
            self.program=self.dvd
            self.nom=self.dvdname
            prog=hotplugactionsconfig.dvd_prog
        elif medi=="audiocd": #Audio CD
            self.icona=self.audiocdicon
            self.descr=self.audiocdprop
            self.program=self.audiocd
            self.nom=self.audiocdname
            prog=hotplugactionsconfig.audiocd_prog
        elif medi=="blankcd": #Blank CD
            self.icona=self.blankcdicon
            self.descr=self.blankcdprop
            self.program=self.blankcd
            self.nom=self.blankcdname
            prog=hotplugactionsconfig.blankcd_prog
        elif medi=="pen":  #Usb
            self.icona=self.penicon
            self.descr=self.penprop
            self.program=self.pen
            self.nom=self.penname
            prog=hotplugactionsconfig.pen_prog
        elif medi=="dvb": #DVB/TDT
            self.icona=self.dvbicon
            self.descr=self.dvbprop
            self.program=self.dvb
            self.nom=self.dvbname
            prog=hotplugactionsconfig.dvb_prog
        elif medi=="wlan": #Wireless / wlan
            self.icona=self.wlanicon
            self.descr=self.wlanprop
            self.program=self.wlan
            self.nom=self.wlanname
            prog=hotplugactionsconfig.wlan_prog
        elif medi=="eth": #Ethernet/RJ45 Device
            self.icona=self.ethicon
            self.descr=self.ethprop
            self.program=self.eth
            self.nom=self.ethname
            prog=hotplugactionsconfig.eth_prog
        elif medi=="fwcam": #Wireless / wlan
            self.icona=self.fwcamicon
            self.descr=self.fwcamprop
            self.program=self.fwcam
            self.nom=self.fwcamname
            prog=hotplugactionsconfig.fwcam_prog
        else:
            print medi+" self.media not recognized"
            continua=False

        #print "medi"
        #print medi

        #Si el programa de execució  està definit, i existeix (no s'ha desinstalat)
        #   executa el programa sel·leccionat.
        #   
        self.programafer=None
        if continua:
            if not prog:  #Si no esta definit  "No Fer Res"
                print "not prog defined"
                if getoutput("which "+prog.split(" ")[0]).split(" ")[0] and not prog=="none": #Si el programa definit, existeix
                    print 
                    self.programafer=prog
                    self.fesaccio()
                else:
                    #Si no, mostra la finestra de sel·lecció
                    print "mostrafinestra"
                    self.mostrafinestra()
                    self.raise_()
                    self.activateWindow()  #I posala davant de tot

        #Function de ensenyar la finestra de sel·lecció
    def mostrafinestra(self):
        #Standar name to window
        windowlabel=self.nom.replace("$mnt$",self.mnt).replace("$blk$",self.blk).replace("$part$",self.blk.replace("/dev/","")).replace("$label$",self.label)
        if self.label<>"":
            #put Window title with self.label
            windowlabel=windowlabel+" - "+self.label
        self.setWindowTitle(windowlabel)
        self.setWindowIcon(QIcon(self.icona))
        self.ui.listWidget.clear()
        self.ui.label.setText(self.descr.replace("$mnt$",self.mnt).replace("$blk$",self.blk).replace("$label$",self.label))
        self.ui.iconamedi.setPixmap(QPixmap(self.icona))

        #real   1 2 3
        #compared  1 3


	#compared list
        #1 3

	#list object nº 2 does not exists
        #2

	#so, list object nº3 becomes object 2
        #2 -> 3

        self.llistatreball=[]
	#De les possibles accions, crea la llista de treball amb els programes que realment estiguin instal·lats
        for i in self.program:
            if getoutput("which "+i[2].split(" ")[0]):
                self.llistatreball.append(i)
        self.llistatreball.append(self.nofer)  #I al final de la llista, dona la possibilitat de no fer res

	#I posa la llista de treball
        for i in self.llistatreball:
            a=QListWidgetItem(self.ui.listWidget)
            a.setText(i[1])
            a.setIcon(QIcon(i[0]))
            self.ui.listWidget.addItem(a)
                #self.ui.iconamedi.setIcon(QIcon(i[0]))
            #print "self.llistatreball"
        #print self.llistatreball
        #Si realment existeix el medi, continua
        self.show()  #Mostrala
        self.raise_()
        self.activateWindow()  #I posala davant de tot



    def fesaccio(self):
        if not self.programafer:
            selecio = str(self.ui.listWidget.currentItem().text().toLocal8Bit())
            #print selecio
            run=self.llistatreball[self.ui.listWidget.currentRow()][2].replace("$mnt$",self.mnt).replace("$blk$",self.blk).replace("$label$",self.label)
        else:
            run=self.programafer.replace("$mnt$",self.mnt).replace("$blk$",self.blk).replace("$label$",self.label)

        #print run
        if run<>"":
            from os import system
            system(run+" &")

        #Si esta marcat recorda la seleccio, recordala
        if self.ui.ch_save.isChecked():
            self.saveconfig()

        #Close window
        self.close()

    def sortir(self):
        self.close()

    def enableboto(self):
        self.ui.boto_fesaccio.setEnabled(1)

    def closeEvent(self, event):
        event.ignore()
        self.hide()




#Load config, global and local, call real import_config with filenames
    def load_config(self):
        global hotplugactionsconfig, hotplugactionslocalfile
        hotplugactionsconffile="hotplugactions_conf.py"
        hotplugactionsglobalfile="/usr/share/kademar/utils/kademarcenter/cfg/"+hotplugactionsconffile
        #print hotplugactionsconffile, hotplugactionsglobalfile
        if path.exists(hotplugactionsglobalfile):
            hotplugactionsconfig=import_from(hotplugactionsglobalfile)

        home=getoutput("echo $HOME")
        hotplugactionslocalfile=home+"/.kademar/"+hotplugactionsconffile
        if path.exists(hotplugactionslocalfile):
            #print localfile
            hotplugactionsconfig=import_from(hotplugactionslocalfile)

#Save config if checkbox is checked
    def saveconfig(self):
        global hotplugactionsconfig, hotplugactionslocalfile
        #print self.llistatreball
        programa=self.llistatreball[self.ui.listWidget.currentRow()][2]
        #print "Saved config", self.media, programa

#Posar aquí tots els self.tipus ordenats per igual, així amb el número de la "i" accedim al mateix per tots
#  Tenim el que s'ha d'escriure: self.nom del medi per comparar, programa pel medi (constant) i el programa real a utilitzar
#    Llest per posar a la config amb el for
        self.tipus=["cdrom", "dvddata", "dvd", "vcd", "audiocd", "pen", "dvb", "wlan", "eth", "fwcam"]
        nomtipus=["cdrom_prog", "dvddata_prog", "dvd_prog", "vcd_prog", "audiocd_prog", "pen_prog", "dvb_prog", "wlan_prog", "eth_prog", "fwcam_prog"]
        varprogs=[hotplugactionsconfig.cdrom_prog, hotplugactionsconfig.dvddata_prog, hotplugactionsconfig.dvd_prog, hotplugactionsconfig.vcd_prog, hotplugactionsconfig.audiocd_prog, hotplugactionsconfig.pen_prog, hotplugactionsconfig.dvb_prog, hotplugactionsconfig.wlan_prog, hotplugactionsconfig.eth_prog, hotplugactionsconfig.fwcam_prog]

#Save with all selections and the new one
        funcions_k.configdir()
        f=open(hotplugactionslocalfile, 'w')
        #Si el medi es el seleccionat (vol dir nova seleccio) escriu el que volem utilitzar
        for i in range(len(self.tipus)):
            if self.tipus[i]==self.media:
                f.writelines(nomtipus[i]+"=\""+programa+"\"\n")
            else:
        #Si no, deixem la resta de la config intacte
                f.writelines(nomtipus[i]+"=\""+varprogs[i]+"\"\n")
        f.close()





    def defineix_variables(self, blk, mnt, label, part=None):
    
        # $blk$   - /dev/sda1
        # $mnt$   - /media/usbdisk
        # $label$ - Pendrive
        # $part$  - sda1
    
        #######
        # CDROM
        #######
        self.cdrom=(
            ["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", self.tr("Open with konqueror"), "konqueror %s" %(mnt)],
            ["/usr/share/icons/oxygen/48x48/apps/k3b.png", self.tr("Copy with K3B"), "k3b --copycd %s" %(blk)],
            )
    
        #Icon
        self.cdromicon="/usr/share/icons/default.kde/48x48/devices/cdrom_unmount.png"
        self.cdromprop=self.tr("New CD media has been inserted %s" %(label)) 
        self.cdromname="CD-Rom"
    
        #######
        # DVD Data
        #######
        self.dvddata=(
            ["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", self.tr("Open with konqueror"), "konqueror %s" %(mnt)],
            ["/usr/share/icons/oxygen/48x48/apps/k3b.png", self.tr("Copy with K3B"), "k3b --copydvd %s" %(blk)],
            )
    
        #Icon
        self.dvddataicon="/usr/share/icons/default.kde/48x48/devices/dvd_unmount.png"
        self.dvddataprop=self.tr("New DVD media has been inserted %s" %(label))
        self.dvddataname="DVD-Rom"
    
        #######
        # DVD  Pelicula
        #######
        self.dvd=(
            ["/usr/share/pixmaps/vlc.png", self.tr("Play with VLC") ,"vlc dvd://%s" %(blk)],
            ["/usr/share/icons/hicolor/48x48/apps/kaffeine.png", self.tr("Play with Kaffeine"), "kaffeine DVD"],
            ["/usr/share/icons/hicolor/48x48/apps/k9copy.png", self.tr("Copy with K9Copy"), "k9copy --input %s" %(blk)],
            ["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", self.tr("Open with konqueror"), "konqueror %s" %(mnt)],
            ["/usr/share/icons/oxygen/48x48/apps/k3b.png", self.tr("Copy with K3B"), "k3b --copydvd %s" %(blk)],
            )
    
        self.dvdicon="/usr/share/icons/default.kde/48x48/devices/dvd_unmount.png"
        self.dvdprop=self.tr("New DVD Movie media has been inserted %s" %(label))
        self.dvdname="DVD-Rom"
    
        #######
        # Audio CD
        #######
        self.audiocd=(
            ["/usr/share/icons/hicolor/48x48/apps/kaffeine.png", "Play with kaffeine", "kaffeine AudioCD"],
            ["/usr/share/pixmaps/vlc.png", self.tr("Play with VLC") ,"vlc cdda://%s" %(blk)],
            ["/usr/share/pixmaps/kaudiocreator.xpm", self.tr("Extract with Kaudiocreator"), "kaudiocreator %s" %(blk)],
            ["/usr/share/pixmaps/gripicon.png", self.tr("Extract with Grip"), "grip --device=%s" %(blk)],
            ["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", self.tr("Extract with Media"), "konqueror media:/%s" %(blk)],
            ["/usr/share/icons/oxygen/48x48/apps/k3b.png", self.tr("Copy with K3B"), "k3b --copycd %s" %(blk)],
            ["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", self.tr("Open with konqueror"), "konqueror %s" %(mnt)],
            #["/usr/share/pixmaps/k3b.xpm", "Copy with K3B", "k3b --copydvd %s" %(blk)],
            )
    
        self.audiocdicon="/usr/share/icons/default.kde/48x48/devices/cdaudio_unmount.png"
        self.audiocdprop=self.tr("New CD Audio media has been inserted")
        self.audiocdname=self.tr("Audio CD")
    
        #######
        # Blank CD
        #######
        self.blankcd=(
            ["/usr/share/icons/oxygen/48x48/apps/k3b.png", self.tr("Burn with K3B"), "k3b"],
            )
    
        #Icon
        self.blankcdicon="/usr/share/icons/default.kde/48x48/devices/cdrom_unmount.png"
        self.blankcdprop=self.tr("New Blank CD media has been inserted") 
        self.blankcdname=self.tr("Blank CD-Rom")

        #######
        # PenDrive
        #######
        self.pen=(
            ["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", self.tr("Open with konqueror"), "konqueror %s" %(mnt)],
            #["/usr/share/pixmaps/k3b.xpm", "Copy with K3B", "k3b"],
            )
    
        #Icon
        self.penicon="/usr/share/icons/default.kde/48x48/devices/usbpendrive_unmount.png"
        self.penprop=self.tr("New Storage USB media has been inserted")
        self.penname=self.tr("USB Storage - %s" %(part))
    
        #######
        # DVB
        #######
        self.dvb=(
            ["/usr/share/icons/hicolor/48x48/apps/kaffeine.png", self.tr("Play with Kaffeine"), "kaffeine"],
            #["/usr/share/pixmaps/vlc.png", "Play with VLC" ,"vlc dvd://%s" %(blk)],
            #["/usr/share/icons/hicolor/48x48/apps/k9copy.png", "Copy with K9Copy", "k9copy --input %s" %(blk)],
            #["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", "Open with konqueror", "konqueror %s" %(mnt)],
            #["/usr/share/pixmaps/k3b.xpm", "Copy with K3B", "k3b --copydvd %s" %(blk)],
            )
    
        self.dvbicon="/usr/share/icons/default.kde/48x48/devices/tv.png"
        self.dvbprop=self.tr("New TDT device has been inserted")
        self.dvbname="TDT/DvB"
    
        #######
        # Wifi Wlan
        #######
        self.wlan=(
            ["/usr/share/icons/crystalsvg/48x48/apps/package_settings.png", self.tr("Configure with CADI"), "cadi --module=internet"],
            #["/usr/share/pixmaps/vlc.png", "Play with VLC" ,"vlc dvd://%s" %(blk)],
            #["/usr/share/icons/hicolor/48x48/apps/k9copy.png", "Copy with K9Copy", "k9copy --input %s" %(blk)],
            #["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", "Open with konqueror", "konqueror %s" %(mnt)],
            #["/usr/share/pixmaps/k3b.xpm", "Copy with K3B", "k3b --copydvd %s" %(blk)],
            )
    
        self.wlanicon="/usr/share/icons/hicolor/48x48/apps/kwifimanager.png"
        self.wlanprop=self.tr("New Wifi device has been inserted")
        self.wlanname=self.tr("Wireless Lan")
    
        #######
        # Wifi Wlan
        #######
        self.eth=(
            ["/usr/share/icons/crystalsvg/48x48/apps/package_settings.png", self.tr("Configure with CADI"), "cadi --module=internet"],
            #["/usr/share/pixmaps/vlc.png", "Play with VLC" ,"vlc dvd://%s" %(blk)],
            #["/usr/share/icons/hicolor/48x48/apps/k9copy.png", "Copy with K9Copy", "k9copy --input %s" %(blk)],
            #["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", "Open with konqueror", "konqueror %s" %(mnt)],
            #["/usr/share/pixmaps/k3b.xpm", "Copy with K3B", "k3b --copydvd %s" %(blk)],
            )
    
        self.ethicon="/usr/share/icons/default.kde/48x48/apps/kcmpci.png"
        self.ethprop=self.tr("New Ethernet wired device has been inserted")
        self.ethname=self.tr("Ethernet")
    
    
        #######
        # FireWire Cam
        #######
        self.fwcam=(
            ["/usr/share/pixmaps/kino.png", self.tr("Capture with Kino"), "kino"],
            ["/usr/share/icons/default.kde/48x48/apps/kdenlive.png", self.tr("Capture with Kdenlive"), "kdenlive"],
            #["/usr/share/pixmaps/vlc.png", "Play with VLC" ,"vlc dvd://%s" %(blk)],
            #["/usr/share/icons/hicolor/48x48/apps/k9copy.png", "Copy with K9Copy", "k9copy --input %s" %(blk)],
            #["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", "Open with konqueror", "konqueror %s" %(mnt)],
            #["/usr/share/pixmaps/k3b.xpm", "Copy with K3B", "k3b --copydvd %s" %(blk)],
            )

        self.fwcamicon="/usr/share/icons/default.kde/48x48/devices/camera_unmount.png"
        self.fwcamprop=self.tr("New Firewire Camera device has been inserted")
        self.fwcamname=self.tr("Firewire Camera")


        #######
        # NO Action
        #######
        self.nofer=["/usr/share/icons/oxygen/48x48/actions/button_cancel.png", self.tr("Do nothing"), ""]
















#Real import (load config) function, other only calls this one
def import_from(filename):
    import os, ihooks
    #"Import module from a named file"
    if  os.path.exists(filename):
        #sys.stderr.write( "WARNING: Cannot import file. "+filename )
    #else:
        loader = ihooks.BasicModuleLoader()
        path, file = os.path.split(filename)
        name, ext = os.path.splitext(file)
        m = loader.find_module_in_dir(name, path)
        if not m:
            raise ImportError, name
        m = loader.load_module(name, m)
        print "Loaded config "+filename
        return m


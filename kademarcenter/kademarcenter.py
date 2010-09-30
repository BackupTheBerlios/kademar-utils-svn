#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################
#         -=|  KADEMARCENTER  |=-            #
#             .Main Program.                #
#  ---------------------------------------  #
#     Author: Adonay Sanz Alsina            #
#     License: GPL 2.0 or higer             #
#     First Creation Date:  03-03-08        #
#  ---------------------------------------  #
#       Main  Center  of  kademar 5.x       #
#############################################

#import dbus, dbus.glib
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from PyQt4 import uic

from commands import getoutput
from os import getuid, path, system
# import global (installed) pyinotify
import os, commands, sys, ihooks

import funcions_k

#Usbtray
from usbtray import *

#Substitut de IvMan
from HardwareDetect import *

import scripts

from ui_kademarcenter import Ui_Form_kademarcenter as uikademarcenter

class kademarcenter(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        #Carrega el Gui
        self.ui = uikademarcenter()
        self.ui.setupUi(self)
        self.usbtrayclosed=True


####
# SOUND CONFIGURATION
####
        self.play="paplay" #Play Program
        self.soundconnect="/usr/share/sounds/KDE_Dialog_Appear.wav" #Sound USB connect
        self.sounddisconnect="/usr/share/sounds/KDE_Dialog_Disappear.wav"

####
# END SOUND CONFIGURATION
####

        self.connect(self.ui.b_settings, SIGNAL("clicked()"), self.showsettings)

        global notifier

        #Load configuration files
        self.load_kademarcenter_config()

####  UsbTray Module  ####
        self.usbtray = UsbTray()
        self.connect(self.usbtray, SIGNAL("showmsg"), self.showmsg)
##########################

####  IvMan Work  ####
        self.HardwareDetect = HardwareDetect()
        self.connect(self.HardwareDetect, SIGNAL("showmsg"), self.showmsg)
        self.connect(self.HardwareDetect, SIGNAL("regeneraformusbtray"), self.regeneraformusbtray)
        self.connect(self.HardwareDetect, SIGNAL("showusbtray"), self.showusbtray)
        self.HardwareDetect.start()
######################

#############
####  TRAY MODULE & ACTIONS
#############
        #### TRAY ####
        self.tray = QSystemTrayIcon(self)
        self.trayMenu = QMenu()
        #Definicio de items del menu (solament el que son, icona i descripcio)
        #self.action_quit = QAction(QIcon("/usr/share/kademar/icons/convertir.png"), self.tr('Quit'), self)
        self.action_mainwindow = QAction(QIcon("/usr/share/kademar/icons/endavant.png"), self.tr("Open kademar Center"), self)
        self.action_settings = QAction(QIcon("/usr/share/kademar/icons/configure.png"), self.tr("Configure"), self)


        #Afegit opcions de dalt, en el menu del context
        self.trayMenu.addAction(self.action_mainwindow)
        self.trayMenu.addAction(self.action_settings)

        #self.trayMenu.addAction(self.action_quit)

        #Connectar Accions al fer click a un del menu, la function que executa
        self.connect(self.action_mainwindow, SIGNAL("triggered()"), self.mainwindow)
        self.connect(self.action_settings, SIGNAL("triggered()"), self.showsettings)

        #self.connect(self.action_quit, SIGNAL("triggered()"), self.quitusbtray)

        #Quan fas clic al tray executa eventsdeltray (function)
        self.tray.connect( self.tray, SIGNAL( "activated(QSystemTrayIcon::ActivationReason)" ), self.eventsdeltray )

        self.trayIcon = QIcon("/usr/share/kademar/utils/kademarcenter/img/kademar.png")
        self.tray.setContextMenu(self.trayMenu)
        self.tray.setIcon(self.trayIcon)
        self.tray.setToolTip("kademar Center")
        self.tray.show()
#############
####  END  TRAY MODULE & ACTIONS
#############

#### INITIAL Services Start  ####
        #Initial start of services
        system(scripts.initial_service_start)
#################################

#### INITIAL DEVICE MOUNT ####
        #Initial mount of already plugged devices
        for udi in getoutput(scripts.initial_mount).split():
            print udi
            print "INITIAL DEVICE"
            system("touch /tmp/kademarcenter-inicial")
            self.HardwareDetect.processa_udi(udi, "add")
            system("rm -f /tmp/kademarcenter-inicial")
##############################

#############
####  PC INFO
#############

#Get PC info & put on info labels
        kernel=funcions_k.versiokernel()
        versiokademar=funcions_k.versiokademar()
        tipuskademar=funcions_k.tipuskademar()

        cpu=getoutput(""" grep 'cpu MHz' /proc/cpuinfo | awk '{ print $4 }' """)
        cpuinfo=getoutput(" cat /proc/cpuinfo | grep 'model name' ")
        ram=getoutput("""  grep 'MemTotal' /proc/meminfo | awk '{ print $2 }' """)
        hostname=getoutput("hostname -f")
        logedusers=getoutput("users")
        numlogedusers=len(logedusers.split(" "))

        self.ui.l_kdm.setText("kademar")
        self.ui.l_kern.setText(kernel)
        self.ui.l_ver.setText(versiokademar)
        self.ui.l_tipu.setText(tipuskademar)
        self.ui.l_cpu.setText(cpu.split("\n")[0]+" Mhz")
        self.ui.l_cpuinfo.setText(cpuinfo)
        self.ui.l_ram.setText(ram+" Mb")
        self.ui.l_host.setText(hostname)

        self.kademarstart()
        
        #if live-cd check if executing 32bit kademar on 64bit Machine
        if not funcions_k.instalat():
            check64bit=getoutput(""" for i in `grep cache_alignment /proc/cpuinfo | cut -d: -f2`; do echo $i; break; done """).strip()
            checkSsse3=getoutput("""  grep -i ssse3 /proc/cpuinfo 2>/dev/null """)
            if checkSsse3 and int(check64bit) >= 64:
                QMessageBox.critical(self, self.tr('Executing 32bit kademar on a 64bit Machine'), self.tr("Your computer is a 64bit capable, but you are executing a 32bit kademar.\nThis can cause performance issues and kademar experience could be reduced.\n\nFor live-cd use there's no problem, but if you want to install kademar on this machine, would be better if you download 64bit version from www.kademar.org"))


#############
####  END PC INFO
#############

        #Comprueba dispositivos USB y muestralo si eso
        self.regeneraformusbtray()

#Set visible/invisible main window
    def mainwindow(self):
        widget.setVisible( not widget.isVisible() )
#Correct method of quit
    def quitusbtray(self):
        app.quit()
        #self.usbtray.close()

#Click events on tray icon
    def eventsdeltray(self, arEvent):
       #Click boto esquerra
       if arEvent == self.tray.Trigger:
          #print "click esquerra"
          self.mainwindow()
       #if arEvent == self.tray.Context:
          #print "click dret"
          #self.regeneramenu()
          #widget.setVisible( not widget.isVisible() )
#Close event of window
    def closeEvent(self, event):
        event.ignore()
        self.mainwindow()
        #global pid,uid
        #self.quitusbtray()

#Show message on tray
    def showmsg(self,tipus, title, msg):
        #print "showmsg function", tipus, title, msg
        global kademarcenterconfig
        if kademarcenterconfig.warn_device_plugged_sound:
            if tipus=="info":
                system(self.play+" "+self.soundconnect+" &")
            elif tipus=="disconnect":
                system(self.play+" "+self.sounddisconnect+" &")
        else:
            print "disabled sound"


        if kademarcenterconfig.warn_device_plugged_ballon:
            self.tray.showMessage(title, msg)
        ##print "MISSATGE"+title+msg
        #system("sleep 1")

    def fifomsg(self, msg):
        #print msg
        print len(msg.split("-"))
        if len(msg.split("-"))>=2:
            self.showmsg("info",msg.split("-")[0],msg.split("-")[1])
        else:
            self.showmsg("info",msg.split("-")[0]," ")

    def showmsgupdate(self, num):
        print "UPDATES"
        print num
        self.showmsg("update",self.tr("Updade Available"),self.tr("Update available for %s packages." %(num)) )


    def regeneraformusbtray(self):
        a = self.usbtray.regeneraform()
        print a
        asplitted=a.split(",")
        #print "canvis usbtray regeneraform kademarcenter"
        #print usbtray.canvis
        #if usbtray.tray.isVisible():
        if asplitted[0] != "si":
            print "kademar center tanca usbtray"
            self.usbtray.tray.hide()
            
            #Warn to close usbtray only once
            if not self.usbtrayclosed:
                self.usbtrayclosed=True
                self.showmsg("info","UsbTray",self.tr("Closed, there's no remaining massive storage devices."))
        else:
            #Activate message "Warn to close usbtray only once"
            if self.usbtrayclosed:
                self.usbtrayclosed=False
            print "kademar center mostra usbtray"
            self.usbtray.tray.show()
            self.usbtray.regeneramenu()
        #else:
            #print "usbtray is not visible"
        #Hi ha hagut canvis i estan registrats
        if asplitted[1]=="si":
            if asplitted[2]=="rem": #Els canvis es de desconnectar dispositius
               self.HardwareDetect.umountdispo(asplitted[3]) #.split(" ")) #Dons els desmuntem

    def showusbtray(self):
        self.usbtray.tray.show()


    def showsettings(self):
        import Settings
        self.settings = Settings.Settings()
        #settings.settings.setParent(self)
        self.connect(self.settings, SIGNAL("end"), self.load_kademarcenter_config)
        self.settings.show()

#Function to start kademarstart if not desactivated
    def kademarstart(self):
        #global kademarstartconfig, kademarstartlocalfile
        kademarstartconffile="kademarstart_conf.py"
        kademarstartglobalfile="/usr/share/kademar/utils/kademarcenter/cfg/"+kademarstartconffile
        if path.exists(kademarstartglobalfile):
            kademarstartconfig=import_from(kademarstartglobalfile)

        home=getoutput("echo $HOME")
        kademarstartlocalfile=home+"/.kademar/"+kademarstartconffile
        if path.exists(kademarstartlocalfile):
            #print localfile
            kademarstartconfig=import_from(kademarstartlocalfile)

        if kademarstartconfig.autostart:
            #system("python /usr/share/kademar/utils/kademarstart/kademarstart.py &")
            from kademarstart_kademarcenter import kademarstart
            self.kademarstart = kademarstart()
            self.kademarstart.show()
            #self.kademarstart.start()
        else:
            print "kademarstart desctivated"


    def load_kademarcenter_config(self):
        global kademarcenterconfig
        kademarcenterconffile="kademarcenter_conf.py"
        kademarcenterglobalfile="/usr/share/kademar/utils/kademarcenter/cfg/"+kademarcenterconffile
        if path.exists(kademarcenterglobalfile):
            kademarcenterconfig=import_from(kademarcenterglobalfile)

        home=getoutput("echo $HOME")
        kademarcenterlocalfile=home+"/.kademar/"+kademarcenterconffile
        if path.exists(kademarcenterlocalfile):
            #print localfile
            kademarcenterconfig=import_from(kademarcenterlocalfile)
        #print dir(kademarcenterconfig)

#Load Configuration
def import_from(filename):
    "Import module from a named file"
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



#One instance of application"
if len(getoutput("ps x | grep -i kademarcenter | egrep python | grep -v grep | awk  ' { print $1 } ' ").split())>2:
   print "Already Running"
   #print getoutput("ps x | grep -i kademarcenter | egrep python")
   system("ps x | grep -i kademarcenter | egrep python > /tmp/KADEMARCENTER.LOG")
   sys.exit()
else:
   ##system("touch "+pid+""+uid)
   #If only one argument, execute it
   if len(sys.argv)<=1:
       pass
   #If the first argument is NOT session (kde autostart) execute it
   elif not sys.argv[1]=="-session":
       pass
   else:  #STOP
       print "Not starting, it's a KDE session autoload"
       sys.exit()

#create kademar folder
# and execute first-time configuration volumes
system('[ ! -e "/home/`whoami`/.kademar" ] && mkdir -p "/home/`whoami`/.kademar" && sh /usr/share/kademar/scripts/engegada/volums')

#open apps by groups
for i in getoutput("cat /proc/cmdline").split():
    if i == "startcsicappgroup1": #movilidad reducida en brazos y manos
        system("( xvkbd & ) ; ( easystroke & ) ; ( kmousetool & )")
    if i == "startcsicappgroup2": #personas mayores
        system("echo hola1")
    if i == "startcsicappgroup3": #Dificultades en la vision con resto visual util
        system("( easystroke & ) ; ( kmag & )")
    if i == "startcsicappgroup4": #Dificultades de aprendizaje
        system("echo hola2")

app = QApplication(sys.argv)
locale = QLocale.system().name()
qtTranslator = QTranslator()
if qtTranslator.load("/usr/share/kademar/utils/kademarcenter/tr/"+locale.split("_")[0]+".qm"):
    app.installTranslator(qtTranslator)
    print "Loaded "+locale
elif qtTranslator.load("/usr/share/kademar/utils/kademarcenter/tr/en.qm"):
    app.installTranslator(qtTranslator)
    print "Loaded "+locale

qtTranslatorQT = QTranslator()
qtTranslatorQT.load("qt_"+locale, "/usr/share/qt4/translations")
app.installTranslator(qtTranslatorQT)

widget = kademarcenter()
#widget.show()

app.exec_()

#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

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

from ui_cadi import Ui_FormCadi as Ui_Form

class cadi(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        global tipus
        self.avisa=True #avisa la sortida

        self.ui_cadi = Ui_Form()
        self.ui_cadi.setupUi(self)
        
        self.ui_cadi.label_3.setVisible(False)
        self.ui_cadi.label_11.setVisible(False)
        self.ui_cadi.b_root.setVisible(False)

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

        self.ui_cadi.l_kdm.setText("kademar")
        self.ui_cadi.l_kern.setText(kernel)
        self.ui_cadi.l_ver.setText(versiokademar)
        self.ui_cadi.l_tipu.setText(tipuskademar)
        self.ui_cadi.l_cpu.setText(cpu.split("\n")[0]+" Mhz")
        self.ui_cadi.l_cpuinfo.setText(cpuinfo)
        self.ui_cadi.l_ram.setText(ram+" Mb")
        self.ui_cadi.l_host.setText(hostname)
        
        if not funcions_k.instalat():
            for i in [ self.ui_cadi.b_users, self.ui_cadi.b_language ]:
                i.setVisible(0)

#############
####  END PC INFO
#############


        #Ponemos el splash
        self.ui_cadi.pages.setCurrentWidget(self.ui_cadi.tab_principal)

        self.path="/usr/share/kademar/utils/cadi"
#####  Signals & Slots  #####

        self.connect(self.ui_cadi.b_sortir, SIGNAL("clicked()"), self.close)

        self.connect(self.ui_cadi.b_root, SIGNAL("clicked()"), self.boto_root)


  #Software
        self.connect(self.ui_cadi.b_software, SIGNAL("clicked()"), self.boto_software)
  #Hardware
        self.connect(self.ui_cadi.b_hardware, SIGNAL("clicked()"), self.boto_hardware)
  #Xarxa
        self.connect(self.ui_cadi.b_xarxa, SIGNAL("clicked()"), self.boto_xarxa)
  #Sistema
        self.connect(self.ui_cadi.b_sistema, SIGNAL("clicked()"), self.boto_sistema)


#SOFTWARE
  #Boto Preferencies del sistema
        self.connect(self.ui_cadi.b_preferencies_sistema, SIGNAL("clicked()"), self.boto_preferencies)
  ##Synaptic
        self.connect(self.ui_cadi.b_synaptic, SIGNAL("clicked()"), self.boto_synaptic)

#HARDWARE
  #Impressores
        self.connect(self.ui_cadi.b_impressores, SIGNAL("clicked()"), self.boto_impressores)
  #Bluetooth
        self.connect(self.ui_cadi.b_bluetooth, SIGNAL("clicked()"), self.boto_bluetooth)
  #Teclats Multimedia
        self.connect(self.ui_cadi.b_teclats_multimedia, SIGNAL("clicked()"), self.boto_teclats_multimedia)
  #Kinfocenter
        self.connect(self.ui_cadi.b_kinfocenter, SIGNAL("clicked()"), self.boto_kinfocenter)
  #Ndiswrapper
        self.connect(self.ui_cadi.b_ndiswrapper, SIGNAL("clicked()"), self.boto_ndiswrapper)

#XARXA
  #Internet & Conectivity Module
        self.connect(self.ui_cadi.b_internet, SIGNAL("clicked()"), self.boto_internet)
  #Modem
        self.connect(self.ui_cadi.b_modem, SIGNAL("clicked()"), self.boto_modem)
  #ADSL/PPPoE
        self.connect(self.ui_cadi.b_pppoe, SIGNAL("clicked()"), self.boto_pppoe)
  #GPRS
        self.connect(self.ui_cadi.b_gprs, SIGNAL("clicked()"), self.boto_gprs)

#SYSTEM
    #Display
        self.connect(self.ui_cadi.b_display_configuration, SIGNAL("clicked()"), self.boto_display_configuration)
    #Users
        self.connect(self.ui_cadi.b_users, SIGNAL("clicked()"), self.boto_users)
  #Services
        self.connect(self.ui_cadi.b_services, SIGNAL("clicked()"), self.boto_services)
  #Language
        self.connect(self.ui_cadi.b_language, SIGNAL("clicked()"), self.boto_language)
  #Grub
        self.connect(self.ui_cadi.b_grub, SIGNAL("clicked()"), self.boto_grub)

#### END Signals & Slots ####

        self.modules=[ ("preferences", self.boto_preferencies), ("synaptic", self.boto_synaptic), ("printer", self.boto_impressores), ("bluetooth", self.boto_bluetooth), ("kboardmmedia", self.boto_teclats_multimedia), ("kinfocenter",self.boto_kinfocenter), ("ndiswrapper", self.boto_ndiswrapper), ("internet", self.boto_internet), ("modem", self.boto_modem), ("pppoe", self.boto_pppoe), ("gprs", self.boto_gprs), ("display",self.boto_display_configuration), ("users", self.boto_users), ("services", self.boto_services), ("language",self.boto_language), ("grub", self.boto_grub) ]
        
        self.tabs=[("software", self.boto_software), ("hardware", self.boto_hardware), ("net", self.boto_xarxa), ("system",self.boto_sistema)]

	a=b=""
        #Open a module if you have passed as a parameter
        for i in sys.argv[1:]:
            if i.find("--module=")<>-1:   # --module=wifi
                module=i.split("=")[1]  # get only wifi
                for i in self.modules:   #search and open it
                    if i[0].find(module)<>-1:
                        i[1]()
            elif i.find("--tab=")<>-1:   # --tab=hadware
                tab=i.split("=")[1]  # get only hardware
                for i in self.tabs:  #search and open it
                    if i[0].find(tab)<>-1:
                        i[1]()
            elif i.find("--help")<>-1:
                print
                print 
                print "CADI: The configurator tool"
                print "---------------------------"
                print
                print "* To open a tab, call with --tab=xxx  param"
                print " - Tabs Availables:"
                for i in self.tabs:
                    b=b+" "+i[0]
                print b
                print
                print "* To open a module, call with --module=xxx  param"
                print " - Modules Availables:"
                for i in self.modules:
                    a=a+" "+i[0]
                print a
                print
                #self.avisa=False

#######    Page Changer    #######
        #def changepage(self, current, previous):
        #if not current:
            #current = previous

        #self.ui.pageWidget.setCurrentIndex(self.ui.listWidget.row(current))
    def boto_hardware(self):
        self.ui_cadi.pages.setCurrentWidget(self.ui_cadi.tab_hardware)
        self.disableButton(self.ui_cadi.b_hardware)
    def boto_software(self):
        self.ui_cadi.pages.setCurrentWidget(self.ui_cadi.tab_software)
        self.disableButton(self.ui_cadi.b_software)
    def boto_xarxa(self):
        self.ui_cadi.pages.setCurrentWidget(self.ui_cadi.tab_xarxa)
        self.disableButton(self.ui_cadi.b_xarxa)
    def boto_sistema(self):
        self.ui_cadi.pages.setCurrentWidget(self.ui_cadi.tab_sistema)
        self.disableButton(self.ui_cadi.b_sistema)

    def disableButton(self, boto):
        for i in self.ui_cadi.b_software, self.ui_cadi.b_hardware, self.ui_cadi.b_sistema, self.ui_cadi.b_xarxa:
           i.setEnabled(1)
        boto.setEnabled(0)
######  END  Page Changer   ######


  #When close Event is active, ask if want to exit
    def closeEvent(self, event):
        if self.avisa:
            reply = QMessageBox.question(self, 'Message',
                self.tr("Are you sure to quit?"), QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

#SOFTWARE
  #Synaptic
    def boto_synaptic(self):
        self.a=QProcess()
        self.a.start("synaptic")

  #Preferències de sistema
    def boto_preferencies(self):
        from preferencies import panelPreferencies
        self.preferencies = panelPreferencies()
        self.preferencies.setParent(self)
        self.preferencies.show()

#HARDWARE
  #Impressores
    def boto_impressores(self):
        self.b=QProcess()
        self.b.start("sh scripts/cadi-cupsconfig-kde")

  #Kinfocenter
    def boto_kinfocenter(self):
        self.c=QProcess()
        self.c.start("kinfocenter")

  #Bluetooth
    def boto_bluetooth(self):
        from bluetooth import panelBluetooth
        self.bluetooth = panelBluetooth()
        self.bluetooth.setParent(self)
        self.bluetooth.show()

  #Teclats multimedia
    def boto_teclats_multimedia(self):
        from teclats_multimedia import panelTeclatsMultimedia
        self.teclats_multimedia = panelTeclatsMultimedia()
        self.teclats_multimedia.setParent(self)
        self.teclats_multimedia.show()

  #Ndiswrapper
    def boto_ndiswrapper(self):
        self.a=QProcess()
        self.a.start("ndisgtk")
#XARXA
  #modem
    def boto_modem(self):
        self.m = QProcess()
        self.m.start("kppp")

  #Internet and Connectivity - wifi ethernet diagnostic
    def boto_internet(self):
        from internet import panelInternet
        self.internet = panelInternet()
        self.internet.setParent(self)
        self.internet.show()
  #ADSL/PPPoe
    def boto_pppoe(self):
        from pppoe import panelPPPoE
        self.pppoe = panelPPPoE()
        self.pppoe.setParent(self)
        self.pppoe.show()
  #GPRS
    def boto_gprs(self):
        self.g = QProcess()
        self.g.start("xterm -e sh scripts/gprsconnect &")

#Sistema
  #Display Configuration
    def boto_display_configuration(self):
        from display import panelDisplay
        self.display = panelDisplay()
        self.display.setParent(self)
        self.display.show()

  #Manage Users
    def boto_users(self):
        from users import panelUsers
        self.users = panelUsers()
        self.users.setParent(self)
        self.users.show()

  #Services
    def boto_services(self):
        from services import panelServices
        self.services = panelServices()
        self.services.setParent(self)
        self.services.show()

  #Idioma
    def boto_language(self):
        from language import panelLanguage
        self.language = panelLanguage()
        self.language.setParent(self)
        self.language.show()

  #GRUB
    def boto_grub(self):
      #get live-cd or installed form
        if funcions_k.installed():
            from grub_installed import panelGrub
        else:
            from grub_livecd import panelGrub
        
        self.grub = panelGrub()
        self.grub.setParent(self)
        self.grub.show()

    #def posa_permisos_del usuari()
        #si root

        #si usuari normal

    def boto_root(self):
        system("nohup kdesu -d --noignorebutton -t -n python cadi.py &")
        self.avisa=False
        self.close()

app = QApplication(sys.argv)
locale = QLocale.system().name()
qtTranslator = QTranslator()
if qtTranslator.load("/usr/share/kademar/utils/cadi/tr/"+locale.split("_")[0]+".qm"):
    app.installTranslator(qtTranslator)
    print "Loaded "+locale
elif qtTranslator.load("/usr/share/kademar/utils/cadi/tr/en.qm"):
    app.installTranslator(qtTranslator)
    print "Loaded "+locale
    
qtTranslatorQT = QTranslator()
qtTranslatorQT.load("qt_"+locale, "/usr/share/qt4/translations")
app.installTranslator(qtTranslatorQT)

cadi = cadi()
cadi.show()
app.exec_()

#if len(getoutput("ps x | grep -i cadi | egrep python | grep -v grep | awk  ' { print $1 } ' ").split())>2:
   #print "Already Running"
   #print getoutput("ps x | grep -i cadi | egrep python")
   #system("ps x | grep -i cadi | egrep python > /tmp/KADEMARCENTER.LOG")
#else:
   ##system("touch "+pid+""+uid)
   #app = QApplication(sys.argv)
   #locale = QLocale.system().name()
   #qtTranslator = QTranslator()
   #if qtTranslator.load("/usr/share/kademar/utils/cadi/tr/"+locale.split("_")[0]+".qm"):
       #app.installTranslator(qtTranslator)
       #print "Loaded "+locale
   #elif qtTranslator.load("/usr/share/kademar/utils/cadi/tr/en.qm"):
       #app.installTranslator(qtTranslator)
       #print "Loaded "+locale

   ##from accions import *
   #cadi = cadi()
   #cadi.show()
   #app.exec_()

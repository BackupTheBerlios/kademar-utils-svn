#!/usr/bin/python
#-*- coding: iso-8859-15 -*-
import funcions_k
import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from PyQt4 import uic
from commands import getoutput
from os import system, path #, getuid   #Used on PID/GID file. Not used -> managed by kademarcenter.

import dbus
import scripts
#import dbus.glib 
#import sys
import commands

from ui_usbtray import Ui_Form_usbtray as uiusbtray



class UsbTray(QWidget):
    def __init__(self):


     #Detect the live-cd start device - no disable possible umount
    	if not funcions_k.instalat():
            self.liveDataDev=getoutput("cat /mnt/live/data")
        else:
            self.liveDataDev=""

        QWidget.__init__(self)
        #uic.loadUi("usbtray.ui", self)  #Load  GUI
        self.ui_usbtray = uiusbtray()
        self.ui_usbtray.setupUi(self)
#GLOBAL VARIABLES - Handlers
#### FORM PRINCIPAL ###
#### Signals & Slots ####
        self.connect(self.ui_usbtray.boto_desconnecta, SIGNAL("clicked()"), self.desconectausb)
        self.connect(self.ui_usbtray.boto_sortir, SIGNAL("clicked()"), self.botosortir)

#A la que es canvia (selecciona) un item a la list, enable el boto de desconecta
        self.connect(self.ui_usbtray.listWidget, SIGNAL("itemSelectionChanged()"), self.enablebotodesconecta)

#Si se li fa dos clics al item de la llista, procesal com si apretes el boto de desconnecta
        self.connect(self.ui_usbtray.listWidget, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.desconectausb)
#### END SIGNAL & SLOTS ####


        global retry, cancel
        retry=self.tr("Retry Extraction")
        cancel=self.tr("Cancel")

#### TRAY ####
        #global tray
    #Definicio Inicial de Tray i el seu menu
        self.tray = QSystemTrayIcon(self)
        self.trayMenu = QMenu()
    #Definicio de items del menu (solament el que son, icona i descripcio)
        self.action_quit = QAction(QIcon("/usr/kademar/icons/convertir.png"), self.tr("Surt"), self)
        self.action_mainwindow = QAction(QIcon("/usr/share/icons/default.kde/22x22/devices/usbpendrive_unmount.png"), self.tr("Obre Gestor d'USB"), self)

    #Afegit opcions de dalt, en el menu del context
    #self.trayMenu.addAction(self.action_about)
    #self.trayMenu.addSeparator()
        self.trayMenu.addAction(self.action_mainwindow)
    #self.trayMenu.addSeparator()
    #self.trayMenu.addAction(self.action_quit)
    #self.trayMenu.clear()  #Neteja menu

    #Connectar Accions al fer click a un del menu, la function que executa
        self.connect(self.action_mainwindow, SIGNAL("triggered()"), self.mainwindow)
        self.connect(self.action_quit, SIGNAL("triggered()"), self.quitusbtray)

    #Quan fas clic esq/dret al tray executa eventsdeltray (function)
        self.tray.connect( self.tray, SIGNAL( "activated(QSystemTrayIcon::ActivationReason)" ), self.eventsdeltray )


        self.trayIcon = QIcon("/usr/share/icons/default.kde/22x22/devices/usbpendrive_unmount.png")
        self.tray.setContextMenu(self.trayMenu)
        self.tray.setIcon(self.trayIcon)
        self.tray.setToolTip("UsbTray") #Tool Hint

#Emplena el listwidget amb els usb
        self.regeneraform()

        self.regeneramenu() #Creem el menu contextual
#### FI TRAY ####
    def quitusbtray(self):
        #global pid,uid
        #system("rm -f "+pid+""+str(uid))
        #app.quit()
        #usbtray.close()
        self.tray.hide() #Estem en mode junts amb kademarcenter, solament amaga, no apaga


#Clicks en el Tray  trigger = click esquerra  .  context = click dret
    def eventsdeltray(self, arEvent):
       #Click boto esquerra
       if arEvent == self.tray.Trigger:
           #print "click esquerra"
           self.regeneraform()
        #Left click, troggle visible mode
           self.mainwindow()
       if arEvent == self.tray.Context:
           #print "click dret"
        #Right click, re-create contextual menu
           self.regeneramenu()

  #Main Function
  #Function to fill  listWidget of available USB devices
    def regeneraform(self):
        print "regenerant"

  #Load  OLD  device list (to compare later if it changes)
        antics=""
        for i in range(self.ui_usbtray.listWidget.count()):
            usb=str(self.ui_usbtray.listWidget.item(i).text())
            usbnum=len(usb.split("-"))-1
            antics+=(usb.split("-")[usbnum])

  #Clear to fill with new device list
        self.ui_usbtray.listWidget.clear()

# get a connection to the system bus
        bus = dbus.SystemBus ()

# get a HAL object and an interface to HAL to make function calls
        self.bus = dbus.SystemBus()
        self.hal_manager_obj = self.bus.get_object("org.freedesktop.Hal", 
                                                   "/org/freedesktop/Hal/Manager")
        self.hal_manager = dbus.Interface(self.hal_manager_obj, "org.freedesktop.Hal.Manager")

    #Get all Storage (volume) udis
        udis = self.hal_manager.FindDeviceByCapability ('storage')

        for udi in udis:  #Process these udi
          #Set object and device = udi
            obj = self.bus.get_object("org.freedesktop.Hal", udi)
            dev = dbus.Interface(obj, 'org.freedesktop.Hal.Device')
          #If it's USB
            if str(dev.GetProperty("storage.bus"))=="usb":
               #print "yes"
               #print str(dev.GetProperty("block.is_volume"))
          #And has volumes available
               if not dev.GetProperty("block.is_volume"):
                   #print "yes2"
          #Get device block
                   block=str(dev.GetProperty("block.device"))[5:] 
          #If it's mounted
                   comproba=""
                   comproba=getoutput("grep /dev/"+block+" /proc/mounts 2>/dev/null")
                 #if it's the livecd boot device, don't appear in the list -> no UMOUNT possible  ^_^  :-[
                   if not comproba=="" and not block==self.liveDataDev[:3]:
          #Find label of /dev/sd?
          #And it partitions  sd?1, sd?2, sd?3
                       udis2= self.hal_manager.FindDeviceStringMatch ("info.parent", udi)
                       label=""
                       for udi2 in udis2:
                           #print "udi2 parent"
                           #print udi2
                           obj2 = self.bus.get_object("org.freedesktop.Hal", udi2)
                           dev2 = dbus.Interface(obj2, 'org.freedesktop.Hal.Device')
                           label=dev2.GetProperty("volume.label")
          #Use the first label found
                           if label<>"":
                               label=label+" - "
                               break
          #Get product & vendor
                       product=str(dev.GetProperty("info.product"))
                       vendor=str(dev.GetProperty("info.vendor"))
                       i="%s %s %s - %s" %(label, product, vendor, block)
                       
          #Add to listWidget
                       self.ui_usbtray.listWidget.addItem(i.strip())

  #Get new devices 
        nous=""
        canvis=""
        for i in range(self.ui_usbtray.listWidget.count()):
            usb=str(self.ui_usbtray.listWidget.item(i).text())
            usbnum=len(usb.split("-"))-1
            nous+=(usb.split("-")[usbnum])

        #print "ANTICS"
        #print antics
        #print "NOUS"
        #print nous
  #Check if Devices added or removed
        if len(antics)>len(nous):
            #print "prioritari antics"
            canvis="rem,"
            for i in antics.split(" "):
                if nous.find(i)==-1:
                    canvis+=i+" "
        elif len(antics)<len(nous):
            canvis="add,"
            #print "prioritari nous"
            for i in nous.split(" "):
                if antics.find(i)==-1:
                    canvis+=i+" "
        #else:
            #print "no hi ha prioritari"
  #Print Changes
	#print "CANVIS"
	#print canvis

  #If there's no device, close it
        if self.ui_usbtray.listWidget.count()==0:
            print "No hay dispsitivos USB de almacenaje montados."
            self.setVisible(0)
            self.tray.hide()
  #Return Changes to kademarcenter
            if canvis<>"":
                return "no,si,"+canvis
            else:
                return "no,no"

            #self.tray.hide()
            #self.quitusbtray()
        else:
            #self.tray.show()
            print "Hay dispositivos USB de almacenaje montados."
  #Return Changes to kademarcenter
            if canvis<>"":
                return "si,si,"+canvis
            else:
                return "si,no"

  #Re create contextual menu
    def regeneramenu(self):
        usb=""
        #print "Regenerant menu"
  #Run mainfunction to know how many devices
        self.regeneraform()

        self.trayMenu.clear()  #Neteja menu
        self.trayMenu.addAction(self.action_mainwindow)  #Add open Main Window Option to menu
        self.trayMenu.addSeparator()  #Add separator to menu

  #Fill contextualmenu with the same information of USB devices
        for i in range(self.ui_usbtray.listWidget.count()):
            usb=str(self.ui_usbtray.listWidget.item(i).text())
            #print i
            #print usb
            self.action = QAction(QIcon("/usr/share/kademar/icons/desconfigura.png"), self.tr('Disconnect ')+" "+usb, self)
            self.trayMenu.addAction(self.action)

            self.connect(self.action, SIGNAL("triggered()"), self.acciodesconectausb)  #When clicks on the menu
            self.connect(self.action, SIGNAL("hovered()"), self.hoveredaccio)  #Hover menu selecction (to process later when click)

  #Add close option - now managed by kademarcenter
        #self.trayMenu.addSeparator()
        #self.trayMenu.addAction(self.action_quit)

#Enable el boto de desconnect al canviar el item de la listWidget
    def enablebotodesconecta(self):
        self.ui_usbtray.boto_desconnecta.setEnabled(1)
        #print "conectat"

    def botosortir(self):
        self.showmsg(self.tr("Ejecución"), self.tr("UsbTray sigue funcionando aquí"))
        self.mainwindow()

  #Troggle main window visibility
    def mainwindow(self):
        self.setVisible( not self.isVisible() )
        #self.showmsg(self.tr("Ejecución"), self.tr("UsbTray sigue funcionando\n aquí"))

  #Set active action when hover - Contextual menu
    def hoveredaccio(self):
        global accioseleccionada
        accioseleccionada=self.trayMenu.activeAction().text()

  #When click on disconnect action of conxtextual menu (previous hover contextual menu)
    def acciodesconectausb(self):
        global accioseleccionada
  #Check and find the number of the row on listWidget
        for i in range(self.ui_usbtray.listWidget.count()):
            usb=str(self.ui_usbtray.listWidget.item(i).text())
  #Language support, but always the usbname will be the same, if match -> it's the correct option
            if str(accioseleccionada).find(usb)>=0:
  #We have the number of the row
                num=i
                break
  #Set current Row, necessary by desconectausb()
        self.ui_usbtray.listWidget.setCurrentRow(i)
        self.desconectausb()

  #Disconnect USB Main Function
    def desconectausb(self):
        global retry, cancel
        usb = str(self.ui_usbtray.listWidget.currentItem().text())
        print "desconnectant usb:"
  #Get USB block device (split name and block)
        numbusblock=len(usb.split("-"))-1
        usbblock=usb.split("-")[numbusblock]
        print usb+" "+usbblock
        error=0
        nextstep=1
  #Execute the disconnect_usb helper
        if getoutput(scripts.umount+" "+usbblock)[-5:]=="ERROR":
        #var=commands.getoutput("grep "+usbblock+" /proc/mounts 2>/dev/null")
        #if var:
            error=1
            nextstep=0
            acaba=0
            while not acaba:
                self.setVisible(1)
                self.a=MessageFailedMount(usb)

                self.a.exec_()

                response = self.a.clickedButton().text()
                if response == retry:
                    print "retrying umount"
                    if not getoutput(scripts.umount+" "+usbblock)[-5:]=="ERROR":
                        error=0
                        nextstep=1
                elif response == cancel:
                    #print "cancel"
                    error=0
                    nextstep=0
                else:
                    #print "force umount"
                    getoutput(scripts.umount_forced+" "+usbblock)
                    error=0
                    nextstep=1

                if not error:
                    acaba=1
                    #print "acaba", acaba

  #Show Tray Message
        if nextstep:
            self.showmsg(self.tr("USB Desconectado"),self.tr("Se ha desconectado %s satisfactoriamente." %(usb)), "disconnect")
  #Disable Disconnect Button on the gui
            self.ui_usbtray.boto_desconnecta.setEnabled(0)
  #Check now USB devices available
            self.regeneraform()
            self.regeneramenu()
        #self.setVisible(False)
        #self.regeneraform()
        #self.regeneramenu()


  #When close Event is active, really ignore it, minimize window and show a tray message
    def closeEvent(self, event):
     #reply = QMessageBox.question(self, 'Message',
         #"Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

     #if reply == QMessageBox.Yes:
         #event.accept()
     #else:
         #event.ignore()
        event.ignore()
        self.mainwindow()
        self.showmsg(self.tr("UsbTray"), self.tr("UsbTray sigue funcionando aquí"))
     #self.tray.hide()

  #Tray Message Main function
    def showmsg(self, title, msg, tipus=""):
        #self.tray.showMessage(title, msg)
        self.emit(SIGNAL("showmsg"), tipus, title, msg)


#ohw msg
class MessageFailedMount(QMessageBox):
    def __init__(self, usb, parent=None):
        QMessageBox.__init__(self, parent)
        global retry, cancel
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle(self.tr("Error on Disconnect"))
        self.addButton(retry, QMessageBox.AcceptRole)
        self.addButton(self.tr("Force Umount (Not Recommended)"), QMessageBox.AcceptRole)
        self.addButton(cancel, QMessageBox.AcceptRole)
        self.setText(self.tr("Have ocurred an error trying to umount the USB device.\n     %s \nBe sure any program accessing it." %(usb)))
	
    def closeEvent(self, event):
        event.ignore()
        self.hide()

#usbtray = usbtray()  #Instance the main class

#####
# To run standalone. Not used -> managed by kademarcenter
####
#One instance of application"
#global pid,uid
#pid="/tmp/kademar-pyqt-usbtray-running-"
#uid=str(getuid())
#print uid
#if path.exists(pid+""+uid):
   #print "Already Running"
#else:
   #system("touch "+pid+""+uid)
   #app = QApplication(sys.argv)
#usbtray = usbtray()  #Instance the main class
   ##widget.show()
   #app.exec_()


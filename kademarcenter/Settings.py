#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from PyQt4 import uic

from commands import getoutput
#from os import getid
from os import path
from os import system

#import funcions_k

from ui_settings import Ui_Form_settings as Ui_Form

class Settings(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        global kademarcenterconfig

        global tipus
        #uic.loadui("ui/cadi.ui", self)
        self.load_kademarcenter_config()

        #print dir(kademarcenterconfig)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pages.setCurrentWidget(self.ui.p_general)
        self.putconfigurationsettings()

#####  Signals & Slots  #####
        #self.connect(self.ui.listWidget, 
                     #SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.changepage)
        self.connect(self.ui.b_general, 
                     SIGNAL("clicked()"), self.boto_general)
        self.connect(self.ui.b_usb, 
                     SIGNAL("clicked()"), self.boto_usb)
        self.connect(self.ui.b_updates, 
                     SIGNAL("clicked()"), self.boto_updates)
        self.connect(self.ui.b_diskcleanup, 
                     SIGNAL("clicked()"), self.boto_diskcleanup)

        for i in self.ui.b_general, self.ui.b_usb, self.ui.b_updates, self.ui.b_diskcleanup:
            i.setVisible(0)

        self.ui.tableWidget.verticalHeader().setVisible(0)
        self.ui.tableWidget.horizontalHeader().setVisible(0)
	
        self.ui.cb_hotplugactions.setChecked(self.kademarcenterconfig.actions_device_plugged)
        self.ui.cb_balloon.setChecked(self.kademarcenterconfig.warn_device_plugged_ballon)
        self.ui.cb_sound.setChecked(self.kademarcenterconfig.warn_device_plugged_sound)

    def boto_general(self):
        self.ui.pages.setCurrentWidget(self.ui.p_general)
    def boto_usb(self):
        self.ui.pages.setCurrentWidget(self.ui.p_usb)
    def boto_updates(self):
        self.ui.pages.setCurrentWidget(self.ui.p_updates)
    def boto_diskcleanup(self):
        self.ui.pages.setCurrentWidget(self.ui.p_diskcleanup)

#### END Signals & Slots ####



  #When close Event is active, ask if want to exit
    def closeEvent(self, event):
        reply = QMessageBox.question(self, self.tr('Exit'),
            self.tr("Do you want to save settings?"), QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            #event.accept()
            #self.close()
            event.ignore()
            self.savesettingstofile()
            self.hide()
        else:
            event.ignore()
            self.hide()
        self.emit(SIGNAL("end"))


    def putconfigurationsettings(self):
        global kademarcenterconfig
        #GENERAL

        #UPDATES
        self.ui.rb_autoupdate.setChecked(1)
        self.ui.rb_only_warn.setChecked(0)
        self.ui.rb_no_update.setChecked(0)
        #self.ui.sb_update_hours
        #USB

        #DISC CLEAN
	
        pass

    def savesettingstofile(self):
        print "saving settings"
        self.options=["actions_device_plugged", "warn_device_plugged_ballon", "warn_device_plugged_sound"]
        self.cboptions=[self.ui.cb_hotplugactions, self.ui.cb_balloon, self.ui.cb_sound]
        

#Save with all selections and the new one
        import funcions_k
        funcions_k.configdir()
        f=open(self.kademarcenterlocalfile, 'w')
        #Si el medi es el seleccionat (vol dir nova seleccio) escriu el que volem utilitzar
        for i in range(len(self.options)):
            f.writelines(self.options[i]+"="+str(self.cboptions[i].isChecked())+"\n")
        f.close()
	
	

    def load_kademarcenter_config(self):
        #global kademarcenterconfig
        self.kademarcenterconffile="kademarcenter_conf.py"
        self.kademarcenterglobalfile="/usr/share/kademar/utils/kademarcenter/cfg/"+self.kademarcenterconffile
        if path.exists(self.kademarcenterglobalfile):
            self.kademarcenterconfig=import_from(self.kademarcenterglobalfile)

        home=getoutput("echo $HOME")
        self.kademarcenterlocalfile=home+"/.kademar/"+self.kademarcenterconffile
        if path.exists(self.kademarcenterlocalfile):
            #print localfile
            self.kademarcenterconfig=import_from(self.kademarcenterlocalfile)
        #print dir(kademarcenterconfig)

#Load Configuration
def import_from(filename):
    import os, commands, sys, ihooks

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

#app = QApplication(sys.argv)
#settings = settings()
#settings.show()
#app.exec_()

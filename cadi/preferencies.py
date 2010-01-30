#!/usr/bin/python
#-*- coding: iso-8859-15 -*-

#
# configure USB sync/async mode
# support if you have deleted mount_mode on config options
#

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from commands import getoutput
from os import path, system

#import funcions_k

from ui_preferencies_sistema import Ui_FormPreferencies as Ui_Form

class panelPreferencies(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        global tipus
        self.ui = Ui_Form()
        self.ui.setupUi(self)

#####  SIGNAL & SLOTS  #####
        self.connect(self.ui.b_sortir, SIGNAL("clicked()"), self.boto_sortir)
        self.connect(self.ui.b_SaX, SIGNAL("clicked()"), self.SaveAndExit)

#### END SIGNAL & SLOTS ####

        self.ui.b_SaX.setEnabled(False)


        f=open('/usr/share/kademar/config','r')
        llista=f.readlines()
        f.close()
        self.found=False
        for i in llista:
            # al repassar linia a linia el fitxer quan troba mount_mode=...
            if i.find("mount_mode=")<>-1:
                linea=i.split('=')
                # si despres de separar en dos la linea per mitja del =
                # troba -a vol dir sincrona està a false en el fitxer de config
                if linea[1].find('-s')<>-1:
                    self.found=True
                    self.ui.rb_sync.setChecked(True)
                    self.ui.rb_async.setChecked(False)
                else:
                    self.found=True
                    self.ui.rb_async.setChecked(True)
                    self.ui.rb_sync.setChecked(False)
        if not self.found:
            self.ui.rb_async.setChecked(True)
            self.ui.rb_sync.setChecked(False)

                #print linea
                #print linea[1].strip()
                # i si no troba -a vol dir que ja està a true, es deixa igual
        #print 'sincrona  =',self.ui.ch_sync.isChecked()

        self.connect(self.ui.rb_sync, SIGNAL("toggled (bool)"), self.enableSaX)
        self.connect(self.ui.rb_async, SIGNAL("toggled (bool)"), self.enableSaX)

    def enableSaX(self):
        self.ui.b_SaX.setEnabled(True)

    def boto_sortir(self):
        self.close()

    def SaveAndExit(self):
        #posar aqui tot el que s'hagi de fer per desar per 
        #defecte la opcio de Sync o no Sync
        f=open('/usr/share/kademar/config','r')
        llista=f.readlines()
        f.close()
        # i ara gravem la opció que toca al fitxer config
        f=open('/usr/share/kademar/config','w')
        for i in llista:
            # al repassar linia a linia el fitxer quan troba mount_mode=...
            if i.find("mount_mode=")<>-1:
                # si el checkbox de sync està marcat, vol dir mode sincrone
                if self.ui.rb_sync.isChecked():
                    linea='mount_mode="-s"\n'
                else:
                    # si no, vol dir mode asincrone
                    linea='mount_mode=""\n'
                f.write(linea)
            else:
                f.write(i)

        if not self.found:
            linea='#Options: Sync (-s) / Async (-a) (default: sync)\n'
            f.write(linea)
            if self.ui.rb_sync.isChecked():
                linea='mount_mode="-s"\n'
            else:
                # si no, vol dir mode asincrone
                linea='mount_mode=""\n'
            f.write(linea)

        f.close()
        self.close()


#app = QApplication(sys.argv)
#preferencies = preferencies()
#preferencies.show()
#app.exec_()
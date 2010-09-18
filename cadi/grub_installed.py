#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from commands import getoutput
from os import path, system

#import funcions_k

from ui_grub_installed import Ui_FormGrub as Ui_Form

class panelGrub(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        global tipus
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.hddIcon="/usr/share/kademar/utils/cadi/img/hdd_unmount.png"
        #self.ui.b_SaX.setEnabled(False)

#####  SIGNAL & SLOTS  #####
        self.connect(self.ui.b_sortir, SIGNAL("clicked()"), self.close)
        self.connect(self.ui.b_expert, SIGNAL("clicked()"), self.boto_expert)
        self.connect(self.ui.b_SaX, SIGNAL("clicked()"), self.SaveAndExit)
        self.connect(self.ui.ch_timeout, SIGNAL("stateChanged (int)"), self.setTimeoutOptions)

        #self.connect(self.ui.le_pin, SIGNAL("textEdited (const QString&)"), self.enableSaX)
        #self.connect(self.ui.b_restore, SIGNAL("clicked()"), self.boto_restore)
        #self.connect(self.ui.listWidget , SIGNAL(" currentRowChanged (int)"), self.enableButtons)

#### END SIGNAL & SLOTS ####


        self.grub="/boot/grub/menu.lst"
        
        temps=""
        f=open(self.grub,'r')
        lineas=f.readlines()
        f.close()
        noms_nous=[]
        noms_vells=[]
        for i in lineas:
            if i.strip()<>'': 
                if i.strip()[0]<>'#':
                    if i[:7].lower()=='default':
                        seleccionat=int(i.split()[1].strip())
                        self.ui.ch_timeout.setChecked(1)
                    #if i.lower().find('timeout')<>-1:
                    if i[:7].lower()=='timeout':
                        temps=int(i.split()[1])
                        self.ui.sb_timeout.setValue(temps)
                    if i.strip().find('title')<>-1:
                        self.ui.cb_boot.addItem(i.replace('title','').strip())
                        noms_nous.append(i.replace('title','').strip())
                        noms_vells.append(i)
        if not temps:
            self.ui.sb_timeout.setValue(0)
            self.ui.ch_timeout.setChecked(0)
        self.ui.cb_boot.setCurrentIndex(seleccionat)


        self.connect(self.ui.sb_timeout, SIGNAL("valueChanged (int)"), self.enableSaX)
        self.connect(self.ui.cb_boot, SIGNAL("currentIndexChanged (int)"), self.enableSaX)
        self.connect(self.ui.ch_timeout, SIGNAL("stateChanged (int)"), self.enableSaX)

    def SaveAndExit(self):
        f=open(self.grub,'r')
        lineas=f.readlines()
        f.close()
        f=open(self.grub,'w')  
        foundTimeout=False
        for i in lineas:
            lin=i
            if i[:7].lower()=='timeout' or i[:8].lower()=='#timeout':
                foundTimeout=True
                if self.ui.ch_timeout.isChecked():
                    lin='timeout '+str(self.ui.sb_timeout.value())+'\n'
                else:
                    lin='#timeout \n'
            if i[:7].lower()=='default':
                lin='default '+str(self.ui.cb_boot.currentIndex())+'\n'
            
            #for n in canvis:
                #if n.split('caracter_de_separacio')[0].strip()==i.strip():
                    #lin=n.split('caracter_de_separacio')[1]+'\n'
                    #break
            # i escric els canvis que hi hagin
            f.write(lin)
        if not foundTimeout:
            if self.ui.ch_timeout.isChecked():
                lin='timeout '+str(self.ui.sb_timeout.value())+'\n'
            else:
                lin='#timeout \n'
            f.write(lin)
        f.close()
        self.close()

    def enableSaX(self):
        self.ui.b_SaX.setEnabled(True)

    def setTimeoutOptions(self):
        self.ui.sb_timeout.setEnabled(self.ui.ch_timeout.isChecked())
        

    def boto_expert(self):
        system("kwrite "+self.grub)


#app = QApplication(sys.argv)
#preferencies = panelGrub()
#preferencies.show()
#app.exec_()
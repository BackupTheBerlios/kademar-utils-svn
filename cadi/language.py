#!/usr/bin/python
#-*- coding: iso-8859-15 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from commands import getoutput
from os import path, system

import funcions_k

from ui_language import Ui_FormLanguage as Ui_Form

class panelLanguage(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        
        self.pathcadi="/usr/share/kademar/utils/cadi"  #Path del instalador
        #Definicio de banderes
        self.band_cat=self.pathcadi+"/img/cat.png"
        self.band_esp=self.pathcadi+"/img/esp.png"
        self.band_eng=self.pathcadi+"/img/eng.png"

#####  SIGNAL & SLOTS  #####
        self.connect(self.ui.b_sortir, SIGNAL("clicked()"), self.boto_sortir)
        self.connect(self.ui.b_SaX, SIGNAL("clicked()"), self.SaveAndExit)
        self.connect(self.ui.b_cat, SIGNAL("clicked()"), self.idiomacat)
        self.connect(self.ui.b_esp, SIGNAL("clicked()"), self.idiomaesp)
        self.connect(self.ui.b_eng, SIGNAL("clicked()"), self.idiomaeng)
#### END SIGNAL & SLOTS ####

        ### System & Language
        self.idioma=funcions_k.idioma()
        if self.idioma==0:
            self.idiomacat()
        elif self.idioma==1:
            self.idiomaesp()
        elif self.idioma==2:
            self.idiomaeng()

        self.ui.b_SaX.setEnabled(False)


    def setidioma(self, lang):
        self.ui.b_SaX.setEnabled(True)

        if lang=="ca":
            self.idioma="ca"
            self.ui.b_cat.setEnabled(0)
            for i in self.ui.b_esp, self.ui.b_eng:
                i.setEnabled(1)
                i.setChecked(0)
            self.ui.l_bandera.setPixmap(QPixmap(self.band_cat))
        elif lang=="es":
            self.idioma="es"
            self.ui.b_esp.setEnabled(0)
            for i in self.ui.b_cat, self.ui.b_eng:
                i.setEnabled(1)
                i.setChecked(0)
            self.ui.l_bandera.setPixmap(QPixmap(self.band_esp))
        elif lang=="en":
            self.idioma="en"
            self.ui.b_eng.setEnabled(0)
            for i in self.ui.b_cat, self.ui.b_esp:
                i.setEnabled(1)
                i.setChecked(0)
            self.ui.l_bandera.setPixmap(QPixmap(self.band_eng))

    def idiomacat(self):
        self.setidioma("ca")
    def idiomaesp(self):
        self.setidioma("es")
    def idiomaeng(self):
        self.setidioma("en")
        
    def boto_sortir(self):
        self.close()

    def SaveAndExit(self):
        system('sh scripts/canvi_idioma '+self.idioma)
        self.close()


#app = QApplication(sys.argv)
#preferencies = preferencies()
#preferencies.show()
#app.exec_()
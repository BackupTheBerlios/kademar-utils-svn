#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from PyQt4 import uic

from commands import getoutput
#from os import getuid
from os import system, path
import funcions_k
from ui_kademarstart import Ui_Form_kademarstart as Ui_Form
import os, commands, sys, ihooks

#global tipus, config, conffile, globalfile, home, localfile


class kademarstart(QWidget):
    def __init__(self, standalone=None):
        QWidget.__init__(self)

        self.standalone=standalone

        global config
        load_config()

        #Load Form
        self.ui_kademarstart = Ui_Form()
        self.ui_kademarstart.setupUi(self)
        self.ui_kademarstart.pages.setCurrentWidget(self.ui_kademarstart.tab_ppal)

        #if not standalone:
        self.ui_kademarstart.b_band_cat.setVisible(0)
        self.ui_kademarstart.b_band_esp.setVisible(0)

        #print config
        if not int(config.autostart):
            self.ui_kademarstart.cb_autostart.setVisible(0)

        #####################
        # Signals & Slots Buttons
        #####################
        #Sortir i Enrera
        self.connect(self.ui_kademarstart.b_sortir, SIGNAL("clicked()"), self.close)
        self.connect(self.ui_kademarstart.b_enrera, SIGNAL("clicked()"), self.boto_enrera)

        # Banderes
        self.connect(self.ui_kademarstart.b_band_cat, SIGNAL("clicked()"), self.boto_cat)
        self.connect(self.ui_kademarstart.b_band_esp, SIGNAL("clicked()"), self.boto_esp)

        # Principal
        self.connect(self.ui_kademarstart.b_notes, SIGNAL("clicked()"), self.boto_notesversio)
        self.connect(self.ui_kademarstart.b_configurar, SIGNAL("clicked()"), self.boto_configurarsistema)
        self.connect(self.ui_kademarstart.b_equip, SIGNAL("clicked()"), self.boto_equip)
        self.connect(self.ui_kademarstart.b_suport, SIGNAL("clicked()"), self.boto_suport)

        # Programes
        self.connect(self.ui_kademarstart.b_cadi, SIGNAL("clicked()"), self.boto_cadi)
        self.connect(self.ui_kademarstart.b_kcontrol, SIGNAL("clicked()"), self.boto_kcontrol)

        # Suport
        self.connect(self.ui_kademarstart.b_faq, SIGNAL("clicked()"), self.boto_faq)
        self.connect(self.ui_kademarstart.b_foro, SIGNAL("clicked()"), self.boto_foro)
        self.connect(self.ui_kademarstart.b_doc, SIGNAL("clicked()"), self.boto_doc)
        self.connect(self.ui_kademarstart.b_email, SIGNAL("clicked()"), self.boto_email)


	#if no Notes versio, do not show
        ruta="/usr/share/kademar/utils/kademarcenter/html/"
        if path.exists(ruta+"notesversio_ca.html") or path.exists(ruta+"notesversio_es.html"):
            pass
        else:
            self.ui_kademarstart.pages.removeTab(1)
            self.ui_kademarstart.b_notes.setEnabled(0)
        #####################
        # END Signals & Slots Buttons
        #####################
        #locale = QLocale.system().name()   #ca_ES
        #global qtTranslator, idioma
        #idioma=locale.split("_")[0]
        #qtTranslator = QTranslator()
        #if qtTranslator.load("/usr/share/kademar/utils/kademarcenter/tr/"+locale.split("_")[0]+".qm"):
            #app.installTranslator(qtTranslator)
            #print "Loaded "+locale
        #elif qtTranslator.load("/usr/share/kademar/utils/kademarcenter/tr/es.qm"):
            #app.installTranslator(qtTranslator)
            #print "Loaded en"
        #Set kademar Label
        versiokademar=funcions_k.versiokademar()
        tipuskademar=funcions_k.tipuskademar()
        self.ui_kademarstart.l_kademar.setText("kademar "+tipuskademar+" "+versiokademar+" GNU/Linux")

        #if idioma=="ca":
            #self.boto_cat()
        #elif idioma=="es":
            #self.boto_esp()

    def boto_faq(self):
        system("x-www-browser http://www.kademar.org/kademarstart/boto_faq.php &")

    def boto_foro(self):
        system("x-www-browser http://www.kademar.org/kademarstart/boto_foro.php &")

    def boto_doc(self):
        system("x-www-browser http://www.kademar.org/kademarstart/boto_doc.php &")

    def boto_email(self):
        system("x-www-browser http://www.kademar.org/kademarstart/boto_email.php &")

    def boto_kcontrol(self):
        system("kcontrol &")

    def boto_cadi(self):
        system("cadi &")

    def boto_enrera(self):
        self.ui_kademarstart.pages.setCurrentWidget(self.ui_kademarstart.tab_ppal)
        #print "notesversio"

    def boto_notesversio(self):
        self.ui_kademarstart.pages.setCurrentWidget(self.ui_kademarstart.tab_notes)
        #print "notesversio"

    def boto_configurarsistema(self):
        self.ui_kademarstart.pages.setCurrentWidget(self.ui_kademarstart.tab_configurar)
        #print "configurar sistema"

    def boto_equip(self):
        self.ui_kademarstart.pages.setCurrentWidget(self.ui_kademarstart.tab_equip)
        #print "equip"

    def boto_suport(self):
        self.ui_kademarstart.pages.setCurrentWidget(self.ui_kademarstart.tab_suport)
        #print "suport"

    def boto_cat(self):
        global idioma
        idioma="ca"
        self.ui_kademarstart.b_band_cat.setEnabled(0)
        self.ui_kademarstart.b_band_esp.setEnabled(1)
        self.translateForm()

    def boto_esp(self):
        global idioma
        idioma="es"
        self.ui_kademarstart.b_band_cat.setEnabled(1)
        self.ui_kademarstart.b_band_esp.setEnabled(0)
        self.translateForm()

    def boto_eng(self):
        global idioma
        idioma="es"
        self.translateForm()

    def translateForm(self):
        global qtTranslator, idioma
        app.removeTranslator(qtTranslator)
        qtTranslator = QTranslator()
        qtTranslator.load("/usr/share/kademar/utils/kademarcenter/tr/"+idioma+".qm")
        app.installTranslator(qtTranslator)
        self.ui_kademarstart.retranslateUi(self)
        self.ui_kademarstart.web_equip.setUrl(QUrl(self.tr("file:///usr/share/kademar/utils/kademarcenter/html/equip_ca.html")))
        self.ui_kademarstart.web_notes.setUrl(QUrl(self.tr("file:///usr/share/kademar/utils/kademarcenter/html/notesversio_ca.html")))
        #Set kademar Label
        versiokademar=funcions_k.versiokademar()
        tipuskademar=funcions_k.tipuskademar()
        self.ui_kademarstart.l_kademar.setText("kademar "+tipuskademar+" "+versiokademar+" GNU/Linux")

        path="/usr/share/kademar/html/"

    def closeEvent(self, event):
        global localfile, home
        if self.ui_kademarstart.cb_autostart.isChecked():
            #system("rm -f $home/.kde/Auto*/kademar.desktop 2>/dev/null")
            #home=getoutput("echo $HOME")
            system("mkdir -p "+home+"/.kademar")
            f=open(localfile,'w')
            f.writelines("autostart=0")
            f.close()
        self.setVisible(0)
        if not self.standalone:
            event.ignore()



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
def load_config():
    global config, localfile, home
    conffile="kademarstart_conf.py"
    globalfile="/usr/share/kademar/utils/kademarcenter/cfg/"+conffile
    if path.exists(globalfile):
        config=import_from(globalfile)

    home=getoutput("echo $HOME")
    localfile=home+"/.kademar/"+conffile
    if path.exists(localfile):
        #print localfile
        config=import_from(localfile)



#to run standalone, use  kademarstart.py

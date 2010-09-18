#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from commands import getoutput
from os import path, system

#import funcions_k

from ui_services import Ui_FormServices as Ui_Form

class panelServices(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        global tipus
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.b_SaX.setEnabled(False)

#####  SIGNAL & SLOTS  #####
        self.connect(self.ui.b_sortir, SIGNAL("clicked()"), self.boto_sortir)
        self.connect(self.ui.b_SaX, SIGNAL("clicked()"), self.SaveAndExit)
        self.connect(self.ui.cb_samba, SIGNAL("clicked()"), self.enableSaX)
        self.connect(self.ui.cb_apache, SIGNAL("clicked()"), self.enableSaX)
        self.connect(self.ui.cb_mysql, SIGNAL("clicked()"), self.enableSaX)
        self.connect(self.ui.cb_cups, SIGNAL("clicked()"), self.enableSaX)
        self.connect(self.ui.cb_ssh, SIGNAL("clicked()"), self.enableSaX)
        self.connect(self.ui.b_open_bum, SIGNAL("clicked()"), self.executeBum)

#### END SIGNAL & SLOTS ####

        if not path.exists("/usr/bin/bum"): 
            self.ui.b_open_bum.setVisible(0)

        self.samba=self.apache=self.mysql=self.cups=self.ssh=False

        self.data=(
        [ "samba", "20", self.ui.cb_samba, False ],
        [ "apache2", "56", self.ui.cb_apache, False ],
        [ "mysql", "20", self.ui.cb_mysql, False ],
        [ "cups", "20", self.ui.cb_cups, False ],
        [ "ssh", "80", self.ui.cb_ssh, False ]
        )

        self.init=getoutput("cat /etc/inittab | grep -v \# | grep initdefault | cut -f2 -d:")

        for i in self.data:
        #daemon exists, set enabled
            if path.exists("/etc/init.d/"+i[0]):
                i[2].setEnabled(True)
             #daemon starting at S80ssh  set checked =Yes
                if path.exists("/etc/rc"+self.init+".d/S"+i[1]+i[0]):
                    i[2].setChecked(True)
                    i[3]=True #save the initial state
                
        #daemon NOT exists, set NOT enabled and not continue
            else:
                i[2].setEnabled(False)

    def enableSaX(self):
        self.ui.b_SaX.setEnabled(True)

    def boto_sortir(self):
        self.close()

    def SaveAndExit(self):
    #check if has been a change of state
      #samba
        if self.ui.cb_samba.isEnabled() and not self.ui.cb_samba.isChecked() == self.data[0][3]:
         #stat true
            if self.ui.cb_samba.isChecked():
                system('update-rc.d -f samba remove')
                system('update-rc.d -f lisa remove')
                #dirs=getoutput('ls /home --ignore=Pc --ignore=ANONYMOUS').split()
                #for i in dirs:
                    #system('mkdir -p /home/'+i+'/.kde3/share/apps/konqsidebartng/entries/ 2>/dev/null')
                    #self.crealandesktop('/home/'+i+'/.kde3/share/apps/konqsidebartng/entries/')
                #system('mkdir -p /etc/skel/.kde3/share/apps/konqsidebartng/entries/ 2>/dev/null')
                #self.crealandesktop('/etc/skel/.kde3/share/apps/konqsidebartng/entries/')
                #system('mkdir -p /root/.kde3/share/apps/konqsidebartng/entries/ 2>/dev/null')
                #self.crealandesktop('/root/.kde3/share/apps/konqsidebartng/entries/')

                system('update-rc.d samba defaults '+self.data[0][1])
                system('update-rc.d lisa defaults '+self.data[0][1])
                system('/etc/init.d/samba restart')
                system('/etc/init.d/lisa restart')
         #stat false
            else:
                system('/etc/init.d/samba stop')
                system('/etc/init.d/lisa stop')
                system('update-rc.d -f samba remove')
                system('update-rc.d -f lisa remove')
                #system('rm -f /home/*/.kde3/share/apps/konqsidebartng/entries/LAN.desktop')
                #system('rm -f /etc/skel/.kde3/share/apps/konqsidebartng/entries/LAN.desktop')
                #system('rm -f /root/.kde3/share/apps/konqsidebartng/entries/LAN.desktop')
      #apache
        if  self.ui.cb_apache.isEnabled() and not self.ui.cb_apache.isChecked() == self.data[1][3]:
         #stat true
            if self.ui.cb_apache.isChecked():
                system('update-rc.d -f apache2 remove')
                system('update-rc.d apache2 defaults '+self.data[1][1])
                system('/etc/init.d/apache2 restart')
         #stat false
            else:
                system('/etc/init.d/apache2 stop')
                system('update-rc.d -f apache2 remove')
      #mysql
        if  self.ui.cb_mysql.isEnabled() and not self.ui.cb_mysql.isChecked() == self.data[2][3]:
         #stat true
            if self.ui.cb_mysql.isChecked():
                system('update-rc.d -f mysql remove')
                system('update-rc.d mysql defaults '+self.data[2][1])
                system('/etc/init.d/mysql restart')
         #stat false
            else:
                system('/etc/init.d/mysql stop')
                system('update-rc.d -f mysql remove')
      #cups
        if  self.ui.cb_cups.isEnabled() and not self.ui.cb_cups.isChecked() == self.data[3][3]:
         #stat true
            if self.ui.cb_cups.isChecked():
                system('update-rc.d -f cups remove')
                system('update-rc.d cups defaults '+self.data[3][1])
                system('/etc/init.d/cups restart')
         #stat false
            else:
                system('/etc/init.d/cups stop')
                system('update-rc.d -f cups remove')
      #ssh
        if  self.ui.cb_ssh.isEnabled() and not self.ui.cb_ssh.isChecked() == self.data[4][3]:
         #stat true
            if self.ui.cb_ssh.isChecked():
                system('update-rc.d -f ssh remove')
                system('update-rc.d ssh defaults '+self.data[4][1])
                system('/etc/init.d/ssh restart')
         #stat false
            else:
                system('/etc/init.d/ssh stop')
                system('update-rc.d -f ssh remove')
        self.close()

    def executeBum(self):
        system("bum")

    def crealandesktop(self,directori):
        f=open(directori+'LAN.desktop','w')
        f.write('[Desktop Entry] \n')
        f.write('Encoding=UTF-8 \n')
        f.write('Icon=samba \n')
        f.write('Name[ca]=Xarxa \n')
        f.write('Name[es]=Red \n')
        f.write('Name[en]=Network \n')
        f.write('Open=false \n')
        f.write('X-KDE-KonqSidebarModule=konqsidebar_tree \n')
        f.write('X-KDE-RelURL=samba \n')
        f.write('X-KDE-TreeModule=Virtual \n')
        f.close()

#app = QApplication(sys.argv)
#preferencies = preferencies()
#preferencies.show()
#app.exec_()
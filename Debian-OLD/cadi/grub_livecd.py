#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from commands import getoutput
from os import path, system

#import funcions_k

from ui_grub_livecd import Ui_FormGrub as Ui_Form

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
        #self.connect(self.ui.le_pin, SIGNAL("textEdited (const QString&)"), self.enableSaX)
        self.connect(self.ui.b_restore, SIGNAL("clicked()"), self.boto_restore)
        self.connect(self.ui.listWidget , SIGNAL(" currentRowChanged (int)"), self.enableButtons)

#### END SIGNAL & SLOTS ####


        self.grubs=getoutput("ls /mnt/*/boot/grub/menu.lst 2>/dev/null").split()
        print self.grubs
        
        for i in self.grubs:
            print i
            a=QListWidgetItem(self.ui.listWidget)
            a.setText(i.replace("/boot/grub/menu.lst",""))
            a.setIcon(QIcon(self.hddIcon))
            self.ui.listWidget.addItem(a)

    def enableButtons(self,num):
        self.ui.b_restore.setEnabled(1)
        self.ui.b_expert.setEnabled(1)
        self.current=num

    def boto_expert(self):
        system("kwrite "+self.grubs[self.current])

    def boto_restore(self):
        ruta=self.grubs[self.current]

        if self.ui.checkBox.isChecked():
            system("cp "+ruta+" /tmp/cadi-grub")

        #if ruta.find('local')<>-1:
        #    ruta='/boot/grub/menu.lst'
        #    directori_a_usar="/"
        variables=ruta[1:].strip().split('/')
        #print variables

        ##############
        # BOOTLOADER #
        ##############
        mbr="auto"
        target="/regenera_grub"
        dirdesti=target+"/boot/grub"
        
        plantilla="/tmp/instalador-environment"
        
        fsarrel=getoutput('blkid /dev/'+variables[1]+' -o value -s TYPE')

        f=open(plantilla,'w')
        f.writelines('particioarrel=/dev/'+variables[1]+' \n')
        f.writelines('fsparticioarrel=/dev/'+fsarrel+' \n')
        f.writelines("#Desti d'instal·lacio  \n")
        f.writelines('DESTI='+target+' \n')
        f.writelines('mbr='+mbr+' \n')
        f.writelines('mbr_dev='+variables[1]+' \n')
        f.writelines('cadi="si" \n')

        f.close()
    
        #system("sh /usr/kademar/utils/instalador/particions-arrancables")
        #system("sh /usr/kademar/utils/instalador/particions-arrancables2") #Guarrada del os-prober
        system("umount /dev/"+variables[1]+" 2>/dev/null")
        system("mkdir "+target+" 2>/dev/null")
        system("mount /dev/"+variables[1]+" "+target)
        system("mount --bind /dev "+target+"/dev")
        system("mount --bind /proc "+target+"/proc")
        system("mount --bind /sys "+target+"/sys")
        system("rm -fr "+dirdesti)
        system("sh /usr/share/kademar/utils/instalador/scripts/linux-arrancables ")
        system("os-prober > /tmp/particions-arrancables")
        system("sh /usr/share/kademar/utils/instalador/scripts/install-bootloader")
        QApplication.processEvents()

        system("sh /usr/share/kademar/utils/instalador/scripts/make-grub_menu")
        QApplication.processEvents()

        system("sh /usr/share/kademar/utils/instalador/scripts/install-bootloader-final")
        
        QApplication.processEvents()
        #desmunta els directoris si existeixen per una fallida de l'instalador
        system("for i in `cat /proc/mounts | grep '"+target+"' | awk ' { print $2 } ' | sort -r`; do umount $i; done")
        system("for i in `cat /proc/mounts | grep '"+target+"' | awk ' { print $2 } ' | sort -r`; do umount $i; done")
        system("umount "+target+" && rm -fr "+target)
        system("mount /dev/"+variables[1])
        ### REFER FSTAB???!!!
    
    
        #################
        # FI BOOTLOADER #
        #################
        if self.ui.checkBox.isChecked():
            system("rm -f "+ruta)
            system("mv /tmp/cadi-grub "+ruta)
            
        QMessageBox.information(self, self.tr("Grub Restored"), self.tr("Grub has been resored on the device"), QMessageBox.Ok)

#app = QApplication(sys.argv)
#preferencies = panelGrub()
#preferencies.show()
#app.exec_()
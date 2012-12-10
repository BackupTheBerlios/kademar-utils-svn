#!/usr/bin/python 
# -*- coding: utf-8 -*-

#############################################
#      * Instalador. Copy Files Part *      #
#  ---------------------------------------  #
#     Author: Adonay Sanz Alsina            #
#     License: GPL 2.0 or higer             #
#     First Creation Date:  03-03-08        #
#  ---------------------------------------  #
#                                           #
#############################################


from PyQt4.QtCore import QThread, SIGNAL
from commands import getoutput
from os import system
from threadCheckspace import *

#import scripts


#Funcio de Format i Còpia de fitxers
class copyfiles(QThread):
    def __init__(self, a, b, c, d ,e, f, g, h, i):
        QThread.__init__(self)
        
        global target, inicial, copiant, mkfilesystems, filesystems, particioarrel, particioswap, particiohome, labelfilesystems, mktunefilesystems

	target=a
	inicial=b
        mkfilesystems=c
        filesystems=d
        particioarrel=e
        particioswap=f
        particiohome=g
        labelfilesystems=h
        mktunefilesystems=i

    def run(self):
        global target, inicial, copiant, mkfilesystems, filesystems, particioarrel, particioswap, particiohome, labelfilesystems, mktunefilesystems
        from os import system
        from commands import getoutput
        print "Zona de Format"

        ####
        #  FILESYSTEMS  HD  &  PARTITIONS
        ####
        #particioarrel[0] -  ARREL  |||   mkfilesystems[particioarrel[1]]  -  particionador (mkfs.reiserfs, mkfs.ext4, etc)
        #particioswap[0]  -  SWAP   |||   mkfilesystems[particioswap[1]]  -  particionador (mkfs.reiserfs, mkfs.ext4,  etc)
        #particiohome[0]  -  HOME   |||   mkfilesystems[particiohome[1]]  -  particionador (mkfs.reiserfs, mkfs.ext4,  etc)

        if mkfilesystems[particioarrel[1]]<>"":
            print "Formatant ARREL  /dev/"+particioarrel[0]+" amb "+mkfilesystems[particioarrel[1]]
            system(mkfilesystems[particioarrel[1]]+" /dev/"+particioarrel[0])
            system(labelfilesystems[particioarrel[1]].replace("$LABEL$",'"kademar 5"').replace('$DISK$','"/dev/'+particioarrel[0]+'"'))
            print  mkfilesystems[particioarrel[1]]+" /dev/"+particioarrel[0]+" Arrel"
            if mktunefilesystems[particioarrel[1]]<>"":
                system(mktunefilesystems[particioarrel[1]].replace("$LABEL$",'"kademar 5"').replace('$DISK$','"/dev/'+particioarrel[0]+'"'))
        if mkfilesystems[particioswap[1]]<>"":
            print "Formatant SWAP  /dev/"+particioswap[0]+" amb "+mkfilesystems[particioswap[1]]
            system(mkfilesystems[particioswap[1]]+" /dev/"+particioswap[0])
            print  mkfilesystems[particioswap[1]]+" /dev/"+particioswap[0]+" Swap"
        if particiohome:
            if mkfilesystems[particiohome[1]]<>"":
                print "Formatant HOME  /dev/"+particiohome[0]+" amb "+mkfilesystems[particiohome[1]]
                system(mkfilesystems[particiohome[1]]+" /dev/"+particiohome[0])
                system(labelfilesystems[particiohome[1]].replace("$LABEL$",'"kademar 5 Home"').replace('$DISK$','"/dev/'+particiohome[0]+'"'))
                print  mkfilesystems[particiohome[1]]+" /dev/"+particiohome[0]+" Home"
        print "Comença copia de Fitxers"

        #TEMP
        from os import system
        #desmunta els directoris si existeixen per una fallida de l'instalador
        system("for i in `cat /proc/mounts | grep '"+target+"' | awk ' { print $2 } ' | sort -r`; do umount $i; done")
        system("mkdir -p "+target)
        # munta la particio arrel on copiarem els fitxers del sistema
        system("mount -rw /dev/"+particioarrel[0]+" "+target)
	#engegem la barra de progress
        #QApplication.processEvents()
        # es creen els directoris home i es munten a les particions seleccionades
        # Si s'ha definit el HOME
        if  particiohome:
            system("mkdir -p "+target+"/home 2>/dev/null")
            system("mount -rw /dev/"+particiohome[0]+" "+target+"/home")
        global espaidisc
        self.espaidisc=checkspace(target, particioarrel, particioswap, particiohome)
        self.connect(self.espaidisc, SIGNAL("progress2"), self.enviaprogress)
        self.espaidisc.start()
        #QApplication.processEvents()
        #TEMP
        system('cp -u -a '+inicial+'/* '+target+' ; echo $? > /tmp/instalador-copia')
        #import time
        #time.sleep(15)
        self.espaidisc.quit()
        self.emit(SIGNAL("acabat"))

        print "emit acabat"

    #Envia al thread principal el progress
    def enviaprogress(self, num):
        self.emit(SIGNAL("progress"), int(num))


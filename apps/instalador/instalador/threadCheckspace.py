#!/usr/bin/python 
# -*- coding: utf-8 -*-

#############################################
#   * Instalador. Check progress status *   #
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

#Comprobació de el progrés de la còpia
class checkspace(QThread):
    def __init__(self, a, b, c, d):
        QThread.__init__(self)
        global target, particioarrel, particioswap, particiohome
        target=a
	particioarrel=b
	particioswap=c
	particiohome=d
        ####
        #  FILESYSTEMS  HD  &  PARTITIONS
        ####
        #selected_partition[0][0]  -  ARREL  |||   mkfilesystems[particioarrel[1]]  -  particionador (mkfs.reiserfs, etc)
        #selected_partition[1][0]  -  SWAP   |||   mkfilesystems[particioswap[1]]  -  particionador (mkfs.reiserfs, etc)
        #selected_partition[2][0]  -  HOME   |||   mkfilesystems[particiohome[1]]  -  particionador (mkfs.reiserfs, etc)



    def run(self):
        from os import path
        global target, particioarrel, particioswap, particiohome

        from os import system
        from commands import getoutput
        from time import sleep

        #print "Check Space Function"

        percent=0
        #suma conté el tamany dels fitxers que s'han de copiar
        #suma=int(getoutput("df / | grep / | awk ' { print $2 } ' "))
        if path.exists("/usr/share/kademar/utils/instalador/distrosize"):
            suma=int(getoutput("cat /usr/share/kademar/utils/instalador/distrosize"))
        else:
            suma=4000000  #4 gb

        #ocupainicial conté el tamany de les particions, per si no s'han formatat
        # pero per si s'ha seleccionat home separats... es comprova cada un d'ells
        ocupaarrel=int(getoutput("df /dev/"+particioarrel[0]+" | grep /dev/"+particioarrel[0]+"  | awk ' { print $3 } ' "))
        if particiohome:
            ocupahome=int(getoutput("df /dev/"+particiohome[0]+" | grep /dev/"+particiohome[0]+"  | awk ' { print $3 } ' "))
        else:
            ocupahome=ocupahomeactual=0

        ocupainicial=ocupaarrel+ocupahome
        ocupaactual=ocupainicial
        
        #TEMP
        while True:
        
        #if not varcopiaacabada:
            #print "comproba la situacio actual de la copia"
            sleep(10)  #Comproba cada 10 segons
            ocupaarrelactual=int(getoutput("df "+target+" | grep "+target+" | awk ' { print $3 } ' "))
            if particiohome:
                ocupahomeactual=int(getoutput("df "+target+"/home | grep "+target+"/home | awk ' { print $3 } ' "))
            ocupaactual=ocupaarrelactual+ocupahomeactual

            cant=ocupaactual-ocupainicial
            percent=int((cant*100)/suma)
#DEBUG
                #print "PERCENT"
                #print percent
                #QApplication.processEvents()  # python QT Yield

            if percent<100 and percent>0:
                self.emit(SIGNAL("progress2"), percent)
                    #QApplication.processEvents()  # python QT Yield

            #else:
                #self.stop()
                #QApplication.processEvents()  # python QT Yield

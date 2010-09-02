#!/usr/bin/python
#-*- coding: iso-8859-15 -*-

# Modul de funcions i variables per us itern de kademar

import os

llenguatge=['ca','es','en']
lleng_euro=['ca_ES@euro','es_ES@euro','en_ES@euro']
escriptori=['Escriptori','Escritorio','Desktop']
autoengega=['Autoengega','Autoarranque','Autostart']
paperera=['Paperera','Papelera','Trash']

#DEPRECATED by QT functions
def idioma():
    # determina quin idioma hi ha instalat mirant si existeix un fitxer determinat a /var, el ca, el es o el en
    idiom=0
    fitxer='/etc/default/locale'
    for i in range(len(llenguatge)):
        if os.path.exists(fitxer):
            f=open(fitxer)
            llista=f.readlines()
            f.close()
            text=''
            for linea in llista:
                if linea.find('LANG=')<>-1:
                    text=linea[5:7]
                    if text=='ca':
                        idiom=0
                        break
                    if text=='es':
                        idiom=1
                        break
                    if text=='en':
                        idiom=2
                        break
    return idiom

def dir_barra(directori):
    # comprova si el cami que es dona acaba amb / i, si no, li posa
    if directori[-1:]<>'/':
        directori=directori+'/'
    return directori
    
#If exists rootsquash -> it's on a live-cd
def instalat():
    if os.path.exists('/initrd/rootsquash') or os.path.exists("/mnt/live/memory/images/kademar.lzm"):
        return False
    else:
        return True
    
def ajuda(self,b,vist,num):
    if vist[num]==False:
        self.timer1.Stop()
        self.textCtrl1.SetValue(b)
    for i in range(len(vist)):
        vist[i]=False
        vist[num]=True

#Return versio de nucli - kernel
def versiokernel():
    from commands import getoutput
    return getoutput("uname -r")

#Return Verso de kademar
def versiokademar():
    from commands import getoutput
    return getoutput("cat /etc/kademar-release 2>/dev/null")

#Return kademar type
def tipuskademar():
    from commands import getoutput
    tipuskademar=getoutput(""". /etc/kademar/config ; echo $kademar_type  2>/dev/null""").lower()
    if tipuskademar=="leo":
        return "Leo - DvD"
    elif tipuskademar=="lyra":
       return "Lyra - CD"
    elif tipuskademar=="khronos":
        return "Khronos - Lite"
    elif tipuskademar=="core":
        return "Core - KDE"
    elif tipuskademar=="heliox":
        return "Heliox"
    else:
        return tipuskademar.capitalize()

#Function to check if internet's available
def internet():
    from commands import getoutput
    if int(getoutput("ping www.google.es -c1 2>/dev/null 1>&2 ; echo $?"))==0:
        return True
    else:
        return False

#Function to check .kademar config directori, if not exists, create it
def configdir():
    from os import system
    system("[ ! -e \"$HOME/.kademar\" ] && mkdir -p \"$HOME/.kademar\" ")


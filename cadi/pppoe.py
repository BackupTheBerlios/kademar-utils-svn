#!/usr/bin/python
#-*- coding: iso-8859-15 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from commands import getoutput
from os import path, system

#import funcions_k
from networkFunctions import grepNetInterfaceLines, grepNetInterfaceInformation

from ui_pppoe import Ui_FormPPPoE as Ui_Form

class panelPPPoE(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

#####  SIGNAL & SLOTS  #####
        self.connect(self.ui.b_sortir, SIGNAL("clicked()"), self.boto_sortir)
        self.connect(self.ui.b_inicia, SIGNAL("clicked()"), self.boto_inicia)
        self.connect(self.ui.b_finish, SIGNAL("clicked()"), self.writeConfig)
        self.connect(self.ui.b_disconfigure, SIGNAL("clicked()"), self.disconfigure)

#### END SIGNAL & SLOTS ####


        self.interfacesFile="/etc/network/interfaces"
        self.img_ethernet="/usr/share/kademar/utils/cadi/img/xarxa.png"


        self.ui.list_net_dev.setIconSize(QSize(32,32))
        self.ui.pages.setCurrentIndex(0)


    def boto_sortir(self):
        self.close()


    def boto_inicia(self):
        self.real_devices=[]
        self.real_devices=self.detectConcentrator() #get ethernet connected to pppoe concentrator
        #print self.real_devices

        if len(self.real_devices)==0:
            # si no hi ha cap eth, vol dir que no es pot configurar
            QMessageBox.critical(self, self.tr("ADSL/PPPoE Provider Not Found"), self.tr("It don't seems to have an ADSL/PPPoE concentrator connectated to any ethernet."), QMessageBox.Ok)
        else:
            #if there's a configured interface, allow to desconfigure it
            if grepNetInterfaceLines("dsl-provider"):
                self.ui.b_disconfigure.setVisible(True)
            else:
                self.ui.b_disconfigure.setVisible(False)

            self.ui.list_net_dev.clear()

            icon=self.img_ethernet
            
            for dev in self.real_devices:
                vendor=grepNetInterfaceInformation(dev, "vendor")
                product=grepNetInterfaceInformation(dev, "product")
                a=QListWidgetItem(self.ui.list_net_dev)
                a.setText(dev+": "+vendor+"\n"+product)
                a.setIcon(QIcon(icon))
                self.ui.list_net_dev.addItem(a)

            self.ui.pages.setCurrentIndex(1)


    def detectConcentrator(self):
        # detecta si hi ha un concentrador que permeti configurar pppoe
        self.interface=getoutput('''b='' ; for i in `ls /sys/class/net/ --ignore=lo --ignore=sit0`; do for mmm in '' '-U'; do a=`pppoe-discovery $mmm -A -I $i 2>&1 | grep "AC-Ethernet-Address"`; if [ -n "$a" ]; then  b="$b $i"; fi; done; done ; echo $b''')
        #self.interface='eth0 eth0 eth1 eth1 eth2 eth2'  # poso això per anar comprovant l'escript
        codis=[]
        if self.interface.strip()<>'':
            llista=self.interface.split()
            # ara netejo la llista, creo un altra, on no hi ha duplicats
            if len(llista)>0:
                for i in llista:
                    if  codis.count(i)==0:
                        codis.append(i)
        return codis


    def disconfigure(self):
        system("( poff 2>/dev/null ) &")  #get down the interface silently
        reversed=True
        network_interface_file=[]
        network_interface_file=grepNetInterfaceLines("dsl-provider", reversed)
        f=open(self.interfacesFile,'w')  #remove
        f.writelines(network_interface_file)
        f.close()
        self.ui.b_disconfigure.setVisible(0)
        QMessageBox.information(self, self.tr("Disconfiguration Done"), self.tr("Has removed successfuly configuration."), QMessageBox.Ok)
        self.ui.pages.setCurrentIndex(0)

    def writeConfig(self):
        self.interface=self.real_devices[self.ui.list_net_dev.currentRow()]
        #print "selected iface", self.interface

        #Be sure that there's no configured interface on the itnerface that we want to configure
        reversed=True
        network_interface_file=[]
        network_interface_file=grepNetInterfaceLines("dsl-provider", reversed)
        f=open(self.interfacesFile,'w')  #remove
        f.writelines(network_interface_file)
        f.close()

        reversed=True
        network_interface_file=[]
        network_interface_file=grepNetInterfaceLines(self.interface, reversed)
        f=open(self.interfacesFile,'w')  #remove
        f.writelines(network_interface_file)
        f.close()

        fitxer='/etc/ppp/options' 
        #fitxer='/home/josep/options' # ho poso per proves, borrar-lo després        
        #en el /etc/ppp/options has de aseguarte que hi hagin les entrades
        # noipdefault i noauth 
        #buscar si hi ha #noipdefault i descomentar-lo, si no hi es posar-li
        #buscar si hi ha auth i posar en el seu lloc noauth. si no hi es, posar-li
        #assigno a la variable llista el contingut del fitxer options
        f=open(fitxer,'r')
        llista=f.readlines()
        f.close()
        #repasso la llista linia per linia
        tnoipdefault=False
        tnoauth=False
        for x in range(len(llista)):
            # si trobo comentat el noipdefault, el descomento
            if llista[x].strip()=='#noipdefault':
                llista[x]='noipdefault\n'
                tnoipdefault=True
            # si trobo el auth el substitueixo per noauth
            if llista[x].strip()=='auth':
                llista[x]='noauth\n'
                tnoauth=True
        # si finalment no existeix noipdefault el afageixo al final del fitxer
        if not tnoipdefault:
            llista.append('noipdefault')
        # si finalment no existeix noauth el afageixo al final del fitxer
        if not tnoauth:
            llista.append('\nnoauth')
        f=open(fitxer,'w')
        for i in llista:
            f.write(i)
        f.close()
        
        fitxer='/etc/ppp/ip-up.d/0clampmss'
        #fitxer='/home/josep/0clampmss'
        #si aquest fitxer no hi es, crear-lo: /etc/ppp/ip-up.d/0clampmss
        if not path.exists(fitxer):
            f=open(fitxer,'w')
            f.write("#!/bin/sh \n")
            f.write("# Enable MSS clamping (autogenerated by kademar  -  CADI pppoe) \n")
            f.write("\n")
            f.write('''iptables -o "$PPP_IFACE" --insert FORWARD 1 -p tcp --tcp-flags SYN,RST SYN -m tcpmss --mss 1400:1536 -j TCPMSS --clamp-mss-to-pmtu \n''')
            f.close()
            system("chmod +x /etc/ppp/ip-up.d/0clampmss")
        #si hi es no fer res    
        
        # als fitxers /etc/ppp/chap-secrets i pap-secrets, s'hi afageix a la ultima linia si no hi es
        # kademar "*" ""
        fitxer='/etc/ppp/chap-secrets'
        f=open(fitxer,'r')
        llista=f.readlines()
        f.close()
        trobat=False
        for i in llista:
            if i.strip()=='''kademar "*" ""''':
                trobat=True
        if not trobat:
            llista.append('''kademar "*" "" \n''')
        
        #fitxer='/home/josep/chap-secrets' #ho poso per proves, borrar-ho després    
            
        f=open(fitxer,'w')
        f.writelines(llista)
        f.close()
            
        fitxer='/etc/ppp/pap-secrets'
        f=open(fitxer,'r')
        llista=f.readlines()
        f.close()
        trobat=False
        for i in llista:
            if i.strip()=='''kademar "*" ""''':
                trobat=True
        if not trobat:
            llista.append('''kademar "*" "" \n''')
        
        #fitxer='/home/josep/pap-secrets' #ho poso per proves, borrar-ho després    
            
        f=open(fitxer,'w')
        f.writelines(llista)
        f.close()
        
        #al fitxer /etc/ppp/peers/provider  maxakarlo
        fitxer='/etc/ppp/peers/provider'
        #fitxer='/home/josep/dsl-provider' # ho poso per proves, borrar-lo després
        f=open(fitxer,'w')
        f.write('noipdefault \n')
        f.write('usepeerdns \n')
        f.write('defaultroute \n')
        f.write('hide-password \n')
        f.write('lcp-echo-interval 20 \n')
        f.write('lcp-echo-failure 3 \n')
        f.write('connect /bin/true \n')
        f.write('noauth \n')
        f.write('persist \n')
        f.write('mtu 1492 \n')
        f.write('noaccomp \n')
        f.write('default-asyncmap \n')
        f.write('plugin rp-pppoe.so '+self.interface+' \n')
        f.write('user "kademar" \n')
        f.write('#pty "/usr/sbin/pppoe -I "'+self.interface+'" -T 80 -m 1452" \n')
        f.close()
        
        #al fitxer /etc/ppp/eth???-dsl-provider    maxakarlo
        fitxer='/etc/ppp/'+self.interface+'-dsl-provider'
        #fitxer='/home/josep/'+self.interface+'-dsl-provider' # ho poso per proves, borrar-lo després
        f=open(fitxer,'w')
        f.write('#!/bin/bash \n')
        f.write('/usr/sbin/pppoe -I '+self.interface+' -T 80 -m 1452  2>&1 >/dev/null \n')
        f.write('pon dsl-provider  2>&1 >/dev/null \n')
        f.close()

        #al fitxer /etc/network/interfaces buscar dsl-provider  i substitueixes d auto a auto
        #    auto dsl-provider
        #    iface dsl-provider inet ppp
        #    provider dsl-provider
        #    post-up sh /etc/network/eth???-dsl-provider &
        
        #obro el fitxer interfaces i ho assigno a variable llista
        f=open(self.interfacesFile,'r')
        llista=f.readlines()
        f.close()
        llista.append('\n')
        llista.append('auto dsl-provider \n')
        llista.append('    iface dsl-provider inet ppp \n')
        llista.append('    provider dsl-provider \n')
        llista.append('    post-up sh /etc/ppp/'+self.interface+'-dsl-provider & \n')
        f=open(self.interfacesFile,'w')  
        f.writelines(llista)
        f.close()

        #run & Try to connect
        system('poff')
        system('pon')


        QMessageBox.information(self, self.tr("Configuration Done"), self.tr("All configuration process has been completed. Now you should have internet."), QMessageBox.Ok)
        self.ui.pages.setCurrentIndex(0)


#app = QApplication(sys.argv)
#preferencies = preferencies()
#preferencies.show()
#app.exec_()
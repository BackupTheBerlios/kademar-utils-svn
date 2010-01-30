#!/usr/bin/python
#-*- coding: iso-8859-15 -*-

#############################################
#            -=|  CADI 5  |=-               #
#     .Internet and Connectivity Module.    #
#  ---------------------------------------  #
#     Author: Adonay Sanz Alsina            #
#     License: GPL 2.0 or higer             #
#     First Creation Date:  29-01-09        #
#  ---------------------------------------  #
#       Module to configure internet        #
#############################################


#todo:
  #FET: fer comprobacions ip/netmask/gateway correctes
  #enable/disenable boto si la key no te el tamany k toca
  #FET: agafar ip antiga per emplenar en way=eth
  #FET: poder desconfigurar una interface
  #FET: autowrite gw

  #def final (quan es diu si es grava o no o solamen executa)
  # gravar la config on toca
  # executar network restart
  #FET: agafar la gw antiga per fer remove default gw


import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from commands import getoutput
from os import path, system

from socket import gethostname
#import funcions_k

from networkFunctions import grepNetInterfaceLines, grepNetInterfaceInformation, getNetworkDevices, ifdown_wired_network

from ui_internet import Ui_FormInternet as Ui_Form

class panelInternet(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        global tipus
        self.ui = Ui_Form()
        self.ui.setupUi(self)

#### Variable definition
        self.pag=0
        self.way="eth"
        self.interfacesFile='/etc/network/interfaces'
        self.img_ok="/usr/share/kademar/utils/cadi/img/ok.png"
        self.img_no="/usr/share/kademar/utils/cadi/img/flag_red.png"
        self.img_search="/usr/share/kademar/utils/cadi/img/search.png"
        self.img_wireless="/usr/share/kademar/utils/cadi/img/network-wireless.png"
        self.img_ethernet="/usr/share/kademar/utils/cadi/img/network-wired.png"
        self.img_wifi_00="/usr/share/kademar/utils/cadi/img/wifi_signal_00.png"
        self.img_wifi_25="/usr/share/kademar/utils/cadi/img/wifi_signal_25.png"
        self.img_wifi_50="/usr/share/kademar/utils/cadi/img/wifi_signal_50.png"
        self.img_wifi_75="/usr/share/kademar/utils/cadi/img/wifi_signal_75.png"
        self.img_wifi_100="/usr/share/kademar/utils/cadi/img/wifi_signal_100.png"
        self.way_eth=[ self.ui.page, self.ui.pag1, self.ui.pag3 ]
        self.way_wifi=[ self.ui.page, self.ui.pag1, self.ui.pag2, self.ui.pag3 ]
        self.waitIcon="/usr/share/kademar/utils/cadi/img/wait.gif"
#### END Variable definition

#Initial preparations
        self.ui.list_net_dev.setIconSize(QSize(32,32))
        self.ui.list_net_wifi.setIconSize(QSize(48,48))
        
        #By default all wifi permanent
        self.ui.cb_permanent.setChecked(1)
        self.ui.cb_permanent.setVisible(0)

        self.makeDiagnostic()

####  Initial Form prepare
        self.initialFormPrepare()

        #fill DNS list
        self.ui.cb_dns.addItem(self.tr("Insert Custom DNS"))
        f=open('/usr/share/kademar/utils/cadi/resources/dns_list','r')
        llista=f.readlines()
        f.close()
        for i in llista:
            self.ui.cb_dns.addItem(i.strip("\n"))
        f=open(self.interfacesFile,'r')
        self.llista=f.readlines()
        f.close()
####

#####  SIGNAL & SLOTS  #####
        self.connect(self.ui.pages, SIGNAL("currentChanged (int)"), self.enterPageEvent)
        self.connect(self.ui.b_sortir, SIGNAL("clicked()"), self.boto_sortir)
        self.connect(self.ui.b_configure, SIGNAL("clicked()"), self.next_pag)
        self.connect(self.ui.b_next, SIGNAL("clicked()"), self.button_next1)
        self.connect(self.ui.b_next2, SIGNAL("clicked()"), self.button_next2)
        self.connect(self.ui.b_next3, SIGNAL("clicked()"), self.button_final)
        self.connect(self.ui.b_prev, SIGNAL("clicked()"), self.prev_pag)
        self.connect(self.ui.b_prev2, SIGNAL("clicked()"), self.prev_pag)
        self.connect(self.ui.b_prev3, SIGNAL("clicked()"), self.prev_pag)
        self.connect(self.ui.b_disconfigure, SIGNAL("clicked()"), self.button_disconfigure)
        self.connect(self.ui.list_net_dev, SIGNAL(" currentRowChanged (int)"), self.enable_next_net_dev_button)
        self.connect(self.ui.list_net_wifi, SIGNAL(" currentRowChanged (int)"), self.enable_next_net_wifi_button)
        self.connect(self.ui.b_reload, SIGNAL("clicked()"), self.reload_wifi_list)
        self.connect(self.ui.cb_dns, SIGNAL("currentIndexChanged (int)"), self.control_cb_dns)
        self.connect(self.ui.rb_ip_static, SIGNAL("clicked()"), self.change_rb_ip)
        self.connect(self.ui.rb_ip_dynamic, SIGNAL("clicked()"), self.change_rb_ip)
        self.connect(self.ui.rb_dns_static, SIGNAL("clicked()"), self.change_rb_dns)
        self.connect(self.ui.rb_dns_dynamic, SIGNAL("clicked()"), self.change_rb_dns)
        self.connect(self.ui.le_ip, SIGNAL("textChanged (const QString&)"), self.autoWriteGateway)
        self.connect(self.ui.le_netmask, SIGNAL("textChanged (const QString&)"), self.validateNetmask)
        self.connect(self.ui.le_gateway, SIGNAL("textChanged (const QString&)"), self.validateGateway)

#### END SIGNAL & SLOTS ####

    def initialFormPrepare(self):
        self.pag=0
        self.ui.l_hostname.setText("("+gethostname()+")")  #Puts localhost name
        self.ui.pages.setCurrentIndex(0) #Put page to 0
        self.ui.l_ip_pc.setText("")
        self.ui.l_ip_router.setText("")
        self.ui.l_key.setVisible(False) 
        self.ui.le_key.setVisible(False)
        self.ui.cb_key_type.setVisible(False)
        self.ui.b_disconfigure.setVisible(False)
        self.ui.cb_autoip.setEnabled(True)
        self.restartIpParameters()

    def boto_sortir(self):
        self.close()


    def next_pag(self):
        if self.pag==0:
            self.ui.pages.setCurrentIndex(self.pag+1)
            self.pag=self.pag+1
        else:
            if self.way=="eth" and not len(self.way_eth)==self.pag:
                self.ui.pages.setCurrentWidget(self.way_eth[self.pag+1])
                self.pag=self.pag+1
            if self.way=="wifi" and not len(self.way_wifi)==self.pag:
                self.ui.pages.setCurrentWidget(self.way_wifi[self.pag+1])
                self.pag=self.pag+1

    def prev_pag(self):
        if self.way=="eth":
            self.ui.pages.setCurrentWidget(self.way_eth[self.pag-1])
        elif self.way=="wifi":
            self.ui.pages.setCurrentWidget(self.way_wifi[self.pag-1])
        self.pag=self.pag-1

    def enterPageEvent(self, page):
        #this function makes things when enter to a concrete page

        if page==1:  #entered to page Devices
            self.ui.list_net_dev.blockSignals(True)
            self.real_devices=[]
            devices=getNetworkDevices() #get network devices
            self.ui.list_net_dev.clear()
            for dev in devices:
                wireless=path.exists("/sys/class/net/"+dev+"/wireless")  #this interface is wireless?
                if wireless:
                    icon=self.img_wireless
                else:
                    icon=self.img_ethernet
                vendor=grepNetInterfaceInformation(dev, "vendor")
                product=grepNetInterfaceInformation(dev, "product")
                a=QListWidgetItem(self.ui.list_net_dev)
                a.setText(dev+": "+vendor+"\n"+product)
                a.setIcon(QIcon(icon))
                self.ui.list_net_dev.addItem(a)
                # eth, true/false, vendor, product
                d=[dev, wireless, vendor, product]
                self.real_devices.append(d)
            self.ui.b_next.setEnabled(False) #disable next button
            self.ui.list_net_dev.blockSignals(False)
                #get hal information about it
            #restart IP parameters
            self.restartIpParameters()

        elif page==2:  #entered to page Wireless networks
            self.reload_wifi_list()
            #restart IP parameters
            self.restartIpParameters()
        elif page==3:
            self.grepOldDeviceSettings()
            self.ui.le_ip.setText(self.returnOldSetting("address"))
            self.ui.le_netmask.setText(self.returnOldSetting("netmask"))
            self.ui.le_gateway.setText(self.returnOldSetting("gateway"))
            self.ui.le_custom_dns.setText(self.returnOldSetting("dns-nameservers"))


    def restartIpParameters(self):
        self.ui.rb_ip_static.setChecked(False)
        self.ui.rb_ip_dynamic.setChecked(True)
        self.ui.rb_dns_static.setChecked(False)
        self.ui.rb_dns_dynamic.setChecked(True)
        self.ui.cb_dns.setCurrentIndex(0)
        self.ui.le_custom_dns.setText("")
        self.change_rb_ip()
        self.change_rb_dns()

#Enable Next button when selects the interface, choose your configuration way and select the device
    def enable_next_net_dev_button(self, item):
        self.ui.b_next.setEnabled(True)
        if self.real_devices[item][1]:
            self.way="wifi"
        else:
            self.way="eth"
        self.device=self.real_devices[item]
        if getoutput("grep "+self.real_devices[item][0]+" "+self.interfacesFile)<>'':
            self.ui.b_disconfigure.setVisible(True)
        else:
            self.ui.b_disconfigure.setVisible(False)


#Enable Next button when selects the wireless network
    def enable_next_net_wifi_button(self, item):
        self.ui.b_next2.setEnabled(True)
        self.xarxa=self.xarxes[item]
        if self.xarxa[3]:
            self.ui.l_key.setVisible(True)
            self.ui.le_key.setVisible(True)
            self.ui.cb_key_type.setVisible(True)
        else:
            self.ui.l_key.setVisible(False)
            self.ui.le_key.setVisible(False)
            self.ui.cb_key_type.setVisible(False)

    def change_rb_ip(self):
        obj=[ self.ui.l_ip, self.ui.le_ip, self.ui.l_netmask, self.ui.le_netmask, self.ui.l_gateway, self.ui.le_gateway ] 
        if self.ui.rb_ip_static.isChecked():
            for i in obj:
                i.setEnabled(True)
        else:
            for i in obj:
                i.setEnabled(False)

    def change_rb_dns(self):
        obj=[ self.ui.cb_dns, self.ui.le_custom_dns ] 
        if self.ui.rb_dns_static.isChecked():
            for i in obj:
                i.setEnabled(True)
        else:
            for i in obj:
                i.setEnabled(False)

    def control_cb_dns(self):
        if self.ui.cb_dns.currentIndex():
            self.ui.le_custom_dns.setVisible(False)
        else:
            self.ui.le_custom_dns.setVisible(True)

    def ipValidator(self, ip):
        if ip<>"":
            if int(ip)>255:
                return False
            else:
                return True
        else:
            return True


#autowrite gateway with the IP params ending with 1
 # and check IP correct
    def autoWriteGateway(self):
        error=False
        ip=self.ui.le_ip.text().split(".")
        for i in range(len(ip)):
            if not self.ipValidator(ip[i]):
                ip[i]="0"
                error=True
                QMessageBox.critical(self, self.tr("IP Error!"), self.tr("Number must be lesser than 255."), QMessageBox.Ok)
        if error:
            self.ui.le_ip.setText(ip[0]+"."+ip[1]+"."+ip[2]+"."+ip[3])
        self.ui.le_gateway.setText(ip[0]+"."+ip[1]+"."+ip[2]+".1")

    def validateNetmask(self):
        error=False
        ip=self.ui.le_netmask.text().split(".")
        for i in range(len(ip)):
            if not self.ipValidator(ip[i]):
                ip[i]="0"
                error=True
                QMessageBox.critical(self, self.tr("Netmask Error!"), self.tr("Number must be lesser than 255."), QMessageBox.Ok)
        if error:
            self.ui.le_netmask.setText(ip[0]+"."+ip[1]+"."+ip[2]+"."+ip[3])

    def validateGateway(self):
        error=False
        ip=self.ui.le_gateway.text().split(".")
        for i in range(len(ip)):
            if not self.ipValidator(ip[i]):
                ip[i]="0"
                error=True
                QMessageBox.critical(self, self.tr("Gateway Error!"), self.tr("Number must be lesser than 255."), QMessageBox.Ok)
        if error:
            self.ui.le_gateway  .setText(ip[0]+"."+ip[1]+"."+ip[2]+"."+ip[3])

    def button_next1(self):
            if self.way=="eth":
                if not self.ui.cb_autoip.isChecked():
                    self.next_pag()
                else:
                    self.finalProcess() #if no IP config needed, finish
            if self.way=="wifi":
                self.next_pag()

#Check key is putted in (if exists), and call real next page function
    def button_next2(self):
        if self.ui.le_key.isVisible():
            if not self.ui.le_key.text():
                QMessageBox.critical(self, self.tr("Wireless Key Error!"), self.tr("A Wireless key must be entered."), QMessageBox.Ok)
            else:
                if not self.ui.cb_autoip.isChecked():
                    self.next_pag()
                else:
                    self.finalProcess() #if no IP config needed, finish
        else:
            if not self.ui.cb_autoip.isChecked():
                self.next_pag()
            else:
                self.finalProcess() #if no IP config needed, finish

#Reload and put Wifi networks on List
    def reload_wifi_list(self):
        self.ui.cb_key_type.setCurrentIndex(0)
        self.ui.le_key.setText("")
        system('ifconfig '+self.device[0]+' up')
        lista=getoutput('iwconfig '+self.device[0])
        continua=True

        #Check if wifi is desactivated
        if lista.lower().find(self.device[0]+'      radio off')<>-1:
            continua=False
        if getoutput("iwlist "+self.device[0]+" scan | grep 'network is down'")<>"":
            continua=False
        if not continua:
            QMessageBox.critical(self, self.tr("Wireless Device Disconnected!"), self.tr("The wireless device is disconnected. Activate it through the computer button, and try it again."), QMessageBox.Ok)

        if continua:
            self.ui.list_net_wifi.blockSignals(True)
            self.ui.list_net_wifi.clear()
            self.xarxes=[]
            self.ui.l_key.setVisible(False)
            self.ui.le_key.setVisible(False)
            self.ui.cb_key_type.setVisible(False)
  #module extracted from OLD CADI (branch-4.x)
            essid=mode=channel=encryption=quality=""
            system('iwlist '+self.device[0]+' scan > /tmp/cadi-wireless')
            f=open('/tmp/cadi-wireless','r')
            llista=f.readlines()
            f.close()
            cells=[]
            for x in range(len(llista)):
                llista[x]=llista[x].strip()
            for x in range(len(llista)):
                if llista[x]<>'':
                    if llista[x][len(llista[x])-1]=='\n':
                        llista[x]=llista[x][:-1]
            num1=len(llista)
            num2=len(llista) #inicia la variable amb el final de la llista
            contador=[]
            for x in range(len(llista)):
                # busca el numero de linia on hi ha el CELL
                if llista[x][:4].lower()=='cell':
                    contador.append(x)

            contador.append(len(llista)-1)  
            for x in range(len(contador)-1):
                cells.append(llista[contador[x]:contador[x+1]])
            for x in range(len(cells)):
                for i in cells[x]:
                    #print i
                    if i.lower().find('essid')<>-1:
                        essid=i.split(':')[1]
                    if i.lower().find('mode')<>-1:
                        mode=i.split(':')[1]
                    if i.lower().find('channel')<>-1:
                        posicio1=i.lower().find('(')
                        posicio2=i.find(')')
                        if posicio1<>-1:
                            linea=i[posicio1+1:posicio2].strip()
                            channel=linea.split()[1]
                        else:
                            channel=i.split(':')[1]
                    if i.lower().find('encryption')<>-1:
                        encryption=i.split(':')[1]
                        if encryption.strip().lower()=='on':
                            encryption=True
                        else:
                            encryption=False
                    if i.lower().find('quality')<>-1:
                        i=i.split()[0]
                    #suport a separació per : o =
                        if i.lower().find('=')<>-1:
                            quality=(i.split('=')[1]).split()[0].split("/")[0]
                        elif i.lower().find(':')<>-1:
                            quality=(i.split(':')[1]).split()[0].split("/")[0]

                self.xarxes.append([essid,mode,channel,encryption,quality])

        #fill on Form QT4
            for i in self.xarxes:
                #Wifi quality image (images extracted from network-manager :-[ )
                icon=self.img_wifi_00       # if no quality recibed
                if int(i[4])<=25:           # less 25% 
                    icon=self.img_wifi_25
                elif int(i[4])<=50:         # less 50%
                    icon=self.img_wifi_50
                elif int(i[4])<=75:
                    icon=self.img_wifi_75   # less 75%
                elif int(i[4])<=100:
                    icon=self.img_wifi_100  # less 100%
                #Wifi encriptation boolean -> label (for translators)
                if i[3]:
                    enc=self.tr("yes")
                else:
                    enc=self.tr("no")
                #append wifi with all information, icon to  list_net_wifi on the GUI
                a=QListWidgetItem(self.ui.list_net_wifi)
                a.setText(i[0]+"\n"+self.tr("Encryption: ")+enc)
                a.setIcon(QIcon(icon))
                self.ui.list_net_wifi.addItem(a)

            self.ui.b_next.setEnabled(False) #disable next button
            self.ui.list_net_wifi.blockSignals(False)

#grep device configuration settings
    def grepOldDeviceSettings(self):
      
        reversed=False
        self.oldDeviceSettings=grepNetInterfaceLines(self.device[0], reversed)
        

#process old settings interface and return the previous parameter
    def returnOldSetting(self, param):
        for i in self.oldDeviceSettings:
            if i.find(param)>=0:
                done=True
                return i.strip().split()[1].replace("\n","")
        if param=="netmask":  #if not netmask, return default netmask
            return "255.255.255.0"
        return "" #if nothin, return blank

#button
    def button_disconfigure(self):
        self.grepOldDeviceSettings()  #grep old dev settings
        self.postConfig("disconfig")  #run final step on disconfig mode
        self.writeConfig("disconfig") #write a desconfigured interfaces file
        self.initialFormPrepare()     #and return to the beginning

#this is the last previous step. Here we check for correct data. If all OK. then call finalProcess
    def button_final(self):
        error=False
        if self.ui.rb_ip_static.isChecked():
            for i in self.ui.le_ip.text().split("."):
                if i=="":
                    if not error:
                        QMessageBox.critical(self, self.tr("IP error"), self.tr("IP must contains numbers."), QMessageBox.Ok)
                        error=True
            for i in self.ui.le_netmask.text().split("."):
                if i=="":
                    if not error:
                        error=True
                        QMessageBox.critical(self, self.tr("Netmask error"), self.tr("Netmask must contains numbers."), QMessageBox.Ok)
            for i in self.ui.le_gateway.text().split("."):
                if i=="":
                    if not error:
                        error=True
                        QMessageBox.critical(self, self.tr("Gateway error"), self.tr("Gateway must contains numbers."), QMessageBox.Ok)
        if self.ui.rb_dns_static.isChecked() and self.ui.le_custom_dns.isVisible():
            if self.ui.le_custom_dns.text()=="":
                if not error:
                    error=True
                    QMessageBox.critical(self, self.tr("Custom DNS Error"), self.tr("Custom DNS entries, must not be blank."), QMessageBox.Ok)

        if not error:
            self.finalProcess()

#This is the last step. Here saves config & run new config & return to diagnostic page

    def finalProcess(self):
    # Here, at last step, you can arribe here with:
    #
    #   - Ethernet (Always save config)
    #
    #   - Wifi
    #     - Saving Config
    #     - Witout Saving Config

        self.ui.pages.setCurrentWidget(self.ui.pag4)
        self.ui.b_sortir.setVisible(False)
        self.grepOldDeviceSettings()
        self.movie=QMovie(self.waitIcon)
        self.ui.l_mng.setMovie(self.movie)
        self.movie.start()

        self.postConfig("disconfig")         #first disconfig the interface
        self.writeConfig()                   #write the new config on interface file
        ifdown_wired_network()               #Down wired interfaces not connected
        self.postConfig()                    #bring up the interface
        
   #continue after config IP in a thread
    def continueConfigStep2(self):
        if not self.ui.cb_permanent.isChecked() and self.way=="wifi": #if don't want permanent, remove config
            print "desconfigurant"
            f=open(self.interfacesFile,'r')
            self.llista=f.readlines()
            f.close()
            self.writeConfig("disconfig")
        self.initialFormPrepare()            #return to beginning
        self.makeDiagnostic()                #and make new diagnostic
        self.movie.stop()
        self.ui.b_sortir.setVisible(True)


#bring down the interface if "disconfig" param, else bring UP
    def postConfig(self, param=None):
        global netdevice
        netdevice=self.device[0]
        #if we had a gateway, remove from default gw list
        if self.returnOldSetting("gateway")<>"":
            system("route del default gw "+self.returnOldSetting("gateway"))
        system("ifdown "+netdevice)
        system("ifdown "+netdevice)
        if not param=="disconfig":
            self.internetConfigure = internetConfigure()
            self.connect(self.internetConfigure, SIGNAL("acabat"), self.continueConfigStep2)
            self.internetConfigure.start()


    def writeConfig(self, param=None): #(self, normal, wifi=None):
        # grep device configuration settings reversed
        #  this means that only retreive interface file without lines about the specified device
        reversed=True
        network_interface_file=grepNetInterfaceLines(self.device[0], reversed)

        #if only want desconfigure, does not grep any other param
        if not param=="disconfig":
    ######
    # Write new lines
    ######
            #begin of interface configuration
            network_interface_file.append("\n")
            network_interface_file.append("allow-hotplug "+self.device[0]+"\n")
    ###
    # IP Section
    ###
            #static IP
            if self.ui.rb_ip_static.isChecked():
                gw=self.ui.le_gateway.text().split(".")
                network_interface_file.append('iface '+self.device[0]+' inet static \n')
                network_interface_file.append('    address '+self.ui.le_ip.text()+'\n')
                network_interface_file.append('    netmask '+self.ui.le_netmask.text()+'\n')
                network_interface_file.append('    gateway '+self.ui.le_gateway.text()+'\n')
                network_interface_file.append('    broadcast '+gw[0]+'.'+gw[1]+'.'+gw[2]+'.255\n')
                network_interface_file.append('    network '+gw[0]+'.'+gw[1]+'.'+gw[2]+'.0\n')

            #dynamic IP
            else:
                network_interface_file.append('iface '+self.device[0]+' inet dhcp\n')

        #DNS Section
            #static DNS
            if self.ui.rb_dns_static.isChecked():
                network_interface_file.append('    # dns-* options are implemented by the resolvconf package, if installed\n')

                #if we choose custom dns, use it
                if self.ui.cb_dns.currentIndex()==0:
                    network_interface_file.append('    dns-nameservers '+self.ui.le_custom_dns.text()+'\n')
                #if not, we have selected one from the list
                else:
                    network_interface_file.append('    dns-nameservers '+self.ui.cb_dns.currentText().split(":")[0]+'\n')

            #dynamic DNS
            else:
                #with static IP & dns dynamic
                if self.ui.rb_ip_static.isChecked():
                    network_interface_file.append('    # dns-* options are implemented by the resolvconf package, if installed\n')
                    #we pass to router the search of DNS
                    network_interface_file.append('    dns-nameservers '+self.ui.le_gateway.text()+'\n')

                #without static IP (all completly DHCP)
                else:
                    pass #Thats all. No more configuration
                    #network_interface_file.append('\n') 

    ###
    # END IP Section
    ###

    ###
    # WIFI Section
    ###
            if self.way=="wifi":
                #self.xarxa  [essid,mode,channel,encryption,quality]
                network_interface_file.append('    pre-up ifconfig '+self.device[0]+' up \n')
                network_interface_file.append('    pre-up iwconfig '+self.device[0]+' essid '+self.xarxa[0]+'\n')
                network_interface_file.append('    pre-up iwconfig '+self.device[0]+' channel '+self.xarxa[2]+'\n')
                if self.xarxa[3]:
                    #check if key is ascii
                    #print self.ui.cb_key_type.currentIndex(), "HOLAAA"
                    if self.ui.cb_key_type.currentIndex()==1:
                        ascii="s:"
                    else:
                        ascii=""
                    #write down
                    network_interface_file.append('    pre-up iwconfig '+self.device[0]+' key '+ascii+self.ui.le_key.text()+' open\n')
                else:
                #no key
                    network_interface_file.append('    pre-up iwconfig '+self.device[0]+' key off\n')
    ###
    # END WIFI Section
    ###

        #new networking not need it
            #Append at the end - if static IP - route add default gw
            #if self.ui.rb_ip_static.isChecked():
                #network_interface_file.append('    up route add default gw '+self.ui.le_gateway.text()+'\n')
                #network_interface_file.append('    down route del default gw '+self.ui.le_gateway.text()+'\n')


        f=open(self.interfacesFile,'w')  #remove
        f.writelines(network_interface_file)
        f.close()

############################
####  DIAGNOSTIC BLOCK  ####
############################

    def makeDiagnostic(self):
####  Diagnostic Thread
        #return to black color
        palette = QPalette()
        brush = QBrush(QColor(0,0,0))  # black color
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active,QPalette.WindowText,brush)
        palette.setBrush(QPalette.Inactive,QPalette.WindowText,brush)
        palette.setBrush(QPalette.Disabled,QPalette.WindowText,brush)
        self.ui.l_final_diag.setPalette(palette)
        self.ui.l_final_diag.setText(self.tr("In Progress..."))
        self.ui.l_img_diag_internet.setPixmap(QPixmap(self.img_search))
        self.ui.l_img_diag_router.setPixmap(QPixmap(self.img_search))
        self.diagnostic=NetworkDiagnostic()
        self.connect(self.diagnostic, SIGNAL("DiagInternet"), self.diag_internet)
        self.connect(self.diagnostic, SIGNAL("DiagRouter"), self.diag_router)
        self.connect(self.diagnostic, SIGNAL("DiagFinal"), self.diag_final)
        self.diagnostic.start()
####  End Diagnostic Thread

#### Functions to recive diagnostics
    #put images of internet diagnostic
    def diag_internet(self, ans):
        if ans:
            self.ui.l_img_diag_internet.setPixmap(QPixmap(self.img_ok))
        else:
            self.ui.l_img_diag_internet.setPixmap(QPixmap(self.img_no))

    #put router diagnostic + all information
    def diag_router(self, ans, router_ip="", eth_provider="", ip_eth=""):
        if ans:
            self.ui.l_img_diag_router.setPixmap(QPixmap(self.img_ok))
            self.ui.l_ip_router.setText(router_ip)
            self.ui.l_inet_eth_provider.setText(eth_provider)
            self.ui.l_ip_pc.setText(ip_eth)
        else:
            self.ui.l_img_diag_router.setPixmap(QPixmap(self.img_no))

    #print to label final diagnostic with colour
    def diag_final(self, diag):
        #There are 3 diag.
	# ok1  - Conection to router OK
	# ok2  - Connection router & internet OK
	# fail - Fails connect all
        if diag=="ok1":
            palette = QPalette()
            brush = QBrush(QColor(255, 128, 0))  # Orange colour
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QPalette.Active,QPalette.WindowText,brush)
            palette.setBrush(QPalette.Inactive,QPalette.WindowText,brush)
            palette.setBrush(QPalette.Disabled,QPalette.WindowText,brush)
            self.ui.l_final_diag.setPalette(palette)
            self.ui.l_final_diag.setText(self.tr("Partial Connection"))

        elif diag=="ok2":
            palette = QPalette()
            brush = QBrush(QColor(0,255,0)) # green colour
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QPalette.Active,QPalette.WindowText,brush)
            palette.setBrush(QPalette.Inactive,QPalette.WindowText,brush)
            palette.setBrush(QPalette.Disabled,QPalette.WindowText,brush)
            self.ui.l_final_diag.setPalette(palette)
            self.ui.l_final_diag.setText(self.tr("Successful"))

        else:
            palette = QPalette()
            brush = QBrush(QColor(255,0,0)) # red colour
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QPalette.Active,QPalette.WindowText,brush)
            palette.setBrush(QPalette.Inactive,QPalette.WindowText,brush)
            palette.setBrush(QPalette.Disabled,QPalette.WindowText,brush)
            self.ui.l_final_diag.setPalette(palette)
            self.ui.l_inet_eth_provider.setText("None")
            self.ui.l_final_diag.setText(self.tr("Failed"))
            self.ui.l_img_diag_internet.setPixmap(QPixmap(self.img_no))
            self.ui.l_img_diag_router.setPixmap(QPixmap(self.img_no))

#### END Functions to recive diagnostics

#Class to make a network diagnostic and get IP, router, internet, etc.
class NetworkDiagnostic(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):

     #Internet Diagnostic
        if not getoutput("ping www.google.com -c1 >/dev/null 2>&1 ; echo $?")[-1]=="0": #this must return 0 to have internet
            if not getoutput("ping www.kademar.org -c1 >/dev/null 2>&1 ; echo $?")[-1]=="0": #check with various servers
                if not getoutput("ping www.yahoo.com -c1 >/dev/null 2>&1 ; echo $?")[-1]=="0": #if previous fails
                    internet=False
                else:
                    internet=True
            else:
                internet=True
        else:
            internet=True

        self.emit(SIGNAL("DiagInternet"), internet)  #Emit Internet Diagnostic

     #Router Diagnostic
        netdevices=getNetworkDevices()
        ip_router=eth_provider=ip_eth_provider=""
        router=False
        for eth in netdevices:
            info=getoutput("arp -i "+eth+" 2>/dev/null | grep "+eth+" 2>/dev/null").split()
            if len(info)>1:
                if getoutput("ping "+info[0]+" -c1 >/dev/null 2>&1 ; echo $?")[-1]=="0": #if we have connection with router
                    eth_provider=eth
                    ip_eth_provider=getoutput("ifconfig "+eth_provider+" | grep Bcast | cut -f2 -d: | cut -f1 -d\ ") #get your IP
                    mac_eth_provider=getoutput("cat /sys/class/net/"+eth_provider+"/address") # get ethernet MAC
                    ip_router=info[0]  # get router IP
                    mac_router=info[2]  # get router MAC
                    router=True #check that we have found a router
                    break

     #This means that we cannot get router information
        if not router:
            #print "second router information"
            a=getoutput("""arp -a >/dev/null 2>&1 ; arp 2>/dev/null | while read line; do if [ "`echo $line | awk ' { print $4 } '`" = "C" ]; then echo $line | awk ' { print $1" "$5 } '; fi; done""").split()
            if len(eth_provider)>0:  #if found and eth_provider
                eth_provider=a[1]
                ip_eth_provider=getoutput("ifconfig "+eth_provider+" | grep Bcast | cut -f2 -d: | cut -f1 -d\ ") #get your IP
                mac_eth_provider=getoutput("cat /sys/class/net/"+eth_provider+"/address")
                ip_router=a[0]
                mac_router=""
                router=True

        self.emit(SIGNAL("DiagRouter"), router, ip_router, eth_provider, ip_eth_provider)  #Emit Router Diagnostic

        #Here you can read if any ethernet is configured and pass a fail diagnostic
        if not router: 
            #momentaniously only pass fail, does not check local IP if don't have connection to router
            self.emit(SIGNAL("DiagFinal"), "fail")
        else:
            self.emit(SIGNAL("DiagFinal"), "ok2")


################################
####  END DIAGNOSTIC BLOCK  ####
################################


class internetConfigure(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global netdevice
        system("ifup "+netdevice)
        #if no work ok, re up it
        system("ping -c1 kademar.org || ping -c1 google.com || ifdown "+netdevice+" ; ifup "+netdevice)
        self.emit(SIGNAL("acabat"))  #Emit Internet Diagnostic

#app = QApplication(sys.argv)
#preferencies = panelInternet()
#preferencies.show()
#app.exec_()
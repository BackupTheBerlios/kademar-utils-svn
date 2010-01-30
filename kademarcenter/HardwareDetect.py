#!/usr/bin/python 
#-*- coding: iso-8859-15 -*-

#############################################
#  *KADEMARCENTER Module: Detecta Hardware*  #
#  ---------------------------------------  #
#     Author: Adonay Sanz Alsina            #
#     License: GPL 2.0 or higer             #
#     First Creation Date:  03-03-08        #
#  ---------------------------------------  #
#    Script to process hardware changes     #
#        It's THE IvMan Substutute          #
#############################################


#############
####  HARDWARE ACTIONS
#############

from PyQt4.QtCore import QThread, SIGNAL
from commands import getoutput
from os import system, path
import dbus, dbus.glib
import scripts
import funcions_k
import os, commands, sys, ihooks


if not funcions_k.instalat():
    global liveDataDev
    liveDataDev="/dev/"+getoutput("cat /mnt/live/data")


class HardwareDetect(QThread):
    windowList=[]
    def __init__(self):
        QThread.__init__(self)

        self.warnedDevices=[]

        self.instaladorRunning="/tmp/instalador-running" 
        #"/tmp/instaladornano-running" 
####
# HARDWARE INITIAL DEFINITIONS - IvMan work
####
        global lshal
        lshal=getoutput("lshal").rsplit('\n') #Guardem l'estat actual de Hardware
        self.bus = dbus.SystemBus()
        self.hal_manager_obj = self.bus.get_object("org.freedesktop.Hal", 
                                                   "/org/freedesktop/Hal/Manager")
        self.hal_manager = dbus.Interface(self.hal_manager_obj,
                                          "org.freedesktop.Hal.Manager")

        # gdl_changed will be invoked when the Global Device List is changed
        # per the hal spec
        self.hal_manager.connect_to_signal("DeviceAdded", 
                         lambda *args: self.gdl_changed("DeviceAdded", *args))
        self.hal_manager.connect_to_signal("DeviceRemoved", 
                         lambda *args: self.gdl_changed("DeviceRemoved", *args))
        self.hal_manager.connect_to_signal("NewCapability", 
                         lambda *args: self.gdl_changed("NewCapability", *args))
####
# END HARDWARE INITIAL DEFINITIONS - IvMan work
####

    def wantWarn(self):
        from os import path
        if path.exists("/tmp/kademarcenter-inicial"):
            return None
        else:
            return True

    def run(self):
        #self.usbaccions("hola")
        pass
#############
####  HARDWARE ACTIONS
#############

    def gdl_changed(self, signal_name, device_udi, *args):
        """This method is called when a HAL device is added or removed."""
        if signal_name=="DeviceAdded":
            #print "\nDeviceAdded, udi=%s"%(device_udi)
            self.processa_udi(device_udi,"add")
        elif signal_name=="DeviceRemoved":
            print "\nDeviceRemoved, udi=%s"%(device_udi)
            self.processa_udi(device_udi,"remove")
            #pass
        elif signal_name=="NewCapability":
            [cap] = args 
            print "\nNewCapability, cap=%s, udi=%s"%(cap, device_udi)
        else:
            print "*** Unknown signal %s"% signal_name    

    def buscalshal(self, udi, accio):
        global lshal
        trobat="no"
        #print udi
        #print accio

        for i in lshal:
            if i=="":
            #print "Nou Hardware UDI"
                trobat="no"
            if i.find(udi)>=0:
                trobat="si"
                #print udi
                #print i, trobat
            if trobat=="si":  #Hem arribat al dispo que volem
                if accio=="volume":
                    if i.find("block.device")>=0:
                        #print "block"
                        #print i
                        #print i.rsplit()[2]
                        print i
                        return i.rsplit()[2].replace("'","")
                #      break
                elif accio=="cdrom":
                    if i.find("cdrom")>=0 or i.find("dvd")>=0 or i.find("cd_r")>=0:
                        print "Era un CDROM"
                        return True
                #       break
                if i.find("udi = '")>=0 and i.find("info.udi")==-1 and i.find(udi)==-1: #Vol dir que hem arribat a un altre dispositiu
                    #print "NOOOVA UDI"
                    #print i
                    trobat="no"
                    #break
                    pass

    def processa_udi(self, udi, accio):
        global lshal

        #print dev.GetAllProperties()
        print "UDI: "+udi
        print "ACCIO: "+accio
        #allprops=dev.GetAllProperties()
        if accio=="add":
                #####
                ## ACCIONS
                #####
                #print "Afegint HW"

            block=mntpoint=label="" #Variables to Zero
    ####
    ## DEFINICIO DEL TIPUS DE MEDI
    ####
            obj = self.bus.get_object("org.freedesktop.Hal", udi)
            dev = dbus.Interface(obj, 'org.freedesktop.Hal.Device')
            if dev.PropertyExists("info.capabilities"):
                props=str(dev.GetPropertyStringList("info.capabilities"))
                print  props
                #print type(dev.GetPropertyStringList("info.capabilities"))
            else:
                props=""
            #CDROM
            if dev.PropertyExists("volume.disc.type"):
                cdrom=str(dev.GetProperty("volume.disc.type"))
                props=''
            else:
                cdrom=""
                #MOUNT EVERITHING WE CAN
            if dev.PropertyExists("volume.is_mounted") and dev.PropertyExists("block.device"):
                block=str(dev.GetProperty("block.device"))
                if dev.PropertyExists("volume.disc.is_blank"):
                    if not dev.GetProperty("volume.disc.is_blank"):
                        print "MUNTANT "+block
                else:
                    print "MUNTANT "+block

                #system("pmount "+block)  #todo:  ntfs-3g & cdfs mount (hal rules)

                #Mount with moutmode of kademarconfig, if fails, mount
                system(scripts.mount+" "+block)  #todo:  ntfs-3g & cdfs mount (hal rules)

                    #lshal=getoutput("lshal").rsplit('\n')
            #Grep product information
            if dev.PropertyExists("info.vendor"):
                vendor=str(dev.GetProperty("info.vendor"))
            else:
                vendor=""
            if dev.PropertyExists("info.product"):
                product=str(dev.GetProperty("info.product"))
            else:
                product=""
            print "product="+product+" vendor="+vendor
                #print props[1]

            #net block device support
            if dev.PropertyExists("net.interface"):
                block=str(dev.GetProperty("net.interface"))
                #print "yes NETWORK interface", block

            #print cdrom
            if cdrom.find("cdrom")>=0 or cdrom.find("dvd")>=0 or cdrom.find("cd_r")>=0:
                label=str(dev.GetProperty("volume.label"))
                mntpoint=str(dev.GetProperty("volume.mount_point"))
                doit=0
                    #Si el mountpoint no e$mount_modesta definit, torna-ho a provar amb 1 segon
                if mntpoint=="":
                    print "2nd loop"
                    #system("sleep 1")
                    import time
                    #system("sleep 1")
                    time.sleep(1)
                    mntpoint=str(dev.GetProperty("volume.mount_point"))

                print cdrom+" encontrao"
                print "CD/DVD ENCHUFAO"
                print dev.GetProperty("block.device")
                #Music CD
                if dev.GetProperty("volume.disc.has_audio") and not doit:
                    print "DE MUSICA ENCHUFAO"
                    system(scripts.mount_audio_cdfs+" "+block+" &")  #use CDFS to mount audioCD only if cannout mount automatic with pmount
                    self.usbactions('audiocd', block, mntpoint, label)
                    doit=1
                #Blank CD
                if dev.GetProperty("volume.disc.is_blank") and not doit:
                    print "VACIO ENCHUFAO"
                    self.usbactions('blankcd', block, mntpoint, label)
                    doit=1
                #Video/vcd/dvd/blueray CD
                if dev.PropertyExists("volume.disc.is_vcd") and not doit:
                    if dev.GetProperty("volume.disc.is_vcd"):
                        print "VCD VIDEO  MEDIA"
                        print "vlc "+block
                        self.usbactions('vcd', block, mntpoint, label)
                        doit=1
                if dev.PropertyExists("volume.disc.is_svcd") and not doit:
                    if dev.GetProperty("volume.disc.is_svcd"):
                        print "SVCD  VIDEO  MEDIA"
                        print "vlc "+block
                        self.usbactions('vcd', block, mntpoint, label)
                        doit=1
                if dev.PropertyExists("volume.disc.is_videodvd") and not doit:
                    if dev.GetProperty("volume.disc.is_videodvd"):
                        print "VIDEODVD VIDEO  MEDIA"
                        print "vlc "+block
                        self.usbactions('vcd', block, mntpoint, label)

                        doit=1
                if dev.PropertyExists("volume.disc.is_blurayvideo") and not doit:
                    if dev.GetProperty("volume.disc.is_blurayvideo"):
                        print "BLURAY VIDEO  MEDIA"
                        print "vlc "+block
                        self.usbactions('vcd', block, mntpoint, label)

                        doit=1

                    #Peli DVD
                if cdrom=="dvd_rom" and not doit:
                    print "vlc2 "+block
                    self.usbactions('cdrom', block, mntpoint, label)
                    doit=1

                    #Other kinds of DVD
                if cdrom.find("dvd")>=0 and not doit:
                    print "DVD data"
                    self.usbactions('dvddata', block, mntpoint, label)
                    doit=1

                    #Data CdRom
                if not doit:
                    self.usbactions('cdrom', block, mntpoint, label)

            #print "paso per aquí"
            #print label, mntpoint, block, doit
    ########   FI CDROM  ########

            if props.find("mouse")>=0:
                print "MOUSE ENCHUFAO"
                self.emit(SIGNAL("showmsg"), "info",self.tr("Mouse Connected"), product+" "+vendor)
            elif props.find("input")>=0:
                print "DISPOSTIVO DE ENTRADA ENCHUFAO"
                self.emit(SIGNAL("showmsg"), "info",self.tr("Input Device Connected"), product+" "+vendor)
            if props.find("storage")>=0 and not cdrom:
                print "PEN ENCHUFAO"
                system(scripts.create_pc_enties+' '+block+' &')
                self.emit(SIGNAL("showusbtray"))
                self.emit(SIGNAL("showmsg"), "info",self.tr("Pendrive Connected"), product+" "+vendor)
            if props.find("volume")>=0 and props.find("block")>=0 and not props.find("volume.disc")>=0:
                print "PARTICION ENCHUFAO"
                print dev.GetProperty("block.device")
                label=str(dev.GetProperty("volume.label"))
                mntpoint=str(dev.GetProperty("volume.mount_point"))
                if mntpoint=="":
                    print "2n bucle"
                    import time
                    #system("sleep 1")
                    time.sleep(2)
                    mntpoint=str(dev.GetProperty("volume.mount_point"))
                system(scripts.create_pc_enties+' '+block+' &')
                self.usbactions('pen', block, mntpoint, label)
                self.emit(SIGNAL("regeneraformusbtray"))
            if props.find("printer")>=0:
                print "IMPRESORA ENCHUFAO"
                system(scripts.start_printer+' &')
                self.emit(SIGNAL("showmsg"), "info",self.tr("Printer Connected"), product+" "+vendor)
            if props.find("scanner")>=0:
                print "SCANNER ENCHUFAO"
                self.emit(SIGNAL("showmsg"), "info",self.tr("Scanner Connected"), product+" "+vendor)
            if props.find("bluetooth_hci")>=0:
                print "BLUETOOTH ENCHUFAO"
                self.emit(SIGNAL("showmsg"), "info",self.tr("Bluetooth Interface Conectada"), product+" "+vendor)
                system("sh scripts/bluetooth_start &")
            if props.find("bluetooth_acl")>=0:
                print "BLUETOOTH SINCRONIZAO"
                self.emit(SIGNAL("showmsg"), "info",self.tr("Bluetooth Interface Syncronized"), product+" "+vendor)
            if props.find("dvb")>=0:
                print "DVB ENCHUFAO"
                self.emit(SIGNAL("showmsg"), "info",self.tr("DVB Connected"), product+" "+vendor)
                self.usbactions('dvb', block, mntpoint, label)
            #print "INTERFACE DE RED ENCHUFAO"
            #print block
            if props.find("net.80211")>=0 or product.lower().find("wireless")>=0:
                print "INTERFACE DE RED  WIRELESS  ENCHUFAO".rsplit()[2]
                #system(scripts.wifi_prepare+' '+block)  #not used now
                self.emit(SIGNAL("showmsg"), "info",self.tr("Wireless Net Device Connected"), product+" "+vendor)
                self.usbactions('wlan', block, mntpoint, label)

            if props.find("net.80203")>=0:
                print "INTERFACE DE RED  RJ45  ENCHUFAO"
                self.usbactions('eth', block, mntpoint, label)
                self.emit(SIGNAL("showmsg"), "info",self.tr("Net Device Connected"), product+" "+vendor)
                self.usbactions('eth', block, mntpoint, label)
                if dev.PropertyExists("net.interface"):
                    net=str(dev.GetProperty("net.interface"))
                    system(scripts.ifup+' '+net)
            if props.find("video4linux")>=0:
                print "WEBCAM  ENCHUFAO"
                self.emit(SIGNAL("showmsg"), "info",self.tr("Webcam Connected"), product+" "+vendor)
            elif props.find("ieee1394")>=0:
                print "CAMARA FIREWIRE CONECTADA"
                if dev.PropertyExists("ieee1394.product"):
                    product=str(dev.GetProperty("ieee1394.product"))
                    vendor=str(dev.GetProperty("ieee1394.vendor"))
                    block=str(dev.GetProperty("ieee1394.device"))
                    self.emit(SIGNAL("showmsg"), "info",self.tr("Firewire Camera Connected"), product+" "+vendor)
                    self.usbactions('fwcam', block, mntpoint, label)


            #TODO:   HD firewire, ipaq/palm, mp3 reconegut, gestor de fotos?

            lshal=getoutput("lshal").rsplit('\n') #Al canvi de hardware torna a carregar la llista de hardware disponible
        if accio=="remove":
            #UMOUNT OLD MOUNTED DEVICES
            dispo=""
            dispo=str(self.buscalshal(udi, "volume"))
            #for i in lshal:
                #print i
            print dispo
            print "DISPO A DESCONNECTAR"
            if dispo<>"None":
            #IF IS A CD
                if self.buscalshal(udi, "cdrom"):
                    print "ES UN CD"
                    self.umountdispo(dispo)
                    self.removeWarnedDevice(dispo)
            #IF IS A USB = HD/MP3/PEN
            #check if umounted correctly
            # else show umount warn
                else:
                    print "ES UN USB"
                    if self.volume_is_mounted(dispo):
                        self.show_usbtray_warn() #avis de que no ho el desconecti a lo brutu
                        system(scripts.umount_forced+" "+dispo) #si estava conectat i la desconnectat a saco, desmuntemlo a saco
                    self.umountdispo(dispo)
                    self.removeWarnedDevice(dispo)
                            #for i in llistamuntats:
                    #if udi==i[0]:
                        #print "desmuntant anteriorment muntat: "+i[1]
                        #system("pumount "+i[1])
                    self.emit(SIGNAL("regeneraformusbtray"))

        if accio=="change":
            print "CHANGED:"
            print udi
            pass

    #############
    ####  END HARDWARE ACTIONS
    #############

    def volume_is_mounted(self, dispo):
        if getoutput("mount | grep -i "+dispo+" 2>/dev/null"):
            print "estava muntat"
            return True

    def show_usbtray_warn(self):
        from usbtray_warn import usbtray_warning
        self.a = usbtray_warning()
        self.a.show()
        self.a.activateWindow()


    #Instance new usbactions window and open for the new media inserted
    def usbactions(self, media, blk, mnt="", label=""):
        if self.wantWarn():
        #if not instalador running
            if funcions_k.instalat():
                self.openHotplugActions(media, blk, mnt, label)
        #in live-mode do not warn about device that you have started with
            else:
                global liveDataDev
                print "liveDataDev", liveDataDev
                print "blk", blk, blk.replace("scd", "sr"), liveDataDev.replace("scd", "sr")
                if not blk.replace("scd", "sr")==liveDataDev.replace("scd", "sr"):
                    if not path.exists(self.instaladorRunning):
                        self.openHotplugActions(media, blk, mnt, label)
                    else:
                        print "no warn because installatior is opened"
                else:
                    print "not warning hotplugactions because it's the live-cd start device: ", blk

    def openHotplugActions(self, media, blk, mnt="", label=""):
        if not blk[:7]=="wmaster":
            if not self.isDeviceInWarnedDevices(blk):
                self.warnedDevices.append(blk)

                global kademarcenterconfig
                self.load_kademarcenter_config()
                if kademarcenterconfig.actions_device_plugged:
                    from hotplugactions import hotplugaction
                    c=hotplugaction()
                    HardwareDetect.windowList.append(c)
                    c.accio(media, blk, mnt, label)
                    c.raise_()
                    c.activateWindow()  #I posala davant de tot
            else:
                print blk, "already warned"

    ############
    ####  UMOUNT ZONE
    ############

    #USB umount with warn /or not
    def umountdispo(self, dispo):
        #print " DESMUNTAR"
        #print dispo
        #print type(dispo)
        #if dispo<>"None":
            #for i in str(dispo).split(" "):
                #print " DESMUNTAR "+i
                #system("pumount "+i)
        system(scripts.umount+" "+str(dispo))

    def closeEvent(self, event):
        #self.hide()
        event.ignore()

    def removeWarnedDevice(self, dev):
        for i in range(len(self.warnedDevices)):
            if self.warnedDevices[i]==dev:
                self.warnedDevices[i]=0

    def isDeviceInWarnedDevices(self, dev):
        for i in range(len(self.warnedDevices)):
            if self.warnedDevices[i]==dev:
                return True
        return False


    def load_kademarcenter_config(self):
        global kademarcenterconfig
        kademarcenterconffile="kademarcenter_conf.py"
        kademarcenterglobalfile="/usr/share/kademar/utils/kademarcenter/cfg/"+kademarcenterconffile
        if path.exists(kademarcenterglobalfile):
            kademarcenterconfig=import_from(kademarcenterglobalfile)

        home=getoutput("echo $HOME")
        kademarcenterlocalfile=home+"/.kademar/"+kademarcenterconffile
        if path.exists(kademarcenterlocalfile):
            #print localfile
            kademarcenterconfig=import_from(kademarcenterlocalfile)
        #print dir(kademarcenterconfig)

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
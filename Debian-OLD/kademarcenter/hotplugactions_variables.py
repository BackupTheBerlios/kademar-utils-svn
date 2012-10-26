#!/usr/bin/python 
# -*- coding: iso-8859-15 -*-

from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *

class HotplugactionsVariables(QDialog):
    def __init__(self):
        #QWidget.__init__(self)
        print "Hotplugactions Variables Loaded"
        
    def defineix_variables(self, blk, mnt, label, part=None):
    
        # $blk$   - /dev/sda1
        # $mnt$   - /media/usbdisk
        # $label$ - Pendrive
        # $part$  - sda1
    
        #######
        # CDROM
        #######
        self.cdrom=(
            ["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", self.tr("Open with konqueror"), "konqueror %s" %(mnt)],
            ["/usr/share/pixmaps/k3b.xpm", self.tr("Copy with K3B"), "k3b --copycd %s" %(blk)],
            )
    
        #Icon
        self.cdromicon="/usr/share/icons/default.kde/48x48/devices/cdrom_unmount.png"
        self.cdromprop=self.tr("S'ha inserit un nou medi CD %s" %(label)) 
        self.cdromname="CD-Rom"
    
        #######
        # DVD Data
        #######
        self.dvddata=(
            ["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", self.tr("Open with konqueror"), "konqueror %s" %(mnt)],
            ["/usr/share/pixmaps/k3b.xpm", self.tr("Copy with K3B"), "k3b --copydvd %s" %(blk)],
            )
    
        #Icon
        self.dvddataicon="/usr/share/icons/default.kde/48x48/devices/dvd_unmount.png"
        self.dvddataprop=self.tr("S'ha inserit un nou medi DVD %s" %(label))
        self.dvddataname="DVD-Rom"
    
        #######
        # DVD  Pelicula
        #######
        self.dvd=(
            ["/usr/share/pixmaps/vlc.png", self.tr("Play with VLC") ,"vlc dvd://%s" %(blk)],
            ["/usr/share/icons/hicolor/48x48/apps/kaffeine.png", self.tr("Open with Kaffeine"), "kaffeine DVD"],
            ["/usr/share/icons/hicolor/48x48/apps/k9copy.png", self.tr("Copy with K9Copy"), "k9copy --input %s" %(blk)],
            ["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", self.tr("Open with konqueror"), "konqueror %s" %(mnt)],
            ["/usr/share/pixmaps/k3b.xpm", self.tr("Copy with K3B"), "k3b --copydvd %s" %(blk)],
            )
    
        self.dvdicon="/usr/share/icons/default.kde/48x48/devices/dvd_unmount.png"
        self.dvdprop=self.tr("S'ha inserit una película DVD %s" %(label))
        self.dvdname="DVD-Rom"
    
        #######
        # Audio CD
        #######
        self.audiocd=(
            ["/usr/share/icons/hicolor/48x48/apps/kaffeine.png", "Open with kaffeine", "kaffeine AudioCD"],
            ["/usr/share/pixmaps/vlc.png", self.tr("Play with VLC") ,"vlc cdda://%s" %(blk)],
            ["/usr/share/icons/locolor/32x32/apps/kaudiocreator.png", self.tr("Extract with Kaudiocreator"), "kaudiocreator %s" %(blk)],
            ["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", self.tr("Extract with Media"), "konqueror media:/%s" %(blk)],
            ["/usr/share/pixmaps/k3b.xpm", self.tr("Copy with K3B"), "k3b --copycd %s" %(blk)],
            ["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", self.tr("Open with konqueror"), "konqueror %s" %(mnt)],
            #["/usr/share/pixmaps/k3b.xpm", "Copy with K3B", "k3b --copydvd %s" %(blk)],
            )
    
        self.audiocdicon="/usr/share/icons/default.kde/48x48/devices/cdaudio_unmount.png"
        self.audiocdprop=self.tr("S'ha inserit un nou medi CD de música")
        self.audiocdname=self.tr("Audio CD")
    
        #######
        # PenDrive
        #######
        self.pen=(
            ["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", self.tr("Open with konqueror"), "konqueror %s" %(mnt)],
            #["/usr/share/pixmaps/k3b.xpm", "Copy with K3B", "k3b"],
            )
    
        #Icon
        self.penicon="/usr/share/icons/default.kde/48x48/devices/usbpendrive_unmount.png"
        self.penprop=self.tr("S'ha inserit un nou medi d'emmagatzematge USB")
        self.penname=self.tr("Almacenaje USB - %s" %(part))
    
        #######
        # DVB
        #######
        self.dvb=(
            ["/usr/share/icons/hicolor/48x48/apps/kaffeine.png", self.tr("Open with Kaffeine"), "kaffeine"],
            #["/usr/share/pixmaps/vlc.png", "Play with VLC" ,"vlc dvd://%s" %(blk)],
            #["/usr/share/icons/hicolor/48x48/apps/k9copy.png", "Copy with K9Copy", "k9copy --input %s" %(blk)],
            #["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", "Open with konqueror", "konqueror %s" %(mnt)],
            #["/usr/share/pixmaps/k3b.xpm", "Copy with K3B", "k3b --copydvd %s" %(blk)],
            )
    
        self.dvbicon="/usr/share/icons/default.kde/48x48/devices/tv.png"
        self.dvbprop=self.tr("S'ha inserit un dispositiu de TDT")
        self.dvbname="TDT/DvB"
    
        #######
        # Wifi Wlan
        #######
        self.wlan=(
            ["/usr/share/icons/default.kde/48x48/apps/package_settings.png", self.tr("Configura amb CADI"), "cadi"],
            #["/usr/share/pixmaps/vlc.png", "Play with VLC" ,"vlc dvd://%s" %(blk)],
            #["/usr/share/icons/hicolor/48x48/apps/k9copy.png", "Copy with K9Copy", "k9copy --input %s" %(blk)],
            #["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", "Open with konqueror", "konqueror %s" %(mnt)],
            #["/usr/share/pixmaps/k3b.xpm", "Copy with K3B", "k3b --copydvd %s" %(blk)],
            )
    
        self.wlanicon="/usr/share/icons/hicolor/48x48/apps/kwifimanager.png"
        self.wlanprop=self.tr("S'ha inserit un dispositiu de Xarxa Inalámbrica")
        self.wlanname=self.tr("Wireless Lan")
    
        #######
        # Wifi Wlan
        #######
        self.eth=(
            ["/usr/share/icons/default.kde/48x48/apps/package_settings.png", self.tr("Configure with CADI"), "cadi"],
            #["/usr/share/pixmaps/vlc.png", "Play with VLC" ,"vlc dvd://%s" %(blk)],
            #["/usr/share/icons/hicolor/48x48/apps/k9copy.png", "Copy with K9Copy", "k9copy --input %s" %(blk)],
            #["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", "Open with konqueror", "konqueror %s" %(mnt)],
            #["/usr/share/pixmaps/k3b.xpm", "Copy with K3B", "k3b --copydvd %s" %(blk)],
            )
    
        self.ethicon="/usr/share/icons/default.kde/48x48/apps/kcmpci.png"
        self.ethprop=self.tr("S'ha inserit un dispositiu de Xarxa de Fils")
        self.ethname=self.tr("Ethernet")
    
    
        #######
        # FireWire Cam
        #######
        self.fwcam=(
            ["/usr/share/pixmaps/kino.png", self.tr("Capture with Kino"), "kino"],
            ["/usr/share/icons/default.kde/48x48/apps/kdenlive.png", self.tr("Capture with Kdenlive"), "kdenlive"],
            #["/usr/share/pixmaps/vlc.png", "Play with VLC" ,"vlc dvd://%s" %(blk)],
            #["/usr/share/icons/hicolor/48x48/apps/k9copy.png", "Copy with K9Copy", "k9copy --input %s" %(blk)],
            #["/usr/share/icons/default.kde/48x48/apps/kfm_home.png", "Open with konqueror", "konqueror %s" %(mnt)],
            #["/usr/share/pixmaps/k3b.xpm", "Copy with K3B", "k3b --copydvd %s" %(blk)],
            )

        self.fwcamicon="/usr/share/icons/default.kde/48x48/devices/camera_unmount.png"
        self.fwcamprop=self.tr("S'ha inserit una càmera FireWire")
        self.fwcamname=self.tr("Firewire Camera")


        #######
        # NO Action
        #######
        self.nofer=["/usr/share/icons/default.kde/32x32/actions/button_cancel.png", self.tr("No fer res"), ""]
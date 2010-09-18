#!/usr/bin/python
# -*- coding: utf-8 -*-

#Scripts to make kademarcenter full power!!!
# OK to use with python or bash

#Start kbluetooth and bluetooth Server
bluetooth="sh /usr/share/kademar/utils/kademarcenter/scripts/bluetooth_start &"

#Update system package command
update="sudo /usr/share/kademar/utils/kademarcenter/scripts/update"

#Up2Date fstab & all physical devices (HD) - (old regenerapc)
update_fstab="sudo /usr/share/kademar/utils/kademarcenter/scripts/update_fstab"

#Warn through FIFO to check updates
warn_update="sudo /usr/share/kademar/utils/kademarcenter/scripts/warn_update"

#Upgrade system package command
upgrade="sudo /usr/share/kademar/utils/kademarcenter/scripts/upgrade"

#mount with pmount options
mount="/usr/share/kademar/utils/kademarcenter/scripts/mount_device"

#umount dev/$1?? devices, and force as root if cannot do
umount="/usr/share/kademar/utils/kademarcenter/scripts/umount_device"
umount_forced="sudo /usr/share/kademar/utils/kademarcenter/scripts/umount_device_forced"
remove_links="sudo /usr/share/kademar/utils/kademarcenter/scripts/umount_remove_links"


#Create PC entries for USB devices
create_pc_enties="sudo /usr/share/kademar/utils/kademarcenter/scripts/create_pc_enties"

#Delete PC entries for USB devices
delete_pc_enties="sudo /usr/share/kademar/utils/kademarcenter/scripts/delete_pc_enties"

#Unlock cdrom on eject
unlock_cdrom="sudo /usr/share/kademar/utils/kademarcenter/scripts/unlock_cdrom"

#Inicial warn of UDI not mounted on system, etc (mount cd, usb, etc)
initial_mount="sh /usr/share/kademar/utils/kademarcenter/scripts/initial_mount"

#Initial start of some services desktop in/dependent
initial_service_start="sh /usr/share/kademar/utils/kademarcenter/scripts/initial_service_start"
initial_service_start_common="sh /usr/share/kademar/utils/kademarcenter/scripts/initial_service_start_common"
initial_service_start_kde="sh /usr/share/kademar/utils/kademarcenter/scripts/initial_service_start_kde"

#Synce start for PDA & WindowsCE
synce_start="sh /usr/share/kademar/utils/kademarcenter/scripts/synce_start"

#UP Eth device
ifup="sudo /usr/share/kademar/utils/kademarcenter/scripts/ifup"

#Script to do ipw3945 hack
wifi_prepare="sudo /usr/share/kademar/utils/kademarcenter/scripts/wifi_prepare"

#Laptop Detector
laptop_detect="sudo /usr/share/kademar/utils/kademarcenter/scripts/laptop_detect"

#mount audio CDFS
mount_audio_cdfs="sudo /usr/share/kademar/utils/kademarcenter/scripts/mount_audio_cdfs"

#Activate all printers
start_printer="sudo /usr/share/kademar/utils/kademarcenter/scripts/start_printer"

#Script to down wired netinterfaces not connected
ifdown_wired_network="sudo /usr/share/kademar/utils/kademarcenter/scripts/ifdown_wired_network"

#script to do system mounts as shm or pts
system_mounts="sudo /usr/share/kademar/utils/kademarcenter/scripts/system_mounts"

#services
samba="sudo /usr/share/kademar/utils/kademarcenter/scripts/samba_start"
cups="sudo /usr/share/kademar/utils/kademarcenter/scripts/cups_start"
lisa="sudo /usr/share/kademar/utils/kademarcenter/scripts/lisa_start"
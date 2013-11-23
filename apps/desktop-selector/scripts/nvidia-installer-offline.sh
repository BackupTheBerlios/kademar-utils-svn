#!/bin/bash 

packets=""
#xorg-video packages on  package  kademar-base
for i in `cat /usr/share/kademar/xorg-video-packages`
do
 [ -n "$(pacman -Q $i 2>/dev/null)" ] && packets="$packets $i"
done


pacman --noconfirm -Rdd $packets
pacman --noconfirm -U /usr/share/desktop-selector/drivers/nvidia/*xz

rm -fr /tmp/nouveau /tmp/radeon



#If error on Nvidia driver, try the legacy one
if [ -n "$(LANG=C modprobe nvidia 2>&1 | grep -i "no such device")" -a -z "`grep nvidiaLegacyDriver=true /etc/desktop-selector/desktop-selector.ini`"  ]; then
  echo "Installing NVIDIA Legacy drivers"
  sudo sh /usr/share/desktop-selector/scripts/nvidia-legacy-installer-offline.sh
  sudo chmod 777 /etc/desktop-selector/desktop-selector.ini
  echo nvidiaLegacyDriver=true >> /etc/desktop-selector/desktop-selector.ini
fi
#!/bin/bash 

packets=""
#xorg-video packages on  package  kademar-base
for i in `cat /usr/share/kademar/xorg-video-packages`
do
 [ -n "$(pacman -Q $i 2>/dev/null)" ] && packets="$packets $i"
done


pacman --noconfirm -Rdd $packets
pacman --noconfirm -U /usr/share/desktop-selector/drivers/nvidia-legacy/*xz

rm -fr /tmp/nouveau /tmp/radeon

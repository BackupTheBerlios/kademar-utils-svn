#!/bin/bash 

 
for i in kademar-meta-xorg kademar-meta-xorg-drivers ati-dri intel-dri nouveau-dri xf86-video-intel-sna xf86-video-intel-uxa  xf86-video-ati xf86-video-intel xf86-video-nouveau
do
 pacman --noconfirm -Rdd "$i"
done


pacman --noconfirm -Rdd libgl 
pacman --noconfirm -U /usr/share/desktop-selector/drivers/nvidia*xz
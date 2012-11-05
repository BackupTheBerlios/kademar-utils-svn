#!/bin/bash 

 
for i in kademar-meta-xorg kademar-meta-xorg-drivers ati-dri xf86-video-intel-sna xf86-video-intel-uxa intel-dri xf86-video-ati xf86-video-intel
do
 pacman --noconfirm -R "$i"
done


pacman -Rdd libgl 
pacman --noconfirm  -S nvidia nvidia-utils
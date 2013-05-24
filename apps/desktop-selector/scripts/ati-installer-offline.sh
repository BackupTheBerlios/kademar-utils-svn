#!/bin/bash 

packets=""
for i in intel-dri kademar-meta-xorg kademar-meta-xorg-drivers libdrm-nouveau1 mesa-libgl mach64-dri mga-dri nouveau-dri ati-dri r128-dri savage-dri sis-dri svga-dri tdfx-dri unichrome-dri xf86-input-elographics xf86-video-apm xf86-video-ark xf86-video-ast xf86-video-ati xf86-video-chips xf86-video-cirrus xf86-video-dummy xf86-video-fbdev xf86-video-geode xf86-video-glint xf86-video-i128 xf86-video-i740 xf86-video-intel xf86-video-intel-sna xf86-video-intel-uxa xf86-video-mach64 xf86-video-mga xf86-video-neomagic xf86-video-nouveau xf86-video-nv xf86-video-openchrome xf86-video-r128 xf86-video-rendition xf86-video-s3 xf86-video-s3virge xf86-video-savage xf86-video-siliconmotion xf86-video-sis xf86-video-sisimedia xf86-video-sisusb xf86-video-tdfx xf86-video-trident f86-video-tseng xf86-video-unichrome xf86-video v4l xf86-video-vesa xf86-video-vmware xf86-video-voodoo lib32-mesa-libgl lib32-nvidia-utils nvidia-304xx nvidia-304xx-utils opencl-nvidia-304xx lib32-nvidia-304xx-utils nvidia nvidia-utils opencl-nvidia nvidia-libgl lib32-nvidia-libgl
do
 [ -n "$(pacman -Q $i 2>/dev/null)" ] && packets="$packets $i"
done


pacman --noconfirm -Rdd $packets
pacman --noconfirm -U /usr/share/desktop-selector/drivers/catalyst/*xz

rm -fr /tmp/nouveau /tmp/radeon

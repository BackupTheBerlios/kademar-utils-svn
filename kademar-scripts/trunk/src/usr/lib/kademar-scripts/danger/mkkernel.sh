#!/bin/bash

apt-get install lm-sensors-source translucency-source cloop-src vaiostat-source device3dfx-source loop-aes-ciphers-source nvidia-kernel-source linux-wlan-ng bcm5700-source drbd-source openafs-modules-source qce-source eagle-adsl-modules-src shfs-source i2c-source  atmelwlandriver-source cdfs-src unicorn-source hubcot-source lufs-source zaptel-source arla-modules-source loop-aes-source thinkpad-source lirc-modules-source userlink-source kernel-patch-evms kernel-patch-device-mapper || exit 1

cd /usr/src

for x in *gz ;do tar xvzpf $x ; done

for x in *bz2 ;do tar xvjpf $x ; done

rm -f linux

ln -s kernel-source-2.4.24 linux

cd linux 

cat Makefile | sed 's/EXTRAVERSION =/EXTRAVERSION = burnix-1/' > Makefile.nou

mv -f Makefile.nou Makefile

cp ../kernel-headers-2.4.24-openmosix-1/.config .

make-kpkg clean

cd ..

make




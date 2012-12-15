#!/bin/sh
# Setup Slax booting from disk (USB or harddrive)
# Requires: extlinux, fdisk
# No commandline arguments.

#modified by kademar linux - oct-2012

set -e

#kademar
[ "`whoami`" != "root" ] && echo "You need to be ROOT user!" && exit 1

# Dummy check for extlinux, to make sure extlinux exists
# even before any further analysis. If doesn't exist, script ends
VERSION=$(extlinux -v 2>&1)

# change working directory to dir from which we are started
CWD="$(pwd)"
BOOT="$(dirname "$0")"
cd "$BOOT"

# find out device and mountpoint
PART="$(df . | tail -n 1 | tr -s " " | cut -d " " -f 1)"
DEV="$(echo "$PART" | sed -r "s:[0-9]+\$::" | sed -r "s:([0-9])[a-z]+\$:\\1:i")"   #"

# check if disk is already bootable. Mostly for Windows discovery
if [ "$(fdisk -l "$DEV" | fgrep "$DEV" | fgrep "*")" != "" ]; then
   echo ""
   echo "Partition $PART seems to be located on a physical disk,"
   echo "which is already bootable. If you continue, your drive $DEV"
   echo "will boot only Kademar Linux by default."
#    echo "Press [Enter] to continue, or [Ctrl+C] to abort..."
#    read junk
fi

#kademar

#change config if we didn't
if [ -z "$(grep "/kademar/boot" *.cfg)" ]; then
  sed s-boot/-/kademar/boot/-g -i *.cfg
fi


#change archisodevice if exists (means that comes from other USB)

archisoolddevice=""
for i in `grep APPEND kademar_sys.cfg`
do
  if [ -n "$(echo $i | grep -i archisodevice)" ] ;then
    archisoolddevice=$i
    break
  fi
done

if [ -n "$archisoolddevice" ]; then
  uuid=$(blkid $PART -o value -s UUID)
  sed s."$archisoolddevice"."archisodevice=/dev/disk/by-uuid/$uuid".g -i *.cfg
fi


#conversió de archisolabel a archisodevice (comes from ISO)
archisolabel=""
for i in `grep APPEND kademar_sys.cfg`
do
  if [ -n "$(echo $i | grep -i archisolabel)" ] ;then
    archisolabel=$i
    break
  fi
done

#change config if we didn't

if [ -n "$archisolabel" ]; then
  uuid=$(blkid $PART -o value -s UUID)
  sed s."$archisolabel"."archisodevice=/dev/disk/by-uuid/$uuid".g -i *.cfg
fi


if [ -e kademar.cfg ]; then
  rm -f syslinux.cfg  #compatible coming from other USB
  mv kademar.cfg syslinux.cfg 2>/dev/null
fi

if [ -e heliox.cfg ]; then
  rm -f syslinux.cfg  #compatible coming from other USB
  mv heliox.cfg syslinux.cfg 2>/dev/null
fi


#fer menu nou amb permanent o no

#end kademar

# install syslinux bootloader
extlinux --install $BOOT

if [ "$DEV" != "$PART" ]; then
    #kademar
    cp /usr/lib/syslinux/mbr.bin $BOOT
  
   # Setup MBR on the first block
   cat "$BOOT/mbr.bin" > "$DEV"

   # Toggle bootable flags
   PART="$(echo "$PART" | sed -r "s:.*[^0-9]::")"
   (
      fdisk -l "$DEV" | fgrep "*" | fgrep "$DEV" | cut -d " " -f 1 \
        | sed -r "s:.*[^0-9]::" | xargs -I '{}' echo -ne "a\n{}\n"
      echo -ne "a\n$PART\nw\n"
   ) | fdisk $DEV >/dev/null 2>&1
fi

echo "Boot installation finished."
cd "$CWD"

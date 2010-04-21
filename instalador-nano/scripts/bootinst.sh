#!/bin/bash

#kademar


set -e
[ "`whoami`" != "root" ] && echo "You need to be ROOT user!" && exit 1


TARGET=""
MBR=""

# Find out which partition or disk are we using
MYMNT=$(cd -P $(dirname $0) ; pwd)
while [ "$MYMNT" != "" -a "$MYMNT" != "." -a "$MYMNT" != "/" ]; do
   TARGET=$(egrep "[^[:space:]]+[[:space:]]+$MYMNT[[:space:]]+" /proc/mounts | tail -n 1 | cut -d " " -f 1)

   if [ "$TARGET" != "" ]; then break; fi
   MYMNT=$(dirname "$MYMNT")
done

if [ "$TARGET" = "" ]; then
   echo "Can't find device to install to."
   echo "Make sure you run this script from a mounted device."
   exit 1
fi

if [ "$(cat /proc/mounts | grep "^$TARGET" | grep noexec)" ]; then
   echo "The disk $TARGET is mounted with noexec parameter, trying to remount..."
   mount -o remount,exec "$TARGET"
fi

MBR=$(echo "$TARGET" | sed -r "s/[0-9]+\$//g")
NUM=${TARGET:${#MBR}}
cd "$MYMNT"

echo "This installer will setup disk $TARGET to boot only kademar."
if [ "$MBR" != "$TARGET" ]; then
   echo
   echo "Warning! Master boot record (MBR) of $MBR will be overwritten."
   echo "If you use $MBR to boot any existing operating system, it will not work"
   echo "anymore. Only kademar will boot from this device. Be careful!"
fi

echo "Flushing filesystem buffers, this may take a while..."
sync

# setup MBR if the device is not in superfloppy format
if [ "$MBR" != "$TARGET" ]; then
   echo "Setting up MBR on $MBR..."
   ./boot/lilo -S /dev/null -M $MBR ext # this must be here to support -A for extended partitions
   echo "Activating partition $TARGET..."
   ./boot/lilo -S /dev/null -A $MBR $NUM
   echo "Updating MBR on $MBR..." # this must be here because LILO mbr is bad. mbr.bin is from syslinux
   cat ./boot/mbr.bin > $MBR
fi

# activating special USB options of Grub
#remove   #kademar# tags
sed s,'#kademar#',,g -i ./boot/grub/menu*

echo "Setting up boot record for $TARGET..."
# ./boot/syslinux/syslinux -d boot/syslinux $TARGET
grub-install --no-floppy --root-directory=$MYMNT $TARGET  

echo "Disk $TARGET should be bootable now. Installation finished."
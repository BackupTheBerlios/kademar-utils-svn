#!/bin/sh
# Setup Slax booting from disk (USB or harddrive)
# Requires: extlinux, fdisk
# No commandline arguments.

#modified by kademar linux - oct-2012

set -e

#kademar
[ "`whoami`" != "root" ] && echo "You need to be ROOT user!" && exit 1

mkmenu(){
  . /etc/locale.conf

  arch=`uname -m`

  kademarType="Kademar"
  [ -e /etc/kademar/config-livecd ] && . /etc/kademar/config-livecd
  PART=$1
  uuid=$(blkid $PART -o value -s UUID)

  if [ "$kademar_type" != "" ]; then
      kademarType=$kademar_type
  else
      if [ -n "$(grep -i heliox /etc/lsb-release)" ]; then
          kademarType=Heliox
      fi
  fi
  kademarTypeMinus=$(echo $kademarType | tr [A-Z [a-z])
    
  sed s."MENU ROWS 6"."MENU ROWS 7".g -i /instalador/nano/isolinux/*_head.cfg
  [ "$kademarType" != "Kademar" ] && sed s."Kademar"."$kademarType".g -i /instalador/nano/isolinux/*_head.cfg


  case "$LANG" in
  *)
  startLabel="Iniciar $kademarType Linux"
  persistentLabel="Cambios Persistentes"
  copyToRam="Copiar a RAM"
  memtestLabel="Programa de analisis de la memoria del ordenador"
  hardwareAnalysisLabel="Programa de analisis del ordenador y obtener informacion"
  hdtLabel="Informacion de Hardware (HDT)"
  rebootLabel="Reiniciar"
  haltLabel="Apagar Ordenador"
  headLabel="Presione [Tab] para editar las opciones de arranque en modo avanzado"
  ;;
  esac

#   sed "s~MENU TABMSG Presione.*MENU TABMSG $headLabel~g -i /instalador/nano/isolinux/menu_head.cfg

  cat > /instalador/nano/isolinux/menu_sys.cfg << EOF
MENU BEGIN 0000
   MENU START
   LABEL default
   MENU LABEL $startLabel
   MENU DEFAULT
   KERNEL /$kademarTypeMinus/boot/$arch/vmlinuz
   INITRD /$kademarTypeMinus/boot/$arch/$kademarType.img
   APPEND archisobasedir=$kademarTypeMinus archisodevice=/dev/disk/by-uuid/$uuid modprobe.blacklist=nouveau,radeon,floppy cow_device=/dev/disk/by-uuid/$uuid

   LABEL -
   MENU LABEL [*] $persistentLabel
   MENU GOTO 1000
   LABEL -
   MENU LABEL [ ] $copyToRam
   MENU GOTO 0001
   
   # http://www.memtest.org/
    LABEL memtest
    TEXT HELP
    $memtestLabel
    ENDTEXT
    MENU LABEL Memtest86+ (RAM test)
    LINUX /isolinux/memtest

    # http://hdt-project.org/
    LABEL hdt
    TEXT HELP
    $hardwareAnalysisLabel
    ENDTEXT
    MENU LABEL $hdtLabel
    COM32 /isolinux/hdt.c32
    APPEND modules_alias=/isolinux/hdt/modalias.gz pciids=/isolinux/hdt/pciids.gz

    LABEL reboot
    MENU LABEL $rebootLabel
    COM32 /isolinux/reboot.c32

    LABEL poweroff
    MENU LABEL $haltLabel
    COM32 /isolinux/poweroff.c32

MENU END


MENU BEGIN 1000
   LABEL default
   MENU LABEL $startLabel
   MENU DEFAULT
   KERNEL /$kademarTypeMinus/boot/$arch/vmlinuz
   INITRD /$kademarTypeMinus/boot/$arch/$kademarType.img
   APPEND archisobasedir=$kademarTypeMinus archisodevice=/dev/disk/by-uuid/$uuid modprobe.blacklist=nouveau,radeon,floppy

   LABEL -
   MENU LABEL [ ] $persistentLabel
   MENU GOTO 0000
   LABEL -
   MENU LABEL [ ] $copyToRam
   MENU GOTO 1111
   
   # http://www.memtest.org/
    LABEL memtest
    TEXT HELP
    $memtestLabel
    ENDTEXT
    MENU LABEL Memtest86+ (RAM test)
    LINUX /isolinux/memtest

    # http://hdt-project.org/
    LABEL hdt
    TEXT HELP
    $hardwareAnalysisLabel
    ENDTEXT
    MENU LABEL $hdtLabel
    COM32 /isolinux/hdt.c32
    APPEND modules_alias=/isolinux/hdt/modalias.gz pciids=/isolinux/hdt/pciids.gz

    LABEL reboot
    MENU LABEL $rebootLabel
    COM32 /isolinux/reboot.c32

    LABEL poweroff
    MENU LABEL $haltLabel
    COM32 /isolinux/poweroff.c32

MENU END


MENU BEGIN 0001
   LABEL default
   MENU LABEL $startLabel
   MENU DEFAULT
   KERNEL /$kademarTypeMinus/boot/$arch/vmlinuz
   INITRD /$kademarTypeMinus/boot/$arch/$kademarType.img
   APPEND archisobasedir=$kademarTypeMinus archisodevice=/dev/disk/by-uuid/$uuid modprobe.blacklist=nouveau,radeon,floppy cow_device=/dev/disk/by-uuid/$uuid copytoram

   LABEL -
   MENU LABEL [*] $persistentLabel
   MENU GOTO 1111
   LABEL -
   MENU LABEL [*] $copyToRam
   MENU GOTO 0000
   
   # http://www.memtest.org/
    LABEL memtest
    TEXT HELP
    $memtestLabel
    ENDTEXT
    MENU LABEL Memtest86+ (RAM test)
    LINUX /isolinux/memtest

    # http://hdt-project.org/
    LABEL hdt
    TEXT HELP
    $hardwareAnalysisLabel
    ENDTEXT
    MENU LABEL $hdtLabel
    COM32 /isolinux/hdt.c32
    APPEND modules_alias=/isolinux/hdt/modalias.gz pciids=/isolinux/hdt/pciids.gz

    LABEL reboot
    MENU LABEL $rebootLabel
    COM32 /isolinux/reboot.c32

    LABEL poweroff
    MENU LABEL $haltLabel
    COM32 /isolinux/poweroff.c32

MENU END

MENU BEGIN 1111
   LABEL default
   MENU LABEL $startLabel
   MENU DEFAULT
   KERNEL /$kademarTypeMinus/boot/$arch/vmlinuz
   INITRD /$kademarTypeMinus/boot/$arch/$kademarType.img
   APPEND archisobasedir=$kademarTypeMinus archisodevice=/dev/disk/by-uuid/$uuid modprobe.blacklist=nouveau,radeon,floppy copytoram

   LABEL -
   MENU LABEL [ ] $persistentLabel
   MENU GOTO 0001
   LABEL -
   MENU LABEL [*] $copyToRam
   MENU GOTO 1000
   
   # http://www.memtest.org/
    LABEL memtest
    TEXT HELP
    $memtestLabel
    ENDTEXT
    MENU LABEL Memtest86+ (RAM test)
    LINUX /isolinux/memtest

    # http://hdt-project.org/
    LABEL hdt
    TEXT HELP
    $hardwareAnalysisLabel
    ENDTEXT
    MENU LABEL $hdtLabel
    COM32 /isolinux/hdt.c32
    APPEND modules_alias=/isolinux/hdt/modalias.gz pciids=/isolinux/hdt/pciids.gz

    LABEL reboot
    MENU LABEL $rebootLabel
    COM32 /isolinux/reboot.c32

    LABEL poweroff
    MENU LABEL $haltLabel
    COM32 /isolinux/poweroff.c32

MENU END

EOF

}




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
# if [ "$(fdisk -l "$DEV" | fgrep "$DEV" | fgrep "*")" != "" ]; then
#    echo ""
#    echo "Partition $PART seems to be located on a physical disk,"
#    echo "which is already bootable. If you continue, your drive $DEV"
#    echo "will boot only Kademar Linux by default."
# #    echo "Press [Enter] to continue, or [Ctrl+C] to abort..."
# #    read junk
# fi

#kademar

#change config if we didn't
# if [ -z "$(grep "/$kademarTypeMinus/boot" *.cfg)" ]; then
#   sed s-boot/-/$kademarTypeMinus/boot/-g -i *.cfg
# fi

# if [ -e kademar.cfg ]; then
#   rm -f syslinux.cfg  #compatible coming from other USB
#   mv kademar.cfg syslinux.cfg 2>/dev/null
# fi
# 
# if [ -e heliox.cfg ]; then
#   rm -f syslinux.cfg  #compatible coming from other USB
#   mv heliox.cfg syslinux.cfg 2>/dev/null
# fi
#   cat > syslinux.cfg << EOF
# INCLUDE /isolinux/menu_head.cfg
# INCLUDE /isolinux/menu_sys.cfg
# EOF


mkmenu $PART

#fer menu nou amb permanent o no

#end kademar

# install syslinux bootloader
extlinux --install $BOOT

if [ "$DEV" != "$PART" ]; then
    #kademar
    cp /usr/lib/syslinux/bios/mbr.bin $BOOT
  
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

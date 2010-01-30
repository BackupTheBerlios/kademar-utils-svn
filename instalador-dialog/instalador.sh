#!/bin/bash

#############################################
#       -=|  INSTALADOR 5 DIALOG|=-         #
#             .Main Program.                #
#  ---------------------------------------  #
#     Author: Adonay Sanz Alsina            #
#     License: GPL 2.0 or higer             #
#     First Creation Date:  11-11-09        #
#  ---------------------------------------  #
#            The Installer                  #
#############################################

#Load installer configuration
. /usr/share/kademar/utils/instalador-dialog/sourcables/preferences

#Load installer functions
# . $pathinstaller/sourcables/functions

#Load configured locales
. /etc/environment

#Load kademar configuration
. /usr/share/kademar/config-livecd

version="`lsb_release -r -s`"
codename="`lsb_release -c -s`"

#Load localization language
case "$LANGUAGE" in
ca*)
. $pathinstaller/translations/installer-lang_ca
#used on config languages
esp=off
eng=off
cat=on
;;
es*)
. $pathinstaller/translations/installer-lang_es
#used on config languages
esp=on
eng=off
cat=off
;;
*)
. $pathinstaller/translations/installer-lang_en
#used on config languages
esp=off
eng=on
cat=off
;;
esac

#Umount installator folders, if was a unsuccessful exit
for i in `cat /proc/mounts | grep "$target" | awk ' { print $2 } ' | sort -r`; do umount $i; done

#Set title of installator
real_title="kademar Linux - $codename $version"

# reset logfile
echo > $logfile

#reset environment
echo "# Taula de Configuracio de la nova instal·lació" > $plantilla
echo "" >> $plantilla

#Support to linux-live and burnix scripts
if [ -e "/mnt/live/memory/images/kademar.lzm" ]; then
	inicial="/mnt/live/memory/images/kademar.lzm"
else
	inicial="/initrd/rootsquash"/dev/null 
fi

#remove dead config
rm -f $tmpdialog $tmpfile /tmp/instalador-copia


dialog --title "$real_title" --yesno "$main_description" $height $width

[ "$?" != 0 ] && exit #exit if no continue

#
# Warn about have a already partitioned HDD
#

while true; do
	dialog --title "$real_title" --yesno "$main_partition" $height $width
	if [ "$?" != 0 ]; then
		#want to partition
		fs_detector="`sh $pathinstaller/scripts/fs-detector 0`" >>$logfile 2>&1       #Script to get hd & partition info
		fsoptions=""

	for i in $fs_detector
	do
		a=`echo $i | cut -d- -f1`
		b="`echo $i | cut -d- -f2` Mb"
		info="`$grephalinfo /dev/$a product` - $b"
		fsoptions="$fsoptions $a \"$info\" off"
	done
	
	# build tmp dialog
	echo "dialog --title \"$real_title\" --radiolist \"$fs_detector_select_disk_partition\" $height $width $height $fsoptions  2>$tmpfile" > $tmpdialog
	
	
	while true; do
		sh $tmpdialog
		[ -n "`cat $tmpfile 2>/dev/null`" ] && break
	done


		sudo cfdisk "/dev/`cat $tmpfile 2>/dev/null`"

	else
		#already partitioned disk
		break
	fi
done


#
# Set HDD where install
#

fs_detector="`sh $pathinstaller/scripts/fs-detector 0`" >>$logfile 2>&1         #Script to get HDD in PC
fsoptions=""

for i in $fs_detector
do
	a="`echo $i | cut -d- -f1`"
	b="`echo $i | cut -d- -f2` Mb"
	info="`$grephalinfo /dev/$a product` - $b"
	fsoptions="$fsoptions $a \"$info\" off"
done

# build tmp dialog - to have spaces between fsoptions
echo "dialog --title \"$real_title\" --radiolist \"$fs_detector_select_disk\" $height $width $height $fsoptions  2>$tmpfile" > $tmpdialog


while true; do
	sh $tmpdialog
	[ -n "`cat $tmpfile 2>/dev/null`" ] && break
done

disk="`cat $tmpfile 2>/dev/null`"


#
# Set ROOT Partition where install
#

fs_detector="`sh "$pathinstaller/scripts/fs-detector" $disk`" >>$logfile 2>&1         #Script to get partition of a HDD
fsoptions=""


for i in $fs_detector
do
	a="`echo $i | cut -d- -f1`"
# 	b="`echo $i | cut -d- -f2`"
	b="`echo $i | cut -d- -f3` Mb"
	info="`$grephalinfo /dev/$a product` - $b"
	fsoptions="$fsoptions $a \"$info\" off"
done

hdinfo="`$grephalinfo /dev/$disk product`"


# build tmp dialog - to have spaces between fsoptions
echo "dialog --title \"$real_title\" --radiolist \"$fs_detector_selected_disk   $disk - $hdinfo \n\n$fs_detector_select_root_partition\" $height $width $height $fsoptions  2>$tmpfile" > $tmpdialog


while true; do
	sh $tmpdialog
	[ -n "`cat $tmpfile 2>/dev/null`" ] && break
done

disk_root="`cat $tmpfile 2>/dev/null`"
echo "particioarrel=/dev/$disk_root" >> $plantilla



#
# Set SWAP Partition where install
#

# fs_detector="`sh scripts/fs-detector $disk`"         #Script to get partition of a HDD
fsoptions=""


for i in $fs_detector
do
	a="`echo $i | cut -d- -f1`"
	if [ "$a" != "$disk_root" ]; then
	# 	b="`echo $i | cut -d- -f2`"
		b="`echo $i | cut -d- -f3` Mb"
		info="`$grephalinfo /dev/$a product` - $b"
		fsoptions="$fsoptions $a \"$info\" off"
	fi
done

hdinfo="`$grephalinfo /dev/$disk product`"


# build tmp dialog - to have spaces between fsoptions
echo "dialog --title \"$real_title\" --radiolist \"$fs_detector_selected_disk   $disk - $hdinfo \n\n$fs_detector_select_swap_partition\" $height $width $height $fsoptions  2>$tmpfile" > $tmpdialog


while true; do
	sh $tmpdialog
	[ -n "`cat $tmpfile 2>/dev/null`" ] && break
done

disk_swap="`cat $tmpfile 2>/dev/null`"
echo "particioswap=/dev/$disk_swap" >> $plantilla



#
# Set HOME partition
#
dialog --title "$real_title" --defaultno --yesno "$fs_detector_ask_home_partition" $height $width
if [ "$?" = 0 ]; then
#User want a home partition separated
	fsoptions=""
	for i in $fs_detector
	do
		a="`echo $i | cut -d- -f1`"
		if [ "$a" != "$disk_root" -a  "$a" != "$disk_swap" ]; then
		# 	b="`echo $i | cut -d- -f2`"
			b="`echo $i | cut -d- -f3` Mb"
			info="`$grephalinfo /dev/$a product` - $b"
			fsoptions="$fsoptions $a \"$info\" off"
		fi
	done
	
	hdinfo="`$grephalinfo /dev/$disk product`"
	
	
	if [ -n "$fsoptions" ]; then
		# build tmp dialog - to have spaces between fsoptions
		echo "dialog --title \"$real_title\" --radiolist \"$fs_detector_selected_disk   $disk - $hdinfo \n\n$fs_detector_select_home_partition\" $height $width $height $fsoptions  2>$tmpfile" > $tmpdialog
		
		rm -f $tmpfile
	
		while true; do
		sh $tmpdialog
		[ -n "`cat $tmpfile 2>/dev/null`" ] && break
		done
		
		disk_home="`cat $tmpfile 2>/dev/null`"
		echo "particiohome=/dev/$disk_home" >> $plantilla
	else
		dialog --title "$real_title" --msgbox "$fs_partition_no_more_left" $height $width

	fi


fi

#
# Format partitions
#
dialog --title "$real_title" --defaultno --yesno "$fs_detailed_format" $height $width
if [ "$?" = 0 ]; then
	#Root
	dialog --title "$real_title" --radiolist "$fs_detailed_root_format" $height $width $height reiserfs "" on ext3 "" off ext2 "" off "$fs_format_noformat" "" off  2>$tmpfile
	fs=`cat $tmpfile 2>/dev/null`
	if [ "$fs" = ext2 -o "$fs" = ext3 -o "$fs" = ext4 ]; then
		echo "fsparticioarrel=$fs" >> $plantilla
		fsparticioarrel=$fs
	fi

	#Home
	if [ -n "$disk_home" ]; then
		dialog --title "$real_title" --radiolist "$fs_detailed_home_format" $height $width $height reiserfs "" on ext3 "" off ext2 "" off "$fs_format_noformat" "" off  2>$tmpfile
		fs=`cat $tmpfile 2>/dev/null`
		if [ "$fs" = ext2 -o "$fs" = ext3 -o "$fs" = ext4 ]; then
			echo "fsparticiohome=$fs" >> $plantilla
			fsparticiohome=$fs
			
		fi
	fi
else
#if default config, format as reiserfs & swap
	echo "fsparticioarrel=$defaultfs" >> $plantilla
	fsparticioarrel=$defaultfs
	if [ -n "$disk_home" ]; then
		echo "fsparticiohome=$defaultfs" >> $plantilla
		fsparticiohome=$defaultfs
	fi

fi

#set target
echo "DESTI=$target" >> $plantilla

dialog --title "$real_title" --yesno "$license_gpl" $height $width
if [ "$?" = 0 ]; then
	echo "license=yes" >> $plantilla
else
	echo "license=no" >> $plantilla
fi

#Language
dialog --title "$real_title" --radiolist "$system_lang_select" $height $width $height ca Català $cat es Castellano  $esp en English $eng  2>$tmpfile

echo "LANGUAGE=`cat $tmpfile 2>/dev/null`" >> $plantilla

#Set pc Name
while true; do
	dialog --title "$real_title" --inputbox "$system_pc_name" $height $width kademar 2>$tmpfile
	[ -n "`cat $tmpfile 2>/dev/null`" ] && break
done
echo "NOM_PC=\"`cat $tmpfile 2>/dev/null`\"" >> $plantilla

#Root admin password
while true; do
	dialog --title "$real_title" --passwordbox "$system_root_passwd1" $height $width 2>$tmpfile
	pass1=`cat $tmpfile 2>/dev/null`
	dialog --title "$real_title" --passwordbox "$system_root_passwd2" $height $width 2>$tmpfile
	pass2=`cat $tmpfile 2>/dev/null`
	
	if [ "$pass1" = "$pass2" -a -n "$pass1" ]; then  #TOT OK
		echo "#Root Password" > $plantillapasswd
		echo "rootpasswd=\"$pass1\"" >> $plantillapasswd
		break
	fi
done

#User Account
dialog --title "$real_title" --inputbox "$user_config_name" $height $width 2>$tmpfile
echo "nom=\"`cat $tmpfile 2>/dev/null`\"" >> $plantilla

start=`cat $tmpfile | awk ' { print $1 } '`
while true; do
	dialog --title "$real_title" --inputbox "$user_config_login" $height $width "$start" 2>$tmpfile
	[ -n "`cat $tmpfile 2>/dev/null`" ] && break
done
echo "login=\"`cat $tmpfile 2>/dev/null`\"" >> $plantilla



while true; do
	dialog --title "$real_title" --passwordbox "$user_config_passwd1" $height $width 2>$tmpfile
	pass1=`cat $tmpfile 2>/dev/null`
	dialog --title "$real_title" --passwordbox "$user_config_passwd2" $height $width 2>$tmpfile
	pass2=`cat $tmpfile 2>/dev/null`
	
	if [ "$pass1" = "$pass2" -a -n "$pass1" ]; then  #TOT OK
		echo "#User Password" >> $plantillapasswd
		echo "passwd=\"$pass1\"" >> $plantillapasswd
		break
	fi
done

dialog --title "$real_title" --defaultno --yesno "$user_config_autologin" $height $width
if [ "$?" = 0 ]; then
	echo "AUTOLOGIN=yes" >> $plantilla
else
	echo "AUTOLOGIN=no" >> $plantilla
fi


echo "mbr=auto " >> $plantilla
echo "mbr_dev=$disk_root" >> $plantilla
echo "#Initrd creation" >> $plantilla
echo "make_initrd=yes" >> $plantilla


########################################
# Now Begins real installation process #
########################################

hdd=$particioswap
if [ -n "$fsparticioarrel" -o -n "$fsparticiohome" ]; then
#if any partition will be formated
#
# 	Support to NO_FORMAT selection
	[ -n "$fsparticioarrel" -a "$fsparticioarrel" != "$fs_format_noformat" ] && hdd="$hdd $disk_root"
	[ -n "$fsparticiohome" -a "$fsparticiohome" != "$fs_format_noformat" ] && hdd="$hdd $disk_home"

	a="$(echo "$begins_installation_with_format" | sed s."%PARTITIONS%"."$hdd".g)"
	final_msg="$begins_installation $a"
fi

dialog --title "$real_title" --msgbox "$final_msg" $height $width

sh "$pathinstaller/scripts/get_system_information.sh" >>$logfile 2>&1

#Be sure all it's disconnected and umounted
while true; do
	umnt-kademar 2>/dev/null
	[ "$?" = 0 ] && break
	dialog --title "$real_title" --msgbox "$be_sure_umounted" $height $width
done



#Load environment profile created
. $plantilla

#
# Format part
#

#root partition
if [ -n "$fsparticioarrel" ]; then
	case "$fsparticioarrel" in
		"ext3")
			mkfs="mkfs.ext3"
		;;
		"ext2")
			mkfs="mkfs.ext2"
		;;
		"ext4")
			mkfs="mkfs.ext4"
		;;
		"reiserfs")
			mkfs="mkfs.reiserfs -q"
		;;
		"xfs")
			mkfs="mkfs.xfs"
		;;
		"jfs")
			mkfs="mkfs.jfs"
		;;
	esac
	echo "Formating $particioarrel"
	$mkfs $particioarrel >>$logfile 2>&1
fi


#swap partition
echo "Formating $particioswap"
mkswap $particioswap >>$logfile 2>&1

#home partition
if [ -n "$particiohome" -a -n "$fsparticiohome" ]; then
	case "$fsparticiohome" in
		"ext3")
			mkfs="mkfs.ext3"
		;;
		"ext2")
			mkfs="mkfs.ext2"
		;;
		"ext4")
			mkfs="mkfs.ext4"
		;;
		"reiserfs")
			mkfs="mkfs.reiserfs -q"
		;;
		"xfs")
			mkfs="mkfs.xfs"
		;;
		"jfs")
			mkfs="mkfs.jfs"
		;;
	esac
	echo "Formating $particiohome"
	$mkfs $particiohome >>$logfile 2>&1
fi

#Umount patitons - in case of failed exit of installer
for i in `cat /proc/mounts | grep "$DESTI" | awk ' { print $2 } ' | sort -r`; do umount $i; done

#Be sure that exists target folder
mkdir -p "$DESTI"

#mount root partition
mount -rw "$particioarrel" "$DESTI"

#mount home partition if is defined
if [ -n "$particiohome" ]; then
	mkdir -p "$DESTI/home"
	mount -rw "$particiohome" "$DESTI/home"
fi



###
# Check initial space on disk, to fill gauge bar
##
if [ -e "/usr/share/kademar/utils/instalador/distrosize" ]; then
	suma="`cat /usr/share/kademar/utils/instalador/distrosize`"
else
	suma=4000000
fi
ocupaarrel=$(df "$particioarrel" | grep "$particioarrel"  | awk ' { print $3 } ')
if [ -n "$particiohome" ]; then
	ocupahome=$(df "$particiohome" | grep "$particiohome"  | awk ' { print $3 } ')
else
	ocupahome=0
	ocupahomeactual=0
fi
ocupainicial=$(($ocupaarrel+$ocupahome))
ocupaactual=$ocupainicial

#
# Begin Real copy
#
( cp -u -a $inicial/* "$DESTI" ; echo $? > /tmp/instalador-copia ) &

#
#Bet a Real gauge
#
dialog --title "$real_title" --gauge "$copying" $height $width 0 & #gauge at 0
while true; do
	sleep 10
	#check copied files and set gauge percentage
	ocupaarrelactual=$(df "$DESTI" | grep "$DESTI" | awk ' { print $3 } ')
	if [ -n "$particiohome" ]; then
		ocupahomeactual=$(df "$DESTI/home" | grep "$DESTI/home" | awk ' { print $3 } ')
	fi
        ocupaactual=$(($ocupaarrelactual+$ocupahomeactual))

        cant=$(($ocupaactual-$ocupainicial))
        percent=$(($cant*100))
        percent=$(($percent/$suma))

        [ "$percent" -gt 100 ] && percent=100

	dialog --title "$real_title" --gauge "$copying" $height $width $percent &
	[ -e "/tmp/instalador-copia" ] && break  #if exists, the copy is finished
done


###############################
# Start System Configurations #
###############################


#Make necessary system mounts
mount --bind /dev "$DESTI/dev"
mount -t proc "$DESTI/proc" "$DESTI/proc"
mount -t sysfs "$DESTI/sys" "$DESTI/sys"

dialog --title "$real_title" --gauge "$configuring" $height $width 0 &

#system config
sh "$pathinstaller/scripts/install-sysconfig" >>$logfile 2>&1
dialog --title "$real_title" --gauge "$configuring" $height $width 16 &

#config root user
sh "$pathinstaller/scripts/install-root_passwd" >>$logfile 2>&1
dialog --title "$real_title" --gauge "$configuring" $height $width 32 &

#load user passwords
. $plantillapasswd

#if home exist of default system user, do not create it
if [ ! -e "$DESTI/home/$login" ]; then
	echo "crea_home=\"creahome_si\"" >> $plantilla
	crea_home="creahome_si"
else
	echo "crea_home=\"creahome_no\"" >> $plantilla
	crea_home="creahome_no"
fi


#initial config normal user
echo "$login:$passwd:1000:100:$nom:/home/$login:/bin/bash" > "$DESTI/var/tmp/usu.txt"
chroot "$DESTI" "/usr/sbin/newusers" "/var/tmp/usu.txt" >>$logfile 2>&1
rm -f "$DESTI/var/tmp/usu.txt" >>$logfile 2>&1

if [ "$crea_home" = "creahome_si" ]; then
	mkdir -p "$DESTI/home/$LOGIN"
	cp -a $inicial/home/kademar/* "$DESTI/home/$LOGIN"
	cp -a $inicial/home/kademar/.??* "$DESTI/home/$LOGIN"
fi
dialog --title "$real_title" --gauge "$configuring" $height $width 48 &

#finish config normal user
sh "$pathinstaller/scripts/install-usuaris" >>$logfile 2>&1

if [ "$login" != "kademar" ]; then
	rm -fr "$DESTI/home/kademar"
fi
dialog --title "$real_title" --gauge "$configuring" $height $width 64 &


#config booot system- part1
sh "$pathinstaller/scripts/install-bootloader" >>$logfile 2>&1
dialog --title "$real_title" --gauge "$configuring" $height $width 80 &

#config booot system - part2
sh "$pathinstaller/scripts/make-grub_menu" >>$logfile 2>&1
dialog --title "$real_title" --gauge "$configuring" $height $width 96 &

sh "$pathinstaller/scripts/install-bootloader-final" >>$logfile 2>&1

dialog --title "$real_title" --gauge "$finishing" $height $width 100 &

if [ -e "$DESTI/usr/share/kademar/install.log.tar.gz" ]; then
	rm -f "$DESTI/usr/share/kademar/install.log.tar.gz"
fi

tar cfz "$DESTI/usr/share/kademar/install.log.tar.gz" "/tmp/kademar*" "/tmp/particions*" "/tmp/instalador-environment" "/tmp/particio_swap" "/var/xserver" "/var/xsession*" "/var/es" "/var/en" "/var/ca" "/etc/environment" "/etc/kademar-release" "/usr/share/kademar/config*" "/var/kademar*" "$DESTI/boot/grub/menu.lst" 2>/dev/null
chmod 400 "$DESTI/usr/share/kademar/install.log.tar.gz"
chown root:root "$DESTI/usr/share/kademar/install.log.tar.gz"

#desmunta els directoris si existeixen per una fallida de l'instalador
for i in `cat /proc/mounts | grep "$DESTI" | awk ' { print $2 } ' | sort -r`; do umount $i; done

#Muntem sistemes de fitxers virtuals
umount "$DESTI/dev" "$DESTI/proc" "$DESTI/proc" 2>/dev/null

#desmunta els directoris si existeixen per una fallida de l'instalador - FORÇAT
for i in `cat /proc/mounts | grep "$DESTI" | awk ' { print $2 } ' | sort -r`; do umount -l $i; done

#Tornem a desmuntaro x tal d'assegurar-nos - FORÇAT
umount -l "$DESTI/dev" "$DESTI/proc" "$DESTI/proc" 2>/dev/null


dialog --title "$real_title" --defaultno --yesno "$finished" $height $width
if [ "$?" = 0 ]; then
	reboot
fi
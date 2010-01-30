#!/bin/bash

[ "$UID" != 0 ] && echo "NEED TO BE ROOT" && exit
# set -x
kver=`uname -r`
krev=`dpkg -l linux-image-$kver | grep -i linux | awk ' { print $3 } '`

echo
echo
echo "###############################################################"
echo
echo " * Preparing Headers for Kernel $kver Revision $krev  *"
echo
echo "###############################################################"
echo
echo


if [ -e "/usr/src/linux-$kver/.config" -a "$1" != "--force" ]; then
	echo "Kernel Headers for version $kver Revision $krev Already Installed"
	echo
	echo "Use  '--force' option to force it!"
	exit
fi


echo "Be sure to have Internet Connection!!!!"
echo
echo -n "Begins in "
for i in 2 1 Now\!
do
echo -n "$i "
sleep 1
done



echo
echo
echo


rm -fr /tmp/$kver-$krev/install.sh
mkdir -p /tmp/$kver-$krev
cd /tmp/$kver-$krev
wget http://packages.kademar.org/kernel/$kver-$krev/install.sh 2>/dev/null


if [ -e install.sh -a -s install.sh ];then

	sh install.sh

else

	echo "No kernel headers found for $kver - $krev"
fi



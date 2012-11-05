#!/bin/sh
#
# Creat per Adonay Sanz Alsina - 22 Abril 09

# Script to grep all system information needed by installer
#   previous this part was on installer starter, but was so slow to start installer


#sudo python /usr/kademar/utils/instalador_utils/canvi_lilo.py 1
#sh /usr/share/kademar/utils/kademarcenter/scripts/update_fstab >>/tmp/kademar-install.log 2>&1  #old regenerapc
sh /usr/share/kademar/utils/instalador/scripts/linux-arrancables >>/tmp/kademar-install.log 2>&1 #copia linux arrancables
cd /usr/share/kademar/utils/instalador
swapoff -a
umnt-kademar >>/tmp/kademar-install.log 2>&1
os-prober > /tmp/particions-arrancables 2>&1
chmod 777 /tmp/particions* 2>&1
#sh /usr/share/kademar/utils/instalador/scripts/particions-arrancables2 >>/tmp/kademar-install.log 2>&1
#!/bin/bash
#set -x
#Execute only from  makefile of kademar-base

echo "##################################################"
echo "###   KADEMARCENTER  IvMan Module + kademarStart ###"
echo "##################################################"

#Si s'ha executat des del makefile, entra a la carpeta correcta
[ "$0" = "../../kademarcenter/prepare.sh" ] && cd ../../kademarcenter && echo "execucio des de makefile"

#Prepare form
for i in kademarcenter usbtray hotplugactions usbtray_warn kademarstart settings
do
    pyuic4 ui/$i.ui > ui_$i.py
done

#Prepare Translation
pylupdate4 kademarcenter.project

#Release translation
lrelease-qt4 kademarcenter.project

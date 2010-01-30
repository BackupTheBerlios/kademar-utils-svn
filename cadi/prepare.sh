#!/bin/bash

#Execute only from  makefile of kademar-base

echo "#################"
echo "###   CADI 5  ###"
echo "#################"

#Si s'ha executat des del makefile, entra a la carpeta correcta
[ "$0" = "../../cadi/prepare.sh" ] && cd ../../cadi

#Prepare form
for i in ui/*
do
    pyuic4 $i > ui_`echo $i | sed s·ui/··g | sed s·.ui··g`.py
done

#Prepare Translation
pylupdate4 cadi.project

#Release translation
lrelease-qt4 cadi.project

rm -f todo

rm -f nohup.out
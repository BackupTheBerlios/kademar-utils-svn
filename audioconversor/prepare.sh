#!/bin/bash

#Execute only from  makefile of kademar-base

echo "###########################"
echo "###   AudioConversor 5  ###"
echo "###########################"

#Si s'ha executat des del makefile, entra a la carpeta correcta
[ "$0" = "../../audioconversor/prepare.sh" ] && cd ../../audioconversor

#Prepare form
for i in ui/*
do
    pyuic4 $i > ui_`echo $i | sed s·ui/··g | sed s·.ui··g`.py
done

#Prepare Translation
pylupdate4 audioconversor.project

#Release translation
lrelease-qt4 audioconversor.project
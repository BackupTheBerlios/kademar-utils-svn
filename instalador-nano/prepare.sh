#!/bin/bash

#Execute only from  makefile of kademar-base

echo "############################"
echo "###   INSTALADOR 5 NANO  ###"
echo "############################"

#Si s'ha executat des del makefile, entra a la carpeta correcta
[ "$0" = "../../instalador-nano/prepare.sh" ] && cd ../../instalador-nano

#Prepare form
pyuic4 ui/instalador.ui > ui_instalador.py

#Prepare Translation
pylupdate4 instalador.project

#Release translation
lrelease-qt4 instalador.project

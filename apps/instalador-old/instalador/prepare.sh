#!/bin/bash

#Execute only from  makefile of kademar-base

echo "########################"
echo "###   INSTALADOR 5   ###"
echo "########################"

#Si s'ha executat des del makefile, entra a la carpeta correcta
[ "$0" = "../../instalador/prepare.sh" ] && cd ../../instalador

#Prepare form
python2-pyuic4 ui/instalador.ui > ui_instalador.py

#Prepare Translation
lupdate instalador.pro

#Release translation
lrelease instalador.pro
#!/bin/bash

#Execute only from  makefile of kdemar-base

echo "#################"
echo "###   rahisi  ###"
echo "#################"

#Prepare form
pyuic4 rahisi.ui > ui_rahisi.py

#Prepare Translation
pylupdate4 rahisi.pro

#Release translation
lrelease rahisi.pro

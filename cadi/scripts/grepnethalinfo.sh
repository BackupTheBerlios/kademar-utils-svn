#!/usr/bin/bash

#
#  Script per obtenir informacio utilitzant hal/dbus
#  Funcio que altres utilitzen, però la utiltzen embebbed 
#  Adonay Sanz Alsina   -  21-03-08  - GNU/GPL v 2.0 or higer
#


# $1 = /dev/sda4  (dispositiu a analitzar)
# $2 = dvd/label/product  (informacio a obtenir)
# set -x

#############################
# FUNCTION GREP HAL INFO    #
#############################

halinfovar=""

#Si el que volem es la informacio del DVD, treiem els CDs introduits en les unitats
udi="`hal-find-by-property --key net.interface --string $1 2>/dev/null`"

case "$2" in

product)
udi="`hal-get-property --udi $udi --key info.parent`"
	key="info.product"
;;

vendor)
udi="`hal-get-property --udi $udi --key info.parent`"

	key="info.vendor"
;;

parent)
        key="info.parent"
;;

*)  #Si no es reconegut, utilitzal tal qual
	key=$2
;;
esac

#Si s'ha localitzat el udi i la key, busca la info en questio (pq no retorni coses rares)
[ -n "$key" -a -n "$udi" ] && halinfovar="`hal-get-property --udi $udi --key  $key`"

#I si ha trobat la info, posteja la variable
[ -n "$halinfovar" ] && echo "$halinfovar"
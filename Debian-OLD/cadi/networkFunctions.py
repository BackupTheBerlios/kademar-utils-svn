#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
 
#
# File with network dedicated functions
# 
# Adonay Jonay Sanz Alsina
# 03-02-09
# 29-06-09
# 

from commands import getoutput
from os import system

#This function returns a list with:
#    reversed=False  -> lines about an specified interface       (grep)
#    reversed=True   -> lines NON about an specified interface   (grep-v)
def grepNetInterfaceLines(eth, reversed=None):
        interfacesFile='/etc/network/interfaces'
        f=open(interfacesFile,'r')
        llista=f.readlines()
        f.close()
        global whiteSpace, reversedList
        found=whiteSpace=nomore=False
        deviceSettings=[]   #this will store lines talking about the specified interface     (grep)
        reversedList=[]     #this will store lines NOT talking about the specified interface (grep -v)

        for i in llista:
            if not found and not nomore:
                if i.find("auto")>=0 or i.find("allow-hotplug")>=0:
                    if i.find(eth)>=0:
                        found=True
                        #print "found primer", i
                    else:
                        #we store lines NOT talking about specified interface to the reversed list
                        writeLine(i)
                        print 1
                else:
                    #we store lines NOT talking about specified interface to the reversed list
                    writeLine(i)
                    print 2
            else:
                if not nomore: #if I don't have finished
                    if i.find("auto")>=0 or i.find("allow-hotplug")>=0:
                        #print "ja esta"
                        #we store lines NOT talking about specified interface to the reversed list

                        writeLine(i)
                        nomore=True
                        #we have found another interface, not process more lines
                    else:
                        #we store lines about the specified interface
                        deviceSettings.append(i)
                else:
                    #we store lines NOT talking about specified interface to the reversed list
                    writeLine(i)
                    print 3  # append directly, cause aren't about  the interface we want to configure

        #finaly return desired list
        if reversed:
            return reversedList
        else:
            return deviceSettings


def writeLine(i):
    #write Line on reversedList, preserving ONLY one space, by stripping differences of two or more "enters" between lines of /etc/network/interfaces
    global reversedList, whiteSpace
    if i.strip()=="" and not whiteSpace:
        whiteSpace=True
        reversedList.append(i)
    elif i.strip()=="" and whiteSpace:
        pass
    elif not i.strip()=="" and whiteSpace:
        whiteSpace=False
        reversedList.append(i)
    else:
        reversedList.append(i)

#Returns information about desired Ethernet (using HAL)
def grepNetInterfaceInformation(eth, desired):
    from commands import getoutput

    if desired=="vendor":
        return getoutput("sh scripts/grepnethalinfo.sh "+eth+" vendor 2>/dev/null")

    if desired=="product":
        return getoutput("sh scripts/grepnethalinfo.sh "+eth+" product 2>/dev/null")

#Returns a list with current network interfaces
def getNetworkDevices():
    return getoutput("ls /sys/class/net/ --ignore=lo --ignore=*master* --ignore=sit0").split()


#Script to down wired interfaces not connected
def ifdown_wired_network():
    system("""for i in `ls /sys/class/net/ --ignore=lo --ignore=*master*`; do if [ ! -e "/sys/class/net/$i/wireless" ]; then [ "`cat /sys/class/net/$i/carrier 2>/dev/null`" = 0 ] && ifdown $i 2>/dev/null; fi;  done""")
    

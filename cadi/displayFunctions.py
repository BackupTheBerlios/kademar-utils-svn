#!/usr/bin/python
# -*- coding: utf-8 -*-


def grepSubSectionLines( reversed=None):
        interfacesFile='/etc/X11/xorg.conf'
        f=open(interfacesFile,'r')
        llista=f.readlines()
        f.close()
        found=nomore=False
        deviceSettings=[]   #this will store lines talking about the specified interface     (grep)
        reversedList=[]     #this will store lines NOT talking about the specified interface (grep -v)
        reversedList2=[]

        for i in llista:
            if not found and not nomore:
                if i.find('DefaultDepth')>=0:
                        found=True
                        #print "found primer", i
                else:
                    #we store lines NOT talking about specified interface to the reversed list
                    reversedList.append(i)
            else:
                if not nomore: #if I don't have finished
                    if i.find('EndSection')>=0:
                        #print "ja esta"
                        #we store lines NOT talking about specified interface to the reversed list
                        reversedList2.append(i)
                        nomore=True
                        #we have found another interface, not process more lines
                    else:
                        #we store lines about the specified interface
                        deviceSettings.append(i)
                else:
                    #we store lines NOT talking about specified interface to the reversed list
                    reversedList2.append(i)  # append directly, cause aren't about  the interface we want to configure

        #finaly return desired list
        if reversed:
            return reversedList, reversedList2
        else:
            return deviceSettings

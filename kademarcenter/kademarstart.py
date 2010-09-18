#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from PyQt4 import uic

from kademarstart_kademarcenter import *

global config
load_config()
##if there's a argument process it
if len(sys.argv)>1:
    #If the first argument is NOT -session (kde autostart) execute it
    if not sys.argv[1]=="-session":
        print "treta comprobacio"
        app = QApplication(sys.argv)
        kademarstart = kademarstart()
        kademarstart.show()
        app.exec_()
    #else prevent start twice
    else:  #STOP
        print "Not starting, it's a KDE session autoload"
        sys.exit()
else:
#if no args, read config
   #if in config does not talk about it, start it
    standalone=True
    app = QApplication(sys.argv)
    kademarstart = kademarstart("standalone")
    kademarstart.show()
    app.exec_()

#!/usr/bin/python
#-*- coding: iso-8859-15 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from commands import getoutput
from os import path, system, listdir

#import funcions_k

from displayFunctions import grepSubSectionLines

from ui_display import Ui_FormDisplay as Ui_Form

class panelDisplay(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        global tipus
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pages.setCurrentIndex(0)
        self.forcedResolutions=[ "2048x1536", "1920x1440", "1920x1200", "1856x1392", "1800x1440", "1792x1344", "1680x1050", "1600x1200", "1440×900", "1400x1050", "1280x1024", "1280x960", "1280x800", "1280x768", "1280x720", "1280x480", "1152x864", "1024x768", "848x480", "800x600", "768x576", "720x576", "720x480", "720x400", "640x960", "640x480" ]

#####  SIGNAL & SLOTS  #####
        self.connect(self.ui.b_sortir, SIGNAL("clicked()"), self.close)
        self.connect(self.ui.b_SaX, SIGNAL("clicked()"), self.SaveAndExit)
        #self.connect(self.ui.le_pin, SIGNAL("textEdited (const QString&)"), self.enableSaX)
        self.connect(self.ui.cb_depth, SIGNAL("currentIndexChanged (const QString&)"), self.enableSaX)
        self.connect(self.ui.cb_dpi, SIGNAL("currentIndexChanged (const QString&)"), self.enableSaX)
        self.connect(self.ui.sldr_resol, SIGNAL("valueChanged (int)"), self.sliderResolutionValue)
        self.connect(self.ui.cb_forceResol, SIGNAL("stateChanged (int)"), self.func_cb_force_resol)


#### END SIGNAL & SLOTS ####

        self.reloadParameters()

    def sliderResolutionValue(self, value):
        self.enableSaX()
        self.ui.l_resolution.setText(str(self.actualResolutions[value]))

    def enableSaX(self):
        self.ui.b_SaX.setEnabled(True)

    def SaveAndExit(self):
    #Change Resolution
        if self.ui.cb_forceResol.isChecked():
            self.wantToForce=True
        else:
            self.wantToForce=False
        self.warn=False
        self.resolToSwitch=self.actualResolutions[self.ui.sldr_resol.value()]
        if not str(self.resolToSwitch)==str(self.currentResolution):
            if QMessageBox.critical(self, self.tr("Display Resolution Change"), self.tr("It's going to change display resolution. If it don't appear correctly, do not touch anything. In 10 second will be back to previous resolution.") , QMessageBox.No, QMessageBox.Ok) == QMessageBox.Ok:
                system("xrandr -s "+self.resolToSwitch)
                self.dialogRevertResolution()
    #Change Depth
        if str(self.currentDepth)<>str(self.ui.cb_depth.currentText()).split()[0]:
            #print "change depth"
            self.warn=True
            self.saveDepth()

    #Change depth
        if self.currentDPI<>self.dpiDefinition[self.ui.cb_dpi.currentIndex()]:
            #print "changeDPI"
            self.warn=True
            self.saveDpi()

    #show warn message
        if self.warn:
            QMessageBox.information(self, self.tr("Restart Needed"), self.tr("You have changed some parameters that needs a sesion restart to aply it.") , QMessageBox.Ok)
        #self.close()

        self.reloadParameters()


    def setDesiredResolutions(self):
        self.ui.sldr_resol.setMaximum(len(self.actualResolutions)-1)
        #put current resol
        for i in range(len(self.actualResolutions)):
            if self.actualResolutions[i]==self.currentResolution:
                self.ui.sldr_resol.setValue(i)
                self.sliderResolutionValue(i)
                break

    def func_cb_force_resol(self):
        self.enableSaX()
        if self.ui.cb_forceResol.isChecked():
            self.actualResolutions=self.forcedResolutions
        else:
            self.actualResolutions=self.resolutionAvailables
        self.setDesiredResolutions()

    def dialogRevertResolution(self):
        self.a=RevertResolution()
        self.connect(self.a, SIGNAL("revert"), self.revertResolution)
        self.connect(self.a, SIGNAL("counter"), self.putCounter)
        self.ui.pages.setCurrentIndex(1)
        self.connect(self.ui.b_ok, SIGNAL("clicked ()"), self.acceptResolution)
        self.connect(self.ui.b_restore, SIGNAL("clicked ()"), self.revertResolution)
        self.a.start()


    def revertResolution(self):
         system("xrandr -s "+self.currentResolution)
         self.ui.pages.setCurrentIndex(0)
         self.reloadParameters()

    def acceptResolution(self):
        self.a.stop()
        self.ui.pages.setCurrentIndex(0)
        self.currentResolution=getoutput("xrandr -q 2>/dev/null  | grep -i \* | awk ' { print $1 } '")
        self.saveResolution()
        self.setDesiredResolutions()
        self.ui.b_SaX.setEnabled(0)

    def putCounter(self, num):
        self.ui.l_countdown.setText(str(num))
        if str(num)=="1":
            self.ui.l_seconds.setText(self.tr("Second"))

    def saveResolution(self):
        height=self.currentResolution.split("x")[1]
        width=self.currentResolution.split("x")[0]

        lista=[]
        lista.append("[Display]\n")
        lista.append("ApplyOnStartup=true\n")
        lista.append("SyncTrayApp=true\n")
        lista.append("\n")
        lista.append("[Screen0]\n")
        lista.append("height="+height+"\n")
        lista.append("width="+width+"\n")

        file="kcmrandrrc"

        for i in listdir("/home/"):
            if i.lower()<>"pc":
                directory="/home/"+i+"/.kde/share/config/"

                system("mkdir "+directory+" -p")
                f=open(directory+file,'w')
                f.writelines(lista)
                f.close()

                #fix perms
                system("chown "+i+":users "+directory+file)

        lista=grepSubSectionLines("reversed")
        xorgfile="/etc/X11/xorg.conf"
        self.depthToSwitch=str(self.ui.cb_depth.currentText()).split()[0]

        #print self.wantToForce
        if self.wantToForce:
            #print "saving config"
            f=open(xorgfile,'w')
            f.writelines(lista[0])
            f.writelines('    DefaultDepth   '+self.depthToSwitch+'\n')
            f.writelines('    SubSection "Display"\n')
            f.writelines('        Depth       '+self.depthToSwitch+'\n')
            f.writelines('        Modes       "'+self.resolToSwitch+'"\n')
            f.writelines("    EndSubSection\n")
            f.writelines(lista[1])
            f.close()
     #save with autodetection
        else:
            #print "not saving config"
            if not self.forcedResol=="":
                #print "removing old config"
                f=open(xorgfile,'w')
                f.writelines(lista[0])
                f.writelines('    DefaultDepth   '+self.depthToSwitch+'\n')

                f.writelines(lista[1])
                f.close()
        


    def saveDepth(self):
        self.depthToSwitch=str(self.ui.cb_depth.currentText()).split()[0]
        system('sed s:"`grep defaultdepth /etc/X11/xorg.conf -i 2>/dev/null`":"    DefaultDepth '+str(self.depthToSwitch)+'":g -i /etc/X11/xorg.conf')


    def saveDpi(self):
        self.dpiToSwitch=self.dpiDefinition[self.ui.cb_dpi.currentIndex()]
        system('sed s-"`grep Xft.dpi /etc/X11/Xresources/x11-common`"-"Xft.dpi: '+str(self.dpiToSwitch)+'"-g -i /etc/X11/Xresources/x11-common')
        if not getoutput("grep Xft.dpi /etc/X11/Xresources/x11-common -i 2>/dev/null"):
            system("echo Xft.dpi:"+str(self.dpiToSwitch)+" >> /etc/X11/Xresources/x11-common")


    def reloadParameters(self):
        self.ui.b_SaX.setEnabled(False)
        
        self.forcedResol=getoutput("""for i in `grep Modes /etc/X11/xorg.conf 2>/dev/null | grep -v \#  | awk ' { print $2 } '`; do echo $i; break; done""").replace('"','').strip()
        #print self.forcedResol
        self.resolutionAvailables=getoutput("xrandr -q 2>/dev/null | awk ' { print $1 } ' | grep -i x").split()

        if self.forcedResol<>"":
         #There's a forced resol
            #print "there's a forced resolution", self.forcedResol
            self.currentResolution=self.forcedResol
            #this variable store what resolutions we are using. If forced or autodetected
            self.actualResolutions=self.forcedResolutions
            self.ui.cb_forceResol.setChecked(1)

        else:
            #print "autodetecting resolution"
         #detect it
            self.currentResolution=getoutput("xrandr -q 2>/dev/null  | grep -i \* | awk ' { print $1 } '")
        #this variable store what resolutions we are using. If forced or autodetected
            self.actualResolutions=self.resolutionAvailables
            self.ui.cb_forceResol.setChecked(0)


        self.setDesiredResolutions()

        #get current depth
        self.currentDepth=getoutput("grep DefaultDepth /etc/X11/xorg.conf -i 2>/dev/null  | grep -v \# | awk ' { print $2 } '")
        if not self.currentDepth:
            self.currentDepth="24"

        if int(self.currentDepth)==24:
            self.ui.cb_depth.setCurrentIndex(0)
        else:
            self.ui.cb_depth.setCurrentIndex(1)

        #get current DPI
        self.currentDPI=getoutput("grep Xft.dpi /etc/X11/Xresources/x11-common 2>/dev/null | grep -v \# | cut -d: -f2")
        self.dpiDefinition=[130, 110, 90, 70, 50]
        if not self.currentDPI:
            self.cur=0
            #print "aqui"
        else:
            if int(self.currentDPI)>=130:
                self.cur=0
            elif int(self.currentDPI)>=110:
                self.cur=1
            elif int(self.currentDPI)>=90:
                self.cur=2
            elif int(self.currentDPI)>=70:
                self.cur=3

            else:
                self.cur=4

        #set current DPI with rational parameters
        self.currentDPI=self.dpiDefinition[self.cur]
        self.ui.cb_dpi.setCurrentIndex(self.cur)

class RevertResolution(QThread):

    def __init__(self):
        QThread.__init__(self)
        #self.run()
        self.countdown=True
        self.counter=10

    def run(self):
        from time import sleep

        for i in reversed(range(self.counter)):
            if self.countdown:
                if not i==0:
                    self.emit(SIGNAL("counter"), i)
                    sleep(1)
                else:
                    self.emit(SIGNAL("revert"))

    def stop(self):
        self.countdown=False
        self.terminate()
#app = QApplication(sys.argv)
#preferencies = preferencies()
#preferencies.show()
#app.exec_()
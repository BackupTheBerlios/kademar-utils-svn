from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from os import system
#import platform
import resource
#from os import listdir

import caditray.notification
import caditray.connects
import caditray.tray
import caditray.daemon
import caditray.common
import caditray.update
import caditray.dbus
import caditray.gui
import caditray.config

#import dbus


class cadiTray(caditray.tray.cadiTray, caditray.daemon.cadiTray, caditray.connects.cadiTray, caditray.notification.cadiTray, caditray.common.cadiTray, caditray.update.cadiTray, caditray.dbus.cadiTray, caditray.gui.cadiTray, caditray.config.cadiTray,QMainWindow):
    def __init__(self,app):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi("/usr/share/caditray/caditray.ui", self)
        #self.dbus=dbus
        #self.initDbus()  #Nothing now. On main.py
        
        self.initDaemon()
        self.prepareConfig()
    
        #self.widget=widget
        self.app=app
        self.imagepath="/usr/share/caditray/img/"
        self.prepareGui()
        
        self.initTray()
        self.initNotify()
        self.initConnects()
        self.initUpdate()

        self.connectToDaemon()
        self.firstCheckUpdates()
        self.putInformationOnGui()

        #self.sendNotify("CADI", self.tr("%1 packages available to update"), self.interfaceDaemon.queryPackagesToUpdate())

#Set visible/invisible main window
    def mainwindow(self):
        self.ui.setVisible( not self.ui.isVisible() )

#Click events on tray icon
    def eventsdeltray(self, arEvent):
       #Left button click
       if arEvent == self.tray.Trigger:
          self.mainwindow()

#Close event of window
    def closeEvent(self, event):
        event.ignore()
        self.mainwindow()

#Ask for a real exit of App
    def askForExit(self):
        oldState=self.isVisible()
        self.setVisible(True)
        if not self.updatingSystem:
            self.setVisible(True)
            #preg = QMessageBox.critical(self, self.tr("Exit from CADI Systray"), self.tr("Do you want to exit from CADI Systray Applet?"), QMessageBox.Yes| QMessageBox.No,  QMessageBox.No)
            preg = self.showWarningMessage("infopreg", self.tr('Exit from CADI Systray'), self.tr('Do you want to exit from CADI Systray Applet?'))
            if preg == QMessageBox.Yes:
                #self.stopServer()
                self.app.processEvents()
                #Try to close daemon. If isn't, continue
                try:
                    self.interfaceDaemon.shutdownService() #Shutdown Daemon
                except:
                    pass
                #self.app.stop.waitForFinished()
                self.app.quit()
        else:
            preg = self.showWarningMessage("critical", self.tr('Unable to exit from CADI Systray'), self.tr('The system is upgrading, you cannot exit until it finish.'))
        self.setVisible(oldState)
         

    def execShellProcess(self, idCommand, idParam = "", idParam2 = ""):
        #Execute a shell order and return the result
        # for pipe commands use idCommand="/bin/bash" idParam="-c" idParam2="shell | piped command"
        param=[]
        if idParam:
            param.append(idParam)
        if idParam2:
            param.append(idParam2)
        proc = QProcess()
        proc.start(idCommand, param)
        proc.waitForFinished()
        result = proc.readAll()
        #self.logMessage(str(result))
        proc.close()
        return str(result)
     
    def fileChangedSlot(self):
        self.sendNotify(self.tr('CADI Systray Applet Updated'),self.tr('It has been updated, you should reboot the Kademar CADI Systray Applet to get the new features.'))
        self.fileWatcher.blockSignals(True)
 
     

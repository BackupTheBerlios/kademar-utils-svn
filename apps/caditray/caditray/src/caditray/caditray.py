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


class cadiTray(caditray.tray.cadiTray, caditray.connects.cadiTray, caditray.notification.cadiTray, QMainWindow):
    def __init__(self,app):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi("/usr/share/caditray/caditray.ui", self)
        #self.lampstackVersion="5.4.11-0"
        #self.widget=widget
        self.app=app
        self.imagepath="/usr/share/caditray/img/"

        self.initTray()
        #self.initNotify()
        self.initConnects()
        

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
        preg = QMessageBox.critical(self, self.tr("Exit from Kademar Bitnami Control Panel"), self.tr("Do you want to exit from Kademar Bitnami Control Panel and Stop the Bitnami Server?"), QMessageBox.Yes| QMessageBox.No,  QMessageBox.No)
        if preg == QMessageBox.Yes:
            #self.stopServer()
            self.app.processEvents()
            #self.app.stop.waitForFinished()
            self.app.quit()

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
        self.sendNotify(self.tr("Bitnami Control Updated"),self.tr("It has been updated, you should reboot the Kademar Bitnami Control Panel to get the new features."))
        self.fileWatcher.blockSignals(True)
 
     

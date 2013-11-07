#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow
from os import path
from socket import socket, AF_INET, SOCK_STREAM

class cadiTray(QMainWindow):

    def isLiveCd(self):
        if path.exists("/run/archiso/bootmnt/"):
            return True
        else:
            return False
        

    def showWarningMessage(self, wantedType, miss1, miss2):
        #Show dialog function
        if wantedType=="critical":
            QMessageBox.critical(self, miss1, miss2, QMessageBox.Ok)
        if wantedType=="warning":
            return QMessageBox.critical(self, miss1, miss2, QMessageBox.Retry, QMessageBox.Ignore)
        if wantedType=="infopreg":
            return QMessageBox.critical(self, miss1, miss2, QMessageBox.Yes| QMessageBox.No,  QMessageBox.No)
        if wantedType=="info":
            QMessageBox.critical(self, miss1, miss2, QMessageBox.Ok)    
            
    def checkInternetConnection(self):
        self.internet=0
        testConn=socket(AF_INET,SOCK_STREAM)
        try:
            testConn.connect(('www.kademar.org',80))
            testConn.close()
            self.internet=1
            #self.setWindowTitle('Gestion Freetec - Conexión al Servidor - Internet')
        except:
            testConn.close()
            self.internet=0
        return self.internet
      
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
        return result
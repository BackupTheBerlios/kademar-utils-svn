#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
#from PyQt4 import *
from PyQt4.QtCore import *
#from gui1 import Ui_MainWindow

class instalador(QMainWindow):

    def toggleDebugVisibility(self):
        state=not(self.ui.FDebug.isVisible())
        
        if state==True:
            self.updateDebugLines()
        
        self.ui.FDebug.setVisible(state)
        
    def updateDebugLines(self):
        while not self.debugStream.atEnd():
            line = self.debugStream.readLine() # //read one line at a time
            self.ui.LWDebug.addItem(line)


    def prepareDebugLogFile(self):
        self.debugFileWatcher=QFileSystemWatcher()
        self.debugFileWatcher.addPath(self.logFile)
  
        self.debugFile=QFile(self.logFile)
        self.debugFile.open(QIODevice.ReadOnly | QIODevice.Text)
  
        self.debugStream = QTextStream(self.debugFile)
        self.connect(self.debugFileWatcher, SIGNAL("fileChanged(const QString&)"), self.fileChangedSlot)
 
 
    def fileChangedSlot(self):
        #print("event")

        while not self.debugStream.atEnd():
            line = self.debugStream.readLine() # //read one line at a time
            self.ui.LWDebug.addItem(line)
        
#def test(event):
    #if event.key() == QtCore.Qt.Key_Delete:
        #print "delete"
    #return QtGui.QTableWidget.keyPressEvent(table, event)
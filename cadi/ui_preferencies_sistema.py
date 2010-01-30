# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/preferencies_sistema.ui'
#
# Created: Sat Dec 26 04:03:35 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FormPreferencies(object):
    def setupUi(self, FormPreferencies):
        FormPreferencies.setObjectName("FormPreferencies")
        FormPreferencies.resize(800,600)
        FormPreferencies.setMinimumSize(QtCore.QSize(800,600))
        self.label_2 = QtGui.QLabel(FormPreferencies)
        self.label_2.setGeometry(QtCore.QRect(-1,0,800,600))
        self.label_2.setMinimumSize(QtCore.QSize(800,600))
        self.label_2.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/bg/cadi.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.pageWidget = QtGui.QStackedWidget(FormPreferencies)
        self.pageWidget.setGeometry(QtCore.QRect(240,70,491,481))
        self.pageWidget.setObjectName("pageWidget")
        self.software = QtGui.QWidget()
        self.software.setObjectName("software")
        self.label_4 = QtGui.QLabel(self.software)
        self.label_4.setGeometry(QtCore.QRect(19,10,461,21))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label = QtGui.QLabel(self.software)
        self.label.setGeometry(QtCore.QRect(30,50,441,331))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.groupBox = QtGui.QGroupBox(self.software)
        self.groupBox.setGeometry(QtCore.QRect(150,390,181,81))
        self.groupBox.setObjectName("groupBox")
        self.rb_async = QtGui.QRadioButton(self.groupBox)
        self.rb_async.setGeometry(QtCore.QRect(30,20,131,26))
        self.rb_async.setObjectName("rb_async")
        self.rb_sync = QtGui.QRadioButton(self.groupBox)
        self.rb_sync.setGeometry(QtCore.QRect(30,50,131,26))
        self.rb_sync.setObjectName("rb_sync")
        self.pageWidget.addWidget(self.software)
        self.label_3 = QtGui.QLabel(FormPreferencies)
        self.label_3.setGeometry(QtCore.QRect(20,10,90,90))
        self.label_3.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/kademar.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.b_sortir = QtGui.QPushButton(FormPreferencies)
        self.b_sortir.setGeometry(QtCore.QRect(20,530,131,41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/enrera.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.b_sortir.setIcon(icon)
        self.b_sortir.setObjectName("b_sortir")
        self.b_SaX = QtGui.QPushButton(FormPreferencies)
        self.b_SaX.setGeometry(QtCore.QRect(20,480,131,41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/enrera.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.b_SaX.setIcon(icon)
        self.b_SaX.setObjectName("b_SaX")

        self.retranslateUi(FormPreferencies)
        self.pageWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FormPreferencies)

    def retranslateUi(self, FormPreferencies):
        FormPreferencies.setWindowTitle(QtGui.QApplication.translate("FormPreferencies", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FormPreferencies", "System Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FormPreferencies", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Mainly there\'s two ways to save data on USB devices</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">  · aSync: Desynchronous Mode </span><span style=\" font-weight:600; font-style:italic;\">(Recomended)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    Using this mode, you have to use the USB manager to unplug the USB device (that appears on the tray, next to clock). It\'s faster than the other mode. It\'s also the mode that uses other Operating Systems.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">  · Sync: Synchronous Mode</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    Using this mode, you can unplug the device afte use it. It\'s slower than the other mode, but it\'s better for people that forgive to use the manager before unplug the devices.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("FormPreferencies", "USB Save Data Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_async.setText(QtGui.QApplication.translate("FormPreferencies", "aSync Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_sync.setText(QtGui.QApplication.translate("FormPreferencies", "Sync Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.b_sortir.setText(QtGui.QApplication.translate("FormPreferencies", "Back", None, QtGui.QApplication.UnicodeUTF8))
        self.b_SaX.setText(QtGui.QApplication.translate("FormPreferencies", "Save && Exit", None, QtGui.QApplication.UnicodeUTF8))


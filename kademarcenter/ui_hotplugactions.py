# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/hotplugactions.ui'
#
# Created: Sat Dec 26 04:03:23 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form_hotplugactions(object):
    def setupUi(self, Form_hotplugactions):
        Form_hotplugactions.setObjectName("Form_hotplugactions")
        Form_hotplugactions.resize(420,370)
        Form_hotplugactions.setMinimumSize(QtCore.QSize(400,350))
        Form_hotplugactions.setMaximumSize(QtCore.QSize(420,370))
        self.label_2 = QtGui.QLabel(Form_hotplugactions)
        self.label_2.setGeometry(QtCore.QRect(0,0,420,370))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/kademarcenter/img/bg/accions.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.boto_fesaccio = QtGui.QPushButton(Form_hotplugactions)
        self.boto_fesaccio.setEnabled(False)
        self.boto_fesaccio.setGeometry(QtCore.QRect(80,310,101,31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.boto_fesaccio.setFont(font)
        self.boto_fesaccio.setObjectName("boto_fesaccio")
        self.boto_sortir = QtGui.QPushButton(Form_hotplugactions)
        self.boto_sortir.setGeometry(QtCore.QRect(250,310,101,31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.boto_sortir.setFont(font)
        self.boto_sortir.setObjectName("boto_sortir")
        self.ch_save = QtGui.QCheckBox(Form_hotplugactions)
        self.ch_save.setGeometry(QtCore.QRect(90,280,231,22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ch_save.setFont(font)
        self.ch_save.setObjectName("ch_save")
        self.listWidget = QtGui.QListWidget(Form_hotplugactions)
        self.listWidget.setGeometry(QtCore.QRect(60,70,301,211))
        self.listWidget.setObjectName("listWidget")
        self.iconamedi = QtGui.QLabel(Form_hotplugactions)
        self.iconamedi.setGeometry(QtCore.QRect(20,10,51,51))
        self.iconamedi.setObjectName("iconamedi")
        self.label = QtGui.QLabel(Form_hotplugactions)
        self.label.setGeometry(QtCore.QRect(80,10,321,41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.retranslateUi(Form_hotplugactions)
        QtCore.QMetaObject.connectSlotsByName(Form_hotplugactions)

    def retranslateUi(self, Form_hotplugactions):
        Form_hotplugactions.setWindowTitle(QtGui.QApplication.translate("Form_hotplugactions", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.boto_fesaccio.setText(QtGui.QApplication.translate("Form_hotplugactions", "D\'Accord", None, QtGui.QApplication.UnicodeUTF8))
        self.boto_sortir.setText(QtGui.QApplication.translate("Form_hotplugactions", "Cancel·la", None, QtGui.QApplication.UnicodeUTF8))
        self.ch_save.setText(QtGui.QApplication.translate("Form_hotplugactions", "Recordar siempre para este tipo", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form_hotplugactions", "Nou Medi Inserit", None, QtGui.QApplication.UnicodeUTF8))


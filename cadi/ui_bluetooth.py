# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/bluetooth.ui'
#
# Created: Sat Dec 26 04:03:33 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FormBluetooth(object):
    def setupUi(self, FormBluetooth):
        FormBluetooth.setObjectName("FormBluetooth")
        FormBluetooth.resize(800,600)
        FormBluetooth.setMinimumSize(QtCore.QSize(800,600))
        self.label_2 = QtGui.QLabel(FormBluetooth)
        self.label_2.setGeometry(QtCore.QRect(0,0,800,600))
        self.label_2.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/bg/cadi.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.pageWidget = QtGui.QStackedWidget(FormBluetooth)
        self.pageWidget.setGeometry(QtCore.QRect(240,70,491,481))
        self.pageWidget.setObjectName("pageWidget")
        self.software = QtGui.QWidget()
        self.software.setObjectName("software")
        self.label_4 = QtGui.QLabel(self.software)
        self.label_4.setGeometry(QtCore.QRect(9,30,471,21))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label = QtGui.QLabel(self.software)
        self.label.setGeometry(QtCore.QRect(40,80,411,41))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.l_logo_blth = QtGui.QLabel(self.software)
        self.l_logo_blth.setGeometry(QtCore.QRect(300,200,121,141))
        self.l_logo_blth.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/bluetooth.png"))
        self.l_logo_blth.setObjectName("l_logo_blth")
        self.groupBox = QtGui.QGroupBox(self.software)
        self.groupBox.setGeometry(QtCore.QRect(70,210,191,121))
        self.groupBox.setObjectName("groupBox")
        self.le_pin = QtGui.QLineEdit(self.groupBox)
        self.le_pin.setGeometry(QtCore.QRect(70,50,81,26))
        self.le_pin.setMaxLength(4)
        self.le_pin.setObjectName("le_pin")
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(19,53,41,20))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.pageWidget.addWidget(self.software)
        self.label_3 = QtGui.QLabel(FormBluetooth)
        self.label_3.setGeometry(QtCore.QRect(20,10,90,90))
        self.label_3.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/kademar.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.b_sortir = QtGui.QPushButton(FormBluetooth)
        self.b_sortir.setGeometry(QtCore.QRect(20,530,131,41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/enrera.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.b_sortir.setIcon(icon)
        self.b_sortir.setObjectName("b_sortir")
        self.b_SaX = QtGui.QPushButton(FormBluetooth)
        self.b_SaX.setGeometry(QtCore.QRect(20,480,131,41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/enrera.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.b_SaX.setIcon(icon)
        self.b_SaX.setObjectName("b_SaX")

        self.retranslateUi(FormBluetooth)
        self.pageWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FormBluetooth)

    def retranslateUi(self, FormBluetooth):
        FormBluetooth.setWindowTitle(QtGui.QApplication.translate("FormBluetooth", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FormBluetooth", "Bluetooth", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FormBluetooth", "You can change the Bluetooth connection PIN to your PC.", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("FormBluetooth", "Bluetooth PIN", None, QtGui.QApplication.UnicodeUTF8))
        self.le_pin.setInputMask(QtGui.QApplication.translate("FormBluetooth", "9999; ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("FormBluetooth", "PIN", None, QtGui.QApplication.UnicodeUTF8))
        self.b_sortir.setText(QtGui.QApplication.translate("FormBluetooth", "Back", None, QtGui.QApplication.UnicodeUTF8))
        self.b_SaX.setText(QtGui.QApplication.translate("FormBluetooth", "Save && Exit", None, QtGui.QApplication.UnicodeUTF8))


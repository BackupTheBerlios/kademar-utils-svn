# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/usbtray.ui'
#
# Created: Sat Dec 26 04:03:23 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form_usbtray(object):
    def setupUi(self, Form_usbtray):
        Form_usbtray.setObjectName("Form_usbtray")
        Form_usbtray.resize(400,350)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form_usbtray.sizePolicy().hasHeightForWidth())
        Form_usbtray.setSizePolicy(sizePolicy)
        Form_usbtray.setMinimumSize(QtCore.QSize(400,350))
        Form_usbtray.setMaximumSize(QtCore.QSize(400,350))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/kademarcenter/img/usbtray_trayicon.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        Form_usbtray.setWindowIcon(icon)
        self.label_3 = QtGui.QLabel(Form_usbtray)
        self.label_3.setGeometry(QtCore.QRect(0,0,400,350))
        self.label_3.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/kademarcenter/img/bg/usbtray.png"))
        self.label_3.setObjectName("label_3")
        self.boto_desconnecta = QtGui.QPushButton(Form_usbtray)
        self.boto_desconnecta.setEnabled(False)
        self.boto_desconnecta.setGeometry(QtCore.QRect(40,300,141,27))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/kademarcenter/img/usbtray_desconecta.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.boto_desconnecta.setIcon(icon)
        self.boto_desconnecta.setIconSize(QtCore.QSize(64,64))
        self.boto_desconnecta.setObjectName("boto_desconnecta")
        self.boto_sortir = QtGui.QPushButton(Form_usbtray)
        self.boto_sortir.setGeometry(QtCore.QRect(220,300,161,27))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/kademarcenter/img/desconfigura.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.boto_sortir.setIcon(icon)
        self.boto_sortir.setIconSize(QtCore.QSize(22,22))
        self.boto_sortir.setAutoRepeat(False)
        self.boto_sortir.setObjectName("boto_sortir")
        self.label = QtGui.QLabel(Form_usbtray)
        self.label.setGeometry(QtCore.QRect(70,10,321,41))
        self.label.setObjectName("label")
        self.listWidget = QtGui.QListWidget(Form_usbtray)
        self.listWidget.setGeometry(QtCore.QRect(55,72,301,200))
        self.listWidget.setFrameShape(QtGui.QFrame.Box)
        self.listWidget.setLineWidth(1)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.listWidget.setObjectName("listWidget")
        self.label_2 = QtGui.QLabel(Form_usbtray)
        self.label_2.setGeometry(QtCore.QRect(20,16,41,31))
        self.label_2.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/kademarcenter/img/usb.png"))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form_usbtray)
        QtCore.QMetaObject.connectSlotsByName(Form_usbtray)

    def retranslateUi(self, Form_usbtray):
        Form_usbtray.setWindowTitle(QtGui.QApplication.translate("Form_usbtray", "USB Device Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.boto_desconnecta.setText(QtGui.QApplication.translate("Form_usbtray", "Disconnect", None, QtGui.QApplication.UnicodeUTF8))
        self.boto_sortir.setText(QtGui.QApplication.translate("Form_usbtray", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form_usbtray", "Select the USB device you want to disconnect\n"
" or extract and click on the button \"Disconnect\"", None, QtGui.QApplication.UnicodeUTF8))


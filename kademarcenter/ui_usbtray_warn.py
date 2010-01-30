# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/usbtray_warn.ui'
#
# Created: Sat Dec 26 04:03:23 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form_Usbtray_Warn(object):
    def setupUi(self, Form_Usbtray_Warn):
        Form_Usbtray_Warn.setObjectName("Form_Usbtray_Warn")
        Form_Usbtray_Warn.resize(500,318)
        font = QtGui.QFont()
        font.setPointSize(12)
        Form_Usbtray_Warn.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/kademarcenter/img/usbtray_trayicon.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        Form_Usbtray_Warn.setWindowIcon(icon)
        self.label = QtGui.QLabel(Form_Usbtray_Warn)
        self.label.setGeometry(QtCore.QRect(19,5,461,91))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setFrameShape(QtGui.QFrame.Box)
        self.label.setFrameShadow(QtGui.QFrame.Plain)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(Form_Usbtray_Warn)
        self.label_2.setGeometry(QtCore.QRect(20,214,451,61))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.b_soritr = QtGui.QPushButton(Form_Usbtray_Warn)
        self.b_soritr.setGeometry(QtCore.QRect(204,273,91,31))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/icons/ok_p.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.b_soritr.setIcon(icon)
        self.b_soritr.setIconSize(QtCore.QSize(22,16))
        self.b_soritr.setObjectName("b_soritr")
        self.label_3 = QtGui.QLabel(Form_Usbtray_Warn)
        self.label_3.setGeometry(QtCore.QRect(12,105,491,111))
        self.label_3.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/kademarcenter/img/usbtray_warn.png"))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Form_Usbtray_Warn)
        QtCore.QObject.connect(self.b_soritr,QtCore.SIGNAL("clicked()"),Form_Usbtray_Warn.hide)
        QtCore.QMetaObject.connectSlotsByName(Form_Usbtray_Warn)

    def retranslateUi(self, Form_Usbtray_Warn):
        Form_Usbtray_Warn.setWindowTitle(QtGui.QApplication.translate("Form_Usbtray_Warn", "Extracció Segura d\'unitat USB", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form_Usbtray_Warn", "ATENCIÓ: S\'ha desconnectat un dispositiu USB, sense haver-lo extret prèviament del sistema. Abans de desconnectar un dispositiu USB per assegurar que les dades queden gravades, s\'ha d\'extraure\'l a través del gestor de dispositius USB, que està al cantó del rellotge.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form_Usbtray_Warn", "Un cop extret amb el gestor de dispositius USB, pots desconnectar-lo de l\'ordinador sense cap perill de perdre les dades gravades en ell.", None, QtGui.QApplication.UnicodeUTF8))
        self.b_soritr.setText(QtGui.QApplication.translate("Form_Usbtray_Warn", "D\'acord", None, QtGui.QApplication.UnicodeUTF8))


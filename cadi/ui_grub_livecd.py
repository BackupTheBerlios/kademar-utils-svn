# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/grub_livecd.ui'
#
# Created: Sat Dec 26 04:03:34 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FormGrub(object):
    def setupUi(self, FormGrub):
        FormGrub.setObjectName("FormGrub")
        FormGrub.resize(800,600)
        FormGrub.setMinimumSize(QtCore.QSize(800,600))
        self.label_2 = QtGui.QLabel(FormGrub)
        self.label_2.setGeometry(QtCore.QRect(0,0,800,600))
        self.label_2.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/bg/cadi.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.pageWidget = QtGui.QStackedWidget(FormGrub)
        self.pageWidget.setGeometry(QtCore.QRect(240,80,491,481))
        self.pageWidget.setObjectName("pageWidget")
        self.software = QtGui.QWidget()
        self.software.setObjectName("software")
        self.label_4 = QtGui.QLabel(self.software)
        self.label_4.setGeometry(QtCore.QRect(9,20,471,21))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label = QtGui.QLabel(self.software)
        self.label.setGeometry(QtCore.QRect(40,80,411,61))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.l_logo_blth = QtGui.QLabel(self.software)
        self.l_logo_blth.setGeometry(QtCore.QRect(300,190,121,141))
        self.l_logo_blth.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/hdd_unmount.png"))
        self.l_logo_blth.setObjectName("l_logo_blth")
        self.groupBox = QtGui.QGroupBox(self.software)
        self.groupBox.setGeometry(QtCore.QRect(60,150,231,211))
        self.groupBox.setObjectName("groupBox")
        self.listWidget = QtGui.QListWidget(self.groupBox)
        self.listWidget.setGeometry(QtCore.QRect(10,30,211,171))
        self.listWidget.setObjectName("listWidget")
        self.checkBox = QtGui.QCheckBox(self.software)
        self.checkBox.setGeometry(QtCore.QRect(60,370,231,41))
        self.checkBox.setObjectName("checkBox")
        self.b_restore = QtGui.QPushButton(self.software)
        self.b_restore.setEnabled(False)
        self.b_restore.setGeometry(QtCore.QRect(70,420,151,30))
        self.b_restore.setObjectName("b_restore")
        self.b_expert = QtGui.QPushButton(self.software)
        self.b_expert.setEnabled(False)
        self.b_expert.setGeometry(QtCore.QRect(260,420,151,30))
        self.b_expert.setObjectName("b_expert")
        self.pageWidget.addWidget(self.software)
        self.label_3 = QtGui.QLabel(FormGrub)
        self.label_3.setGeometry(QtCore.QRect(20,10,90,90))
        self.label_3.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/kademar.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.b_sortir = QtGui.QPushButton(FormGrub)
        self.b_sortir.setGeometry(QtCore.QRect(20,540,131,41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/enrera.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.b_sortir.setIcon(icon)
        self.b_sortir.setObjectName("b_sortir")

        self.retranslateUi(FormGrub)
        self.pageWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FormGrub)

    def retranslateUi(self, FormGrub):
        FormGrub.setWindowTitle(QtGui.QApplication.translate("FormGrub", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FormGrub", "Restore Boot Sector - Grub", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FormGrub", "Boot Sectoy may be deleted when another Operative System where installed. Restore it using this section.", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("FormGrub", "Select for Restore", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("FormGrub", "Do not rebuild menu", None, QtGui.QApplication.UnicodeUTF8))
        self.b_restore.setText(QtGui.QApplication.translate("FormGrub", "Restore Grub", None, QtGui.QApplication.UnicodeUTF8))
        self.b_expert.setText(QtGui.QApplication.translate("FormGrub", "Expert Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.b_sortir.setText(QtGui.QApplication.translate("FormGrub", "Back", None, QtGui.QApplication.UnicodeUTF8))


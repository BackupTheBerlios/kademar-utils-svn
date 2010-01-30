# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/teclats_multimedia.ui'
#
# Created: Sat Dec 26 04:03:35 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FormTeclatsMultimedia(object):
    def setupUi(self, FormTeclatsMultimedia):
        FormTeclatsMultimedia.setObjectName("FormTeclatsMultimedia")
        FormTeclatsMultimedia.resize(800,600)
        FormTeclatsMultimedia.setMinimumSize(QtCore.QSize(800,600))
        self.label_2 = QtGui.QLabel(FormTeclatsMultimedia)
        self.label_2.setGeometry(QtCore.QRect(0,0,800,600))
        self.label_2.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/bg/cadi.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.pageWidget = QtGui.QStackedWidget(FormTeclatsMultimedia)
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
        self.label.setGeometry(QtCore.QRect(30,49,441,81))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.l_logo_blth = QtGui.QLabel(self.software)
        self.l_logo_blth.setGeometry(QtCore.QRect(80,140,321,270))
        self.l_logo_blth.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/kcontrol_teclats.png"))
        self.l_logo_blth.setObjectName("l_logo_blth")
        self.b_keyboard = QtGui.QPushButton(self.software)
        self.b_keyboard.setGeometry(QtCore.QRect(130,430,221,41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/kcontrol.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.b_keyboard.setIcon(icon)
        self.b_keyboard.setIconSize(QtCore.QSize(32,32))
        self.b_keyboard.setObjectName("b_keyboard")
        self.pageWidget.addWidget(self.software)
        self.label_3 = QtGui.QLabel(FormTeclatsMultimedia)
        self.label_3.setGeometry(QtCore.QRect(20,10,90,90))
        self.label_3.setPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/kademar.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.b_sortir = QtGui.QPushButton(FormTeclatsMultimedia)
        self.b_sortir.setGeometry(QtCore.QRect(20,540,131,41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../usr/share/kademar/utils/cadi/img/enrera.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.b_sortir.setIcon(icon)
        self.b_sortir.setObjectName("b_sortir")

        self.retranslateUi(FormTeclatsMultimedia)
        self.pageWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FormTeclatsMultimedia)

    def retranslateUi(self, FormTeclatsMultimedia):
        FormTeclatsMultimedia.setWindowTitle(QtGui.QApplication.translate("FormTeclatsMultimedia", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FormTeclatsMultimedia", "Multimedia Keyboards", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FormTeclatsMultimedia", "You can configure your multimedia keyboard choosing your model on the control panel and then, press \'Apply\'.\n"
"You can start it, using \"Open Control Panel\" bottom button.", None, QtGui.QApplication.UnicodeUTF8))
        self.b_keyboard.setText(QtGui.QApplication.translate("FormTeclatsMultimedia", "Open Control Panel", None, QtGui.QApplication.UnicodeUTF8))
        self.b_sortir.setText(QtGui.QApplication.translate("FormTeclatsMultimedia", "Back", None, QtGui.QApplication.UnicodeUTF8))


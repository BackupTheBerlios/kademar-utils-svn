#!/usr/bin/python
#-*- coding: iso-8859-15 -*-


#############################################
#       -=|  CSS-MIAMI V 2.0  |=-           #
#             .Modulo Editor.               #
#  ---------------------------------------  #
#     Author: Adonay Sanz Alsina            #
#     License: GPL 3.0 or higer             #
#     First Creation Date:  15-07-08        #
#  ---------------------------------------  #
#        Content Editor inside Div          #
#############################################

from PyQt4.QtGui import *
from PyQt4 import uic
from PyQt4.QtCore import *
import sys, os

class visor(QDialog):
    """
    class of editor div content and set properties of text, images, tables, links...
    @signal ok returns text (str)
    """
    def __init__(self,alto,ancho,tamano,texto):
        QDialog.__init__(self)
        self.alt_boton=alto
        self.ancho_boton=ancho
        self.tam_icono=tamano
        self.texto=texto
        uic.loadUi("visor.ui", self)

        self.diricons="/usr/share/icons/default.kde/"+str(self.tam_icono)+"x"+str(self.tam_icono)+"/apps/"

        self.connect(self.b_accept, SIGNAL("clicked()"), self.accept)
        self.connect(self.b_cancel, SIGNAL("clicked()"), self.close)
        self.connect(self.radioButton, SIGNAL("clicked()"), self.activa_programa)
        self.connect(self.radioButton_2, SIGNAL("clicked()"), self.activa_programa)
        self.connect(self.checkBox, SIGNAL("clicked()"), self.activa_texto)
        self.connect(self.comboBox, SIGNAL("activated(int)"), self.pon_programas)
        self.connect(self.listWidget, SIGNAL("itemClicked(QListWidgetItem *)"), self.pon_datos)
        #self.listWidget.itemClicked.connect(self.pon_datos)
        #self.connect(self.comboBox, SIGNAL("activated(int)"), self.pon_datos)
        self.lineEdit.setFocus()

        self.dbL = QSqlDatabase()
        self.dbL = QSqlDatabase.addDatabase("QSQLITE")
        self.dbL.setDatabaseName('rahisi.db')
        self.datos_final=[]
        self.pushButton.resize(self.ancho_boton,self.alt_boton)
        self.checkBox.setChecked(self.texto)
        self.lee_datos_menu()

    def pon_datos(self,codigo):
        self.dbL.open()
        value = self.listWidget.currentItem().text()
        consulta='SELECT * FROM Programas WHERE Nombre_ca="'+value+'" ;'
        self.result=self.dbL.exec_(consulta)
        self.result.first()
        num=self.result.value(0).toInt()[0]
        self.textEdit.setText(self.result.value(7).toString())
        self.lineEdit.setText(self.result.value(4).toString())
        self.lineEdit_2.setText(self.result.value(8).toString())
        dicon=str(self.result.value(9).toString())
        if dicon.find("/"):
            icono=self.diricons+dicon+".png"
        else:
            icono=dicon
        icon = QIcon()
        icon.addPixmap(QPixmap(icono), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)
        if self.checkBox.isChecked():
            self.pushButton.setText(self.result.value(4).toString())
        else:
            self.pushButton.setText("")
        self.datos_final=[self.result.value(0).toInt()[0], self.result.value(1).toString(), self.result.value(2).toString(), self.result.value(3).toString(), self.result.value(4).toString(), self.result.value(5).toString(), self.result.value(6).toString(), self.result.value(7).toString(), self.result.value(8).toString(), self.result.value(9).toString()]

    def lee_datos_menu(self):
        self.dbL.open()
        consulta='SELECT * FROM Programas ORDER BY Categoria ;'
        self.result=self.dbL.exec_(consulta)
        #Codigo  #Categoria  #Nombre_en    #Nombre_es   #Nombre_ca
        #Descripcion_en  #Descripcion_es   #Descripcion_ca  #Ejecutable  #Icono TEXT  #Categorias
        self.comboBox.clear()
        listaCategorias=QStringList()
        while self.result.next():
            listaCategorias.append(self.result.value(1).toString())
        self.dbL.close()
        listaCategorias.removeDuplicates()
        self.comboBox.addItems(listaCategorias)

    def pon_programas(self,indice):
        categoria=self.comboBox.itemText(self.comboBox.currentIndex())
        self.dbL.open()
        consulta='SELECT * FROM Programas WHERE Categoria="'+categoria+'" ORDER BY Nombre_ca ;'
        self.result=self.dbL.exec_(consulta)
        #Codigo   #Categoria   #Nombre_en   #Nombre_es   #Nombre_ca    #Descripcion_en
        #Descripcion_es  #Descripcion_ca    #Ejecutable  #Icono TEXT   #Categorias
        lista=QStringList()
        self.listWidget.clear()
        y=26
        while self.result.next():
            Codigo=self.result.value(0).toString()
            Nombre_ca=self.result.value(4).toString()
            Descripcion_ca=self.result.value(7).toString()
            icono=self.result.value(8).toString()
            lista.append(Nombre_ca)
            self.listWidget.resize(240,y)
            y+=17
        self.dbL.close()
        #lista.removeDuplicates()
        #icon = QIcon(icono)
        #pixmap = icon.pixmap(self.tam_icono, self.tam_icono)
        ##item = QListWidgetItem(icon,self.listWidget.Item())
        #item.setIcon(icon)
        #item.setStatusTip(icon)

        self.listWidget.addItems(lista)

    def activa_programa(self):
        if self.radioButton.isChecked():
            self.comboBox.setEnabled(True)
            self.listWidget.setEnabled(True)
            self.lineEdit_2.setEnabled(False)
        else:
            self.comboBox.setEnabled(False)
            self.listWidget.clear()
            self.listWidget.setGeometry(240,26)
            self.ListWidget.setEnabled(False)
            self.lineEdit_2.setEnabled(True)

    def activa_texto(self):
        if self.checkBox.isChecked():
            self.lineEdit.setEnabled(True)
        else:
            self.lineEdit.setEnabled(False)

    def accept(self):
        self.emit(SIGNAL("ok"), self.datos_final)
        self.close()


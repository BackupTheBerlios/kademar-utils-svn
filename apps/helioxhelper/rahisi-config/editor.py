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

from PyQt4.QtSql import *



class editor(QDialog):
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

        self.Codigo=""
        self.Categoria=""
        self.Nombre_en=""
        self.Nombre_es=""
        self.Nombre_ca=""
        self.Descripcion_en=""
        self.Descripcion_es=""
        self.Descripcion_ca=""
        self.Ejecutable=""
        self.Icono=""
        self.Categorias=""

        uic.loadUi("editor.ui", self)

        self.diricons="/usr/share/icons/hicolor/"+str(self.tam_icono)+"x"+str(self.tam_icono)+"/apps/"

        self.connect(self.b_accept, SIGNAL("clicked()"), self.accept)
        self.connect(self.b_cancel, SIGNAL("clicked()"), self.close)
        self.connect(self.radioButton, SIGNAL("clicked()"), self.activa_programa)
        self.connect(self.radioButton_2, SIGNAL("clicked()"), self.activa_programa)
        self.connect(self.checkBox, SIGNAL("clicked()"), self.activa_texto)
        self.connect(self.comboBox, SIGNAL("activated(int)"), self.pon_programas)
        self.connect(self.listWidget, SIGNAL("itemClicked(QListWidgetItem *)"), self.pon_datos)
        self.connect(self.lineEdit, SIGNAL("textChanged (const QString&)"), self.pon_texto_boton)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.busca_icono)
        self.lineEdit.setFocus()

        self.dbL = QSqlDatabase()
        self.dbL = QSqlDatabase.addDatabase("QSQLITE")
        self.dbL.setDatabaseName('rahisi.db')
        self.datos_final=[]
        self.pushButton.resize(self.ancho_boton,self.alt_boton)
        if self.texto:
            self.checkBox.setChecked(self.texto)
            self.activa_texto()
        
        locale = QLocale.system().name()   #ca_ES
        self.idiomas=["en","es","ca"]      # los tres idiomas que usamos
        self.idioma=self.idiomas.index(locale.split("_")[0])  # numero de idioma para facilitar las asignaciones en los result.value
        self.lee_datos_menu()

    def busca_icono(self):
        fileName = QFileDialog.getOpenFileName(self, "Selecciona un Icono", '/usr/share/icons' , "Ficheros de Icono (*.png)")
        if not fileName.strip()=='':
            icon = QIcon()
            icon.addPixmap(QPixmap(fileName), QIcon.Normal, QIcon.Off)
            self.pushButton.setIcon(icon)
            self.Icono=fileName
        
    def pon_texto_boton(self, texto):
        if self.checkBox.isChecked():
            self.pushButton.setText(texto)
            self.Nombre_ca=texto

    def pon_datos(self,codigo):
        self.dbL.open()
        value = self.listWidget.currentItem().text()
        consulta='SELECT * FROM Programas WHERE Nombre_'+self.idiomas[self.idioma]+'="'+value+'" ;'
        self.result=self.dbL.exec_(consulta)
        self.result.first()
        num=int(self.result.value(0))
        self.textEdit.setText(self.result.value(5+self.idioma))
        self.lineEdit.setText(self.result.value(2+self.idioma))
        self.lineEdit_2.setText(self.result.value(8))
        dicon=self.result.value(9)
        if dicon.find("/"):
            icono=self.diricons+dicon+".png"
        else:
            icono=dicon
        icon = QIcon()
        icon.addPixmap(QPixmap(icono), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)

        if self.checkBox.isChecked():
            texto=self.lineEdit.text()
            self.pushButton.setText(texto)
        else:
            texto=""
            self.pushButton.setText(texto)
        self.Codigo=int(self.result.value(0))
        self.Categoria=self.result.value(1)
        self.Nombre_en=self.result.value(2)
        self.Nombre_es=self.result.value(3)
        self.Nombre_ca=texto   # self.result.value(4)
        self.Descripcion_en=self.result.value(5)
        self.Descripcion_es=self.result.value(6)
        self.Descripcion_ca=self.result.value(7)
        self.Ejecutable=self.result.value(8).strip()
        self.Icono=icono
        self.Categorias=self.result.value(10)

    def lee_datos_menu(self):
        self.dbL.open()
        consulta='SELECT * FROM Programas ORDER BY Categoria ;'
        self.result=self.dbL.exec_(consulta)
        #Codigo  #Categoria  #Nombre_en    #Nombre_es   #Nombre_ca
        #Descripcion_en  #Descripcion_es   #Descripcion_ca  #Ejecutable  #Icono TEXT  #Categorias
        self.comboBox.clear()
        listaCategorias=[]
        while self.result.next():
            listaCategorias.append(self.result.value(1))
        self.dbL.close()
        listaCategorias = list(set(listaCategorias))
        listaCategorias.sort()
        self.comboBox.addItems(listaCategorias)

    def pon_programas(self,indice):
        categoria=self.comboBox.itemText(self.comboBox.currentIndex())
        self.dbL.open()
        consulta='SELECT * FROM Programas WHERE Categoria="'+categoria+'" ORDER BY Nombre_'+self.idiomas[self.idioma]+' ;'
        self.result=self.dbL.exec_(consulta)
        #Codigo   #Categoria   #Nombre_en   #Nombre_es   #Nombre_ca    #Descripcion_en
        #Descripcion_es  #Descripcion_ca    #Ejecutable  #Icono TEXT   #Categorias
        lista=[]
        self.listWidget.clear()
        y=26
        while self.result.next():
            Codigo=self.result.value(0)
            Nombre=self.result.value(2+self.idioma)
            Descripcion=self.result.value(5+self.idioma)
            icono=self.result.value(8)
            lista.append(Nombre)
            self.listWidget.resize(240,y)
            y+=17
        self.dbL.close()
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
            texto=self.lineEdit.text()
            self.pushButton.setText(texto)
            self.Nombre_ca=texto
            self.lineEdit.setEnabled(True)
        else:
            texto=""
            self.pushButton.setText(texto)
            self.Nombre_ca=texto
            self.lineEdit.setEnabled(False)

    def accept(self):
        self.datos_final=[self.Codigo, self.Categoria, self.Nombre_en, self.Nombre_es,self.Nombre_ca, self.Descripcion_en, self.Descripcion_es,self.Descripcion_ca, self.Ejecutable, self.Icono, self.Categorias]
        self.emit(SIGNAL("ok"), self.datos_final)
        self.close()


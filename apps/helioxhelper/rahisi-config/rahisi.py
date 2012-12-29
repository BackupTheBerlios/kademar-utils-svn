#!/usr/bin/python
#-*- coding: iso-8859-15 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
from ui_rahisi import Ui_Rahisi as Ui_Form
from qtoolbuttonwithevents import *

global nomore, globalpath,mgeometry,tgeometry
nomore=False

class Rahisi(QWidget):
    def __init__(self, parent=None):
        global mgeometry,tgeometry
        QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        #desktop = QApplication.desktop()
        #self.totalGeometry=desktop.screenGeometry ()
        #self.maxGeometry=desktop.availableGeometry ()
        #tgeometry=self.totalGeometry
        #mgeometry=self.maxGeometry
        #Open completly installer on the screen
        desktop_widget = QApplication.desktop()
        geometry = desktop_widget.screenGeometry()
        self.setGeometry(0,23, geometry.width(),geometry.height()-23)  #23px are the window handlers (kwin,etc)
        
        self.setAcceptDrops(1)
        self.botons=[]
        self.numbotones=0
        self.diricons="/usr/share/icons/default.kde/48x48/apps/"
        self.color_fondo1=""
        self.color_fondo2=""
        self.pixmap = QPixmap()
        self.pixmap.load("images/transparent.png")
        self.ui.label.setPixmap (self.pixmap)
        self.settings=QSettings("ProyectoHeliox", "HelioxHelper")
        self.writeConfig()
        
        self.connect(self.ui.pushButton, SIGNAL("clicked()"), self.boto_sortir)
        self.connect(self.ui.pushButton_5, SIGNAL("clicked()"), self.buscar_imagen)
        self.connect(self.ui.toolButton, SIGNAL("clicked()"), self.pon_color_fondo1)
        self.connect(self.ui.toolButton_4, SIGNAL("clicked()"), self.pon_color_fondo2)
        self.connect(self.ui.toolButton_2, SIGNAL("clicked()"), self.gradientBeginColor)
        self.connect(self.ui.toolButton_5, SIGNAL("clicked()"), self.gradientEndColor)
        self.connect(self.ui.toolButton_3, SIGNAL("clicked()"), self.borderColorFocused)
        self.connect(self.ui.toolButton_6, SIGNAL("clicked()"), self.borderColorNormal)
        self.connect(self.ui.toolButton_7, SIGNAL("clicked()"), self.borderColorHovered)
        self.connect(self.ui.checkBox, SIGNAL("clicked()"), self.imagen)
        self.connect(self.ui.checkBox_2, SIGNAL("clicked()"), self.autostart)
        self.connect(self.ui.checkBox_3, SIGNAL("clicked()"), self.fullscreen)
        self.connect(self.ui.checkBox_4, SIGNAL("clicked()"), self.completefullscreen)
        self.connect(self.ui.checkBox_5, SIGNAL("clicked()"), self.alwaysOnTop)
        self.connect(self.ui.checkBox_6, SIGNAL("clicked()"), self.alwaysOnBottom)
        self.connect(self.ui.checkBox_7, SIGNAL("clicked()"), self.closeConfirm)
        self.connect(self.ui.checkBox_8, SIGNAL("clicked()"), self.speechText)
        self.connect(self.ui.spinBox_3, SIGNAL("valueChanged(int)"), self.size)
        self.connect(self.ui.comboBox_2, SIGNAL("activated(int)"), self.whereIsPlacedWindow)
        self.connect(self.ui.checkBox_9, SIGNAL("clicked()"), self.fondo_degradado)
        self.connect(self.ui.checkBox_10, SIGNAL("clicked()"), self.tray_icon)
        self.connect(self.ui.checkBox_11, SIGNAL("clicked()"), self.left_clic)
        self.connect(self.ui.checkBox_12, SIGNAL("clicked()"), self.right_clic)
        self.connect(self.ui.checkBox_13, SIGNAL("clicked()"), self.show_minimize)
        self.connect(self.ui.checkBox_14, SIGNAL("clicked()"), self.show_restore)
        self.connect(self.ui.checkBox_15, SIGNAL("clicked()"), self.show_settings)
        self.connect(self.ui.checkBox_16, SIGNAL("clicked()"), self.show_exit)
        self.connect(self.ui.checkBox_17, SIGNAL("clicked()"), self.autoborders)
        self.connect(self.ui.spinBox_4, SIGNAL("valueChanged(int)"), self.redondeado)
        self.connect(self.ui.checkBox_20, SIGNAL("clicked()"), self.top_left)
        self.connect(self.ui.checkBox_21, SIGNAL("clicked()"), self.top_right)
        self.connect(self.ui.checkBox_22, SIGNAL("clicked()"), self.bottom_left)
        self.connect(self.ui.checkBox_23, SIGNAL("clicked()"), self.bottom_right)
        self.connect(self.ui.pushButton_3, SIGNAL("clicked()"), self.pon_boton)
        self.connect(self.ui.comboBox, SIGNAL("activated(int)"), self.imageSize)
        self.connect(self.ui.checkBox_19, SIGNAL("clicked()"), self.iconAbove)
        self.connect(self.ui.checkBox_18, SIGNAL("clicked()"), self.showLabels)
        self.connect(self.ui.spinBox, SIGNAL("valueChanged(int)"), self.minimumHeight)
        self.connect(self.ui.spinBox_6, SIGNAL("valueChanged(int)"), self.maximumHeight)
        self.connect(self.ui.spinBox_8, SIGNAL("valueChanged(int)"), self.minimumWidth)
        self.connect(self.ui.spinBox_7, SIGNAL("valueChanged(int)"), self.maximumWidth)
        self.connect(self.ui.spinBox_9, SIGNAL("valueChanged(int)"), self.pixelsBorderNormal)
        self.connect(self.ui.spinBox_10, SIGNAL("valueChanged(int)"), self.pixelsBorderFocused)
        self.connect(self.ui.spinBox_11, SIGNAL("valueChanged(int)"), self.pixelsRoundedBorder)
        self.connect(self.ui.pushButton_4, SIGNAL("clicked()"), self.borra_boton)
        self.connect(self.ui.pushButton_6, SIGNAL("clicked()"), self.guardar_botones)
        self.connect(self.ui.listWidget, SIGNAL("itemActivated(QListWidgetItem *)"), self.ver_ocultar_flechas)
        self.connect(self.ui.toolButton_8, SIGNAL("clicked()"), self.sube_item)
        self.connect(self.ui.toolButton_9, SIGNAL("clicked()"), self.baja_item)
        #self.pushButton_2 = QToolButtonWithEvents(self.ui.label)
        #self.pushButton_2 = QPushButton(self.ui.label)
        #self.pushButton_2.setObjectName("pushButton_2")
        #self.pushButton_2.setText("pushButton_2")
        #self.pushButton_2.setVariable("exec", "audacity")
        #self.pushButton_2.setVariable("icon", "/user/share/apps/icon.png")
        #self.pushButton_2.setVariable("desc", "progama de askjfe")
        #self.pushButton_2.setVariable("Applications", "audacity")

        #self.pushButton_6 = QToolButtonWithEvents(self.ui.label)
        #self.pushButton_6.setObjectName("pushButton_2")
        #self.ui.gridLayout_2.addWidget(self.pushButton_6, 0, 1, 1, 1)
        #self.pushButton_6 = QtGui.QPushButton(self.label)
        #self.pushButton_6.setObjectName("pushButton_6")
        #self.gridLayout_2.addWidget(self.pushButton_6, 0, 1, 1, 1)

        #self.pushButton_17 = QtGui.QPushButton(self.label)
        #self.pushButton_17.setObjectName("pushButton_17")
        #self.gridLayout_2.addWidget(self.pushButton_17, 1, 0, 1, 1)
        locale = QLocale.system().name()   #ca_ES
        self.idiomas=["en","es","ca"]      # los tres idiomas que usamos
        self.idioma=self.idiomas.index(locale.split("_")[0])  # numero de idioma para facilitar las asignaciones en los result.value
        
        
    def sube_item(self):
        num=self.ui.listWidget.currentRow()
        if num>0:
            unoviejo=self.botons[num-1]
            dosviejo=self.botons[num]
            self.botons[num-1]=dosviejo
            self.botons[num]=unoviejo
            self.ui.listWidget.clear()
            for i in self.botons:
                item = QListWidgetItem(str(i[2]))
                self.ui.listWidget.addItem(item)
            
    def baja_item(self):
        num=self.ui.listWidget.currentRow()
        maximo=len(self.botons)
        if num<maximo:
            unoviejo=self.botons[num]
            dosviejo=self.botons[num+1]
            self.botons[num]=dosviejo
            self.botons[num+1]=unoviejo
            self.ui.listWidget.clear()
            for i in self.botons:
                item = QListWidgetItem(str(i[2]))
                self.ui.listWidget.addItem(item)
        
    def ver_ocultar_flechas(self):
        self.ui.toolButton_8.setEnabled(True)
        self.ui.toolButton_9.setEnabled(True)
        
    def guardar_botones(self):
        self.settings.beginWriteArray("Applications/app")
        numbotones=len(self.botons)
        for x in range(numbotones):
            self.settings.setArrayIndex(x)
            text=self.botons[x][2+self.idioma]
            self.settings.setValue("name", str(text))
            text=self.botons[x][9]
            self.settings.setValue("icon", str(text))
            text=self.botons[x][5+self.idioma]
            self.settings.setValue("desc", str(text))
            text=self.botons[x][8]
            self.settings.setValue("exec", str(text))
        self.settings.endArray()

    def pon_boton(self):
        """
        open dialog for config button
        """
        from editor import editor as content_editor
        tam_icono=int(self.ui.comboBox.itemText(self.ui.comboBox.currentIndex()))
        texto=self.ui.checkBox_18.isChecked()
        alto=self.ui.spinBox.value()
        ancho=self.ui.spinBox_8.value()
        self.editor=content_editor(alto,ancho,tam_icono,texto)
        self.connect(self.editor,SIGNAL("ok"),self.configura_boton)
        self.editor.show()

    def configura_boton(self,datos):
    #self.datos_final=[self.Codigo,         self.Categoria,      self.Nombre_en,  self.Nombre_es, self.Nombre_ca, self.Descripcion_en,                   
                      #self.Descripcion_es, self.Descripcion_ca, self.Ejecutable, self.Icono,     self.Categorias]
        boto=[]
        for x in range(len(datos)):
            boto.append(str(datos[x]))
        if str(datos[4]).strip()=="":
            self.ui.checkBox_18.setChecked(False)
        else:
            self.ui.checkBox_18.setChecked(True)
        self.botons.append(boto)
        item = QListWidgetItem(str(boto[2]))
        self.ui.listWidget.addItem(item)
        self.numbotones+=1
        if self.numbotones>0:
            self.ui.pushButton_4.setEnabled(True)
            self.ui.pushButton_6.setEnabled(True)
        else:
            self.ui.pushButton_4.setEnabled(False)
            self.ui.pushButton_6.setEnabled(False)
            
    def borra_boton(self):
        num=self.ui.listWidget.currentRow()
        texto=self.botons[num]
        self.botons.remove(texto)
        item = self.ui.listWidget.takeItem(num)
        item = None
        self.numbotones-=1

    def writeConfig(self):
        if (self.settings.value("General/autostart") == ""):
            self.settings.beginGroup("General")
            self.settings.setValue("autostart", "1")
            self.settings.setValue("fullscreen", "0")
            self.settings.setValue("completeFullscreen", "0")
            self.settings.setValue("alwaysOnTop", "0")
            self.settings.setValue("alwaysOnBottom", "0")
            self.settings.setValue("whereIsPlacedWindow", "2")
            self.settings.setValue("closeConfirm", "1")
            self.settings.setValue("speechText", "1")
            self.settings.setValue("speechPath", "/usr/share/helioxhelper/speech")
            self.settings.endGroup()

            self.settings.beginGroup("Panel")
            self.settings.setValue("size", "350")
            self.settings.setValue("percentage", "90%")
            self.settings.setValue("align", "center")
            self.settings.endGroup()

            self.settings.beginGroup("Tray Icon")
            self.settings.setValue("showTrayIcon", "1")
            self.settings.setValue("leftClickContextualMenu", "0")
            self.settings.setValue("rightClickContextualMenu", "1")
            self.settings.endGroup()

            self.settings.beginGroup("Contextual Menu")
            self.settings.setValue("showMinimize", "1")
            self.settings.setValue("showRestore", "1")
            self.settings.setValue("showSettings", "1")
            self.settings.setValue("showExit", "1")
            self.settings.endGroup()

            self.settings.beginGroup("Background")
            self.settings.setValue("wallpaperBackground", "0")
            self.settings.setValue("backgroundPath", "")
            self.settings.setValue("gradientBackground", "1")
            self.settings.setValue("gradientOrientation", "0")
            self.settings.setValue("gradientBeginColor", "#ffffff")
            self.settings.setValue("gradientEndColor", "#ffffff")
            self.settings.endGroup()

            self.settings.beginGroup("Round Corners")
            self.settings.setValue("autoBorders", "1")
            self.settings.setValue("roundedMargin", "25")
            self.settings.setValue("top_left", "1")
            self.settings.setValue("top_right", "0")
            self.settings.setValue("bottom_left", "1")
            self.settings.setValue("bottom_right", "0")
            self.settings.endGroup()

            self.settings.beginGroup("App Buttons")
            self.settings.setValue("imageSize", "32")
            self.settings.setValue("iconAbove", "1")
            self.settings.setValue("showLabels", "true")
            self.settings.setValue("minimumHeight", "40")
            self.settings.setValue("maximumHeight", "0")
            self.settings.setValue("minimumWidth", "100")
            self.settings.setValue("maximumWidth", "0")
            self.settings.setValue("pixelsBorderNormal", "1")
            self.settings.setValue("pixelsBorderFocused", "2")
            self.settings.setValue("pixelsRoundedBorder", "10")
            self.settings.setValue("borderColorNormal", "#7d7d7d")
            self.settings.setValue("borderColorFocused", "#679cd0")
            self.settings.setValue("borderColorHovered", "#679cd0")
            self.settings.setValue("gradientBeginColor", "#e3e2e1")
            self.settings.setValue("gradientEndColor", "#cac9c8")
            self.settings.setValue("fontSize", "13")
            self.settings.endGroup()

            self.settings.beginGroup("Applications")
            self.settings.sync()

            # "Writting default Settings"

            self.settings.beginWriteArray("app")
            self.settings.setArrayIndex(0)
            self.settings.setValue("name", "LibreOffice")
            self.settings.setValue("icon", "/usr/share/icons/hicolor/48x48/apps/libreoffice-startcenter.png")
            self.settings.setValue("desc", "Write your documents")
            self.settings.setValue("exec", "libreoffice")
            self.settings.setArrayIndex(1)
            self.settings.setValue("name", "FireFox")
            self.settings.setValue("icon", "/usr/share/icons/hicolor/48x48/apps/firefox.png")
            self.settings.setValue("desc", "Browse the web")
            self.settings.setValue("exec", "firefox")
            self.settings.setArrayIndex(2)
            self.settings.setValue("name", "newRow")
            self.settings.setValue("icon", "")
            self.settings.setValue("desc", "")
            self.settings.setValue("exec", "")
            self.settings.setArrayIndex(3)
            self.settings.setValue("name", "VLC")
            self.settings.setValue("icon", "/usr/share/icons/hicolor/48x48/apps/vlc.png")
            self.settings.setValue("desc", "Video and Music Mediaplayer")
            self.settings.setValue("exec", "vlc")
            self.settings.setArrayIndex(4)
            self.settings.setValue("name", "Pidgin")
            self.settings.setValue("icon", "/usr/share/icons/hicolor/48x48/apps/pidgin.png")
            self.settings.setValue("desc", "Multi Instant Messenger")
            self.settings.setValue("exec", "pidgin")
            self.settings.endArray()
            self.settings.endGroup()
        else:
            self.ui.checkBox.setChecked(int(self.settings.value("Background/wallpaperBackground", 0)))
            self.ui.lineEdit_2.setText(self.settings.value("Background/backgroundPath", ""))
            if self.ui.checkBox.isChecked():
                self.pixmap.load(self.ui.lineEdit_2.text())
                self.ui.label.setPixmap (self.pixmap)
                self.imagen()
            self.ui.checkBox_2.setChecked(int(self.settings.value("General/autostart", 0)))
            self.ui.checkBox_3.setChecked(int(self.settings.value("General/fullscreen", 0)))
            self.ui.checkBox_4.setChecked(int(self.settings.value("General/completeFullscreen", 0)))
            self.ui.checkBox_5.setChecked(int(self.settings.value("General/alwaysOnTop", 0)))
            self.ui.checkBox_6.setChecked(int(self.settings.value("General/alwaysOnBottom", 0)))
            self.ui.checkBox_7.setChecked(int(self.settings.value("General/closeConfirm", 0)))
            self.ui.checkBox_8.setChecked(int(self.settings.value("General/speechText", 0)))
            self.ui.spinBox_3.setValue(int(self.settings.value("Panel/size", 350)))
            self.ui.checkBox_9.setChecked(int(self.settings.value("Background/gradientBackground", 0)))
            if self.ui.checkBox_9.isChecked():
                self.ui.label_12.setVisible(True)
                self.ui.label_14.setVisible(True)
                self.ui.toolButton_4.setVisible(True)
            else:
                self.ui.label_12.setVisible(False)
                self.ui.label_14.setVisible(False)
                self.ui.toolButton_4.setVisible(False)
            self.color_fondo1 = self.settings.value ("Background/gradientBeginColor", "#ffffff")
            self.color_fondo2 = self.settings.value ("Background/gradientEndColor", "#ffffff")
            gradient = QLinearGradient(0, 0, 0, 400)
            gradient.setColorAt(0.0, QColor(self.color_fondo1))
            gradient.setColorAt(1.0, QColor(self.color_fondo2))
            paleta=self.ui.label.palette()
            paleta.setBrush(QPalette.Window, QBrush(gradient))
            self.ui.label.setPalette(paleta)
            
            color=QColor(self.color_fondo1)
            paleta=QPalette(self.ui.frame_9.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.frame_9.setPalette(QPalette(color))

            color=QColor(self.color_fondo2)
            paleta=QPalette(self.ui.frame_8.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.frame_8.setPalette(QPalette(color))
        
            self.ui.checkBox_10.setChecked(int(self.settings.value("Tray Icon/showTrayIcon", 0)))
            self.ui.checkBox_11.setChecked(int(self.settings.value("Tray Icon/leftClickContextualMenu", 0)))
            self.ui.checkBox_12.setChecked(int(self.settings.value("Tray Icon/rightClickContextualMenu", 0)))
            self.ui.checkBox_13.setChecked(int(self.settings.value("Contextual Menu/showMinimize", 0)))
            self.ui.checkBox_14.setChecked(int(self.settings.value("Contextual Menu/showRestore", 0)))
            self.ui.checkBox_15.setChecked(int(self.settings.value("Contextual Menu/showSettings", 0)))
            self.ui.checkBox_16.setChecked(int(self.settings.value("Contextual Menu/showExit", 0)))

            self.ui.checkBox_17.setChecked(int(self.settings.value("Round Corners/autoBorders", 1)))
            self.ui.spinBox_4.setValue(int(self.settings.value("Round Corners/roundedMargin", 25)))
            self.ui.checkBox_20.setChecked(int(self.settings.value("Round Corners/top_left", 1)))
            self.ui.checkBox_21.setChecked(int(self.settings.value("Round Corners/top_right", 0)))
            self.ui.checkBox_22.setChecked(int(self.settings.value("Round Corners/bottom_left", 1)))
            self.ui.checkBox_23.setChecked(int(self.settings.value("Round Corners/bottom_right", 0)))

            num=self.settings.value("App Buttons/imageSize", 48)
            n=self.ui.comboBox.findText(num)
            if n==-1:
                n=2
            self.ui.comboBox.setCurrentIndex(n)

            self.ui.checkBox_19.setChecked(int(self.settings.value("App Buttons/iconAbove", 1)))
            self.ui.checkBox_18.setChecked(bool(self.settings.value("App Buttons/showLabels", 1)))
            self.ui.spinBox.setValue(int(self.settings.value("App Buttons/minimumHeight", 40)))
            self.ui.spinBox_6.setValue(int(self.settings.value("App Buttons/maximumHeight", 0)))
            self.ui.spinBox_8.setValue(int(self.settings.value("App Buttons/minimumWidth", 100)))
            self.ui.spinBox_7.setValue(int(self.settings.value("App Buttons/maximumWidth", 0)))
            self.ui.spinBox_9.setValue(int(self.settings.value("App Buttons/pixelsBorderNormal", 1)))
            self.ui.spinBox_10.setValue(int(self.settings.value("App Buttons/pixelsBorderFocused", 2)))
            self.ui.spinBox_11.setValue(int(self.settings.value("App Buttons/pixelsRoundedBorder", 10)))
            
            self.color_borde_normal = self.settings.value ("App Buttons/borderColorNormal", "#ffffff")
            color=QColor(self.color_borde_normal)
            paleta=QPalette(self.ui.frame_3.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.frame_3.setPalette(QPalette(color))
            
            self.color_borde_focused = self.settings.value ("App Buttons/borderColorFocused", "#ffffff")
            color=QColor(self.color_borde_focused)
            paleta=QPalette(self.ui.frame_4.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.frame_4.setPalette(QPalette(color))

            self.color_borde_hovered = self.settings.value ("App Buttons/borderColorHovered", "#ffffff")
            color=QColor(self.color_borde_hovered)
            paleta=QPalette(self.ui.frame_5.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.frame_5.setPalette(QPalette(color))
            
            self.color_boton_begin = self.settings.value ("App Buttons/gradientBeginColor", "#ffffff")
            color=QColor(self.color_boton_begin)
            paleta=QPalette(self.ui.frame_6.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.frame_6.setPalette(QPalette(color))
            
            self.color_boton_end = self.settings.value ("App Buttons/gradientEndColor", "#ffffff")
            color=QColor(self.color_boton_end)
            paleta=QPalette(self.ui.frame_7.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.frame_7.setPalette(QPalette(color))
            self.numbotones=0
            self.settings.beginReadArray("Applications/app")
            self.numpags = int(self.settings.value("size"))
            self.botons=[]
        
        #self.datos_final=[self.Codigo,         self.Categoria,      self.Nombre_en,  self.Nombre_es, self.Nombre_ca, self.Descripcion_en,                   
                      #self.Descripcion_es, self.Descripcion_ca, self.Ejecutable, self.Icono,     self.Categorias]
        
            for x in range(self.numpags):
                self.settings.setArrayIndex(x)
                self.numbotones+=1
                nom=self.settings.value("name")
                icon=self.settings.value("icon")
                desc=self.settings.value("desc")
                exe=self.settings.value("exec")
                self.botons.append([' ', ' ', nom, nom, nom, desc, desc, desc, exe, icon, ' ']) 
                item = QListWidgetItem(str(nom))
                self.ui.listWidget.addItem(item)
            self.settings.endArray()
            if self.numbotones>0:
                self.ui.pushButton_4.setEnabled(True)
                self.ui.pushButton_6.setEnabled(True)
            

    def imagen(self):
        if self.ui.checkBox.isChecked():
            self.settings.setValue("Background/wallpaperBackground", "1")
            fichero=self.ui.lineEdit_2.text()
            self.settings.setValue("Background/backgroundPath", fichero)
            self.pixmap.load(fichero)
            self.ui.label.setPixmap (self.pixmap)
            self.settings.sync()
        else:
            self.settings.setValue("Background/wallpaperBackground", "0")
            fichero="images/transparent.png"
            self.settings.setValue("Background/backgroundPath", fichero)
            self.pixmap.load(fichero)
            self.ui.label.setPixmap (self.pixmap)
            self.settings.sync()

    def autostart(self):
        num=self.ui.checkBox_2.isChecked()==True
        self.settings.setValue("General/autostart", int(num))
        self.settings.sync()

    def fullscreen(self):
        num=self.ui.checkBox_3.isChecked()==True
        self.settings.setValue("General/fullscreen", int(num))
        self.settings.sync()

    def completefullscreen(self):
        num=self.ui.checkBox_4.isChecked()==True
        self.settings.setValue("General/completeFullscreen", int(num))
        self.settings.sync()

    def alwaysOnTop(self):
        num=self.ui.checkBox_5.isChecked()==True
        self.settings.setValue("General/alwaysOnTop", int(num))
        self.settings.sync()

    def alwaysOnBottom(self):
        num=self.ui.checkBox_6.isChecked()==True
        self.settings.setValue("General/alwaysOnBottom", int(num))
        self.settings.sync()

    def closeConfirm(self):
        num=self.ui.checkBox_7.isChecked()==True
        self.settings.setValue("General/closeConfirm", int(num))
        self.settings.sync()

    def speechText(self):
        num=self.ui.checkBox_8.isChecked()==True
        self.settings.setValue("General/speechText", int(num))
        self.settings.sync()

    def whereIsPlacedWindow(self,posicion):
        self.settings.setValue("General/whereIsPlacedWindow", posicion)
        self.settings.sync()

    def size(self):
        ancho=self.ui.spinBox_3.value()
        self.settings.setValue("Panel/size", ancho)
        self.settings.sync()

    def buscar_imagen(self):
        fileName = QFileDialog.getOpenFileName(self, self.tr("Selecciona una Imagen"),                                                              '',self.tr("Ficheros de Imatge (*.png *.jpg)"))
        if not fileName.strip()=='':
            camino,fichero=os.path.split(str(fileName))
            self.ui.lineEdit_2.setText(fileName)
            if self.ui.checkBox.isChecked():
                self.pixmap.load(fileName)
                self.ui.label.setPixmap (self.pixmap)
                self.settings.setValue("Background/backgroundPath", fileName)
                self.settings.sync()

    def fondo_degradado(self):
        if self.ui.checkBox_9.isChecked():
            self.settings.setValue("Background/gradientBackground", 1)
            self.ui.label_12.setVisible(True)
            self.ui.label_14.setVisible(True)
            self.ui.toolButton_4.setVisible(True)
            self.ui.frame_8.setVisible(True)
            gradient = QLinearGradient(0, 0, 0, 400)
            gradient.setColorAt(0.0, QColor(self.color_fondo1))
            gradient.setColorAt(1.0, QColor(self.color_fondo2))
            paleta=self.ui.label.palette()
            paleta.setBrush(QPalette.Window, QBrush(gradient))
            self.ui.label.setPalette(paleta)
            paleta=QPalette(self.ui.frame_8.palette())
            color=QColor(self.color_fondo2)
            paleta.setColor(paleta.Base,color)
            self.ui.frame_8.setPalette(QPalette(color))
        else:
            self.settings.setValue("Background/gradientBackground", 0)
            self.ui.label_12.setVisible(False)
            self.ui.label_14.setVisible(False)
            self.ui.toolButton_4.setVisible(False)
            self.ui.frame_8.setVisible(False)
            color=QColor(self.color_fondo1)
            paleta=QPalette(self.ui.label.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.label.setPalette(QPalette(color))

    def pon_color_fondo1(self):
        color= QColorDialog.getColor(Qt.white, self)
        if color.isValid():
            self.color_fondo1=color.name()
            paleta=QPalette(self.ui.frame_9.palette())
        paleta.setColor(paleta.Base,color)
        self.ui.frame_9.setPalette(QPalette(color))
        self.ui.label.setPalette(QPalette(color))
        self.settings.setValue("Background/gradientBeginColor", color.name())

    def pon_color_fondo2(self):
        color= QColorDialog.getColor(Qt.white, self)
        if color.isValid():
            self.color_fondo2=color.name()
            self.settings.setValue("Background/gradientBackground", 1)
            self.settings.setValue("Background/gradientBeginColor", self.color_fondo1)
            self.settings.setValue("Background/gradientEndColor", self.color_fondo2)
            self.settings.sync()
            
            gradient = QLinearGradient(0, 0, 0, 400)
            gradient.setColorAt(0.0, QColor(self.color_fondo1))
            gradient.setColorAt(1.0, QColor(self.color_fondo2))
            paleta=self.ui.label.palette()
            paleta.setBrush(QPalette.Window, QBrush(gradient))
            self.ui.label.setPalette(paleta)
            paleta=QPalette(self.ui.frame_8.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.frame_8.setPalette(QPalette(color))

    def tray_icon(self):
        num=self.ui.checkBox_10.isChecked()==True
        self.settings.setValue("Tray Icon/showTrayIcon", int(num))
        self.settings.sync()

    def left_clic(self):
        num=self.ui.checkBox_11.isChecked()==True
        self.settings.setValue("Tray Icon/leftClickContextualMenu", int(num))
        self.settings.sync()

    def right_clic(self):
        num=self.ui.checkBox_12.isChecked()==True
        self.settings.setValue("Tray Icon/rightClickContextualMenu", int(num))
        self.settings.sync()

    def show_minimize(self):
        num=self.ui.checkBox_13.isChecked()==True
        self.settings.setValue("Contextual Menu/showMinimize", int(num))
        self.settings.sync()

    def show_restore(self):
        num=self.ui.checkBox_14.isChecked()==True
        self.settings.setValue("Contextual Menu/showRestore", int(num))
        self.settings.sync()

    def show_settings(self):
        num=self.ui.checkBox_15.isChecked()==True
        self.settings.setValue("Contextual Menu/showSettings", int(num))
        self.settings.sync()

    def show_exit(self):
        num=self.ui.checkBox_16.isChecked()==True
        self.settings.setValue("Contextual Menu/showExit", int(num))
        self.settings.sync()

    def autoborders(self):
        num=self.ui.checkBox_17.isChecked()==True
        self.settings.setValue("Round Corners/autoBorders", int(num))
        self.settings.sync()

    def redondeado(self):
        ancho=self.ui.spinBox_4.value()
        self.settings.setValue("Round Corners/roundedMargin", ancho)
        self.settings.sync()

    def top_left(self):
        num=self.ui.checkBox_20.isChecked()==True
        self.settings.setValue("Round Corners/top-left", int(num))
        self.settings.sync()

    def top_right(self):
        num=self.ui.checkBox_21.isChecked()==True
        self.settings.setValue("Round Corners/top-right", int(num))
        self.settings.sync()

    def bottom_left(self):
        num=self.ui.checkBox_22.isChecked()==True
        self.settings.setValue("Round Corners/bottom-left", int(num))
        self.settings.sync()

    def bottom_right(self):
        num=self.ui.checkBox_23.isChecked()==True
        self.settings.setValue("Round Corners/bottom-right", int(num))
        self.settings.sync()

    def imageSize(self):
        num=self.ui.comboBox.currentItem().trimmed()
        self.settings.setValue("App Buttons/imageSize", int(num))
        self.settings.sync()
        
    def iconAbove(self):
        num=self.ui.checkBox_19.isChecked()==True
        self.settings.setValue("App Buttons/iconAbove", int(num))
        self.settings.sync()
    
    def showLabels(self):
        num=self.ui.checkBox_18.isChecked()==True
        self.settings.setValue("App Buttons/showLabels", int(num))
        self.settings.sync()
        
    def minimumHeight(self):
        num=self.ui.spinBox.value()
        self.settings.setValue("App Buttons/minimumHeight", int(num))
        self.settings.sync()
        
    def maximumHeight(self):
        num=self.ui.spinBox_6.value()
        self.settings.setValue("App Buttons/maximumHeight", int(num))
        self.settings.sync()     
        
    def minimumWidth(self):
        num=self.ui.spinBox_8.value()
        self.settings.setValue("App Buttons/minimumWidth", int(num))
        self.settings.sync()   
        
    def maximumWidth(self):
        num=self.ui.spinBox_7.value()
        self.settings.setValue("App Buttons/maximumWidth", int(num))
        self.settings.sync()    
        
    def pixelsBorderNormal(self):
        num=self.ui.spinBox_8.value()
        self.settings.setValue("App Buttons/pixelsBorderNormal", int(num))
        self.settings.sync()
        
    def pixelsBorderFocused(self):
        num=self.ui.spinBox_8.value()
        self.settings.setValue("App Buttons/pixelsBorderFocused", int(num))
        self.settings.sync()
        
    def pixelsRoundedBorder(self):
        num=self.ui.spinBox_7.value()
        self.settings.setValue("App Buttons/pixelsRoundedBorder", int(num))
        self.settings.sync()  
        
    def gradientBeginColor(self):
        color= QColorDialog.getColor(Qt.white, self)
        if color.isValid():
            self.color_borde=color
            paleta=QPalette(self.ui.frame_6.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.frame_6.setPalette(QPalette(color))
            self.settings.setValue("App Buttons/gradientBeginColor", color.name())

    def gradientEndColor(self):
        color= QColorDialog.getColor(Qt.white, self)
        if color.isValid():
            self.color_borde=color
            paleta=QPalette(self.ui.frame_7.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.frame_7.setPalette(QPalette(color))
            self.settings.setValue("App Buttons/gradientEndColor", color.name())
        
    def borderColorNormal(self):
        color= QColorDialog.getColor(Qt.white, self)
        if color.isValid():
            self.color_borde=color
            paleta=QPalette(self.ui.frame_3.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.frame_3.setPalette(QPalette(color))
            self.settings.setValue("App Buttons/borderColorNormal", color.name())

    def borderColorFocused(self):
        color= QColorDialog.getColor(Qt.white, self)
        if color.isValid():
            self.color_borde=color
            paleta=QPalette(self.ui.frame_4.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.frame_4.setPalette(QPalette(color))
            self.settings.setValue("App Buttons/borderColorFocused", color.name())
        
    def borderColorHovered(self):
        color= QColorDialog.getColor(Qt.white, self)
        if color.isValid():
            self.color_borde=color
            paleta=QPalette(self.ui.frame_5.palette())
            paleta.setColor(paleta.Base,color)
            self.ui.frame_5.setPalette(QPalette(color))
            self.settings.setValue("App Buttons/borderColorHovered", color.name())
        
    def boto_sortir(self):
        self.close()


app = QApplication(sys.argv)

#locale = QLocale.system().name()
#qtTranslator = QTranslator()
#if qtTranslator.load("/usr/share/kdemar/utils/audioconversor5/tr/"+locale.split("_")[0]+".qm"):
    #app.installTranslator(qtTranslator)
    #print "Loaded "+locale
#elif qtTranslator.load("/usr/share/kdemar/utils/audioconversor5/tr/en.qm"):
    #app.installTranslator(qtTranslator)
    #print "Loaded "+locale

Rahisi = Rahisi()

if sys.platform[:3].lower()=='win':
    Rahisi.setGeometry(5,30,1020,700)
#else:
    #Rahisi.setGeometry(mgeometry)
Rahisi.show()
app.exec_()

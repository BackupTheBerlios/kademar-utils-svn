# -*- coding: iso-8859-15 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
#import os
#from ui_rahisi import Ui_Rahisi as Ui_Form

#global nomore, globalpath,mgeometry,tgeometry
#nomore=False

class QToolButtonWithEvents(QToolButton):
    def __init__(self, settings1, settings2, parent=None):
        QToolButton.__init__(self)

    #self.connect(self.ui.pushButton, SIGNAL("clicked()"), self.boto_sortir)
    #self.connect(self, SIGNAL(clicked()), SLOT(buttonClickedFunction()))

         #m_property = QString("")


    #settings = QSettings(settings1, settings2)

    #setVisualStyle()

    #self.setAutoRaise(true)

   ## DE MOMENT NO  #installEventFilter(this)



    def buttonClickedFunction(self):
        self.emit(SIGNAL("buttonClicked"),ejecutable, icona, desc, app )

    def setVariable(self, tipus, valor):
        if tipus=="ejecutable":
            ejecutable=valor
        elif tipus=="icona":
            icona=valor



#def QToolButtonWithEvents::setVisualStyle()
#{
   #//QSettings settings("ProyectoHeliox", "HelioxHelper")

    #QString pixelsBorderNormal = settings->value("App Buttons/pixelsBorderNormal").toString()
    #QString pixelsBorderFocused = settings->value("App Buttons/pixelsBorderFocused").toString()
    #QString pixelsRoundedBorder = settings->value("App Buttons/pixelsRoundedBorder").toString()
    #QString borderColorNormal = settings->value("App Buttons/borderColorNormal").toString()
    #QString borderColorFocused = settings->value("App Buttons/borderColorFocused").toString()
    #QString borderColorHovered = settings->value("App Buttons/borderColorHovered").toString()
    #QString gradientBeginColor = settings->value("App Buttons/gradientBeginColor").toString()
    #QString gradientEndColor = settings->value("App Buttons/gradientEndColor").toString()
    #QString fontSize = settings->value("App Buttons/fontSize").toString()


    #bNormal = QString("QToolButtonWithEvents {background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 %1, stop: 1 %2) border-style: solid "
                              #"border-width: %3px border-radius: %4px border-color: %5 font: bold %6px padding: 2px}").arg(gradientBeginColor).arg(gradientEndColor).arg(pixelsBorderNormal).arg(pixelsRoundedBorder).arg(borderColorNormal).arg(fontSize)

    #//Reversed exists cause QtoolbuttonwithEvents:Focus doesn't work (workarround fix)
    #// for focus event - workarround CSS fix
    #bNormalFocused = QString("QToolButtonWithEvents  { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 %1, stop: 1 %2)  border-style: solid" "border-width: %3px border-radius: %4px border-color: %5 font: bold %6px }").arg(gradientBeginColor).arg(gradientEndColor).arg(pixelsBorderFocused).arg(pixelsRoundedBorder).arg(borderColorFocused).arg(fontSize)

    #bHover= QString("QToolButtonWithEvents:hover  { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 %1, stop: 1 %2)  border-style: solid" "border-width: %3px border-radius: %4px border-color: %5 font: bold %6px}").arg(gradientBeginColor).arg(gradientEndColor).arg(pixelsBorderFocused).arg(pixelsRoundedBorder).arg(borderColorHovered).arg(fontSize)

    #bPressed= QString("QToolButtonWithEvents:pressed  { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 %2, stop: 1 %1)  border-style: solid border-width: %3px border-radius: %4px border-color: %5 font: bold %6px }").arg(gradientBeginColor).arg(gradientEndColor).arg(pixelsBorderNormal).arg(pixelsRoundedBorder).arg(borderColorNormal).arg(fontSize)

    #this->setStyleSheet(bNormal+bHover+bPressed)

    #//this->setStyleSheet("QToolButtonWithEvents:hover  { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #a1bdd1, stop: 1 #d4d3d2)  border-style: solid border-width: 20px border-radius: 3px border-color: #679cd0 font: bold 13px }")

#}


#########################################


         #NO MES


#########################################





#def QToolButtonWithEvents::focusInEvent( QFocusEvent * event )
#{
    #event->accept()
    #extern bool speech
    #if ( speech == 1 ){
        #QString *txt = new QString(this->text())
        #QString *desc = new QString(toolTipText)
        #if (blockedSignals == false) {
            #if (speeching == false){
                #if (this->isVisible() == true){
                    #if (*desc != ""){
                        #this->readCaption(desc)
                   #//    qDebug() << blockedSignals
                    #} else {
                        #this->readCaption(txt)
                    #}
                #}
            #}
        #}
    #//    txt->append(". ")
      #//  txt->append(desc)

        #//if (blockedSignals == false) {
          #//  this->readCaption(txt)
         #// //  qDebug() << blockedSignals
       #// } //else {
       #//    // qDebug() << blockedSignals
       #//  //   qDebug() << "Shhh! No puedo hablar"
       #//// }
       #// qDebug() << "es este"
      #//  qDebug() << event->type()


  #//      qDebug() << "talking by focus event... " << txt->toLocal8Bit()

    #}
#}

#def QToolButtonWithEvents::setTextProperty( QString *prop, QString *value)
#{
    #m_property = QString (*prop)
    #m_propertyValue = QString (*value)
#}

#//workarround of  stylesheet  widget:focus  doesn't work
#bool QToolButtonWithEvents::eventFilter(QObject* object,QEvent* event)

#{
    #if( event->type( ) == QEvent::FocusIn )
       #{
           #setStyleSheet(bNormalFocused+bHover+bPressed)
#//           QToolTip::showText(QPoint(0,0),toolTipText)


       #} else if ( event->type( ) == QEvent::FocusOut ) {
           #setStyleSheet(bNormal+bHover+bPressed)
           #QToolTip::hideText()
 #//  } else if (event->type() == QEvent::HoverEnter) {
 #//       QToolTip::showText(this->mapToGlobal(QPoint()),QString ("Help reminder sho : push Button"))
    #} else if ((event->type() == QEvent::HoverLeave) || ( event->type( ) == QEvent::FocusOut ))  {
        #QToolTip::hideText()
    #}
    #if ((event->type( ) == QEvent::KeyRelease ) || (event->type() == QEvent::HoverEnter)){
        #this->showToolTip()
    #}
    #event->accept()


#}



#def QToolButtonWithEvents::setToolTip(QString &label){

    #toolTipText = label
#}

#def QToolButtonWithEvents::showToolTip()
#{
#//    qDebug() << this->geometry()
#//    qDebug() << this->geometry().y()
    #int x = this->mapToGlobal( QPoint() ).x()
    #int y = this->mapToGlobal(QPoint()).y()

    #//int x = this->geometry().x()+this->geometry().width()/2
    #//int y = this->geometry().y()+this->geometry().height()/2

    #//int gy = this->geometry().height()
    #//y = y + gy
    #QToolTip::showText(QPoint(x,y),toolTipText)
#}

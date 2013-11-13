#include "qpushbuttonwithevents.h"
#include "QPushButton"
#include "QObject"
#include "QWidget"
#include <QProcess>
#include <QString>
#include <QEvent>
#include <QFocusEvent>
#include <QDebug>

QPushButtonWithEvents::QPushButtonWithEvents(QWidget *parent) :
    QPushButton(parent)
{
    connect(this, SIGNAL(clicked()),
                 this, SLOT(buttonClickedFunction()));
    m_property = QString("");
    this->setDefaultStyleSheet();

}

void QPushButtonWithEvents::readCaption( QString * label )
{
    QProcess *readcommand = new QProcess();
    readcommand->start(QString("spd-say \"%1\"").arg(*label));
}

void QPushButtonWithEvents::setDefaultStyleSheet()
{
    this->setStyleSheet("QPushButtonWithEvents {background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #e3e2e1, stop: 1 #cac9c8); border-style: solid ; border-width: 1px; border-radius: 3px; border-color: #7d7d7d; font: bold 13px; min-width: 10em; padding: 2px;} QPushButtonWithEvents:hover  { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #a1bdd1, stop: 1 #d4d3d2) ; border-style: solid; border-width: 2px; border-radius: 3px; border-color: #679cd0; font: bold 13px; min-width: 10em;} QPushButtonWithEvents:pressed  { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #d4d3d2, stop: 1 #a1bdd1) ; border-style: solid; border-width: 2px; border-radius: 3px; border-color: #679cd0; font: bold 13px; min-width: 10em;} ");
}

QString QPushButtonWithEvents::textProperty()
{
    return m_property;
}

QString QPushButtonWithEvents::textPropertyValue()
{
    return m_propertyValue;
}

void QPushButtonWithEvents::buttonClickedFunction()
{
    //qDebug() << "signal"; // << m_listNumber;
    emit buttonClicked(m_property, m_propertyValue);
}

void QPushButtonWithEvents::enterEvent( QEvent * event )
{
    event->accept();
    extern bool speech;
    if ( speech == 1 ){
        QString *txt = new QString(this->text());
        this->readCaption(txt);
    }
    //qDebug() << "talking... " << QString(this->text());
}


void QPushButtonWithEvents::focusInEvent( QFocusEvent * event )
{
    this->setStyleSheet("QPushButtonWithEvents  { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #a1bdd1, stop: 1 #d4d3d2) ; border-style: solid; border-width: 2px; border-radius: 3px; border-color: #679cd0; font: bold 13px; min-width: 10em;} QPushButtonWithEvents:pressed  { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #d4d3d2, stop: 1 #a1bdd1) ; border-style: solid; border-width: 2px; border-radius: 3px; border-color: #679cd0; font: bold 13px; min-width: 10em;} ");
    event->accept();
    extern bool speech;
    if ( speech == 1 ){
        QString *txt = new QString(this->text());
        this->readCaption(txt);
    }
    //qDebug() << "talking by tab key focus... "  << QString(this->text());

}

void QPushButtonWithEvents::focusOutEvent( QFocusEvent * event )
{
    this->setDefaultStyleSheet();
}

void QPushButtonWithEvents::setTextProperty( QString *prop, QString *value)
{
    m_property = QString (*prop);
    m_propertyValue = QString (*value);
}

#include "qpushbuttonwithevents.h"
#include "QPushButton"
#include "QObject"
#include "QWidget"
#include <QProcess>
#include <QString>
#include <QEvent>
#include <QDebug>
#include <QFocusEvent>


QPushButtonWithEvents::QPushButtonWithEvents(QWidget *parent) :
    QPushButton(parent)
{
}

void QPushButtonWithEvents::readCaption( QString * label )
{
    QProcess *readcommand = new QProcess();
    readcommand->start(QString("spd-say \"%1\"").arg(*label));
}


void QPushButtonWithEvents::enterEvent( QEvent * event )
{
    event->accept();
    extern bool speech;
    if ( speech == 1 ){
        QString *txt = new QString(this->text());
        this->readCaption(txt);
    }
    qDebug() << "parlant";

}

//TODO: on key focus, use readCaption function
//void QPushButtonWithEvents::

void QPushButtonWithEvents::focusInEvent( QFocusEvent * event )
{
    event->accept();
    extern bool speech;
    if ( speech == 1 ){
        QString *txt = new QString(this->text());
        this->readCaption(txt);
    }
    qDebug() << "parlant per focus" << QString(this->text());

}

#include "qpushbuttonwithevents.h"
#include "QPushButton"
#include "QObject"
#include "QWidget"
#include <QProcess>
#include <QString>
#include <QEvent>

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
    QString *txt = new QString(this->text());
    this->readCaption(txt);

}

//TODO: on key focus, use readCaption function
//void QPushButtonWithEvents::

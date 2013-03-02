#include "qradiobuttonwithevents.h"
#include "QObject"
#include "QWidget"
#include <QProcess>
#include <QString>
#include <QEvent>
#include <QFocusEvent>
#include <QDebug>

QRadioButtonWithEvents::QRadioButtonWithEvents(QWidget *parent) :
    QRadioButton(parent)
{
    connect(this, SIGNAL(clicked()),
                 this, SLOT(buttonClickedFunction()));
}

void QRadioButtonWithEvents::readCaption( QString * label )
{
    QProcess *readcommand = new QProcess();
    readcommand->start(QString("spd-say \"%1\"").arg(*label));
}


void QRadioButtonWithEvents::enterEvent( QEvent * event )
{
    event->accept();
    extern bool speech;
    if ( speech == 1 ){
        QString *txt = new QString(this->text());
        this->readCaption(txt);
    }
    //qDebug() << "talking... " << QString(this->text());
}


void QRadioButtonWithEvents::focusInEvent( QFocusEvent * event )
{
    event->accept();
    extern bool speech;
    if ( speech == 1 ){
        QString *txt = new QString(this->text());
        this->readCaption(txt);
    }
    //qDebug() << "talking by tab key focus... "  << QString(this->text());

}

void QRadioButtonWithEvents::buttonClickedFunction()
{
    extern bool speech;
    QString *txt = new QString(tr("Activated")+" "+this->text());
    if ( speech == 1 ){

        this->readCaption(txt);
    }
    //qDebug() << "talking... " << txt->toAscii();
}

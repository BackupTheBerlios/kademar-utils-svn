#include "qcheckboxwithevents.h"
#include "QObject"
#include "QWidget"
#include <QProcess>
#include <QString>
#include <QEvent>
#include <QFocusEvent>
#include <QDebug>
#include <QBool>
QCheckBoxWithEvents::QCheckBoxWithEvents(QWidget *parent) :
    QCheckBox(parent)
{
    connect(this, SIGNAL(clicked()),
                 this, SLOT(readClicked()));
}

void QCheckBoxWithEvents::readCaption( QString * label )
{
    QProcess *readcommand = new QProcess();
    readcommand->start(QString("spd-say \"%1\"").arg(*label));
}


void QCheckBoxWithEvents::enterEvent( QEvent * event )
{
    event->accept();
    extern bool speech;
    if ( speech == 1 ){
        QString *txt = new QString(this->text());
        this->readCaption(txt);
    }
    //qDebug() << "talking... " << QString(this->text());
}


void QCheckBoxWithEvents::focusInEvent( QFocusEvent * event )
{
    event->accept();
    extern bool speech;
    if ( speech == 1 ){
        QString *txt = new QString(this->text());
        this->readCaption(txt);
    }
    //qDebug() << "talking by tab key focus... "  << QString(this->text());

}

void QCheckBoxWithEvents::readClicked()
{
    extern bool speech;
    QString *txt = new QString();
    if (this->isChecked() == true){
        *txt = QString(tr("Activated")+" "+this->text());
        //*txt = QString(tr("Activated")+" "+this->text());
    } else {
        *txt = QString(tr("Desactivated")+" "+this->text());
    }

    if ( speech == 1 ){
        this->readCaption(txt);
    }
    //qDebug() << "talking... " << txt->toAscii();
}

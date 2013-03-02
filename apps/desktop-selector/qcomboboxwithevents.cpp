#include "qcomboboxwithevents.h"
#include "QObject"
#include "QWidget"
#include <QProcess>
#include <QString>
#include <QEvent>
#include <QFocusEvent>
#include <QDebug>

QComboBoxWithEvents::QComboBoxWithEvents(QWidget *parent) :
    QComboBox(parent)
{
    connect(this, SIGNAL(activated(int)),
                 this, SLOT(readClicked()));
}

void QComboBoxWithEvents::readCaption( QString * label )
{
    QProcess *readcommand = new QProcess();
    readcommand->start(QString("spd-say \"%1\"").arg(*label));
}


void QComboBoxWithEvents::enterEvent( QEvent * event )
{
    event->accept();
    extern bool speech;
    if ( speech == 1 ){
        QString *txt = new QString(this->currentText());
        this->readCaption(txt);
    }
    //qDebug() << "talking... " << QString(this->currentText());
}


void QComboBoxWithEvents::focusInEvent( QFocusEvent * event )
{
    event->accept();
    extern bool speech;
    if ( speech == 1 ){
        QString *txt = new QString(this->currentText());
        this->readCaption(txt);
    }
    //qDebug() << "talking by tab key focus... "  << QString(this->currentText());

}

void QComboBoxWithEvents::readClicked()
{
    extern bool speech;
    if ( speech == 1 ){
        QString *txt = new QString(this->currentText());
        this->readCaption(txt);
    }
    //qDebug() << "talking by highlight... " << this->currentText().toAscii();

}

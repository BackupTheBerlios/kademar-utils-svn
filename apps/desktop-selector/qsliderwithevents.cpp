#include "qsliderwithevents.h"
#include "QObject"
#include "QWidget"
#include <QProcess>
#include <QString>
#include <QEvent>
#include <QFocusEvent>
#include <QDebug>
#include <QBool>

extern QList<QString> graphicResolutions;

QSliderWithEvents::QSliderWithEvents(QWidget *parent) :
    QSlider(parent)
{
    connect(this, SIGNAL(valueChanged(int)),
                 this, SLOT(readSlider(int)));
}

void QSliderWithEvents::readCaption( QString * label )
{
    QProcess *readcommand = new QProcess();
    readcommand->start(QString("spd-say \"%1\"").arg(*label));
}


void QSliderWithEvents::enterEvent( QEvent * event )
{
    event->accept();
    //extern bool speech;
    this->readSlider(this->value());
    //qDebug() << "talking... "; // << QString(this->text());
}


void QSliderWithEvents::focusInEvent( QFocusEvent * event )
{
    event->accept();
    //extern bool speech;
    this->readSlider(this->value());
    //qDebug() << "talking by tab key focus... "; // << QString(this->text());
}

void QSliderWithEvents::readSlider(int value)
{
    extern bool speech;
    extern QList<QString> graphicResolutions;

    //int num = this->value();
    QString *txt = new QString(graphicResolutions[value]);
    //QList<QString> *list1 = new QList<QString>;
    //*list1 = txt->split("x");

    //*txt = "%1 "+tr("per")+" %2";//.arg(*list1[0]);

    //*txt->replace(QRegExp("x"), QString(tr("per")));
    if ( speech == 1 ){

        this->readCaption(txt);
    }
    //qDebug() << "talking... " << txt->toAscii();
}

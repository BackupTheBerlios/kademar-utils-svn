#include <QtGui/QApplication>
#include "desktopselector.h"
#include <QTranslator>
#include <QString>
#include <QLocale>
#include <QFile>

int main(int argc, char *argv[])
{
    QFile *f = new QFile("/etc/kademar/config-livecd");
    f->open(QIODevice::ReadOnly);
    QString *fContent = new QString(f->readAll());
    if ( (fContent->contains("desktop_selector=no")) || (fContent->contains("desktop_selector=\"no\"")) || (fContent->contains("desktop_selector = \"no\"")) || (fContent->contains("desktop_selector = no")))
    {
        QApplication a(argc, argv);
    } else {
        QApplication a(argc, argv);

        QString qmPath = ":/tr/tr/";

        QTranslator appTranslator;
        appTranslator.load(QLocale::system().name(), qmPath);
        a.installTranslator(&appTranslator);

        QTranslator qtTranslator;
        qtTranslator.load("qt_" + QLocale::system().name(), "/usr/share/qt4/translations");
        a.installTranslator(&qtTranslator);

        DesktopSelector w;
        w.show();
        return a.exec();
    }
}

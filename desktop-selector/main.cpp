#include <QtGui/QApplication>
#include "desktopselector.h"
#include <QTranslator>
#include <QString>
#include <QLocale>

int main(int argc, char *argv[])
{
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

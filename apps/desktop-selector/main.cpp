#include <QtGui/QApplication>
#include "desktopselector.h"
#include <QTranslator>
#include <QString>
#include <QLocale>
#include <QFile>
#include <QTranslator>

QTranslator *appTranslator;
QTranslator *qtTranslator;


int main(int argc, char *argv[])
{
    //QFile *f = new QFile("/etc/kademar/config-livecd");
    //f->open(QIODevice::ReadOnly);
    //QString *fContent = new QString(f->readAll());
    //if ( (fContent->contains("desktop_selector=no")) || (fContent->contains("desktop_selector=\"no\"")) || (fContent->contains("desktop_selector = \"no\"")) || (fContent->contains("desktop_selector = no")))
    QSettings settings("/home/clawlinux/desktop-selector.ini", QSettings::IniFormat);

    if (settings.value("START").toString() != ""){
        if (QBool(settings.value("START").toBool()) == QBool(false)){
            QApplication app(argc, argv);
        } else {
            QApplication app(argc, argv);
            app.setQuitOnLastWindowClosed(true);

             qtTranslator = new QTranslator();
            //qtTranslator.load("qt_" + QLocale::system().name(), "/usr/share/qt4/translations");
            app.installTranslator(qtTranslator);

            appTranslator = new QTranslator();
            app.installTranslator(appTranslator);

            DesktopSelector w;
            w.show();
            return app.exec();
        }
    } else {
        QApplication app(argc, argv);


        /*QString qmPath = ":/tr/tr/";

        QTranslator appTranslator;
        appTranslator.load(QLocale::system().name(), qmPath);
        a.installTranslator(&appTranslator);
*/
        qtTranslator = new QTranslator();
        //qtTranslator.load("qt_" + QLocale::system().name(), "/usr/share/qt4/translations");
        app.installTranslator(qtTranslator);

        appTranslator = new QTranslator();
        app.installTranslator(appTranslator);

        DesktopSelector w;
        w.show();
        return app.exec();
    }
}

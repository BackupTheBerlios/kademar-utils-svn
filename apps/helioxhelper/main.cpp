#include <QApplication>
#include "helioxhelper.h"
#include <writeConfig.h>
//#include <iostream>
//#include <QSharedMemory>
#include <SingleApplication.h>

int main(int argc, char *argv[])
{
    SingleApplication a(argc, argv, "/ProyectoHeliox/HelioxHelper");

        if (a.isRunning())
        {
            a.sendMessage("message from other instance.");
            return 0;
        }

    bool autoStartDetection;
    autoStartDetection=false;
    QSettings settings("ProyectoHeliox", "HelioxHelper");
    QStringList list = QCoreApplication::arguments ();
    //qDebug() << list;
    for (int i = 0; i < list.size(); ++i){
        if (list.at(i) == "autostart" ){
            autoStartDetection=true;
        }
    }

    //if autostart parameter force read autostart variable (used on /usr/share/autostart/helioxhelper-autostart.desktop
    if ((settings.value("General/autostart").toString() != "") && (settings.value("General/autostart").toBool() == false) && (autoStartDetection == true)) {
        qWarning() << "Not autostart HelioxHelper, requested on config file";
    } else {

              a.setQuitOnLastWindowClosed(false);
              writeConfig();
              HelioxHelper *w = new HelioxHelper;

              // connect message queue to the main window.
              QObject::connect(&a, SIGNAL(messageAvailable(QString)), w, SLOT(activateWindowSignal(QString)));

              //Set window flags depending config
              if (settings.value("General/alwaysOnTop").toBool() == true) {
                  w->setWindowFlags(Qt::Tool | Qt::FramelessWindowHint | Qt::CustomizeWindowHint | Qt::WindowStaysOnTopHint);
              } else if (settings.value("General/alwaysOnBottom").toBool() == true) {
                  w->setWindowFlags(Qt::Tool | Qt::FramelessWindowHint | Qt::CustomizeWindowHint | Qt::WindowStaysOnBottomHint);
              } else {
                  w->setWindowFlags(Qt::Tool | Qt::FramelessWindowHint | Qt::CustomizeWindowHint);
              }

              //a.setActiveWindow(&w);
              //a.setActiveWindow();
              w->show();
              //w.grabKeyboard();
              //w.setFocus(Qt::ActiveWindowFocusReason);
              //w.setFocusPolicy(Qt::StrongFocus); //solved not grabbing tabulator
              w->activateWindow();
              return a.exec();


    }
}



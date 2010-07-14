#include <QtGui/QApplication>
#include "desktopselector.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    DesktopSelector w;
    w.show();
    return a.exec();
}

#ifndef HELIOXHELPER_H
#define HELIOXHELPER_H

#include <QWidget>
#include <QMenu>
#include <QSystemTrayIcon>
#include <QDesktopWidget>
#include <QDebug>
#include <QPainter>
#include <QPixmap>
#include <QBitmap>
#include <QSettings>
#include <QFile>
#include <QDir>
#include <QEvent>
#include <QKeyEvent>
#include <QIODevice>
#include <QProcess>
#include <qtoolbuttonwithevents.h>
//#include <qtsingleclass

namespace Ui {
class HelioxHelper;
}

class HelioxHelper : public QWidget
{
    Q_OBJECT
    
public:
    explicit HelioxHelper(QWidget *parent = 0);
    ~HelioxHelper();
  // void writeConfig();
    
private slots:
    void iconActivated(QSystemTrayIcon::ActivationReason reason);
    void troggleShowMainWindow();
    void minimizeWindow();
    void startApplication(QString string, QString prop);
    void activateWindowSignal(QString string);


private:
    Ui::HelioxHelper *ui;
    QSystemTrayIcon *trayIcon;
    QMenu *trayIconMenu;
    //  void createIconGroupBox();
    //       void createMessageGroupBox();
    void createActions();
    void createTrayIcon();
    QAction *quitAction;
    QAction *normalAction;
    QAction *minimizeAction;
    void setWindowSize();
    void createConnections();
    void setWidgetSize();
    void setStyleClass();
    QRegion roundedRect(const QRect& rect, int r);
    //QSettings settings("ProyectoHeliox", "HelioxHeper");

    struct Applications {
         QString appName;
         QString appIcon;
         QString appDesc;
         QString appExec;
     };
    void setGuiLookAndFeel();

    void createApplicationButtons();

    int numCol;
    int numRow;
    int position;

//protected:
//    bool eventFilter(QObject* object,QEvent* event);
};

#endif // HELIOXHELPER_H

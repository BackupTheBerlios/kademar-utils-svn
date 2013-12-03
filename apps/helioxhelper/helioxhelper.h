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
#include <QWidget>
#include <QDir>
#include <QEvent>
#include <QKeyEvent>
#include <QIODevice>
#include <QProcess>
#include <qtoolbuttonwithevents.h>
//#include <qtsingleclass
#include <qactionwithevents.h>
#include <wideiconsmenu.h>
//#include <QFrame>

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
    void changeLanguage(QString prop, QString value);
    void showLanguageMenu();
    void showAbout();
    void settingsWindow();
    void reloadConfiguration();
    void showMenu();
//    void showAppBox();

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
    QAction *settingsAction;
    QAction *aboutAction;
    void setWindowSize();
    void createConnections();
    void setWidgetSize();
    void setStyleClass();
    QSettings *settings;
    QString settings1;
    QString settings2;
    QRegion roundedRect(const QRect& rect, int r);
    //QSettings settings("ProyectoHeliox", "HelioxHeper");
    QList <QProcess* > startedApps;
    QList< QToolButtonWithEvents* > listApplicationButtons;
    QMenu *languageMenu;
    QHash<QString, QString> dict;
    void defineLanguageDictionary();
    QList< QActionWithEvents* > listLangActions;
    QString execShellProcess(QString idCommand, QString idParam, QString idParam2);
    void createLanguageButton(QString *lang);
    void createLanguageButtons();
    int numlanguage;
    int numApp;
    QProcess settingsProcess;
    QToolButtonWithEvents *languageButtonSelection;
    QToolButtonWithEvents *helioxButtonSelection;
   // QFrame *separatorButtons;
    QDesktopWidget qDesktopWidget;


    void blockAllApplicationButtonSignals(bool value);


    struct Applications {
         QString appName;
         QString appIcon;
         QString appDesc;
         QString appExec;
     };
 //   void setGuiLookAndFeel();

    void createApplicationButtons();

    int numCol;
    int numRow;
    int position;
    QString selectedLanguage;
    QWidget *aboutWidget;

protected:
    void changeEvent(QEvent *e);
};

#endif // HELIOXHELPER_H

 #ifndef DESKTOPSELECTOR_H
#define DESKTOPSELECTOR_H

#include <QMainWindow>
//#include "process.h"
#include <QSettings>
#include <QMenu>
#include <QAction>
#include "wideiconsmenu.h"
#include <qactionwithevents.h>
#include <qpushbuttonwithevents.h>
#include <QGridLayout>
#include <QLabel>
#include <QHBoxLayout>
#include <qtoolbuttonwithevents.h>



namespace Ui {
    class DesktopSelector;
}

class DesktopSelector : public QMainWindow {
    Q_OBJECT
public:
    DesktopSelector(QWidget *parent = 0);
    ~DesktopSelector();
    void setMaxResolution();
    void createDesktopButtons();
    void defineLanguageDictionary();
    void nextPage();

    void setupPages();
    void prepareGui();
    QString execShellProcess(QString idCommand, QString idParam, QString idParam2);
    void defineGraphicList();
    void translateGui();
   // void changeEvent(QEvent* event);
    void readCaptionConst( QString & label );
    void changeLanguage(QString *lang);
    void confirmShutReboot(QString &action);
    void detectGraphicCard();

public slots:
    void askForShutdown();
    void writeSettings(QString string, QString prop, int next = 1);
    void cancelShutdown();
    void shutdownButton();
    void rebootButton();
    void readLabelOnEnterPage(int);
    void finalSteps();
    void showLanguageMenu();
    void showDesktopMenu();

    //void startDesktop(const int &m_listNumber);
    //void startDesktop(QString m_property);
    void resolSliderValueChanged(int);
    void changeForcedState(int);
    void previousPage();
    void showAccessibilityOptions();
    void showAdvancedConfiguration();
    void showAdvancedAccessibilityConfiguration();
    void returnToUseSelectionPageFromAccessibility();
    void showSimpleAccessibilityConfiguration();
    void returnToUseSelectionPageFromDisplay();
    void createUserButton(QString *user);
    void installVideoDriver(QString driver);

protected:
    void changeEvent(QEvent *e);

private:
    Ui::DesktopSelector *ui;
    void setConnects();
    void createDesktopButton(QString *desk, QString *recommended);
    void createLanguageButton(QString *lang);
    int numdesktop;
    int numlanguage;
    int numpages;
    int numusers;
    QString buttonStyleSheet;
    QString selectedLang;
    QString selectedDesktop;
    QString selectedDriver;
    QString selectedResol;
    QString selectedUser;
    bool detectedNvidia;
    bool detectedAti;
    QList< QActionWithEvents* > listLangActions;
    QList< QActionWithEvents* > listDesktopActions;
    QList< QGridLayout* > listGridLayout;
    QList< QPushButtonWithEvents* > listDesktopButtons;
    QList< QLabel* > listDesktopImage;
    QList< QPushButtonWithEvents* > listUserButtons;
    QList< QLabel* > listUserLabels;
    bool installingDrivers;


    QList< QHBoxLayout* > listHorizontalLayout;
    QList< QPushButtonWithEvents* > listLangButtons;

    QHash<QString, QString> dict;

    QList< QWidget* > listPages;



    QMenu *languageMenu;
    QMenu *desktopMenu;

    //Process pro;


};

#endif // DESKTOPSELECTOR_H

#include "desktopselector.h"
#include "ui_desktopselector.h"
#include "QDesktopWidget"
#include "QPixmap"
//#include "QMessageBox"
#include "QString"
#include "QTextStream"
#include "QFile"
#include "QProcess"
#include "QDebug"
#include "QList"
#include "QLabel"
#include "QTranslator"
#include "QLocale"
#include "QApplication"

bool speech;

QList< QGridLayout* > listGridLayout;
QList< QPushButtonWithEvents* > listDesktopButtons;
QList< QLabel* > listDesktopImage;

QList< QHBoxLayout* > listHorizontalLayout;
QList< QPushButtonWithEvents* > listLangButtons;

QHash<QString, QString> dict;

QList< QWidget* > listPages;

QList<QString> graphicResolutions;

QSettings settings("/etc/kademar/desktop-selector.ini", QSettings::IniFormat);

QList< QAction* > listLangActions;
QList< QAction* > listDesktopActions;
//QMenu *languageMenu = new QMenu;


extern QTranslator *appTranslator;

extern QTranslator *qtTranslator;
//extern QApplication *app;

DesktopSelector::DesktopSelector(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::DesktopSelector)
{
    extern QSettings settings;

    languageMenu = new QMenu(this);
    desktopMenu = new QMenu(this);

    ui->setupUi(this);
    ui->hslider_resolutions->blockSignals(true);  //block read before configure
    numdesktop=0;
    numlanguage=0;
    numpages=0;
    detectedAti=false;
    detectedNvidia=false;
    languageMenu->addSeparator();

    //No comments... :)
    this->prepareGui();
    //this->translateGui();
    this->changeLanguage(new QString("es"));

    // Manual Button Creation
    /*
    this->createDesktopButton(new QString("kde4"), new QString("true"));
    this->createDesktopButton(new QString("kde3"), new QString("false"));
    this->createDesktopButton(new QString("gnome"), new QString("false"));
    this->createDesktopButton(new QString("lxde"), new QString("false"));
    */
    /*
    this->createLanguageButton(new QString("ca"));
    this->createLanguageButton(new QString("es"));
    this->createLanguageButton(new QString("en"));
    this->createLanguageButton(new QString("mx"));
    */
    this->createLanguageButton(new QString("mx"));
    this->createLanguageButton(new QString("fr"));

    this->setupPages(); //setup pages after know actual situation

    //Use detect-monitor to configure it
    QProcess *dresol = new QProcess();
    dresol->start(QString("/usr/share/kademar/scripts/engegada/detect-monitor"));
    //TODO IF not configured manually

    //Detect if want speech-dispatcher use if isn't on configuration file
    extern bool speech;
    speech=0;

    if (settings.value("SPEECH").toString() == ""){

        QFile *cmdline = new QFile("/proc/cmdline");
        cmdline->open(QIODevice::ReadOnly);
        QString *cmdlineContent = new QString(cmdline->readAll());
        if ( (cmdlineContent->contains("scrread")) || (cmdlineContent->contains("screenread")) )
        {
            speech=1;

        }
        //qDebug() << "speech activated by speech-dispatcher detection. Result:" << speech;
    } else {
        speech=bool(settings.value("SPEECH").toBool());
        //qDebug() << "speech activated by config file. Result:" << speech;
    }

    //qDebug() << "after: " << speech;

    if ( speech == 1 ){
        //configure Volumes (usefull to screenreader)
        QProcess *volumes = new QProcess();
        volumes->start(QString("/usr/share/kademar/scripts/engegada/volums"));
        volumes->waitForFinished();

    }
    ui->hslider_resolutions->blockSignals(false);  //read again after configure

    //qDebug() << settings.value("DisableLaptopDetect").toBool();
    if (settings.value("DisableLaptopDetect").toBool() != true )
    {
        QString what;
        QString *laptop = new QString(execShellProcess(QString("/bin/sh"), QString("-c"), QString("laptop-detect 2>/dev/null | echo $?")));
        if (laptop->contains("0")){
            what="off";
        } else {
            what="on";
        }
       // qDebug() << what;
        QProcess *lap = new QProcess();
        lap->start(QString("numlockx %1").arg(what));

    }


 //   qDebug() << "selectedLang" << selectedLang;

   // qDebug() << "selectedDesktop" << selectedDesktop;
}


DesktopSelector::~DesktopSelector()
{
    delete ui;
}

void DesktopSelector::changeEvent(QEvent *e)
{
    QMainWindow::changeEvent(e);
    switch (e->type()) {
    case QEvent::LanguageChange:
        ui->retranslateUi(this);
        //put again good resolution on label, not useless translation
        this->resolSliderValueChanged(ui->hslider_resolutions->value());
        this->detectGraphicCard();
        break;        
    default:
        e->accept();
        break;

    }
}



/*
*******************************
***                         ***
***  Common Function Part   ***
***                         ***
*******************************
*/
void DesktopSelector::prepareGui()
{
    //Add new GridLayout to append to desktop frame and put new name
    listGridLayout << new QGridLayout(ui->desktopFrame);
    listGridLayout[numdesktop]->setObjectName(QString("gridLayout_%1").arg(numdesktop));

    //Add new horitzontalLayout (HBox) to append to desktop frame and put new name
    listHorizontalLayout << new QHBoxLayout(ui->languageFrame);
    listHorizontalLayout[numlanguage]->setObjectName(QString("horizontalLayout_%1").arg(numlanguage));

    //StyleSheet for title label
    ui->desktopLabel->setStyleSheet("QLabel { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #7d7d7d, stop: 1 white) ; border-style: outset; border-width: 1px; border-radius: 5px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px; margin-bottom: 10px;}");
    ui->languageLabel->setStyleSheet("QLabel { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #7d7d7d, stop: 1 white) ; border-style: outset; border-width: 1px; border-radius: 5px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px; margin-bottom: 10px;}");
    ui->displayLabel->setStyleSheet("QLabel { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #7d7d7d, stop: 1 white) ; border-style: outset; border-width: 1px; border-radius: 5px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px; margin-bottom: 10px;}");
    ui->accessibilityLabel->setStyleSheet("QLabel { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #7d7d7d, stop: 1 white) ; border-style: outset; border-width: 1px; border-radius: 5px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px; margin-bottom: 10px;}");
    //languageMenu->setStyleSheet("QMenu { width: 150px; } QMenu::item {padding-top: 10px;padding-bottom: 10px; width: 150px;};");
        //languageMenu->set
    //languageMenu->setStyleSheet("QMenu::item{ padding-top: 4px; padding-left: 5px; padding-right: 15px; padding-bottom: 4px; }");
    languageMenu->setStyleSheet("QMenu { border-radius: 10px; border: 1px solid rgb(110, 110, 110); font: bold 14px; }  QMenu::item {font-weight: bold; }");
    desktopMenu->setStyleSheet("QMenu { border-radius: 10px; border: 1px solid rgb(110, 110, 110); font: bold 14px; }  QMenu::item {font-weight: bold; }");


    //languageMenu->setStyle(new myStyle);
    int iconswidth = 16+4+16;

    languageMenu->setStyle( new WideIconsMenu( iconswidth ) );
    desktopMenu->setStyle( new WideIconsMenu( iconswidth ) );



    ui->l_shutdown->setStyleSheet("QLabel { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #7d7d7d, stop: 1 white) ; border-style: outset; border-width: 1px; border-radius: 5px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px; margin-bottom: 10px;}");

    //StyleSheet for frames
    ui->controlFrame->setStyleSheet("QWidget#controlFrame { background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 #939494, stop: 1 white) ; border-style: outset; border-width: 1px; border-radius: 5px; border-color: beige; font: bold 14px; min-width: 10em;}");
    ui->displayFrame->setStyleSheet("QFrame#displayFrame  { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #dadada, stop: 1 white) ; border-style: outset; border-width: 1px; border-radius: 5px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px;}");
    ui->languageFrame->setStyleSheet("QFrame#languageFrame { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #dadada, stop: 1 white) ; border-style: outset; border-width: 1px; border-radius: 5px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px;}");
    ui->desktopFrame->setStyleSheet("QFrame#desktopFrame  { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #dadada, stop: 1 white) ; border-style: outset; border-width: 1px; border-radius: 5px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px;}");
    ui->shutdownFrame->setStyleSheet("QFrame#shutdownFrame  { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #dadada, stop: 1 white) ; border-style: outset; border-width: 1px; border-radius: 5px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px;}");
    ui->accessibilityFrame->setStyleSheet("QFrame#accessibilityFrame  { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #dadada, stop: 1 white) ; border-style: outset; border-width: 1px; border-radius: 5px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px;}");


    //ui->b_startDesktop->setStyleSheet(QString("QPushButtonWithEvents %1").arg(buttonStyleSheet));

    connect(ui->b_shutdown, SIGNAL(clicked()), this, SLOT(askForShutdown()));
    connect(ui->b_cancel, SIGNAL(clicked()), this, SLOT(cancelShutdown()));
    connect(ui->b_shutdownComputer, SIGNAL(clicked()), this, SLOT(shutdownButton()));
    connect(ui->b_rebootComputer, SIGNAL(clicked()), this, SLOT(rebootButton()));
    connect(ui->b_previous, SIGNAL(clicked()), this, SLOT(previousPage()));
    connect(this->ui->hslider_resolutions, SIGNAL(valueChanged(int)), this, SLOT(resolSliderValueChanged(int)));
    connect(ui->ch_forceDriver, SIGNAL(stateChanged(int)), this, SLOT(changeForcedState(int)));
    connect(ui->ch_forceResol, SIGNAL(stateChanged(int)), this, SLOT(changeForcedState(int)));
    connect(ui->stackedWidget, SIGNAL(currentChanged(int)), this, SLOT(readLabelOnEnterPage(int)));
    connect(ui->b_startDesktop, SIGNAL(clicked()), this, SLOT(finalSteps()));
    connect(ui->b_language, SIGNAL(clicked()), this, SLOT(showLanguageMenu()));
    connect(ui->b_desktop, SIGNAL(clicked()), this, SLOT(showDesktopMenu()));


    //stethic tune
    ui->b_previous->setVisible(false);
    ui->advancedAccessibilityGroupBox->setVisible(false);

    //this->setConnects();
    this->setMaxResolution();
    this->createDesktopButtons();

    this->defineLanguageDictionary();
    //this->createLanguageButtons();
    this->defineGraphicList();

    this->detectGraphicCard();
}

void DesktopSelector::readCaptionConst( QString & label )
{
    extern bool speech;
    if ( speech == 1 ){
        QProcess readcommand;
        readcommand.start(QString("spd-say \"%1\"").arg(label));
        readcommand.waitForFinished();
    }
    //        qDebug() << label;
}

//Write settings to file to start with your options
void DesktopSelector::writeSettings(QString string, QString prop, int next)
{
    /*
    if (string == "")
    {


    }

    //QString *varDesktop = new QString("DESKTOP=" + *desk + "\n");
    QFile *file = new QFile("/var/tmp/xserver");
    if ( file->open( QIODevice::Append ) )
    {
        QTextStream stream( file );
        stream <<QString(string + "=" + prop + "\n");
    }
    file->close();
    */


    //Process funtions of actual page
    //qDebug() << listPages[numpages]->objectName();
    QString *name = new QString(listPages[numpages]->objectName());
    if (*name == "languagePage") {
        //qDebug() << string << prop;
        this->changeLanguage(new QString(prop));
        selectedLang=prop;
       // qDebug() << "selectedLang" << selectedLang;

    } else if (*name == "desktopPage") {
        //qDebug() << string << prop;
        selectedDesktop=prop;
    } else if (*name == "displayPage") {
        qDebug() << string << prop;
        if (ui->ch_forceDriver->isChecked())
        {
            selectedDriver=ui->cb_chipset->currentText();
        }
        if (ui->ch_forceResol->isChecked())
        {
            extern QList<QString> graphicResolutions;
            selectedResol=graphicResolutions[ui->hslider_resolutions->value()];
        }
    }

    //Write settings
    //extern QSettings settings;

    //settings.setValue(string,prop);
    //settings.sync();


    //qDebug() << string << prop;
 //   value
   //         if (settings.value("LANGLIST").toString() == ""){

    if (next == 1){
        this->nextPage();
    }
}

void DesktopSelector::setupPages()
{
    extern QSettings settings;

    extern QList< QWidget* > listPages;



    //listPages << ui->accessibilityPage;


    //
    //  LANGUAGE PAGE SETUP
    //

    //If only found one language or desktop, not add to pages to show
    //if (numlanguage != 1){
    //    listPages << ui->languagePage;
    //} else

    //qDebug() << settings.value("lang").toString();

    //if pre-configured language, load it
    if (settings.value("LANG").toString() != ""){
        this->changeLanguage(new QString(settings.value("LANG").toString()));
        selectedLang=QString(settings.value("LANG").toString());
    } else{
    //if not pre-configured language, look on langlist
        //if not pre-configured langlist to select, use default langlist
        if (settings.value("LANGLIST").toString() == ""){
            this->createLanguageButton(new QString("ca"));
            this->createLanguageButton(new QString("es"));
            this->createLanguageButton(new QString("en"));

            //and load page
            listPages << ui->languagePage;

            //qDebug() << settings.value("LANGLIST").toString();
        } else {
            //qDebug() << QString(settings.value("LANGLIST").toString()).split(" ");
            //create languages of langlist
            foreach (QString lang, settings.value("LANGLIST").toString().split(" ")){
                //qDebug() << lang;
                this->createLanguageButton(new QString(lang));
            }
            //if not created, means that langlist only has one, load it
            //if only is one language configured on langlist, load it
            if ((numlanguage == 1) || (numlanguage == 0)){
                //listLangButtons[numlanguage]->buttonClickedFunction();
                this->changeLanguage(new QString(settings.value("LANGLIST").toString()));
                //this->writeSettings("LANG",settings.value("LANGLIST").toString(), 0);
                selectedLang=QString(settings.value("LANGLIST").toString());
            } else {
                //and load page
                listPages << ui->languagePage;
            }

        }
        //    changeLanguage
    }


    //if not pre-configured desktop
    if (settings.value("DESKTOP").toString() == ""){
        //and it detected more than 1 desktop, load page
        if (numdesktop != 1){
                listPages << ui->desktopPage;
        } else {
            selectedDesktop=listDesktopButtons[0]->textPropertyValue();
        }
        //Other possibilities to not be added
            //listPages << ui->desktopPage;
    } else {
        selectedDesktop=settings.value("DESKTOP").toString();
    }


    //If preconfigured xmodule do not show free/non-free  choose frame
    if (settings.value("XMODULE").toString() != ""){
        ui->driverFrame->setVisible(false);
        ui->displayChipetLabel->setVisible(false);
        ui->ch_forceDriver->setVisible(false);
        ui->cb_chipset->setVisible(false);
        selectedDriver=settings.value("XMODULE").toString();
        //qDebug() << "driverframe disabled XMODULE";
    }
    //If preconfigured FREE_DRIVER want, do not show chipset free/non-free choose frame
    if (settings.value("FREE_DRIVER").toString() != ""){
        //if (QBool(settings.value("FREE_DRIVER").toBool()) == QBool(false)){
            ui->driverFrame->setVisible(false);
            ui->displayChipetLabel->setVisible(false);
            ui->displayChipetLabel->setVisible(false);

            //qDebug() << "driverframe disabled FREE_DRIVER";
        //}
    }
    //If not display advanced configuration, hide frame
    if ((settings.value("DRIVER_ADVANCED").toString() != "")){
        if (QBool(settings.value("DRIVER_ADVANCED").toBool()) == QBool(false)){
            ui->advancedConfigurationFrame->setVisible(false);
            //qDebug() << "advancedconfigurationframe disabled DRIVER_ADVANCED";
        }
    }

    if (settings.value("RESOL").toString() != ""){
        ui->driverFrame->setVisible(false);
        ui->displayChipetLabel->setVisible(false);
        ui->l_resol->setVisible(false);
        ui->ch_forceResol->setVisible(false);
        ui->hslider_resolutions->setVisible(false);
        selectedResol=settings.value("RESOL").toString();
        //qDebug() << "driverframe disabled XMODULE";
    }

    //If free/non-free driver configured or advanced configuration disabled = add page
    if ((ui->advancedConfigurationFrame->isHidden() == false) || (ui->driverFrame->isHidden() == false )){
        listPages << ui->displayPage;
    }

    //qDebug() << listPages.size();

    //Load first page
    if (listPages.size() > 0 ){
        ui->stackedWidget->setCurrentWidget(listPages[numpages]);
    } else {
       qDebug() << "exiting";
       finalSteps();  //process final steps of all
       QCoreApplication::processEvents();
       deleteLater(); //put on list the app to be removed

        //app->exit();
        //this->closeEvent();
    }


}

//Move along stacked widget pages
void DesktopSelector::nextPage()
{
    numpages=numpages+1;
    extern QList< QWidget* > listPages;
    ui->stackedWidget->setCurrentWidget(listPages[numpages]);
    //Make visible previousButton if it's the case
    if (!(ui->b_previous->isVisible())){
        ui->b_previous->setVisible(true);
    }



}

//Move along stacked widget pages
void DesktopSelector::previousPage()
{
    numpages=numpages-1;
    extern QList< QWidget* > listPages;
    ui->stackedWidget->setCurrentWidget(listPages[numpages]);
    if (numpages == 0){
        ui->b_previous->setVisible(false);
    }

}

//Read label on enter stacked page
void DesktopSelector::readLabelOnEnterPage(int num)
{
    QString label;
    if (num == 1) {
        label = ui->languageLabel->text();
        this->readCaptionConst(label);
    } else if (num == 0) {
        label = ui->desktopLabel->text();
        this->readCaptionConst(label);
    } else if (num == 2) {
        label = ui->displayLabel->text();
        this->readCaptionConst(label);
    } else if (num == 3) {
        label = ui->l_shutdown->text();
        this->readCaptionConst(label);
    }


}

QString DesktopSelector::execShellProcess(QString idCommand, QString idParam = "", QString idParam2 = ""){
    QString result, command;
    QProcess *pro = NULL;

    //Get command
    //command = QString(idCommand+" "+idParam);
    QStringList slArgs;
    slArgs << idParam << idParam2;
    //Process command
    pro = new QProcess();
    pro->setProcessChannelMode(QProcess::MergedChannels);
    pro->start(idCommand, slArgs);
    if (pro->waitForFinished()) {
        result = QString(pro->readAll());
        //Trim
        if (result != NULL && result.isEmpty() == false){
            result = result.trimmed();
        }
    }
    pro->close();

    //Free mem
    if (pro != NULL){
        delete pro;
    }

    return result;
}

/*
*******************************
***        E  N  D          ***
***  Common Function Part   ***
***        E  N  D          ***
*******************************
*/


void DesktopSelector::setMaxResolution()
{

    extern QSettings settings;
    QString wallpaper;
    if (settings.value("WALLPAPER") != ""){
        wallpaper=settings.value("WALLPAPER").toString();
    }
    QDesktopWidget qDesktopWidget;
    QRect screenSize = qDesktopWidget.screenGeometry();
    //qDebug() << screenSize.width();
    DesktopSelector::setGeometry(0,0,screenSize.width(),screenSize.height());
    //ui->background->setGeometry(0,0,screenSize.width(),screenSize.height());
    QFile *filebg = new QFile(QString("%1/%2x%3.png").arg(wallpaper).arg(screenSize.width()).arg(screenSize.height()) );
    if  (!(filebg->exists())) {

        filebg->setFileName(QString("%1/%2x%3.jpg").arg(wallpaper).arg(screenSize.width()).arg(screenSize.height()));
    }
    if  (!(filebg->exists())) {

        filebg->setFileName(QString(wallpaper));
    }
    if  (!(filebg->exists())) {

        filebg->setFileName(QString("/usr/share/wallpapers/Gota de Gebrada/contents/images/1280x1024.png"));
    }
    if  (!(filebg->exists())) {

        filebg->setFileName(QString("/usr/share/wallpapers/kademar.png"));
    }


    //ui->background->setPixmap(QPixmap(filebg->fileName()));
    ui->centralWidget->setStyleSheet(QString("QWidget#centralWidget { background-image: url(%1) };").arg(filebg->fileName()));

    //qDebug() << filebg->fileName();
}


/*
*******************************
***                         ***
***  Shutdown  Select Part  ***
***                         ***
*******************************
*/

void DesktopSelector::askForShutdown()
{
    ui->controlFrame->setVisible(false);
    ui->stackedWidget->setCurrentWidget(ui->shutdownPage);
}

void DesktopSelector::cancelShutdown()
{
    //return to previous page
    extern QList< QWidget* > listPages;
    ui->stackedWidget->setCurrentWidget(listPages[numpages]);
    ui->controlFrame->setVisible(true);
}


void DesktopSelector::shutdownButton()
{
        //qDebug() << "shutdown";
        QString action = "halt";
        this->confirmShutReboot(action);
}

void DesktopSelector::rebootButton()
{
    //qDebug() << "reboot";
    QString action = "reboot";
    this->confirmShutReboot(action);

}

void DesktopSelector::confirmShutReboot(QString &action)
{
    QProcess *halt = new QProcess();
    halt->start(QString(action));
    //execShellProcess(QString("/usr/bin/sudo"), action);
}


/*
*******************************
***        E  N  D          ***
***  Shutdown  Select Part  ***
***        E  N  D          ***
*******************************
*/

/*
*******************************
***                         ***
***  Desktop  Select Part   ***
***                         ***
*******************************
*/


void DesktopSelector::createDesktopButtons()
{
    //desktop file to detect ; desktop name to start
    QHash<QString, QString> desktops;
    desktops["/opt/trinity/bin/startkde"] = "kde3";
    desktops["/usr/bin/startkde"] = "kde4";
    desktops["/usr/bin/startgnome"] = "gnome";
    desktops["/usr/bin/startlxde"] = "lxde";
    desktops["/usr/bin/starticewm"] = "icewm";

    //Create file to check if exists desktop
    QFile *desktop = new QFile();

    //Check on desktops to detevt
    QHashIterator<QString, QString> i(desktops);
    while (i.hasNext()) {
         i.next();
         desktop->setFileName(QString(i.key()));
         if  (desktop->exists()) {
                 this->createDesktopButton(new QString(i.value()), new QString("false"));
         }
     }
}

void DesktopSelector::createDesktopButton(QString *desk, QString *recommended)
{
    // Create Desktop Buttons on GUI
    //extern int numdesktop;
    extern QList< QGridLayout* > listGridLayout;
    extern QList< QPushButtonWithEvents* > listDesktopButtons;
    extern QList< QLabel* > listDesktopImage;

    //Add new button with objectname and minimum size
    listDesktopButtons << new QPushButtonWithEvents(ui->desktopFrame);
    listDesktopButtons[numdesktop]->setObjectName(QString("b_%1").arg(*desk));
    listDesktopButtons[numdesktop]->setMinimumSize(QSize(170, 40));

    //Put label to Desktop Button, depending if it's recommended or not
    if (*recommended == "true"){
        listDesktopButtons[numdesktop]->setText(QString("Start %1 Desktop %2").arg(*desk).arg("(Recommended)"));
    }else{
        listDesktopButtons[numdesktop]->setText(QString("Start %1 Desktop").arg(*desk));
    }

    //Put property on button wich will be written on configuration file
    listDesktopButtons[numdesktop]->setTextProperty(new QString("DESKTOP"), new QString(*desk)); //set text button property to write on file

    //listDesktopButtons[numdesktop]->setStyleSheet(QString("QPushButtonWithEvents %1").arg(buttonStyleSheet));

    //Add new Label with Desktop Image
    listDesktopImage << new QLabel("", ui->centralWidget);
    listDesktopImage[numdesktop]->setObjectName(QString("l_%1").arg(*desk));

    //listDesktopImage[numdesktop]->setStyleSheet("QLabel#label1 {margin-left: 50px; background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #5E5E5E, stop: 1 white) ;}");
    listDesktopImage[numdesktop]->setMinimumSize(QSize(64, 64));
    listDesktopImage[numdesktop]->setMaximumSize(QSize(64, 64));
    listDesktopImage[numdesktop]->setPixmap(QPixmap(QString(":/img/%1").arg(*desk)));
    listDesktopImage[numdesktop]->setScaledContents(true);

    // Add to GridLayout desktop Button
    listGridLayout[0]->addWidget(listDesktopButtons[numdesktop], numdesktop, 1, 1, 1);

    // Add to GridLayout desktop Label
    listGridLayout[0]->addWidget(listDesktopImage[numdesktop], numdesktop, 0, 1, 1);

    connect(listDesktopButtons[numdesktop], SIGNAL( buttonClicked(QString, QString)), this, SLOT(writeSettings(QString, QString)));


    extern QList< QAction* > listDesktopActions;
    //listDesktopActions << new QAction(QIcon(QString(":/img/%1").arg(*desk))),*desk, this);
    listDesktopActions << new QAction(QIcon(QString(":/img/%1").arg(*desk)),*desk,this);
    desktopMenu->addAction(listDesktopActions[numdesktop]);


    numdesktop=numdesktop+1;
    //qDebug() << numdesktop;
}

/*void DesktopSelector::startDesktop(QString m_property){
    //Get information from WHO sends the signal
    QObject* pObject = sender();
    QString name = pObject->objectName();
    qDebug() << QString(m_property);
    //qDebug() << name.replace("b_","");   //  b_kde4  -> kde4
    writeSettings(new QString("DESKTOP=" + name.replace("b_","")) ); //   b_kde4  -> kde4  &  write start desktop settings
}*/


/*
*******************************
***        E  N  D          ***
***  Desktop  Select Part   ***
***        E  N  D          ***
*******************************
*/


/*
*******************************
***                         ***
***  Language Select Part   ***
***                         ***
*******************************
*/
void DesktopSelector::defineLanguageDictionary()
{
    extern QHash<QString, QString> dict;
    dict["ca"] = "Català";     dict["ca_ES"] = "Català";
    dict["es"] = "Castellano";     dict["es_ES"] = "Castellano";

    dict["en"] = "English";
    dict["fr"] = "French";
    dict["it"] = "Italiano";
    dict["de"] = "Deuche";
    dict["pt"] = "Português";
    dict["gl"] = "Galego";

    //Derivados en Mexico
    dict["mx"] = "Mexicano";
    dict["myn"] = "Maya"; dict["mx_myn"] = "Maya";
}

void DesktopSelector::changeLanguage(QString *lang){

    //translator story
    QString qmPath = ":/tr/tr/";

    //QTranslator appTranslator;
    appTranslator->load(*lang, qmPath);

    //QTranslator qtTranslator;
    qtTranslator->load("qt_" + *lang, "/usr/share/qt4/translations");

}

void DesktopSelector::createLanguageButton(QString *lang)
{
    // Create Desktop Buttons on GUI
    extern QList< QHBoxLayout* > listHorizontalLayout;
    extern QList< QPushButtonWithEvents* > listLangButtons;
    extern QHash<QString, QString> dict;  //real language names

    //Add new button with objectname and minimum size
    listLangButtons << new QPushButtonWithEvents(ui->languageFrame);
    listLangButtons[numlanguage]->setObjectName(QString("b_%1").arg(*lang));
    listLangButtons[numlanguage]->setMinimumSize(QSize(170, 40));    

    QString realLanguageName = dict.value(*lang);

    //hack to recover good accents and punctuation - losed on qhash "dict"
    QByteArray byteArray = realLanguageName.toAscii();
    const char * processingString = byteArray.data();
    QString realLanguageNameTrans = QString::fromLocal8Bit(processingString);

    listLangButtons[numlanguage]->setText(QString("  " + realLanguageNameTrans));
    listLangButtons[numlanguage]->setTextProperty(new QString("LANG"), new QString(*lang)); //set text button property to write on file

    //listDesktopImage[numdesktop]->setStyleSheet("QLabel#label1 {margin-left: 50px; background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #5E5E5E, stop: 1 white) ;}");
    listLangButtons[numlanguage]->setMinimumSize(QSize(64,  64));
    //listLangButtons[numlanguage]->setMaximumSize(QSize(64, 64));
    listLangButtons[numlanguage]->setIcon(QPixmap(QString(":/img/img/lang/%1.png").arg(*lang)));
    listLangButtons[numlanguage]->setIconSize(QSize(48,48));
    //listLangButtons[numlanguage]->setStyleSheet(QString("QPushButtonWithEvents %1").arg(buttonStyleSheet));
    //listLangButtons[numlanguage]->setStyleSheet("QPushButtonWithEvents:hover  { background-color: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 1, stop: 0 #f0efee, stop: 1 #d4d3d2) ; border-style: outset; border-width: 1px; border-radius: 3px; border-color: #444444; font: bold 14px; min-width: 10em; padding: 6px; margin-bottom: 10px;}");
    listLangButtons[numlanguage]->setMinimumWidth(140);
    // Add to GridLayout desktop Button
    listHorizontalLayout[0]->addWidget(listLangButtons[numlanguage]);

    connect(listLangButtons[numlanguage], SIGNAL( buttonClicked(QString, QString)), this, SLOT(writeSettings(QString, QString)));

    //create menu entry
    extern QList< QAction* > listLangActions;
    listLangActions << new QAction(QIcon(QPixmap(QString(":/img/img/lang/%1.png").arg(*lang))),realLanguageNameTrans, this);
    languageMenu->addAction(listLangActions[numlanguage]);



    numlanguage=numlanguage+1;
    //qDebug() << numlanguage;
}

/*
void DesktopSelector::translateGui(){

    //QApplication a = new QApplication(this);
    QString qmPath = ":/tr/tr/";

    QTranslator appTranslator;
    appTranslator.load(QLocale::system().name(), qmPath);
    a.installTranslator(&appTranslator);

    QTranslator qtTranslator;
    qtTranslator.load("qt_" + QLocale::system().name(), "/usr/share/qt4/translations");
    a.installTranslator(&qtTranslator);

}*/

/*
*******************************
***        E  N  D          ***
***  Language Select Part   ***
***        E  N  D          ***
*******************************
*/


/*
*******************************
***                         ***
***   Graphic Select Part   ***
***                         ***
*******************************
*/

void DesktopSelector::defineGraphicList()
{
    QDesktopWidget qDesktopWidget;
    QRect screenSize = qDesktopWidget.screenGeometry();

    //Prepare list of Resolutions of display
    extern QList<QString> graphicResolutions;
    graphicResolutions <<  "2048x1536" << "1920x1440" << "1920x1200" << "1856x1392" << "1800x1440" << "1792x1344" << "1680x1050" << "1600x1200" << "1440x900" << "1400x1050" << "1280x1024" << "1280x960" << "1280x800" << "1280x768" << "1280x720" << "1280x480" << "1152x864" << "1024x768" << "848x480" << "800x600" << "768x576" << "720x576" << "720x480" << "720x400" << "640x960" << "640x480";

    //Prepare resolution slider to
    this->ui->hslider_resolutions->setMaximum(graphicResolutions.count()-1);

    //prepare chipset list and fill driver combobox
    QList<QString> graphicChipset;
    graphicChipset << "vesa" << "apm" << "ark" << "chips" << "cirrus" << "cyrix" << "ati" << "fglrx" << "radeonhd" << "radeon" << "glint" << "i128" << "i740" << "imstt" << "intel" << "mga" << "neomagic" << "newport" << "nsc" << "nv" << "nvidia" << "rendition" << "s3" << "s3virge" << "savage" << "siliconmotion" << "sis" << "tdfx" << "tga" << "trident" << "tseng" << "vboxvideo" << "via" << "vmware";
    int num=0;
    foreach( QString label, graphicChipset )  {
        ui->cb_chipset->addItem("");
        ui->cb_chipset->setItemText(num, label);
        num=num+1;
    }

    //Put current resolution to resolution Slider
    this->ui->hslider_resolutions->setValue(graphicResolutions.indexOf(QString("%1x%2").arg(screenSize.width()).arg(screenSize.height())));
}

//Put resolution name on label when resolution slider moves
void DesktopSelector::resolSliderValueChanged(int value)
{
    extern QList<QString> graphicResolutions; //Take real name from global resolution list
    this->ui->l_resol->setText(graphicResolutions[value]);
}

//Changed State of Checkbox to force Driver or resolution
void DesktopSelector::changeForcedState(int value)
{
    QObject* pObject = sender();
    if (pObject->objectName() == "ch_forceResol"){
        //forced resolution
        ui->hslider_resolutions->setEnabled(QBool(value));
        ui->l_resol->setEnabled(QBool(value));
    } else {
        //forced driver
        ui->cb_chipset->setEnabled(QBool(value));
        ui->driverFrame->setEnabled(!QBool(value));
    }
    //qDebug() << QBool(value) << name;
}

void DesktopSelector::detectGraphicCard()
{
    //Lspci VGA Line
    QString *grafic = new QString(execShellProcess(QString("/bin/sh"), QString("-c"), QString("lspci | grep -i [vV][Gg][Aa] | sed s.'VGA compatible controller: '..g | sed s,'[0-9][0-9]:[0-9][0-9].[0-9]',,g | cut -d'(' -f1")));

    //put lspci | grep -i vga  on detected label
    this->ui->displayDetectedLabel->setText(tr("Detected: ")+" "+*grafic);

    //put nvidia or ati chipset logo on display logo or disable radiobutton choose
    if (grafic->contains(QRegExp("[Nn][Vv][Ii][Dd][Ii][Aa]"))) {
        this->ui->displayChipetLabel->setPixmap(QPixmap(QString(":/img/img/display-nvidia.png")));
        detectedNvidia=true;
    } else if (grafic->contains(QRegExp(" [Aa][Tt][Ii] "))) {
        this->ui->displayChipetLabel->setPixmap(QPixmap(QString(":/img/img/display-ati.png")));
        detectedAti=true;
    } else {
        //this->ui->rb_propietaryDriver->setVisible(false);
        //this->ui->rb_freeDriver->setVisible(false);
        this->ui->driverFrame->setVisible(false);
        ui->displayChipetLabel->setVisible(false);
    }
}


void DesktopSelector::finalSteps()
{
/*    //If possibility to choose free or propietary driver
    if (this->ui->driverFrame->isVisible() == true)
    {
        if (this->ui->rb_propietaryDriver->isChecked() == true)
        {
            this->writeSettings("FREE_DRIVER","false", 0);
        } else {
            this->writeSettings("FREE_DRIVER","true", 0);
        }
    }

    extern QList<QString> graphicResolutions;

    //If forced chipset selected, use it
    if (this->ui->ch_forceResol->isChecked() == true)
    {
        this->writeSettings("RESOL",graphicResolutions[ui->hslider_resolutions->value()], 0);
    }  */


    QFile *file2 = new QFile("/var/tmp/xserver");
    if ( file2->open( QIODevice::WriteOnly ) )
    {
        QTextStream stream( file2 );
        stream <<QString("DESKTOP=" + selectedDesktop + "\n");
        stream <<QString("LANG=" + selectedLang + "\n");
    }
    file2->close();

    QFile *file = new QFile("/etc/X11/xorg.conf.d/10-driver.conf");
    if ((ui->ch_forceDriver->isChecked()) || (selectedDriver != "")){
        if (ui->ch_forceDriver->isChecked())
        {
            selectedDriver=ui->cb_chipset->currentText();
        }
        if ( file->open( QIODevice::WriteOnly  | QIODevice::Text) )
        {
            QTextStream stream( file );
            stream << "Section \"Device\"\n";
            stream << "  Identifier \"<default device>\"\n";
            stream << "  Driver \""+ selectedDriver +"\"\n";
            stream << "EndSection\n";
        }
        file->close();
    } else {
        file->remove();
    }


    QFile *file1 = new QFile("/etc/X11/xorg.conf.d/10-monitor.conf");
    if ((ui->ch_forceResol->isChecked()) || (selectedResol != "")){
        if (ui->ch_forceResol->isChecked())
        {
            extern QList<QString> graphicResolutions;
            selectedResol=graphicResolutions[ui->hslider_resolutions->value()];
        }
        if ( file1->open( QIODevice::WriteOnly  | QIODevice::Text) )
        {
            QTextStream stream( file1 );
            stream << "Section \"Screen\"\n";
            stream << "  Identifier \"<default screen>\"\n";
            stream << "  DefaultDepth            24 #Choose the depth (16||24)\n";
            stream << "  SubSection             \"Display\"\n";
            stream << "    Depth               24\n";
            stream << "    Modes              \""+ selectedResol +"\" #Choose the resolution\n";
            stream << "  EndSubSection\n";
            stream << "EndSection\n";
        }
        file1->close();
    } else {
        file1->remove();
    }

    if ((detectedNvidia) && (settings.value("nvidia").toBool() == false))
    {
        if (!(settings.value("FREE_DRIVER").toBool() == true)){
            if ((ui->rb_propietaryDriver->isChecked()) || !(ui->rb_freeDriver->isChecked()))
            {
                extern QSettings settings;
                settings.setValue("nvidia", "true");
                QProcess* nvidia = new QProcess();
                connect(nvidia, SIGNAL(error(QProcess::ProcessError)), this, SLOT(close()));
                connect(nvidia, SIGNAL(destroyed()), this, SLOT(close()));
                connect(nvidia, SIGNAL(finished(int)), this, SLOT(close()));
                ui->b_startDesktop->setEnabled(false);
                ui->advancedConfigurationFrame->setVisible(false);
                ui->driverFrame->setVisible(false);
                ui->displayLabel->setVisible(false);
                ui->b_startDesktop->setVisible(false);
                ui->displayDetectedLabel->setText(tr("Installing Nvidia Drivers"));
                ui->displayDetectedLabel->setAlignment(Qt::AlignHCenter);
                ui->controlFrame->setVisible(false);
                ui->gridLayout_7->removeItem(ui->horizontalSpacer_9);
                ui->displayChipetLabel->setVisible(false);
                nvidia->start(QString("/usr/share/desktop-selector/scripts/nvidia-installer-offline.sh"));
            }
        }
    }

    //qDebug() << detectedNvidia;
    //qDebug() << detectedAti;
    //qDebug() << settings.value("FREE_DRIVER").toBool();

    //if not install propietary drivers, close
    // if detected nvidia or ati but using free driver, close
    //  else install propietary driver, it will close alone
    if ( detectedNvidia && (settings.value("FREE_DRIVER").toBool() == false)) {
        if ((ui->rb_freeDriver->isChecked()) || !(ui->rb_propietaryDriver->isChecked()))
        {
            this->close();
        }
    } else if ( detectedAti && (settings.value("FREE_DRIVER").toBool() == false)) {
        if ((ui->rb_freeDriver->isChecked()) || !(ui->rb_propietaryDriver->isChecked()))
        {
            this->close();
        }
    } else {
        this->close();
    }



}

/*
*******************************
***        E  N  D          ***
***   Graphic Select Part   ***
***        E  N  D          ***
*******************************
*/


/*
 *MENUS
 */

void DesktopSelector::showLanguageMenu(){
    languageMenu->exec(QCursor::pos());

}


void DesktopSelector::showDesktopMenu(){
    desktopMenu->exec(QCursor::pos());

}


//void DesktopSelector::showAdvancedConfiguration(){

//}

#include "helioxhelper.h"
#include "ui_helioxhelper.h"
#include <QToolButton>

bool speech;
//extern QSettings settings;

//QSettings settings("ProyectoHeliox", "HelioxHelper");

//QList< QToolButtonWithEvents* > listApplicationButtons;
//QList< QLabel* > listApplicationImage;


HelioxHelper::HelioxHelper(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::HelioxHelper)
{

    selectedLanguage="";
    settings1 = "ProyectoHeliox";
    settings2 = "HelioxHelper";
    settings = new QSettings(settings1, settings2);

    //loadConfig();
    numCol=0;
    numRow=0;

    //Initial define - to not crash on first reloadConfiguration()
    languageButtonSelection = new QToolButtonWithEvents(this, settings1, settings2, selectedLanguage);
    helioxButtonSelection = new QToolButtonWithEvents(this, settings1, settings2, selectedLanguage);
    //separatorButtons = new QFrame();
    position = settings->value("General/whereIsPlacedWindow").toInt();

    languageMenu = new QMenu(this);
    numlanguage=0;
    numApp=0;

    QDesktopWidget qDesktopWidget;


    //settingsProcess = new QProcess();
    defineLanguageDictionary();
    createLanguageButtons();

    ui->setupUi(this);
  //  loadConfig();

    extern bool speech;
    speech=0;

    //appBox = new QWidget();
    //appBox->show();
    //appBox->activateWindow();
    //appBox->setWindowFlags(Qt:: CustomizeWindowHint);
            //(Qt::Tool | Qt::FramelessWindowHint | Qt::CustomizeWindowHint);




    if (settings->value("General/speechText").toString() == ""){

        QFile *cmdline = new QFile("/proc/cmdline");
        cmdline->open(QIODevice::ReadOnly);
        QString *cmdlineContent = new QString(cmdline->readAll());
        if ( (cmdlineContent->contains("scrread")) || (cmdlineContent->contains("screenread")) )
        {
            speech=1;

        }
        //qDebug() << "speech activated by speech-dispatcher detection. Result:" << speech;
    } else {
        speech=bool(settings->value("General/speechText").toBool());
        //qDebug() << "speech activated by config file. Result:" << speech;
    }

    createActions();
    createTrayIcon();


    //extern QSettings settings;

    createConnections();

    //createApplicationButtons();


    setWindowIcon(QIcon(":/images/trayicon.png"));



    reloadConfiguration();

    if (settings->value("Tray Icon/showTrayIcon").toBool() == true ){
        trayIcon->show();
    }

    setFocus();
    raise();

    //QApplication::processEvents();
    //QCoreApplication::processEvents(QEventLoop::AllEvents, 100);
    //qDebug() << "cambio hecho";
    //listApplicationButtons[0]->setBlockedSignals(false);


//    QProcess updateApps;
//    updateApps.start("rahisi-config-update-apps");

}

HelioxHelper::~HelioxHelper()
{
    delete ui;
}

void HelioxHelper::createConnections()
{
        QDesktopWidget* desktop = QApplication::desktop();
    connect(trayIcon, SIGNAL(activated(QSystemTrayIcon::ActivationReason)),
                 this, SLOT(iconActivated(QSystemTrayIcon::ActivationReason)));

    //rload all when desktop resolution changes
    connect(desktop, SIGNAL(resized ( int )),this,SLOT(reloadConfiguration()));
}

void HelioxHelper::iconActivated(QSystemTrayIcon::ActivationReason reason)
{
    switch (reason) {
    case QSystemTrayIcon::Trigger:
        //qDebug() << "hola";

        if (settings->value("Tray Icon/leftClickContextualMenu").toBool() == false) {
            troggleShowMainWindow();
        } else {
            //trayIcon->contextMenu();
            trayIconMenu->exec(QCursor::pos());
          //  qDebug() << "Open context menu from left click";
        }

        break;
    case QSystemTrayIcon::DoubleClick:
        //iconComboBox->setCurrentIndex((iconComboBox->currentIndex() + 1)
                                      //% iconComboBox->count());
        //break;
     //   qDebug() << "hola2";
        break;
    case QSystemTrayIcon::MiddleClick:
        //showMessage();
        //break;
       // qDebug() << "hola3";
        break;
//case QSystemTrayIcon::Context:
 //       qDebug() << "hola4";
        //trayIconMenu->
   //     break;
    default:
        ;
    }
}

void HelioxHelper::createActions()
 {
     normalAction = new QAction(QIcon(":/images/restore.png"),tr("&Restore"), this);
     connect(normalAction, SIGNAL(triggered()), this, SLOT(troggleShowMainWindow()));

     quitAction = new QAction(QIcon(":/images/quit.png"), tr("&Quit"), this);
     connect(quitAction, SIGNAL(triggered()), qApp, SLOT(quit()));

     minimizeAction = new QAction(QIcon(":/images/minimize.png"),tr("Mi&nimize"), this);
     connect(minimizeAction, SIGNAL(triggered()), this, SLOT(minimizeWindow()));

     settingsAction = new QAction(QIcon(":/images/settings.png"),tr("&Settings"), this);
     connect(settingsAction, SIGNAL(triggered()), this, SLOT(settingsWindow()));

//     restoreAction = new QAction(tr("&Restore"), this);
//     connect(restoreAction, SIGNAL(triggered()), this, SLOT(showNormal()));


 }

 void HelioxHelper::createTrayIcon()
 {

     trayIconMenu = new QMenu(this);
     if (settings->value("Contextual Menu/showRestore").toBool() == true){
         trayIconMenu->addAction(normalAction);
         trayIconMenu->addSeparator();
     }

     if (settings->value("Contextual Menu/showMinimize").toBool() == true){
         trayIconMenu->addAction(minimizeAction);
         trayIconMenu->addSeparator();
     }

     if (settings->value("Contextual Menu/showExit").toBool() == true){
         trayIconMenu->addAction(quitAction);
     }

     if (settings->value("Contextual Menu/showSettings").toBool() == true){
         trayIconMenu->addAction(settingsAction);
     }


     if (settings->value("Contextual Menu/showExit").toBool() == true){
         trayIconMenu->addAction(quitAction);
     }

     trayIcon = new QSystemTrayIcon(this);
     trayIcon->setContextMenu(trayIconMenu);

     QIcon icon = QIcon(":/images/trayicon.png");
     trayIcon->setIcon(icon);
 }


 /*void HelioxHelper::setGuiLookAndFeel()
 {


     //setWindowFlags(Qt::Tool | Qt::CustomizeWindowHint | Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint);

 }*/


 void HelioxHelper::troggleShowMainWindow()
 {
     if (this->isVisible() == false){
         //blockAllApplicationButtonSignals();
                      this->setVisible(!(this->isVisible()));
     } else {
        // blockAllApplicationButtonSignals();
         // if window is visible (but down other windows)
 //        this->raise();
         //QApplication::setActiveWindow(this);
         //*a->setActiveWindow(*a);
         this->activateWindow();
     }
 }

 void HelioxHelper::minimizeWindow()
 {
    // blockAllApplicationButtonSignals(true);
     //qDebug() << "min";

     this->setVisible(false);

     //blockAllApplicationButtonSignals(false);

 }

 void HelioxHelper::setWidgetSize()
  {
    // extern QSettings settings;
      QRect screenSize;
      screenSize = qDesktopWidget.availableGeometry();


      if (settings->value("General/fullscreen").toBool() == true) {
          if (settings->value("General/completeFullscreen").toBool() == true) {
              screenSize = qDesktopWidget.screenGeometry();
          }

          setGeometry(0,0,screenSize.width(), screenSize.height());
          //qDebug() << screenSize;

      } else {

          QString size;
          QString percentage;
          QString align;
          size = settings->value("Panel/size").toString();
          align = settings->value("Panel/align").toString();
          percentage = settings->value("Panel/percentage").toString();
          //qDebug() << screenSize;

          int xVar; int yVar; int yHeight; int xWidth;
         // QString xVar;
          if (position == 0) {
              //left position
              if (percentage == QString("0") ){
                  yVar = size.toInt();
                  yHeight = screenSize.height();
              } else {
                  int size;
                  size = percentage.replace("%","").toInt();
                  int num;
                  int y = screenSize.height();
                  num = (size * y);
                  num = num/100;
                  //qDebug() << num;
                  //qDebug() << *size)/100;

                  yHeight = num;
                  if (align == "center"){
                      num = (y-num)/2;
                      //qDebug() << num;
                  } else if (align == "top") {
                      num = 0;
                  } else if (align == "bottom") {
                      num = 0+num;
                  }

                  yVar = num;
              }
              xVar = 0;
              xWidth = size.toInt();



          } else if (position == 1) {
              //top position

              if (percentage == QString("0") ){
                  xVar = 0;
                  xWidth = screenSize.width();
              } else {


                  int size;
                  size = percentage.replace("%","").toInt();
                  int num;
                  int x = screenSize.width();
                  num = (size * x);
                  num = num/100;
                  //qDebug() << num;
                  //qDebug() << *size)/100;

                  xWidth = num;
                  if (align == "center"){
                      num = (x-num)/2;
                      //qDebug() << num;
                  } else if (align == "left") {
                      num = 0;
                  } else if (align == "right") {
                      num = 0+num;
                  }

                  xVar = num;


              }
              yVar = 0;
              yHeight = size.toInt();


          } else if (position == 2) {
              //right position
              xVar = screenSize.width()-size.toInt();
            //  yVar = 0;
              xWidth = size.toInt();
            //  yHeight = screenSize.height();

              if (percentage == QString("0") ){
                  yVar = size.toInt();
                  yHeight = screenSize.height();
              } else {
                  int size;
                  size = percentage.replace("%","").toInt();
                  int num;
                  int y = screenSize.height();
                  num = (size * y);
                  num = num/100;
                  yHeight = num;
                  if (align == "center"){
                      num = (y-num)/2;
                  } else if (align == "top") {
                      num = 0;
                  } else if (align == "bottom") {
                      num = 0+num;
                  }

                  yVar = num;
              }

          } else if (position == 3) {
              //bottom position

              if (percentage == QString("0") ){
                  xVar = 0;
                  xWidth = screenSize.width();
              } else {


                  int size;
                  size = percentage.replace("%","").toInt();
                  int num;
                  int x = screenSize.width();
                  num = (size * x);
                  num = num/100;
                  xWidth = num;
                  if (align == "center"){
                      num = (x-num)/2;
                  } else if (align == "left") {
                      num = 0;
                  } else if (align == "right") {
                      num = 0+num;
                  }

                  xVar = num;


              }
              yHeight = size.toInt();
              yVar = screenSize.height()-size.toInt();


          }
          setGeometry(xVar , yVar , xWidth ,yHeight);

         // qDebug() << position->toLatin1();
         // qDebug() << xVar.toInt();
          /*
          qDebug() << "sreen width" << screenSize.width();
          qDebug() << "x width position substracted size" << screenSize.width()-settings->value("Panel/size").toInt();
          qDebug() << "settings size variable" <<  settings->value("Panel/size").toInt();
          qDebug() << "screen height" << screenSize.height();
          */
      }

  }

 void HelioxHelper::setStyleClass()
 {
     //ui->pushButton->setStyleSheet("QToolButton {background-color: transparent;}");
    // this->setAttribute(Qt::WA_TranslucentBackground, true);
     if (settings->value("General/fullscreen").toBool() == false) {
         setMask(roundedRect(this->rect(), settings->value("Round Corners/roundedMargin").toInt()));
     }



     //QRegion* region = new QRegion(*(new QRect(this->x()+5,this->y()+5,190,190)),QRegion::Ellipse);
     //setMask(*region);

     if (settings->value("Background/wallpaperBackground").toBool() == true){
         if (settings->value("Background/backgroundPath").toString() != ""){

           //Backround Image path
            QString imgPath = settings->value("Background/backgroundPath").toString();
//            qDebug() << imgPath;
//            setStyleSheet(QString("QWidget#HelioxHelper {background-image: url(%1);}").arg(imgPath));
             QPalette palette;
             palette.setBrush(this->backgroundRole(), QBrush(QImage(imgPath)));
             this->setPalette(palette);
         }
     } else if (settings->value("Background/gradientBackground").toBool() == true) {

         QString beginColor = settings->value("Background/gradientBeginColor").toString();
         QString endColor = settings->value("Background/gradientEndColor").toString();
         if (settings->value("Background/gradientOrientation").toInt() == 1) {
            //Horitzontal Gradient Orientation
             ui->scrollAreaWidgetContents->setStyleSheet(QString("QWidget {background-color: qlineargradient(x1: 0, y1: 1, x2: 1, y2: 1, stop: 0 %1, stop: 1 %2);}").arg(beginColor).arg(endColor));
         } else {
            //Vertical Graident Orientation
             ui->scrollAreaWidgetContents->setStyleSheet(QString("QWidget {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 %1, stop: 1 %2);}").arg(beginColor).arg(endColor));
         }

     } else {
       //Plain color, using first color of gradient
         QString beginColor = settings->value("Background/gradientbeginColor").toString();
         ui->scrollAreaWidgetContents->setStyleSheet(QString("QWidget {background-color: %1;}").arg(beginColor));
     }


     languageMenu->setStyleSheet("QMenu { border-radius: 10px; border: 1px solid rgb(110, 110, 110); font: bold 14px; }  QMenu::item {font-weight: bold; }");

     int iconswidth = 16+4+16;

     languageMenu->setStyle( new WideIconsMenu( iconswidth ) );

     trayIconMenu->setStyleSheet("QWidget {border: 10px; border-radius 10px;}");

     trayIconMenu->setStyleSheet("QWidget {border: 10px; border-radius 10px;}");

     /*QPainter painter(this);
     qDebug() << rect();
             painter.setRenderHint(QPainter::Antialiasing); // we need this in order to get correct rounded corners
             painter.setPen(QPen(QBrush(Qt::black), 2.0));
             painter.setBrush(QBrush(QColor(Qt::yellow)));
             painter.drawRoundedRect(rect().adjusted(2,1,-2,-1), 5, 5);

             QPainterPath path;
                     path.addRoundedRect(rect().adjusted(1, -1, -1, 0), 25, 25);
                     //return QRegion(path.toFillPolygon().toPolygon());
                     QBitmap Bitmap(size());
                             Bitmap.clear();
                             QPainter Painter(&Bitmap);

                             Painter.setClipRegion(QRegion(path.toFillPolygon().toPolygon()));
                             Painter.fillRect(rect(), Qt::color1);
                             Painter.end();

                             setMask(Bitmap);*/
 }


 QRegion HelioxHelper::roundedRect(const QRect& rect, int r)
{

     QRegion::RegionType topLeft;
     QRegion::RegionType topRight;
     QRegion::RegionType bottomLeft;
     QRegion::RegionType bottomRight;
     topLeft = topRight = bottomLeft = bottomRight = QRegion::Rectangle;

     if (settings->value("Round Corners/autoBorders").toBool() == true) {

         if (position == 0) {
           //left position
             topLeft = QRegion::Rectangle;
             topRight = QRegion::Ellipse;
             bottomLeft = QRegion::Rectangle;
             bottomRight = QRegion::Ellipse;

         } else if (position == 1) {
           //top position
             topLeft = QRegion::Rectangle;
             topRight = QRegion::Rectangle;
             bottomLeft = QRegion::Ellipse;
             bottomRight = QRegion::Ellipse;

         } else if (position == 2) {
           //right position
             topLeft = QRegion::Ellipse;
             topRight = QRegion::Rectangle;
             bottomLeft = QRegion::Ellipse;
             bottomRight = QRegion::Rectangle;

         } else if (position == 3) {
           //bottom position
             topLeft = QRegion::Ellipse;
             topRight = QRegion::Ellipse;
             bottomLeft = QRegion::Rectangle;
             bottomRight = QRegion::Rectangle;
         }
     } else {
         if (settings->value("Round Corners/top-left").toBool() == true){
             topLeft = QRegion::Ellipse;
         } else {
             topLeft = QRegion::Rectangle;
         }
         if (settings->value("Round Corners/top-right").toBool() == true){
             topRight = QRegion::Ellipse;
         } else {
             topRight = QRegion::Rectangle;
         }
         if (settings->value("Round Corners/bottom-left").toBool() == true){
             bottomLeft = QRegion::Ellipse;
         } else {
             bottomLeft = QRegion::Rectangle;
         }
         if (settings->value("Round Corners/bottom-right").toBool() == true){
             bottomRight = QRegion::Ellipse;
         } else {
             bottomRight= QRegion::Rectangle;
         }
     }

     QRegion region;
     // middle and borders
     region += rect.adjusted(r, 0, -r, 0);
     region += rect.adjusted(0, r, 0, -r);

     // top left
     QRect corner(rect.topLeft(), QSize(r*2, r*2));
     region += QRegion(corner, topLeft);

     // top right
     corner.moveTopRight(rect.topRight());
     region += QRegion(corner, topRight);

     // bottom left
     corner.moveBottomLeft(rect.bottomLeft());
     region += QRegion(corner, bottomLeft );

     // bottom right
     corner.moveBottomRight(rect.bottomRight());
     region += QRegion(corner, bottomRight );

     return region;
 }



 void HelioxHelper::createApplicationButtons()
 {

//     extern QList< QToolButtonWithEvents* > listApplicationButtons;

     //extern QList< QLabel* > listApplicationImage;
     int imageSize = settings->value("App Buttons/imageSize").toInt();
     int buttonMinHeight = settings->value("App Buttons/minimumHeight").toInt();
     int buttonMaxHeight = settings->value("App Buttons/maximumHeight").toInt();
     bool iconAbove = settings->value("App Buttons/iconAbove").toBool();
     int buttonMinWidth = settings->value("App Buttons/minimumWidth").toInt();
     int buttonMaxWidth = settings->value("App Buttons/maximumWidth").toInt();
     bool showLabel =  settings->value("App Buttons/showLabels").toBool();

     //QList<Applications> apps;
     int size = settings->beginReadArray("Applications/app");

     //qDebug() << size;
     for (int i = 0; i < size; ++i) {
        settings->setArrayIndex(i);
        QString name = settings->value("name").toString();

        if ((name == "newRow") || (name == "newCol") || (name == "newLine")) {

            if ((position == 0) || (position == 2)) {
                //Vertical orientation
                numCol=numCol+1;
                numRow=0;
                //qDebug() << "vertical";
             } else {
                //Horizontal Orientation
                numRow=numRow+1;
                numCol=0;
                //qDebug() << "horitzontal";

            }
            listApplicationButtons << new QToolButtonWithEvents(this, settings1, settings2, selectedLanguage);
            listApplicationButtons[i]->setVisible(0);

        } else {

            QString name = settings->value("name").toString();
            QString icon = settings->value("icon").toString();
            QString desc = settings->value("desc").toString();
            QString exec = settings->value("exec").toString();

            listApplicationButtons << new QToolButtonWithEvents(this, settings1, settings2, selectedLanguage);
            listApplicationButtons[i]->setObjectName(QString("b_%1").arg(name));
            listApplicationButtons[i]->setText(name);

            listApplicationButtons[0]->setBlockedSignals(1);


            //listApplicationButtons[numButtons]->setMinimumSize(QSize(170, 40));
            // good characters lost on .config
            QByteArray byteArray = desc.toLatin1();
            const char * processingString = byteArray.data();
            QString realdesc = QString::fromLocal8Bit(processingString);

            listApplicationButtons[i]->setToolTip(realdesc);
            listApplicationButtons[i]->setAccessibleName(name);
            listApplicationButtons[i]->setAccessibleDescription(desc);
            //listApplicationButtons[i]->setMinimumHeight(buttonMinHeight);
            listApplicationButtons[i]->setIconSize(QSize(imageSize, imageSize));
            listApplicationButtons[i]->setIcon(QPixmap(QString("%1").arg(icon)));

            ui->gridLayout->addWidget(listApplicationButtons[i], numRow, numCol, 1, 1);

            if (buttonMaxHeight == 0){
                buttonMaxHeight=listApplicationButtons[i]->maximumHeight();
            }

            if (buttonMaxWidth == 0){
               buttonMaxWidth=listApplicationButtons[i]->maximumWidth();
            }

            if (buttonMinHeight == 0){
                buttonMinHeight=listApplicationButtons[i]->minimumHeight();
            }

            if (buttonMinWidth == 0){
               buttonMinWidth=listApplicationButtons[i]->minimumWidth();
            }

            listApplicationButtons[i]->setMinimumSize(QSize(buttonMinWidth,buttonMinHeight));
            listApplicationButtons[i]->setMaximumSize(QSize(buttonMaxWidth,buttonMaxHeight));

          //  qDebug() << "min Size " << QSize(buttonMinWidth,buttonMinHeight);
          //  qDebug() << "max Size " << QSize(buttonMaxWidth,buttonMaxHeight);
            if (iconAbove == true){
                //listApplicationButtons[i]->setStyleSheet(QString("background: url(%1) top center no-repeat; padding-top: %2px; padding-bottom: 4px;").arg(icon).arg(imageSize+(imageSize/5)*3));
                  listApplicationButtons[i]->setToolButtonStyle(Qt::ToolButtonTextUnderIcon);

            } else {
                listApplicationButtons[i]->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
            }

            if (showLabel == false){
                listApplicationButtons[i]->setToolButtonStyle(Qt::ToolButtonIconOnly);
            }

            //Don't show buttons that don't do nothing
            if (exec == ""){
                listApplicationButtons[i]->setVisible(false);
            }

            //Put property on button wich will be written on configuration file
            listApplicationButtons[i]->setTextProperty(new QString("EXEC"), new QString(exec)); //set text button property to write on file

           // connect(listApplicationButtons[i], SIGNAL(clicked()), this, SLOT(showAppBox()));
            connect(listApplicationButtons[i], SIGNAL( buttonClicked(QString, QString)), this, SLOT(startApplication(QString, QString)));


            if ((position == 0) || (position == 2) ) {
                //Vertical orientation
            //    qDebug() << "vertical";
                numRow=numRow+1;

             } else {
                //Horizontal Orientation
                numCol=numCol+1;

            //    qDebug() << "horitzontal";

            }

        }

     }
     settings->endArray();

     if (settings->value("General/languages").toBool() == true){
          if ((numlanguage != 0) && (numlanguage != 1)){
              numRow=numCol=0;
         languageButtonSelection = new QToolButtonWithEvents(this, settings1, settings2, selectedLanguage);
         languageButtonSelection->setIcon(QIcon(":/images/language.png"));
         languageButtonSelection->setMaximumSize(QSize(22,22));

         helioxButtonSelection = new QToolButtonWithEvents(this, settings1, settings2, selectedLanguage);
         helioxButtonSelection->setIcon(QIcon(":/images/trayicon.png"));
         helioxButtonSelection->setMaximumSize(QSize(22,22));
        // separatorButtons = new QFrame();
         //separatorButtons->setFrameShadow(QFrame::Sunken);

         QString desc;
         desc ="Configura el idioma";
         QByteArray byteArray = desc.toLatin1();
         const char * processingString = byteArray.data();
         QString realdesc = QString::fromLocal8Bit(processingString);


         languageButtonSelection->setToolTip(realdesc);
         ui->gridLayoutMainButtons->addWidget(languageButtonSelection, numRow, numCol, 1, 1);

         if (!((position == 0) || (position == 2) )) {
             //Vertical orientation
         //    qDebug() << "vertical";
             numRow=numRow+1;

          } else {
             //Horizontal Orientation
             numCol=numCol+1;
         //    qDebug() << "horitzontal";
         }

         ui->gridLayoutMainButtons->addWidget(helioxButtonSelection, numRow, numCol, 1, 1);
         ui->line->setVisible(1);


            connect(languageButtonSelection, SIGNAL(buttonClicked(QString,QString)), this, SLOT(showLanguageMenu()));
         }


     }

 }

 void HelioxHelper::startApplication(QString string, QString prop)
 {
     //qDebug() << "Starting" << prop;

     //extern QList <QProcess* > startedApps;

  //   qDebug() << prop.split(" ")[1];
     if (string == "EXEC")
     {
         startedApps << new QProcess();
         startedApps[startedApps.size()-1]->start(prop);
     }

//     myProcess->start(prop);

 }

 void HelioxHelper::activateWindowSignal(QString string)
 {
     qDebug() << "Activating" << string;
    // this->setVisible(true);
   // /  this->activateWindow();
   //  this->setFocus();
    // this->grabKeyboard();
    // this->grabMouse();
   // this->raise();
     //this->set
     troggleShowMainWindow();
 }


 void HelioxHelper::defineLanguageDictionary()
 {
     //extern QHash<QString, QString> dict;
     dict["ca"] = "Català";     dict["ca_ES"] = "Català";
     dict["es"] = "Castellano";     dict["es_ES"] = "Castellano";

     dict["en"] = "English"; dict["en_GB"] = "English"; dict["en_US"] = "English"; dict["en_IE"] = "English";
     dict["fr"] = "French"; dict["fr_FR"] = "French";
     dict["it"] = "Italiano"; dict["it_IT"] = "Italiano";
     dict["de"] = "Deuche"; dict["de_DE"] = "Deuche";
     dict["pt"] = "Português"; dict["pt_PT"] = "Português"; dict["pt_BR"] = "Português";
     dict["gl"] = "Galego"; dict["gl_ES"] = "Galego";

     //Derivados en Mexico
     dict["mx"] = "Mexicano"; dict["es_MX"] = "Mexicano";
     dict["myn"] = "Maya"; dict["myn_MX"] = "Maya";
     dict["nah"] = "Nahuatl"; dict["nah_MX"] = "Nahuatl";
     dict["pua"] = "P'urhépecha"; dict["pua_MX"] = "P'urhépecha";
 }


 QString HelioxHelper::execShellProcess(QString idCommand, QString idParam = "", QString idParam2 = ""){
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



 void HelioxHelper::createLanguageButtons()
 {

 if (settings->value("General/LANGLIST").toString() == ""){
     //find witch languages are on system
     QString *langs = new QString(execShellProcess(QString("/bin/sh"), QString("-c"), QString("grep -v \\# /etc/locale.gen | awk ' { print $1 } ' | sed s.@euro..g | sed s_.UTF-8__g | sort -u")));

     foreach (QString lang, langs->split("\n")){
         //qDebug() << lang;
         this->createLanguageButton(new QString(lang));
     }

     //qDebug() << settings->value("General/LANGLIST").toString();
   } else {
      //qDebug() << QString(settings->value("General/LANGLIST").toString()).split(" ");
     //create languages of langlist
     foreach (QString lang, settings->value("General/LANGLIST").toString().split(" ")){
         //qDebug() << lang;
         this->createLanguageButton(new QString(lang));
     }
   }
 }

 void HelioxHelper::createLanguageButton(QString *lang){


     QFile *filebg = new QFile(QString("%1/.config/ProyectoHeliox/HelioxHelper_%2.conf").arg(QDir::homePath()).arg(*lang));
     if  (filebg->exists()) {

         //Add new button with objectname and minimum size
         QString realLanguageName = dict.value(*lang);

         //hack to recover good accents and punctuation - losed on qhash "dict"
         QByteArray byteArray = realLanguageName.toLatin1();
         const char * processingString = byteArray.data();
         QString realLanguageNameTrans = QString::fromLocal8Bit(processingString);

         //create menu entry
         listLangActions << new QActionWithEvents(this);
         //extern QList< QActionWithEvents* > listLangActions;
         QFile *filebg = new QFile(QString(":/images/lang/%1.png").arg(*lang) );
         if  (filebg->exists()) {
             listLangActions[numlanguage]->setIcon(QIcon(QString(":/images/lang/%1.png").arg(*lang)));
             listLangActions[numlanguage]->setText(realLanguageNameTrans);
     //        listLangActions << new QActionWithEvents(QIcon(QPixmap(QString(":/images/lang/%1.png").arg(*lang))),realLanguageNameTrans, this);
         } else {
             listLangActions[numlanguage]->setIcon(QIcon(QString(":/images/lang/%1.png").arg(*lang).split("_")[0]));
             listLangActions[numlanguage]->setText(realLanguageNameTrans);
             //listLangActions << new QActionWithEvents(QIcon(QPixmap(QString(":/images/lang/%1.png").arg(QString(*lang).split("_")[0]))),realLanguageNameTrans, this);
         }

         languageMenu->addAction(listLangActions[numlanguage]);
         listLangActions[numlanguage]->setTextProperty(new QString("LANG"), new QString(*lang)); //set text button property to write on file
         connect(listLangActions[numlanguage], SIGNAL( actionClicked(QString, QString)), this, SLOT(changeLanguage(QString, QString)));

         numlanguage=numlanguage+1;
         //qDebug() << numlanguage;

     }
 }



 void HelioxHelper::changeLanguage(QString prop, QString value){
     if (prop == "LANG"){
        delete (settings);
        selectedLanguage=value;
        settings1="ProyectoHeliox";
        settings2=QString("HelioxHelper_%1").arg(selectedLanguage);


        settings = new QSettings("ProyectoHeliox", QString("HelioxHelper_%1").arg(value));
        ////settings->setPath();
        //qDebug() << settings->applicationName();
        //settings->sync();

         //listApplicationButtons << new QToolButtonWithEvents(this);

         //createApplicationButtons();
        reloadConfiguration();
     }
 }


 void HelioxHelper::showLanguageMenu(){
     languageMenu->exec(QCursor::pos());
 }


 void HelioxHelper::blockAllApplicationButtonSignals(bool value){

     while (listApplicationButtons.size() != 0){
         for (int i = 0; i < listApplicationButtons.size(); ++i)  {
             qDebug() << "desac" << listApplicationButtons[i]->text();
             listApplicationButtons[i]->setSimpleBlockedSignals(value);
         }
     }

  //   QListIterator<QToolButtonWithEvents*> i(listApplicationButtons);
  //   while (i.hasNext()){
         //i.next();

         //qDebug() << i.next();
  //       qDebug() << listApplicationButtons[i]->text();

  //   }

 }


 void HelioxHelper::settingsWindow(){
     //ettingsProcess=QProcess();
   //  connect(settingsProcess,SIGNAL(finished()), this, SLOT(reloadConfiguration()));

    settingsProcess.start("rahisi-config");
    settingsProcess.waitForFinished();
    reloadConfiguration();

 }


 void HelioxHelper::reloadConfiguration(){
    //qDebug() << "Hola";
     //qDebug() << listApplicationButtons.size();
    while (listApplicationButtons.size() != 0){
        for (int i = 0; i < listApplicationButtons.size(); ++i)  {
            delete(listApplicationButtons[i]);
            listApplicationButtons.removeAt(i);
        }

    }

    delete(languageButtonSelection);
    delete(helioxButtonSelection);
    ui->line->setVisible(0);

    //languageButtonSelection->setVisible(false);
    numRow=0;
    numCol=0;
    numApp=0;

    createApplicationButtons();
    //setGuiLookAndFeel();

    setWidgetSize();
    setStyleClass();
 }

 //void HelioxHelper::showAppBox(){
 //    qDebug() << "Hola";
 //}

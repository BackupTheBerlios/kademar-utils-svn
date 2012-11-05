#include "helioxhelper.h"
#include "ui_helioxhelper.h"
#include <QToolButton>

bool speech;
//extern QSettings settings;

QSettings settings("ProyectoHeliox", "HelioxHelper");

QList< QToolButtonWithEvents* > listApplicationButtons;
//QList< QLabel* > listApplicationImage;

QList <QProcess* > startedApps;

HelioxHelper::HelioxHelper(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::HelioxHelper)
{

    QSettings settings("ProyectoHeliox", "HelioxHelper");

    //loadConfig();
    numCol=0;
    numRow=0;

    position = settings.value("General/whereIsPlacedWindow").toInt();


    ui->setupUi(this);
  //  loadConfig();

    extern bool speech;
    speech=0;

    if (settings.value("General/speechText").toString() == ""){

        QFile *cmdline = new QFile("/proc/cmdline");
        cmdline->open(QIODevice::ReadOnly);
        QString *cmdlineContent = new QString(cmdline->readAll());
        if ( (cmdlineContent->contains("scrread")) || (cmdlineContent->contains("screenread")) )
        {
            speech=1;

        }
        //qDebug() << "speech activated by speech-dispatcher detection. Result:" << speech;
    } else {
        speech=bool(settings.value("General/speechText").toBool());
        //qDebug() << "speech activated by config file. Result:" << speech;
    }

    createActions();
    createTrayIcon();

    createConnections();

    createApplicationButtons();


    setWindowIcon(QIcon(":/images/trayicon.png"));

    setGuiLookAndFeel();

    if (settings.value("Tray Icon/showTrayIcon").toBool() == true ){
        trayIcon->show();
    }

    setFocus();
    raise();

    //QApplication::processEvents();
    //QCoreApplication::processEvents(QEventLoop::AllEvents, 100);
    //qDebug() << "cambio hecho";
    //listApplicationButtons[0]->setBlockedSignals(false);



}

HelioxHelper::~HelioxHelper()
{
    delete ui;
}

void HelioxHelper::createConnections()
{
    connect(trayIcon, SIGNAL(activated(QSystemTrayIcon::ActivationReason)),
                 this, SLOT(iconActivated(QSystemTrayIcon::ActivationReason)));

}

void HelioxHelper::iconActivated(QSystemTrayIcon::ActivationReason reason)
{
    switch (reason) {
    case QSystemTrayIcon::Trigger:
        //qDebug() << "hola";

        if (settings.value("Tray Icon/leftClickContextualMenu").toBool() == false) {
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

//     settingsAction = new QAction(QIcon(":/images/settings.png"),tr("&Settings"), this);
//     connect(settingsAction, SIGNAL(triggered()), this, SLOT(settingsWindow()));

//     restoreAction = new QAction(tr("&Restore"), this);
//     connect(restoreAction, SIGNAL(triggered()), this, SLOT(showNormal()));


 }

 void HelioxHelper::createTrayIcon()
 {

     trayIconMenu = new QMenu(this);
     if (settings.value("Contextual Menu/showRestore").toBool() == true){
         trayIconMenu->addAction(normalAction);
         trayIconMenu->addSeparator();
     }

     if (settings.value("Contextual Menu/showMinimize").toBool() == true){
         trayIconMenu->addAction(minimizeAction);
         trayIconMenu->addSeparator();
     }

     if (settings.value("Contextual Menu/showExit").toBool() == true){
         trayIconMenu->addAction(quitAction);
     }

//     if (settings.value("Contextual Menu/showSettings").toBool() == true){
//         trayIconMenu->addAction(quitSettings);
//     }


     if (settings.value("Contextual Menu/showExit").toBool() == true){
         trayIconMenu->addAction(quitAction);
     }

     trayIcon = new QSystemTrayIcon(this);
     trayIcon->setContextMenu(trayIconMenu);

     QIcon icon = QIcon(":/images/trayicon.png");
     trayIcon->setIcon(icon);
 }


 void HelioxHelper::setGuiLookAndFeel()
 {
     setWidgetSize();

     setStyleClass();

     //setWindowFlags(Qt::Tool | Qt::CustomizeWindowHint | Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint);

 }


 void HelioxHelper::troggleShowMainWindow()
 {
     if (this->isVisible() == false){
                      this->setVisible(!(this->isVisible()));
     } else {
         // if window is visible (but down other windows)
 //        this->raise();
         //QApplication::setActiveWindow(this);
         //*a->setActiveWindow(*a);
         this->activateWindow();
     }
 }

 void HelioxHelper::minimizeWindow()
 {
     this->setVisible(false);
 }

 void HelioxHelper::setWidgetSize()
  {
    // extern QSettings settings;
      QDesktopWidget qDesktopWidget;
      QRect screenSize;
      screenSize = qDesktopWidget.availableGeometry();


      if (settings.value("General/fullscreen").toBool() == true) {
          if (settings.value("General/completeFullscreen").toBool() == true) {
              screenSize = qDesktopWidget.screenGeometry();
          }

          setGeometry(0,0,screenSize.width(), screenSize.height());
          //qDebug() << screenSize;

      } else {

          QString widthSize;
          QString heightSize;
          widthSize = settings.value("Panel/widthSize").toString();
          heightSize = settings.value("Panel/heigthSize").toString();
         // qDebug() << size.toInt();

          int xVar; int yVar; int yHeight; int xWidth;
         // QString xVar;
          if (position == 0) {
              //left position
              xVar = 0;
              yVar = widthSize.toInt();
              xWidth = widthSize.toInt();
              yHeight = screenSize.height();


          } else if (position == 1) {
              //top position
              xVar = 0;
              yVar = 0;
              xWidth = screenSize.width();
              yHeight = widthSize.toInt();

          } else if (position == 2) {
              //right position
              xVar = screenSize.width()-widthSize.toInt();
              yVar = 0;
              xWidth = widthSize.toInt();
              yHeight = screenSize.height();


          } else if (position == 3) {
              //bottom position
              xVar = 0;
              yVar = screenSize.height()-widthSize.toInt();
              xWidth = screenSize.width();
              yHeight = widthSize.toInt();
          }
          setGeometry(xVar , yVar , xWidth ,yHeight);

         // qDebug() << position->toAscii();
         // qDebug() << xVar.toInt();
          /*
          qDebug() << "sreen width" << screenSize.width();
          qDebug() << "x width position substracted size" << screenSize.width()-settings.value("Panel/widthSize").toInt();
          qDebug() << "settings size variable" <<  settings.value("Panel/widthSize").toInt();
          qDebug() << "screen height" << screenSize.height();
          */
      }

  }

 void HelioxHelper::setStyleClass()
 {
     //ui->pushButton->setStyleSheet("QToolButton {background-color: transparent;}");
    // this->setAttribute(Qt::WA_TranslucentBackground, true);
     if (settings.value("General/fullscreen").toBool() == false) {
         setMask(roundedRect(this->rect(), settings.value("Round Corners/roundedMargin").toInt()));
     }



     //QRegion* region = new QRegion(*(new QRect(this->x()+5,this->y()+5,190,190)),QRegion::Ellipse);
     //setMask(*region);

     if (settings.value("Background/wallpaperBackground").toBool() == true){
         if (settings.value("Background/backgroundPath").toString() != ""){

           //Backround Image path
            QString imgPath = settings.value("Background/backgroundPath").toString();
//            qDebug() << imgPath;
//            setStyleSheet(QString("QWidget#HelioxHelper {background-image: url(%1);}").arg(imgPath));
             QPalette palette;
             palette.setBrush(this->backgroundRole(), QBrush(QImage(imgPath)));
             this->setPalette(palette);
         }
     } else if (settings.value("Background/gradientBackground").toBool() == true) {

         QString beginColor = settings.value("Background/gradientBeginColor").toString();
         QString endColor = settings.value("Background/gradientEndColor").toString();
         if (settings.value("Background/gradientOrientation").toInt() == 1) {
            //Horitzontal Gradient Orientation
             setStyleSheet(QString("QWidget#HelioxHelper {background-color: qlineargradient(x1: 0, y1: 1, x2: 1, y2: 1, stop: 0 %1, stop: 1 %2);}").arg(beginColor).arg(endColor));
         } else {
            //Vertical Graident Orientation
             setStyleSheet(QString("QWidget#HelioxHelper {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 %1, stop: 1 %2);}").arg(beginColor).arg(endColor));
         }

     } else {
       //Plain color, using first color of gradient
         QString beginColor = settings.value("Background/gradientbeginColor").toString();
         setStyleSheet(QString("QWidget#HelioxHelper {background-color: %1;}").arg(beginColor));
     }




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

     if (settings.value("Round Corners/autoBorders").toBool() == true) {

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
         if (settings.value("Round Corners/top-left").toBool() == true){
             topLeft = QRegion::Ellipse;
         } else {
             topLeft = QRegion::Rectangle;
         }
         if (settings.value("Round Corners/top-right").toBool() == true){
             topRight = QRegion::Ellipse;
         } else {
             topRight = QRegion::Rectangle;
         }
         if (settings.value("Round Corners/bottom-left").toBool() == true){
             bottomLeft = QRegion::Ellipse;
         } else {
             bottomLeft = QRegion::Rectangle;
         }
         if (settings.value("Round Corners/bottom-right").toBool() == true){
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

     extern QList< QToolButtonWithEvents* > listApplicationButtons;

     //extern QList< QLabel* > listApplicationImage;
     int imageSize = settings.value("App Buttons/imageSize").toInt();
     int buttonMinHeight = settings.value("App Buttons/minimumHeight").toInt();
     int buttonMaxHeight = settings.value("App Buttons/maximumHeight").toInt();
     bool iconAbove = settings.value("App Buttons/iconAbove").toBool();
     int buttonMinWidth = settings.value("App Buttons/minimumWidth").toInt();
     int buttonMaxWidth = settings.value("App Buttons/maximumWidth").toInt();
     bool showLabel =  settings.value("App Buttons/showLabels").toBool();

     //QList<Applications> apps;
     int size = settings.beginReadArray("Applications/app");

     //qDebug() << size;
     for (int i = 0; i < size; ++i) {
        settings.setArrayIndex(i);
        QString name = settings.value("name").toString();

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
            listApplicationButtons << new QToolButtonWithEvents(this);
            listApplicationButtons[i]->setVisible(0);

        } else {

            QString name = settings.value("name").toString();
            QString icon = settings.value("icon").toString();
            QString desc = settings.value("desc").toString();
            QString exec = settings.value("exec").toString();

            listApplicationButtons << new QToolButtonWithEvents(this);
            listApplicationButtons[i]->setObjectName(QString("b_%1").arg(name));
            listApplicationButtons[i]->setText(name);

            listApplicationButtons[0]->setBlockedSignals(1);


            //listApplicationButtons[numButtons]->setMinimumSize(QSize(170, 40));
            listApplicationButtons[i]->setToolTip(desc);
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
     settings.endArray();

 }

 void HelioxHelper::startApplication(QString string, QString prop)
 {
     //qDebug() << "Starting" << prop;

     extern QList <QProcess* > startedApps;

  //   qDebug() << prop.split(" ")[1];
     startedApps << new QProcess();
     startedApps[startedApps.size()-1]->start(prop);

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

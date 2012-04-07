#include "desktopselector.h"
#include "ui_desktopselector.h"
#include "QDesktopWidget"
#include "QPixmap"
#include "QMessageBox"
#include "QString"
#include "QTextStream"
#include "QFile"
#include "QProcess"
#include "QDebug"

bool speech;
DesktopSelector::DesktopSelector(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::DesktopSelector)
{

this->close();
    ui->setupUi(this);
    this->setConnects();
    this->setMaxResolution();
    this->removeDesktops();
    //Use detect-monitor to configure it
    QProcess *dresol = new QProcess();
    dresol->start(QString("/usr/share/kademar/scripts/engegada/detect-monitor"));
    QString label = tr("Select the desktop you want to use");

    //Detect if want speech-dispatcher use
    extern bool speech;
    speech=0;
    QFile *cmdline = new QFile("/proc/cmdline");
    cmdline->open(QIODevice::ReadOnly);
    QString *cmdlineContent = new QString(cmdline->readAll());
    if ( (cmdlineContent->contains("scrread")) || (cmdlineContent->contains("screenread")) )
    {
        speech=1;
    }

    //qDebug() << "after: " << speech;

    if ( speech == 1 ){
        //configure Volumes (usefull to screenreader)
        QProcess *volumes = new QProcess();
        volumes->start(QString("/usr/share/kademar/scripts/engegada/volums"));
        volumes->waitForFinished();

        QProcess *readcommand = new QProcess();
        readcommand->start(QString("spd-say \"%1\"").arg(label));
    }
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
        break;
    default:
        break;
    }
}

void DesktopSelector::setConnects()
{
    //connect(ui->generalAction, SIGNAL(triggered()), this, SLOT(changeView()));
    connect(ui->b_kde3, SIGNAL(clicked()), this, SLOT(startDesktopKde3()));
    connect(ui->b_kde4, SIGNAL(clicked()), this, SLOT(startDesktopKde4()));
    connect(ui->b_lxde, SIGNAL(clicked()), this, SLOT(startDesktopLxde()));
    connect(ui->b_gnome, SIGNAL(clicked()), this, SLOT(startDesktopGnome()));
    connect(ui->b_icewm, SIGNAL(clicked()), this, SLOT(startDesktopIcewm()));
    connect(ui->b_shutdown, SIGNAL(clicked()), this, SLOT(askForShutdown()));
}


void DesktopSelector::askForShutdown()
{
    QString label = tr("Are you sure to shutdown the computer?");
    extern bool speech;
    if ( speech == 1 ){
        QProcess *readcommand = new QProcess();
        readcommand->start(QString("spd-say \"%1\"").arg(label));
    }
    QMessageBox *dial = new QMessageBox();
    dial->setWindowTitle(tr("Shutdown Computer"));
    dial->setText(label);
    dial->setStandardButtons(QMessageBox::No | QMessageBox::Yes);
    dial->setDefaultButton(QMessageBox::No );
    if (dial->exec() == QMessageBox::Yes) {
        QFile *file = new QFile("/var/tmp/xsession-commands");
        //QTextStream *stream = new QTextStream();
        if ( file->open( QIODevice::WriteOnly ) )
        {
            QTextStream stream( file );
            stream << "shutdown halt force\n";
        }
        file->close();

        QFile *file2 = new QFile("/var/tmp/xserver");
        //QTextStream *stream2 = new QTextStream();
        if ( file2->open( QIODevice::Append ) )
        {
            QTextStream stream2( file2 );
            stream2 << "DESKTOP=none\n";
        }
        file2->close();

        this->close();
    }
}

void DesktopSelector::setMaxResolution()
{
    QDesktopWidget qDesktopWidget;
    QRect screenSize = qDesktopWidget.screenGeometry();
    //qDebug() << screenSize.width();
    DesktopSelector::setGeometry(0,0,screenSize.width(),screenSize.height());
    ui->background->setGeometry(0,0,screenSize.width(),screenSize.height());
    QFile *filebg = new QFile(QString("/usr/share/wallpapers/Gota de Gebrada/contents/images/%1x%2.png").arg(screenSize.width()).arg(screenSize.height()) );
    if  (!(filebg->exists())) {

        filebg->setFileName(QString("/usr/share/wallpapers/Gota de Gebrada/contents/images/1280x1024.png"));
    }

    if  (!(filebg->exists())) {

        filebg->setFileName(QString("/usr/share/wallpapers/kademar.png"));
    }

    ui->background->setPixmap(QPixmap(filebg->fileName()));

    //qDebug() << filebg->fileName();
}

void DesktopSelector::removeDesktops()
{
    QFile *desktop = new QFile();
    //KDE3
    desktop->setFileName(QString("/opt/trinity/bin/startkde"));
    if  (!(desktop->exists())) {
            ui->b_kde3->setVisible(0);
            ui->l_kde3->setVisible(0);
    }
    //KDE4
    desktop->setFileName(QString("/usr/bin/startkde"));
    if  (!(desktop->exists())) {
            ui->b_kde4->setVisible(0);
            ui->l_kde4->setVisible(0);
    }
    //GNOME
    desktop->setFileName(QString("/usr/bin/startgnome"));
    if  (!(desktop->exists())) {
            ui->b_gnome->setVisible(0);
            ui->l_gnome->setVisible(0);
    }
    //LXDE
    desktop->setFileName(QString("/usr/bin/startlxde"));
    if  (!(desktop->exists())) {
            ui->b_lxde->setVisible(0);
            ui->l_lxde->setVisible(0);
    }
    //ICEWM
    desktop->setFileName(QString("/usr/bin/starticewm"));
    if  (!(desktop->exists())) {
            ui->b_icewm->setVisible(0);
            ui->l_icewm->setVisible(0);
    }
}


void DesktopSelector::writeSettings(QString *desk){
    //QString *varDesktop = new QString("DESKTOP=" + *desk + "\n");
    QFile *file = new QFile("/var/tmp/xserver");
    //QTextStream *stream = new QTextStream();
    if ( file->open( QIODevice::Append ) )
    {
        QTextStream stream( file );
        stream <<QString("DESKTOP=" + *desk + "\n");
        //stream << QString("DESKTOP=%1\n").arg(*desk);
    }
    file->close();
    this->close();
}


// Desktop Starter
void DesktopSelector::startDesktopKde3()
{
    writeSettings(new QString ("kde3"));
}

void DesktopSelector::startDesktopKde4()
{

    this->writeSettings(new QString("kde4"));
}

void DesktopSelector::startDesktopGnome()
{
    this->writeSettings(new QString("gnome"));
}

void DesktopSelector::startDesktopLxde()
{
    this->writeSettings(new QString("lxde"));
}

void DesktopSelector::startDesktopIcewm()
{
    this->writeSettings(new QString("icewm"));
}
